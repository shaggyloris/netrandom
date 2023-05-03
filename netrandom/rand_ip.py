import random
import ipaddress


def generate_random_ipv4(
    allow_loopback: bool = False,
    allow_multicast: bool = False,
    allow_link_local: bool = False,
    allow_public: bool = True,
    allow_private: bool = True,
    require_type: str = None
) -> ipaddress.IPv4Address:
    """
    Generate a random IPv4 address. Allows some options to specify type of address to generate.
    
    :param allow_loopback: (bool) Whether to accept an IP address that is 127.0.0.0/8
    :param allow_multicast: (bool) Whether to allow multicast IPs
    :param allow_link_local:
    :param allow_public:
    :param allow_private:
    :param require_type:
    :return:
    """
    type_mapping = {
        "loopback": "is_loopback",
        "multicast": "is_multicast",
        "link_local": "is_link_local",
        "global": "is_global",
        "private": "is_private"
        }
    if require_type:
        if require_type not in type_mapping:
            raise ValueError(f"Invalid require type provided: {require_type}. Must be one of {type_mapping.keys()}")
        require_type = type_mapping.get(require_type)
    while True:
        ip = ipaddress.IPv4Address(random.randint(1, 2**32 - 1))
        if require_type and getattr(ip, require_type):
            break
        elif require_type and not getattr(ip, require_type):
            continue
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
    """
    Generates a random IPv4 network. Utilizes the same option as generate_random_ipv4 to create the base address.
    
    Adds additional minimum and maximum prefix options to fit specific criteria.
    
    Minimum prefix must be greater than or equal to 8 and maximum prefix must be less than or equal to 32.
    
    :param minimum_prefix: (int) Minimum prefix allowed for the network
    :param maximum_prefix: (int) Maximum prefix allowed for the network
    :param allow_loopback: (bool) Whether to allow network defined in RFC 3330
    :param allow_multicast: (bool) Whether to allow a network defined in RFC 3171
    :param allow_link_local: (bool) Whether to allow a network defined in RFC 3927
    :param allow_public: (bool) Whether to allow a network defined as public. See here: https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
    :param allow_private: (bool) Whether to allow network defined as private. See here: https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
    :return:
    """
    net_addr = generate_random_ipv4(allow_loopback=allow_loopback, allow_multicast=allow_multicast,
                                    allow_link_local=allow_link_local, allow_public=allow_public,
                                    allow_private=allow_private)
    if minimum_prefix > maximum_prefix:
        raise ValueError("Minimum prefix is greater than maximum prefix")
    minimum_prefix = max(minimum_prefix, 8)
    maximum_prefix = max(8, min(maximum_prefix, 32))
    
    mask = random.randint(minimum_prefix, maximum_prefix)
    network = ipaddress.IPv4Network((net_addr, mask), strict=False)
    return network
