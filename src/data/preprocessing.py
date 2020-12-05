import pandas as pd

UNIT = 'ms' # Network-stats records packet timing in milliseconds.

def unbin_packets(df):
    """
    Takes tables in the network-stats output format, and 'unbins' the packet-
    level measurements so that each packet gets its own row.
    """
    
    df = df.drop(columns=[
        'Time', '1->2Bytes', '2->1Bytes', '1->2Pkts', '2->1Pkts'
    ])
    
    packet_cols = ['packet_times', 'packet_sizes', 'packet_dirs']
    
    # Convert the strings `val1;val2;` into lists `[val1, val2]`
    df[packet_cols] = (
        df.loc[:,packet_cols]
        .apply(lambda ser: ser.str.split(';').str[:-1])
    )
    
    # 'Explode' the lists so each element gets its own row.
    exploded = (
        df.apply(
            lambda ser: ser.explode().astype(int) if ser.name in packet_cols else ser
        )
    )
    
    return exploded

def index_by_flow(df):

    keys = ['IP1', 'IP2', 'packet_dirs']

    indexed = (
        df
        .sort_values(keys)
        .set_index(keys)
    )
    
    return indexed

def dominating_flow(df, threshold=0.9):
    """
    Takes in a DataFrame indexed by (IP1, IP2, direction). If a pair of IPs has
    more than `threshold` proportion of the packet data, then consider it the
    main flow and remove all other pairs.
    """

    pair_props = df.index.droplevel(2).value_counts(normalize=True)

    if pair_props[0] > threshold:
        return df.loc[pair_props.index[0]]

    else:
        raise Warning("No dominating flow could be found for this data.")

def split_on_direction(df):
    """
    Takes in a DataFrame indexed by (IP1, IP2, direction) and spits out two
    DataFrames, (uploaded_packets, downloaded_packets).
    """
    # NOTE: Some data had a global IP as the client... it got put in IP2 by
    # network-stats, so the whole 'sending' vs 'receiving' may not be accurate.

    uploaded = df.loc[(slice(None), slice(None), 1)]
    downloaded = df.loc[(slice(None), slice(None), 2)]

    return (uploaded, downloaded)

def chunk(df, chunk_length='60s'):
    """
    Returns a list of DataFrames, each `chunk_length` long in duration.
    """
    
    df_time = df.assign(timestamp=pd.to_datetime(df.packet_times, unit='ms'))
    # Important that we specify `origin='start'`, otherwise specifying a minute
    # will create chunks at e.g. 5:01, 5:02, ..., when we want to just take
    # 60s from the very first observation
    resampled = df_time.resample(chunk_length, on='timestamp', origin='start')

    chunks = []
    for (timestamp, frame) in resampled:
        chunks.append(frame)

    # Get rid of last chunk if it's incomplete
    last = chunks[-1]
    if last.timestamp.max() - last.timestamp.min() < pd.Timedelta(chunk_length):
        chunks.pop()

    return chunks

def preprocess(
    df, chunk_length='60s', isolate_flow=False, dominating_threshold=0.9,
    split_directions=False
    ):
    """
    Returns a list of DataFrames, each containing `chunk_length` worth of per-
    packet measurements.
    
    If `isolate_flow` is True, then a main flow between a pair of IPs will be
    found whose presense is greater than the `dominating_threshold`. In absense
    of a main flow a Warning will be raised and the file will be ignored.

    If `split_directions` is True, then separate chunks will be returned for
    each packet direction in the data, so a tuple of lists will be returned,
    (uploading_chunks, downloading_chunks).
    """
    
    unbinned = unbin_packets(df)

    indexed = index_by_flow(unbinned)

    data = indexed

    if isolate_flow:
        data = dominating_flow(data, dominating_threshold)

    if split_directions:
        uploading, downloading = split_on_direction(data)
        up_chunks = chunk(uploading, chunk_length)
        down_chunks = chunk(downloading, chunk_length)
        return (up_chunks, down_chunks)
    else:
        chunks = chunk(data, chunk_length)
        return chunks
    
