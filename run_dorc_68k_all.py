'''
Apply DORC to the pbmc 68k dataset and visualization

@author:chenxofhit@gmail.com
@since: 2019-01-10
'''

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'

# set font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Roboto'

# set the style of the axes and the text color
plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'
plt.rcParams['text.color']='#333F4B'
plt.rcParams['legend.fontsize']='small'

import time
import numpy as np
from scipy import io

import sys
sys.path.append('utils')
import preprocess as pp
import dao as dao
import pickle

method = "dorc"

filename = "./data/dat.cell_expression.mm"
X = io.mmread(filename)

X_array = X.toarray()

genes = np.arange(1, X_array.shape[1]+1)

datasave = "output_68k"
dao.create_folder(datasave)
preprocessedData, selGenes = pp.ranger_preprocess(X_array, genes, optionToSave=False, dataSave=datasave)
pickle.dump(preprocessedData, open("./output_68k/preprocessedData.p", "wb"))
pickle.dump(selGenes, open("./output_68k/selGenes.p", "wb"))

import dorc
random_state = np.random.RandomState(1)
predictions, scores, duration = dorc.dorc(preprocessedData, random_state)
pickle.dump(predictions, open("./output_68k/predictions_{}.p".format(method), "wb"))
pickle.dump(scores, open("./output_68k/scores_{}.p".format(method), "wb"))

from MulticoreTSNE import MulticoreTSNE as TSNE
t0 = time.time()
tsne = TSNE(n_jobs=16, random_state=1)
X_embedded = tsne.fit_transform(preprocessedData)
t1 = time.time()
durationTsne = round(t1 - t0, ndigits=4)
print("Total running tsne time is :" + str(durationTsne) + " s")

pickle.dump(X_embedded, open("./output_68k/X_embedded.p", "wb"))

import pickle
X_embedded = pickle.load(open("./output_68k/X_embedded.p", "rb"))
predictions = pickle.load(open("./output_68k/predictions_{}.p".format(method), "rb"))

import pandas as pd

annotation_name = "./data/dat.cell_annotation.csv"
annotation = pd.read_csv(annotation_name, sep=",", header=0)
pickle.dump(annotation, open("./output_68k/annotation.p", "wb"))

fig, ax = plt.subplots()
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], s=5, c='lightgray', edgecolors=None, marker='.', linewidths=0)
rareind = np.where(predictions == 1)[0]
plt.scatter(X_embedded[rareind, 0], X_embedded[rareind, 1], s=5, c='red', edgecolors=None, marker='.', linewidths=0, label='rare')

# change the style of the axis spines
#ax.spines['top'].set_color('none')
#ax.spines['right'].set_color('none')
# ax.spines['left'].set_smart_bounds(True)
# ax.spines['bottom'].set_smart_bounds(True)
#
# # set the spines position
# ax.spines['bottom'].set_position(('axes', -0.04))
# ax.spines['left'].set_position(('axes', 0.015))

#remove axis
#plt.axis('off')
plt.xlabel("tSNE-1")
plt.ylabel("tSNE-2")

#remove white margin of the plots
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0.2)

plt.savefig("./output_68k/plot_tsne_{}.svg".format(method), format='svg', dpi=100)
plt.savefig("./output_68k/plot_tsne_{}.png".format(method), dpi=100)

plt.show()

print('Hi, coffee time now !')