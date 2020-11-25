import numpy as np
import matplotlib.pyplot as plt

def flowpic(df, bins=1500):
    """
    Takes in a DataFrame of per-packet measurements and creates a FlowPic. A
    FlowPic is essentially a 2D Histogram of packet size (up to 1500 Bytes) and
    arrival time (normalized from 0 to 1500).

    If drawing arguments are specified, will draw a figure as well.
    """
    
    c = df[['packet_times', 'packet_sizes']]

    c = c[c.packet_sizes <= 1500]
    c.packet_times = c.packet_times - c.packet_times.min()
    c.packet_times = c.packet_times / c.packet_times.max() * 1500
    
    # /\/\/\/\/\/\/\
    #! TODO: Extend FlowPic so that the histogram has a channel for direction.
    #
    # We can have a second channel act as the proportion of packets that are
    # being downloaded. So a 1.0 would mean all packets were downloaded in that
    # bin, and 0.0 would mean all packets in that bin were uploaded.
    # \/\/\/\/\/\/\/

    h = np.histogram2d(c.packet_times, c.packet_sizes, bins=bins)[0]
    h = h / h.max()

    return h