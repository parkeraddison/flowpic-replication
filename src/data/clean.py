# How do we find the client's IP without prior knowledge? Remember, this needs
# to work on data coming from anyone.
#
# We can start by filtering out purely local communications, then see what IPs
# remain. Local communications are internal<-->internal, where an internal IP is
# one that starts with 10.0.x 0.0x, 172.16.x, 192.168.x, 169.254.x
#
# Furthermore, IPs that start with 224.x-239.x are 'multicast' IPs, and those
# starting with 255.x are 'broadcast' IPs. We can ignore these when trying to
# find what the client machine IP is.

# Why does this need to be a tuple? Because str.startswith will complain if you
# give it a list!
internal_ranges = ('10.0.', '0.0.', '172.16.', '192.168.', '169.254.')
multicast_ranges = tuple(str(i)+'.' for i in range(224,239+1))
broadcast_ranges = ('255.',)


internal_comm = lambda df: (
    (df.IP1.str.startswith(internal_ranges))
    & (df.IP2.str.startswith(internal_ranges))
)
multicast_comm = lambda df: (
    (df.IP2.str.startswith(multicast_ranges))
)
broadcast_comm = lambda df: (
    (df.IP2.str.startswith(broadcast_ranges))
)

def get_client_ip(df):
    """
    Attempts to find which IP belongs to the client machine. Works by ignoring
    all internal network communications, multicasts, and broadcasts. The local
    address will always be in the IP1 column due to how network-stats works, and
    this method should be enough to narrow IP1 down to one address. In the event
    that multiple addresses are still present, the most frequent address is
    assumed to belong to the client.
    """
    return df[
        ~internal_comm(df)
        & ~multicast_comm(df)
        & ~broadcast_comm(df)
    ].IP1.value_counts().index[0]

client_comm = lambda df: (
    (df.IP1 == get_client_ip(df))
)

def get_vpn_ip(df):
    """
    Attempts to find the IP belonging to the VPN service. Works by determining
    the client IP, then returning whichever IP the client communicates with
    most frequently.

    Note: This should only be used under the explicit assumption that a VPN is
    indeed in use.
    """
    return df.IP2.value_counts().index[0]

vpn_comm = lambda df: (
    (df.IP2 == get_vpn_ip(df))
)

def clean(df):
    """
    Isolates the traffic flow between the client and VPN service.
    """
    return df[vpn_comm(df)]
