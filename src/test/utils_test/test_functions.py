import re
from utils import get_ip_list


def test_get_ip_list():
    ips = get_ip_list()
    assert isinstance(ips, list)
    for ip in ips:
        assert re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}', ip)