import numpy as np
import matplotlib.pyplot as plt

def flowpic(df, bins=1500):
    """
    Takes in a DataFrame of per-packet measurements and creates a FlowPic. A
    FlowPic is essentially a 2D Histogram of packet size (up to 1500 Bytes) and
    arrival time (normalized from 0 to 1500). The FlowPic also has an additional
    dimension for the proportion of packets that were downloaded in each bin.

    NOTE: Currently the direction channel is filled with 0.5... not sure how
    fine of an idea this is honestly.

    """

    c = df[['packet_dirs', 'packet_times', 'packet_sizes']]

    c = c[c.packet_sizes <= 1500]
    c.packet_times = c.packet_times - c.packet_times.min()
    c.packet_times = c.packet_times / c.packet_times.max() * 1500

    hist_bins=bins
    binrange = [[0, 1500], [0, 1500]]
    hist = np.histogram2d(c.packet_times, c.packet_sizes, bins=hist_bins, range=binrange)
    h = hist[0]
    h = h / h.max()

    # For each bin we want to calculate the proportion of packets that were down-
    # loaded. A 1.0 means all packets in that bin were downloaded packets, and 0.0
    # means all packets in that bin were uploaded.
    cut_bins = np.arange(bins)
    timebins = np.searchsorted(cut_bins, c.packet_times, side='right') - 1
    sizebins = np.digitize(c.packet_sizes, cut_bins, right=False) - 1
    c['bin'] = list(zip(timebins, sizebins))
    c.packet_dirs = c.packet_dirs - 1
    download_props = c.groupby('bin').packet_dirs.mean()
    prop_bins = download_props.index.values

    # Start off with a 'grey' channel -- all values are equally up- and downloaded.
    download_channel = np.full((1500,1500), 0.5)
    # Then fill in the calculated values from above
    download_channel[list(zip(*prop_bins))] = download_props.values
    dc = download_channel

    flowpic = np.dstack([h, dc])

    return flowpic