import numpy as np
import seaborn as sns
from scipy import ndimage

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def frame_d6(ax):
    ax.set_xlim(-122.425, -122.355)
    ax.set_ylim(37.763, 37.835)


def frame_all(ax):
    ax.set_xlim(-122.52, -122.36)
    ax.set_ylim(37.705, 37.835)


def frame_ti(ax):
    ax.set_xlim(-122.382, -122.355)
    ax.set_ylim(37.80, 37.835)


def frame_soma(ax):
    ax.set_xlim(-122.425, -122.38)
    ax.set_ylim(37.763, 37.795)


def frame_mainland(ax):
    ax.set_xlim(-122.52, -122.371)
    ax.set_ylim(37.705, 37.815)


def save_map(fig, ax, fname, dpi=300, **kwargs):
    fig.set_dpi(dpi)
    fig.tight_layout()
    sns.despine(ax=ax, left=True, bottom=True)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.savefig(fname, dpi=dpi, bbox_inches='tight', **kwargs)


def compute_heatmap(d, bins=(100, 100), smoothing=1.3):
    def getx(pt):
        return pt.coords[0][0]

    def gety(pt):
        return pt.coords[0][1]

    x = list(d.geometry.apply(getx))
    y = list(d.geometry.apply(gety))
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(
        logheatmap, smoothing, mode='nearest')
    return logheatmap, extent


def plot_heatmap(logheatmap, extent, **kwargs):
    cmap = pylab.cm.jet
    # Get the colormap colors
    my_cmap = cmap(np.arange(cmap.N))

    # Set alpha
    my_cmap[:, -1] = np.linspace(0, 1, cmap.N)

    # Create new colormap
    my_cmap = ListedColormap(my_cmap)

    ax = plt.imshow(logheatmap, cmap=my_cmap, extent=extent, **kwargs)
    # plt.colorbar()
    plt.gca().invert_yaxis()
    return ax


def heatmap(d, bins=(100, 100), smoothing=1.3, **kwargs):
    plot_heatmap(*compute_heatmap(d, bins, smoothing), **kwargs)
