import pytest
from server.uploader.helpers import PortProvider, UnableToGetAvailablePortError


def test_get_random_port_success(mocker):
    pp = PortProvider()
    mocker.patch('server.uploader.helpers.PortProvider._is_port_available', return_value=True)
    try:
        pp.get_random_port()
    except Exception as ex:
        assert False, f"Failed to get random port: {ex}"


def test_get_random_port_failure(mocker):
    pp = PortProvider()
    mocker.patch('server.uploader.helpers.PortProvider._is_port_available', return_value=False)
    with pytest.raises(UnableToGetAvailablePortError) as e:
        pp.get_random_port()