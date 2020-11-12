import pandas as pd

def roll(df, column, seconds, stats=['mean']):
    """
    Computes a rolling statistic or many statistics. Where the rolling
    statistic is not yet valid (hasn't yet reached the window size) NaNs will
    be returned.

    Parameters
    ----------
    df : pd.DataFrame
    column : str
    seconds : int
    stats : str or callable, or list of str or callable
    """
    
    window_width = pd.offsets.Second(seconds)

    return (
        df
        [column]
        .rolling(window_width)
        .agg(stats)
        .where(df.index >= window_width)
    )
