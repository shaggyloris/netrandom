import random


def format_mac(num: int, sep: str, chunk_size: int) -> str:
    value = f"{num:x}"
    mac = sep.join(
        [value[i : i + chunk_size] for i in range(0, len(value), chunk_size)]
    )
    return mac


def cisco_format(num: int) -> str:
    return format_mac(num, ".", 4)


def standard_format(num: int) -> str:
    return format_mac(num, "-", 2)


def windows_format(num: int) -> str:
    return format_mac(num, ":", 2)


def generate_random_mac(format: str = "standard") -> str:
    formatters = {
        "standard": standard_format,
        "windows": windows_format,
        "cisco": cisco_format,
    }
    num = random.randint(1, 2**48)

    if format not in formatters:
        raise ValueError(f"Invalid format value {format}")

    formatter = formatters.get(format)
    return formatter(num)
