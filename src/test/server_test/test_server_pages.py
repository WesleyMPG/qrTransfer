import pytest
from time import sleep


def test_example(selenium, base_url):
    selenium.get(f'{base_url}/upload')
    sleep(5)