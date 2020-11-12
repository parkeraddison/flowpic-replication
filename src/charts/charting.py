import src.features
import matplotlib.pyplot as plt

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