import src.features
import matplotlib.pyplot as plt

def plot_rolling(df, column, seconds, stat='mean', ax=None, label=None):
    """
    Computes a rolling feature and draws it on a line plot.
    """

    # plt.plot(
    #     rolled_feature.index.total_seconds(),
    #     rolled_feature[c],
    #     ax=ax, label=label
    # )
    pass


def compare_window_size(
    browsing, streaming,
    column, seconds, stat, filters=[],
    ax=None, title=None, xlabel=None, ylabel=None, legend=True):
    """
    Draws an overlaid plot of rolling window statstics for browsing data versus
    streaming data, with multiple plots for different window sizes.
    
    Parameters
    ----------
    browse, stream : DataFrame
        Tables for browsing and streaming data, respectively.
    col : str
        Name of column to compute statistic of and plot.
    seconds : list of int
        The window size.
    stat : str or callable
        The function to apply to each window. Certain well-known text can be
        specified, such as 'mean', 'min', 'count'.
    filters : list of callable
        Filters to be applied to each frame before calculating windows.
        See `features.filter`.
        
    Returns
    -------
    matplotlib.axes
    """