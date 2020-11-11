# Often, filters may be useful -- these differ from cleaning since they happen 
# after some feature extending has already occurred. One useful filter would 
# be to only look at packets which were uploaded (pdir == 1) or only which were 
# downloaded (pdir == 2).

upload_pkts = lambda df: (
    df.pdir == 1
)
download_pkts = lambda df: (
    df.pdir == 2
)

def filter(df, *funcs):
    """
    Filters are designed to be applied to preprocessed data, prior to feature
    computation.

    Examples
    --------
    >>> # Returns only rows of df which correspond to an uploaded packet.
    >>> filter(df, upload_pkts)
    >>> ...
    """
    
    for func in funcs:
        df = df[func(df)]
    return df
