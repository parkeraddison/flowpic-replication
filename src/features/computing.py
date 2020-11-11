def roll(df, column, seconds, stats=['mean']):
    """
    Parameters
    ----------
    df : pd.DataFrame
    column : str
    seconds : int
    stats : list of str or callable
    """
    
    window_width = str(seconds)+'s'

    return (
        df
        [column]
        .rolling(window_width)
        .agg(stats)
    )
