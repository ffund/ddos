import math

import matplotlib.pyplot as plt
import numpy as np

x1 = []
y1 = []
lim1 = []

f1 = open("red.res", "rb")
for aline in f1:
    l, vals = aline.split(':')
    points = [float(i) for i in vals.strip().split(' ')]
    rho = 6*float(l)*0.54*0.008 + 6*250*0.54*0.008

    mean = sum(points)/len(points)
    sigma2 = sum([(i-mean)*(i-mean) for i in points])/len(points)
    stderr = math.sqrt(sigma2)/math.sqrt(len(points))
    llim = mean - (2.776*stderr)        # 0.95 confidence interval for 5 points
    ulim = mean + (2.776*stderr)        # 0.95 confidence interval for 5 points
    lim = 2.776*stderr

    print "Rho={},E[N]={},s2={},stderr={},Lower Limit={}, Upper Limit={}".format(rho, mean, sigma2, stderr, llim, ulim)
    x1.append(rho)
    y1.append(mean)
    lim1.append(lim)

f1.close()

x1 = np.array(x1)
y1 = np.array(y1)
lim1 = np.array(lim1)

plt.errorbar(x1, y1, yerr=lim1, fmt='x', label='Testbed')

plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
plt.xlabel(r'Total Attack Bandwidth (Mbps)')
plt.ylabel(r'Average User Bandwidth (Mbps)')

plt.savefig('result-red.png')

plt.clf()

x1 = []
y1 = []
lim1 = []

f1 = open("tbf.res", "rb")
for aline in f1:
    l, vals = aline.split(':')
    points = [float(i) for i in vals.strip().split(' ')]
    rho = 2*float(l)*0.54*0.008

    mean = sum(points)/len(points)
    sigma2 = sum([(i-mean)*(i-mean) for i in points])/len(points)
    stderr = math.sqrt(sigma2)/math.sqrt(len(points))
    llim = mean - (2.776*stderr)        # 0.95 confidence interval for 5 points
    ulim = mean + (2.776*stderr)        # 0.95 confidence interval for 5 points
    lim = 2.776*stderr

    print "Rho={},E[N]={},s2={},stderr={},Lower Limit={}, Upper Limit={}".format(rho, mean, sigma2, stderr, llim, ulim)
    x1.append(rho)
    y1.append(mean)
    lim1.append(lim)

f1.close()

x1 = np.array(x1)
y1 = np.array(y1)
lim1 = np.array(lim1)

plt.errorbar(x1, y1, yerr=lim1, fmt='x', label='Testbed')

plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
plt.xlabel(r'Total Attack Bandwidth (Mbps)')
plt.ylabel(r'Average User Bandwidth (Mbps)')

plt.savefig('result-tbf.png')
