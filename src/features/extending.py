# A hackish 'pipeline' for extending our columns.
def extend(df, *funcs):
    """
    We can extend our preprocessed data to create new columns that statistics
    can be computed on.

    Conditioning on existing features of df should be done before
    extending.

    Examples
    --------
    >>> # Returns df with an additional inter-arrival time column computed.
    >>> extend(df, inter_arrival_time)
    >>> ...
    
    >>> # To condition on a factor, like direction, we first group then apply.
    >>> df.groupby('pdir').apply(extend, inter_arrival_time)
    >>> ...
    """

    for func in funcs:
        df = func(df)
    return df

def inter_arrival_time(df):
    """
    Returns df with a new `msdelta` column, containing the millisecond time
    delta between a packet arrival and the arrival of the previous packet.
    """
    # Converting to numeric for better stability with statistical functions
    df['msdelta'] = df.index.to_series().diff().dt.total_seconds() * 1000
    return df
