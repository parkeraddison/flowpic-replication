import src.features
import numpy as np
import matplotlib.pyplot as plt

def grow_around_index(indexes, growth, xmin=0, xmax=1499, ymin=0, ymax=1499):
    """
    Takes a sequence of indexes and returns a sequence including all indexes to
    the left, right, up, down of those indexes.
    """

    grown = set()

    for (x,y) in indexes:

        minx = max(xmin, x-growth)
        maxx = min(xmax, x+growth)
        miny = max(ymin, y-growth)
        maxy = min(ymax, y+growth)
        
        # See: https://stackoverflow.com/questions/11144513/cartesian-product-of-x-and-y-array-points-into-single-array-of-2d-points
        kernel = np.transpose([
            np.tile(range(minx, maxx+1), (maxy-miny+1)),
            np.repeat(range(miny,maxy+1), (maxx-minx+1))
        ])
        
        grown.update(map(tuple, kernel))

    return np.array(list(grown))


def flowpic(flowpic, figsize=(10,10), **kwargs):
    """
    Takes in a FlowPic histogram output and charts it for visual comprehension.
    This means that the picture gets exaggerated by setting all non-zero values
    to maximum luminance, and making each bin look larger than a single pixel!

    **kwargs are passed to plt.scatter
    """

    hist, downprop = [e.squeeze() for e in np.dsplit(flowpic, 2)]

    options = {'cmap': 'Greys', 'origin': 'lower', 'vmin': 0, 'vmax': 1}

    fig, ax = plt.subplots(figsize=figsize)

    plt.scatter(
        *np.argwhere(hist > 0).T,
        # The color is based on the download proportion.
        c=downprop[hist>0],
        marker='s', s=40,
        **kwargs
        )
    colorbar = plt.colorbar(orientation='horizontal')
    colorbar.set_label('Proportion downloaded')
    plt.xlim(0, 1500)
    plt.ylim(0, 1500)

    plt.xlabel('Normalized arrival time')
    plt.ylabel('Packet size (bytes)')
    # plt.show()

    return fig, ax



# def plot_rolling(df, column, seconds, stat='mean', ax=None, label=None):
#     """
#     Computes a rolling feature and draws it on a line plot.
#     """

#     # plt.plot(
#     #     rolled_feature.index.total_seconds(),
#     #     rolled_feature[c],
#     #     ax=ax, label=label
#     # )
def compare_rolling(browse, stream, col, seconds, stat='mean', filters=[],
                ax=None, title=None, xlabel=None, ylabel=None, legend=True):
    """
    Draws an overlaid plot of rolling window statstics for browsing data versus
    streaming data.
    
    Parameters
    ----------
    browse, stream : DataFrame
        Tables for browsing and streaming data, respectively.
    col : str
        Name of column to draw.
    seconds : int
        The window size.
    stat : {'mean', 'count', callable}
        The function to apply to each window.
    filters : list of callable
        Filters to be applied to each frame before calculating windows.
        
    Return
    ------
    matplotlib.axes
    """
    
    if ax is None:
        fig, ax = plt.subplots()
    
    def plot_rolling(df, col, label=None):
    
        # rolled = df.rolling(str(seconds)+'s')
        frame = src.features.roll(df, col, seconds, stat)

        # if type(stat) == str:
        #     frame = rolled.agg(stat)
        # else:
        #     frame = rolled.apply(stat)

        ax.plot(
            frame.index.total_seconds(),
            frame,
            label=label
        )
    
    b_filt = src.features.filter(browse, *filters)
    s_filt = src.features.filter(stream, *filters)
    
    plot_rolling(b_filt, col, 'Browsing')
    plot_rolling(s_filt, col, 'Streaming')
    
    #> Now handled by roll function.
    # Shade region where rolling window is effective
    # maxseconds = min(b_filt.index[-1], s_filt.index[-1]).total_seconds()
    # ax.axvspan(seconds, max(seconds, maxseconds-seconds), color='#0f01')
    
    # Title and labels
    ax.set_title(title or f"Rolling {stat} {col}, window={seconds}s")
    ax.set_xlabel(xlabel or 'Time delta from first packet (seconds)')
    ax.set_ylabel(ylabel or f"{stat} {col}")
    
    if legend:
        ax.legend()


# def compare_window_size(
#     browsing, streaming,
#     column, seconds, stat, filters=[],
#     ax=None, title=None, xlabel=None, ylabel=None, legend=True):
#     """
#     Draws an overlaid plot of rolling window statstics for browsing data versus
#     streaming data, with multiple plots for different window sizes.
    
#     Parameters
#     ----------
#     browse, stream : DataFrame
#         Tables for browsing and streaming data, respectively.
#     col : str
#         Name of column to compute statistic of and plot.
#     seconds : list of int
#         The window size.
#     stat : str or callable
#         The function to apply to each window. Certain well-known text can be
#         specified, such as 'mean', 'min', 'count'.
#     filters : list of callable
#         Filters to be applied to each frame before calculating windows.
#         See `features.filter`.
        
#     Returns
#     -------
#     matplotlib.axes
#     """