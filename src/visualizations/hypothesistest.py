import sys
import os
srcpath = os.path.split(os.path.abspath(''))[0]
hyppath = os.path.join(srcpath, 'hypothesistest/')
sys.path.append(hyppath)
from weekend_longer import *
import matplotlib.pyplot as plt
import numpy as np

info = WeekendLonger()

#plt.style.use('ggplot')

plt.figure(figsize=(12, 8))    
ax = plt.subplot(111)    

plt.xlim(0, 1)    
plt.xticks(range(200, 800, 100), [str(x) + " Miles" for x in range(200, 800, 100)], fontsize=14)    

plt.ylim(0, 1)
plt.yticks(fontsize=14)

ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False) 

plt.xlabel('Miles Traveled', fontsize = 14)
plt.title('Probability', fontsize = 20)

x = np.linspace

weekend = 

plt.plot(data['LengthOfStay'], data['count(LengthOfStay)'])
plt.tight_layout()
plt.savefig(imagepath + '/HistogramOfNights.png') 



if __name__ == '__main__':
    print(info.weekend_avg)
    print(info.longer_avg)
    print(info.weekend_std)
    print(info.longer_std)