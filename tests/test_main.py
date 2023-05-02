import ipaddress
import pytest
from netrandom import generate_random_mac, generate_random_ipv4


def test_generate_mac():
    ...

def test_generate_ip():
    pub_ip = generate_random_ipv4(allow_private=False)
    assert pub_ip.is_global is True
    priv_ip = generate_random_ipv4(allow_public=False)
    assert priv_ip.is_private is True
    
    loopback = generate_random_ipv4(allow_loopback=True,
                                    allow_multicast=False,
                                    allow_public=False,
                                    allow_link_local=False)
    assert loopback.is_loopback is True


