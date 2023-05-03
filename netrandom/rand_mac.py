import random


def format_mac(num: int, sep: str, chunk_size: int, capitalize: bool = False) -> str:
    value = f"{num:012x}"
    mac = sep.join(
        [value[i : i + chunk_size] for i in range(0, len(value), chunk_size)]
    )
    if capitalize:
        mac = mac.upper()
    return mac


def cisco_format(num: int) -> str:
    return format_mac(num, ".", 4)


def ieee_format(num: int) -> str:
    return format_mac(num, "-", 2, capitalize=True)


def ietf_format(num: int) -> str:
    return format_mac(num, ":", 2)


def generate_random_mac(format: str = "ieee") -> str:
    """
    Generates a random mac address utilizing the specified format based off common representations of MAC addresses.
    
    Formats:
      ieee: group of 2 uppercase hex characters dash seperated = E7-14-44-F8-16-93
      ietf: group of 2 lowercase hex characters colon seperated = dc:9f:e3:59:40:2c
      cisco: group of 4 lowercase hex characters period seperated = 2ffe.eda8.50fb
    
    Note: This doesn't support any nuance within the specification. It strictly generates a random number from 1-2^48
          then converts it to the applicable format.
    
    :param format: (str) One of ieee, ietf, or cisco
    :return: (str)
    """
    formatters = {
        "ieee": ieee_format,
        "ietf": ietf_format,
        "cisco": cisco_format,
    }
    if format not in formatters:
        raise ValueError(f"Invalid format value {format}")
    
    num = random.randint(1, 2**48)
    
    formatter = formatters.get(format)
    return formatter(num)
