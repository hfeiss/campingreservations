import sys
import os
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
cleanpath = os.path.join(datapath, 'cleaned/')
imagepath = os.path.join(rootpath, 'images/')
hyppath = os.path.join(srcpath, 'hypothesistest/')
sys.path.append(hyppath)
from weekend_longer import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

info = WeekendLonger()

# plt.style.use('ggplot')

plt.figure(figsize=(12, 8))
ax = plt.subplot(111)

plt.xlim(150, 950)
plt.xticks(range(200, 1000, 100), [str(x) + " Miles" for x in range(200, 1000, 100)], fontsize=14)

plt.ylim(-0.0005, .01)
plt.yticks([])

ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.tick_params(axis="both", which="both", bottom="off", labelbottom="on")

# plt.xlabel('Miles Traveled', fontsize = 14)
plt.title('Probability of Average Distance for a Year', fontsize=20, loc='right')

x = np.linspace(150, 950, 1000)

weekend_dist = stats.norm(loc=info.weekend_avg, scale=info.weekend_std)
y_weekend = weekend_dist.pdf(x)
plt.plot(x, y_weekend, label='Two Nights or Less')
plt.fill_between(x, 0, y_weekend, alpha=0.25)

longer_dist = stats.norm(loc=info.longer_avg, scale=info.longer_std)
y_longer = longer_dist.pdf(x)
plt.plot(x, y_longer, label='Longer than Two Nights')
plt.fill_between(x, 0, y_longer, alpha=0.25)

plt.legend(fontsize=14, loc='upper left')
plt.tight_layout()

if __name__ == '__main__':
    plt.savefig(imagepath + '/HypothesisTest.png')
    print(f'P-value of observing this average: {weekend_dist.cdf(info.longer_avg):.3f}')
