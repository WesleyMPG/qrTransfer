from subprocess import Popen
from time import sleep
import pytest
from server.uploader.helpers import PortProvider, UnableToGetAvailablePortError


@pytest.fixture
def port_provider():
    return PortProvider()


def test_port_is_numeric(port_provider):
    port = port_provider.get_random_port()
    assert isinstance(port, int)


def test_port_is_random(port_provider):
    port1 = port_provider.get_random_port()
    port2 = port_provider.get_random_port()
    assert port1 != port2


def test_retry_if_randomized_port_is_in_use(mocker, port_provider):
    mocker.patch('server.uploader.helpers.randint', side_effect=[8080, 5001])
    mocker.patch('server.uploader.helpers.PortProvider._is_port_available', side_effect=[False, True])
    port = port_provider.get_random_port()
    assert port == 5001


def test_get_random_port_failure_on_max_port_tries_reached(mocker, port_provider):
    mock = mocker.patch('server.uploader.helpers.PortProvider._is_port_available', return_value=False)
    with pytest.raises(UnableToGetAvailablePortError) as e:
        port_provider.get_random_port()
        assert mock.call_count == PortProvider.MAX_PORT_TRIES