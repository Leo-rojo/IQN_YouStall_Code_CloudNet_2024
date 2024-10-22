import pylab
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib as mpl
mpl.rc('hatch', color='k', linewidth=3)

font_general = {'family' : 'sans-serif',
                        #'weight' : 'bold',
                        'size'   : 50}
plt.rc('font', **font_general)

def lighten_color(color, amount=0.5):
    """Lightens the given color by mixing it with white. 'amount' ranges from 0 (no change) to 1 (white)."""
    c = mcolors.to_rgba(color)
    return [(1.0 - amount) * c[i] + amount for i in range(3)] + [1]  # Keep alpha as 1

# Define lighter versions of the colors by mixing them with white
light_red = lighten_color('red', 0.5)  # Lighter red
light_blue = lighten_color('blue', 0.5)  # Lighter blue
light_green = lighten_color('green', 0.5)  # Lighter green

# create a figure for the data
figData = pylab.figure()
ax = pylab.gca()

a=np.arange(0,8,1)
barWidth=3
b=[i+barWidth-0.05 for i in a]
c=[i+barWidth-0.05 for i in b]
d=[i+barWidth-0.05 for i in c]
#plt.bar(a, [1,2,3,4,5,6,7,8], color ='w', width = barWidth-0.1,linewidth=0,label='Testing ABR:',align='edge')
plt.bar(b, [1, 2, 3, 4, 5, 6, 7, 8], color=light_red, width=barWidth-0.1, linewidth=0, label='news', align='edge', hatch='//', alpha=1)  # News bars with diagonal hatch
plt.bar(c, [1, 2, 3, 4, 5, 6, 7, 8], color=light_green, width=barWidth-0.1, linewidth=0, label='music', align='edge', hatch='.', alpha=1)  # Music bars with opposite diagonal hatch
plt.bar(d, [1, 2, 3, 4, 5, 6, 7, 8], color=light_blue, width=barWidth-0.1, linewidth=0, label='sports', align='edge', hatch='\\', alpha=1)  # Sports bars with star hatch


# create a second figure for the legend
figLegend = pylab.figure(figsize = (20,10),dpi=100)

# produce a legend for the objects in the other figure
pylab.figlegend(*ax.get_legend_handles_labels(), loc = 'upper left',ncol=5,frameon=False)
figLegend.savefig("legendbar.pdf",bbox_inches='tight')
plt.close()
plt.close()