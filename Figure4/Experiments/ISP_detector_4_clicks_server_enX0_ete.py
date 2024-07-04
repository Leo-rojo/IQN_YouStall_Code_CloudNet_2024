import pyshark
import time
from collections import Counter
import os

# Constants
MIN_PATTERN_SIZE = 1180 #min size of 200ok packets
MAX_PATTERN_SIZE = 1288 #max size of 200ok packets
PIECE_OF_CHUNKS = 1292 #max size of packet, lot of them belong to chunks
DETECTION_TIME_WINDOW = tw = 0.300  # Time window to detect the pattern (in seconds)
NR_OF_CLICKS = 4

def save_patterns_and_clear(folder_path):
    global patterns_timestamps
    global ws
    if patterns_timestamps:  # Check if the list is not empty
        with open(folder_path + 'Detector_1.txt', "a") as f:
            for timestamp in patterns_timestamps:
                f.write(f"PF-{timestamp}\n")
    if ws:
        with open(folder_path + 'Detector_1_ws.txt', "a") as f:
            for timestamp in ws:
                f.write(f"PF-{timestamp}\n")
        patterns_timestamps.clear()
        ws.clear()
def save_candidate_packets_time(folder_path):
    global timestamp_of_candidate
    if timestamp_of_candidate:  # Check if the list is not empty
        with open(folder_path + 'timestamp_of_candidate.txt', "a") as f:
            for timestamp in timestamp_of_candidate:
                f.write(f"{timestamp}\n")
        timestamp_of_candidate.clear()
def start_live_capture(interface, live_capture_duration, folder_path):
    pattern_array = []
    global timestamp_of_candidate
    chunk_streams = []
    chunk_stream = None
    start_time = time.time()
    calculate_chunk_stream = True
    global patterns_timestamps
    global ws
    start_time_save_candidate = time.time()

    def reset_pattern_array():
        nonlocal pattern_array
        pattern_array = []

    def packet_callback(packet):
        nonlocal pattern_array, streams, chunk_streams, start_time, chunk_stream, calculate_chunk_stream,start_time_save_candidate
        try:
            if packet.udp.srcport == '443':  #filter by packets that are sent from the server
                size = int(packet.length)
                sniff_timestamp = float(packet.sniff_timestamp)
                stream=packet.udp.stream

                # Use the first 10 seconds to detect the stream dedicated to send chunks, if any (it can be that the stream is using http2/1)
                if time.time()-start_time<=10: #first ten seconds, detect the stream with the most packets of 1292 bytes (chunks)
                    if size == PIECE_OF_CHUNKS:
                        chunk_streams.append(stream)
                elif calculate_chunk_stream == True:
                    if chunk_streams != []:
                        stream_counter = Counter(chunk_streams)
                        max_stream = max(stream_counter, key=stream_counter.get)
                        max_count = stream_counter[max_stream]
                        if max_count>30:
                            chunk_stream = max_stream
                            print('chuks are sent through http3 stream nr: '+str(chunk_stream))
                        else:
                            chunk_stream = 'chunks are sent through http1/2'
                            print(chunk_stream)
                        calculate_chunk_stream = False
                    else:
                        chunk_stream = 'chunks are sent through http1/2'
                        calculate_chunk_stream = False

                # Detection of the unique pattern (This has the pure scope of showing the correctness of the settings, and if the packets are received correctly and autoplay clicked correctly)
                # The detection of stall and the inference of their length happen in Plotting folder
                if chunk_stream is not None:
                    if MIN_PATTERN_SIZE <= size <= MAX_PATTERN_SIZE and stream!=chunk_stream:
                        print(f'Packet: {size}--{sniff_timestamp}--{stream}')#--{time_delta}')
                        timestamp_of_candidate.append(sniff_timestamp)
                        pattern_array.append((size, sniff_timestamp,stream))
                        # Remove packets that are outside the sliding window
                        pattern_array = [pkt for pkt in pattern_array if sniff_timestamp - pkt[1] <= DETECTION_TIME_WINDOW]
                        # Check for stall detection
                        if len(pattern_array) >= NR_OF_CLICKS:
                            found_time = pattern_array[-1][1]
                            patterns_timestamps.append(found_time)
                            print("--Pattern found at:", found_time)
                            print("--Pattern array:",pattern_array)
                            ws.append(pattern_array[-1][1] - pattern_array[0][1])
                            reset_pattern_array()
                            save_patterns_and_clear(folder_path)
                        else:
                            print("Pattern not detected, sliding window...")

                #every two seconds call save_cum_time
                if time.time()-start_time_save_candidate>=2:
                    save_candidate_packets_time(folder_path)
                    start_time_save_candidate = time.time()

        except AttributeError:
            pass

    try:
        print('Live capture started at:', time.time())
        capture = pyshark.LiveCapture(interface=interface, bpf_filter='udp') # Use the BPF filter to capture packets that use UDP (QUIC protocol)
        capture.apply_on_packets(packet_callback, timeout=live_capture_duration)
    except Exception as e:
        print(f"An error occurred while capturing packets: {e}")
    finally:
        capture.close()
        print('Live capture stopped at:', time.time())


if __name__ == "__main__":
    Network_id = '1000Kbps'
    Video_link = 'https://www.youtube.com/watch?v=znN1GoKbPf4'
    length_individual_exp = 3000
    EC2_interface = 'enX0'
    video_id = Video_link.split('=')[-1]
    folder_path = 'Results/' + video_id + '_' + Network_id + '/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    patterns_timestamps=[]
    timestamp_of_candidate = []
    ws = []
    # Start live capture
    start_live_capture(EC2_interface, length_individual_exp, folder_path)
