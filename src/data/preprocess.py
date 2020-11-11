UNIT = 'ms' # Network-stats records packet timing in milliseconds.

def packet_flows(df):
    """
    Reconstructs a dataframe of individual packet-flows when given a dataframe
    coming from network-stats. Packet flow measurements include packet size,
    packet direction, and packet timing. The outputted packet times will be
    relative to the first packet in this dataframe.

    The data from network-stats are essentially 1-second binned packet flows
    summarized by `sum` and `count`. This function un-bins the individual packet
    measurements to allow for different bins and statistics to be applied.
    """
    
    # Each of the extended columns, 'packet_times', 'packet_sizes', and
    # 'packet_dirs' contains a semicolon separated (and trailing) string of
    # measurements.
    #
    # We can extract these measurements such that each row contains a native
    # Python list of measurements. The `sum` in this setting simply aggregates
    # all lists down each column.
    lists = (
        df.filter(like='packet')
        .apply(lambda ser: ser.str.split(';').str[:-1])
        .sum()
    )
    
    frame = pd.DataFrame({
        'ptime': lists.packet_times,
        'psize': lists.packet_sizes,
        'pdir' : lists.packet_dirs
    }).astype(int)
    
    # Need to sort by arrival to ensure monotonicity -- will be useful for
    # rolling windows and computing inter-arrival times.
    frame = frame.sort_values('ptime')
    
    # Replace timestamp with a delta from the first packet
    frame['ptime'] = pd.to_timedelta(frame.ptime - frame.ptime[0], UNIT)
    frame = frame.set_index('ptime')
    
    return frame

def preprocess(df):
    """
    Turns a cleaned dataframe containing network-stats output into a dataframe
    of packet flows, ready for feature engineering.
    """
    return packet_flows(df)
