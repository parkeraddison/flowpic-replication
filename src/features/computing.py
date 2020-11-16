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

def mean_packet_size(df):
    return df.psize.mean()

def mean_inter_packet_delay(df):
    return df.msdelta.mean()

def send_receive_ratio(df):
    send = df[df.pdir == 1]
    receive = df[df.pdir == 2]
    # There are some files that don't follow the naming convention and cause
    # novpn data to get through our ETL pipeline. These mess with our cleaning
    # script and cause errors.
    #! TODO: Need to make more robust name parsing -- or fix naming errors.
    try:
        return send.shape[0] / receive.shape[0]
    except ZeroDivisionError:
        return -1
