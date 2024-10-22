import os

categories = ['news', 'music', 'sport']
base_path = '../Results/Results_'

# Initialize the arrays with the specified patterns
for category in categories:
    result_dir = base_path + category
    array_400 = []   # Pattern: no, yes, no, yes, ...
    array_800 = []   # Pattern: no, no, no, yes, ...
    array_1200 = []  # Pattern: no, no, no, no, no, yes, ...
    array_1600 = []  # Pattern: no, no, no, no, no, no, no, yes, ...
    array_2000 = []  # Pattern: no, no, no, no, no, no, no, no, no, yes, ...

    if not os.path.exists(result_dir):
        print(f"Directory {result_dir} does not exist. Skipping...")
        continue

    for fold in os.listdir(result_dir):
        path = os.path.join(result_dir, fold, 'p_0.2', 'Detected_clicks_0.2.txt')

        if not os.path.isfile(path):
            print(f"File {path} does not exist. Skipping...")
            continue

        try:
            with open(path, 'r') as f:
                read_timestamp = f.readlines()
                num_lines = len(read_timestamp)

                # Append values to the arrays according to the specified patterns
                array_400.extend([read_timestamp[i].strip() for i in range(num_lines) if i % 2 == 1])
                array_800.extend([read_timestamp[i].strip() for i in range(num_lines) if i % 4 == 3])
                array_1200.extend([read_timestamp[i].strip() for i in range(num_lines) if i % 6 == 5])
                array_1600.extend([read_timestamp[i].strip() for i in range(num_lines) if i % 8 == 7])
                array_2000.extend([read_timestamp[i].strip() for i in range(num_lines) if i % 10 == 9])

                # Print the number of lines read from the file
                print(f"Read {num_lines} lines from {path}")
        except Exception as e:
            print(f"An error occurred while reading {path}: {e}")


    # create folder to save the results
    if not os.path.exists(f"Results_{category}"):
        os.makedirs(f"Results_{category}")
    # Save the arrays to files
    for i in [0.4, 0.8, 1.2, 1.6, 2.0]:
        if not os.path.exists(f"Results_{category}/p_"+str(i)):
            os.makedirs(f"Results_{category}/p_"+str(i))
    with open(f"Results_{category}/p_0.4/Detected_clicks_0.4.txt", 'w') as f:
        f.write('\n'.join(array_400))
    with open(f"Results_{category}/p_0.8/Detected_clicks_0.8.txt", 'w') as f:
        f.write('\n'.join(array_800))
    with open(f"Results_{category}/p_1.2/Detected_clicks_1.2.txt", 'w') as f:
        f.write('\n'.join(array_1200))
    with open(f"Results_{category}/p_1.6/Detected_clicks_1.6.txt", 'w') as f:
        f.write('\n'.join(array_1600))
    with open(f"Results_{category}/p_2.0/Detected_clicks_2.0.txt", 'w') as f:
        f.write('\n'.join(array_2000))

    # Display the generated arrays for verification
    print(f"Array with alternate no and yes pattern for {category}:", array_400)
    print(f"Array with three no then one yes pattern for {category}:", array_800)
    print(f"Array with five no then one yes pattern for {category}:", array_1200)
    print(f"Array with seven no then one yes pattern for {category}:", array_1600)
    print(f"Array with nine no then one yes pattern for {category}:", array_2000)
