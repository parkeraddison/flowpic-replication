# The primary part of cleaning is merely getting rid of un-interesting flows.
# Since we are operating under the assumption that a VPN is in use, our clenaing
# can hopefully isolate *just* the client<->VPN flow.
#
# The way we do this is by removing any communications to link-local IPs, any
# multicast communications, and any communications between two private IPs.
#
# We can enforce that all communications remaining are between a private IP and
# a global IP.
import ipaddress


# internal_prefixes = ('10.0.', '0.0.', '172.16.', '192.168.', '169.254.')
# multicast_prefixes = tuple(str(i)+'.' for i in range(224,239+1))
# broadcast_prefixes = ('255.',)
# hopbyhop_protocol = 0


# internal_comm = lambda df: (
#     (df.IP1.str.startswith(internal_prefixes))
#     & (df.IP2.str.startswith(internal_prefixes))
# )
# multicast_comm = lambda df: (
#     (df.IP2.str.startswith(multicast_prefixes))
# )
# broadcast_comm = lambda df: (
#     (df.IP2.str.startswith(broadcast_prefixes))
# )
# hopbyhop_comm = lambda df: (
#     df.Proto == hopbyhop_protocol
# )

# def get_client_ip(df):
#     """
#     Attempts to find which IP belongs to the client machine. Works by ignoring
#     all internal network communications, multicasts, and broadcasts. The local
#     address will always be in the IP1 column due to how network-stats works, and
#     this method should be enough to narrow IP1 down to one address. In the event
#     that multiple addresses are still present, the most frequent address is
#     assumed to belong to the client.
#     """
#     return df[
#         ~internal_comm(df)
#         & ~multicast_comm(df)
#         & ~broadcast_comm(df)
#         & ~hopbyhop_comm(df)
#     ].IP1.value_counts().index[0]

# client_comm = lambda df: (
#     (df.IP1 == get_client_ip(df))
# )

# def get_vpn_ip(df):
#     """
#     Attempts to find the IP belonging to the VPN service. Works by determining
#     the client IP, then returning whichever IP the client communicates with
#     most frequently.

#     Note: This should only be used under the explicit assumption that a VPN is
#     indeed in use.
#     """
#     return df.IP2.value_counts().index[0]

# vpn_comm = lambda df: (
#     (df.IP2 == get_vpn_ip(df))
# )

def clean(df):
    """
    Attempts to filter out everything besides the traffic flow between the
    client and VPN service.
    """

    ip1, ip2 = df.IP1.map(ipaddress.ip_address), df.IP2.map(ipaddress.ip_address)

    either_link_local = (
        (ip1.map(lambda x: x.is_link_local))
        | (ip2.map(lambda x: x.is_link_local))
    )

    either_multicast = (
        (ip1.map(lambda x: x.is_multicast))
        | (ip2.map(lambda x: x.is_multicast))
    )

    both_private = (
        (ip1.map(lambda x: x.is_private))
        & (ip2.map(lambda x: x.is_private))
    )

    private_to_global = (
        (
            (ip1.map(lambda x: x.is_private))
            & (ip2.map(lambda x: x.is_global))
        ) | (
            (ip2.map(lambda x: x.is_private))
            & (ip1.map(lambda x: x.is_global))
        )
    )

    return df[
        ~either_link_local
        & ~either_multicast
        & ~both_private
        # & private_to_global
    ]

    # # return df[vpn_comm(df)]
    # return df[
    #     ~internal_comm(df)
    #     & ~multicast_comm(df)
    #     & ~broadcast_comm(df)
    #     & ~hopbyhop_comm(df)
    # ]

