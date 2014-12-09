import pylab as py
import numpy as np

import matplotlib.cm as cm
import matplotlib.colors as colors

####

params = {'backend': 'ps',
          'axes.labelsize': 10,
          'text.fontsize': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True}
          # 'figure.figsize': fig_size}
# py.rcParams.update(params)

#####

file = open('coverage', 'r')
source = file.readlines()
file.close()

source = [i.split(' ') for i in source]
source = zip(*source)[1]
data = map(float, source)

#####

py.clf()
# fig=py.figure()
# ax = fig.add_subplot(111)
n, bins, patches = py.hist(data, bins=50, range=(0,1), normed=True, alpha=0.75)

# normalizacja do 1
locs,labels = py.yticks()
py.yticks(locs[1:], map(lambda x: "%.2f" % (x/sum(n)), locs[1:]))

fracs = n.astype(float)/n.max()
norm = colors.normalize(0, 1)

for thisfrac, thispatch in zip(fracs, patches):
    color = cm.jet(norm(thisfrac))
    thispatch.set_facecolor(color)

py.xlabel('Percentage of labeled zones')
py.ylabel('Documents in bin')
py.title('Histogram of labeled zones')

py.savefig('hist.pdf', transparent = True)
py.show()
#####
n, bins, patches = py.hist(data, 50, range=(0,1), normed=True, cumulative=1, alpha=0.75)

fracs = 1-n.astype(float)/n.max()
norm = colors.normalize(0, 1)
for thisfrac, thispatch in zip(fracs, patches):
    color = cm.jet(norm(thisfrac))
    thispatch.set_facecolor(color)

py.ylim(0, 1)

py.xlabel('Percentage of labeled zones')
py.ylabel('Percentage of documents')
# py.title('Histogram of labeled zones')

py.savefig('revCumHist.pdf', transparent = True)


# #####
# # n, bins, patches = py.hist(data, 50, range=(0,1), normed=True, cumulative=1, alpha=0.75)
# # fracs = n.astype(float)/n.max()
# # norm = colors.normalize(0, 1)
# # for thisfrac, thispatch in zip(fracs, patches):
# #     color = cm.jet(norm(thisfrac))
# #     thispatch.set_facecolor(color)
py.show()
