import random
import ipaddress


def generate_random_ipv4(
    allow_loopback: bool = False,
    allow_multicast: bool = False,
    allow_link_local: bool = False,
    allow_public: bool = True,
    allow_private: bool = True,
) -> ipaddress.IPv4Address:
    """
    Generate a random IPv4 address. Allows some options to specify type of address to generate.

    :param allow_loopback: (bool) Whether to accept an IP address that is 127.0.0.0/8
    :param allow_multicast: (bool) Whether to allow multicast IPs
    :param allow_link_local:
    :param allow_public:
    :param allow_private:
    :return:
    """
    while True:
        ip = ipaddress.IPv4Address(random.randint(1, 2**32 - 1))
        if ip.is_loopback and not allow_loopback:
            continue
        elif ip.is_multicast and not allow_multicast:
            continue
        elif ip.is_link_local and not allow_link_local:
            continue
        elif ip.is_global and not allow_public:
            continue
        elif ip.is_private and not allow_private:
            continue
        else:
            break
    return ip


def generate_random_ipv4_network(
    minimum_prefix: int = 8,
    maximum_prefix: int = 32,
    allow_loopback: bool = False,
    allow_multicast: bool = False,
    allow_link_local: bool = False,
    allow_public: bool = True,
    allow_private: bool = True,
) -> ipaddress.IPv4Network:
    net_addr = generate_random_ipv4(
        allow_loopback=allow_loopback,
        allow_multicast=allow_multicast,
        allow_link_local=allow_link_local,
        allow_public=allow_public,
        allow_private=allow_private,
    )
    minimum_prefix = max(minimum_prefix, 8)
    maximum_prefix = min(maximum_prefix, 32)

    mask = random.randint(minimum_prefix, maximum_prefix)
    network = ipaddress.IPv4Network((net_addr, mask), strict=False)
    return network
