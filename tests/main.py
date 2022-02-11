import importlib
import subprocess
import time

import importlib_resources

import pkg_resources
from src.remote_controller.controllers.remote_controller import RemoteController


def print_hi():
    controller = RemoteController("N0AA003759K70700223")
    bluetooth_adapter = controller.get_bluetooth_adapter()
    bluetooth_adapter.enable()
    time.sleep(2)
    assert bluetooth_adapter.is_enabled()
    bluetooth_adapter.disable()
    time.sleep(2)
    assert not bluetooth_adapter.is_enabled()



if __name__ == '__main__':
    print_hi()
