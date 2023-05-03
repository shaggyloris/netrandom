import re
import pytest
from netrandom import generate_random_mac, generate_random_ipv4, generate_random_ipv4_network

GEN_MAC_RGX = re.compile(r"^([a-fA-F0-9]{2,4}[:\-.]){2,5}([a-fA-F0-9]{2,4})$")
IEEE_MAC_RGX = re.compile(r"^([A-F0-9]{2}-){5}[A-F0-9]{2}$")
IETF_MAC_RGX = re.compile(r"^([a-f0-9]{2}:){5}[a-f0-9]{2}$")
CISCO_MAC_RGX = re.compile(r"^([a-f0-9]{4}.){2}[a-f0-9]{4}$")

def test_generate_mac():
    mac = generate_random_mac()
    assert isinstance(mac, str) is True
    match = GEN_MAC_RGX.match(mac)
    assert bool(match) is True
    
def test_mac_format():
    formats = [
        ("ieee", IEEE_MAC_RGX),
        ("ietf", IETF_MAC_RGX),
        ("cisco", CISCO_MAC_RGX)
        ]
    for fmt, rgx in formats:
        mac = generate_random_mac(format=fmt)
        assert bool(rgx.match(mac)) is True
        
    with pytest.raises(ValueError):
        generate_random_mac(format="foo")

def test_generate_ip():
    tests = [
        ({"require_type": "global"}, "is_global"),
        ({"require_type": "private"}, "is_private"),
        ({"require_type": "loopback"}, "is_loopback"),
        ({"require_type": "link_local"}, "is_link_local")
        ]
    for kwargs, attr in tests:
        ip = generate_random_ipv4(**kwargs)
        assert getattr(ip, attr) is True


def test_generate_network():
    with pytest.raises(ValueError):
        generate_random_ipv4_network(minimum_prefix=32, maximum_prefix=10)
    
    tests = [
        (8, 32),
        (24, 32),
        (8, 16),
        (16, 16)
        ]
    for min_p, max_p in tests:
        # Run each test 3 times because, you know, random
        for _ in range(3):
            net = generate_random_ipv4_network(minimum_prefix=min_p, maximum_prefix=max_p)
            assert min_p <= net.prefixlen <= max_p
