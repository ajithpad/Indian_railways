#code to draw the gradient
import pylab as pl
import numpy as np

gradient = []
for ii in range(7):
    gradient += range(25)
    
gradient = np.array(gradient)
gradient = gradient/24.
gradient = gradient.reshape(1,-1)


fig = pl.figure(figsize=(500/227., 330/227.),frameon = False)
ax1 = fig.add_subplot(111)
ax1.imshow(np.sin(3*gradient), extent=[0, 10080, 0, 20+1], aspect='auto', cmap='gray')
ax1.set_position([0,0,1,1])
ax1.axis('off')
pl.savefig('/Users/ajith/City Scientist/site/data/stat/public/images/bg.png', format = 'png', dpi = 227)
