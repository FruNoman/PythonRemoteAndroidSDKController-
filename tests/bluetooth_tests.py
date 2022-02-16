import time
from remote_controller.controllers.remote_controller import RemoteController
from remote_controller.adapters.bluetooth.bluetooth_adapter import ScanMode
from remote_controller.adapters.bluetooth.bluetooth_adapter import ProfileType


def bluetooth_enable_disable():
    controller = RemoteController("0000")
    bluetooth_adapter = controller.get_bluetooth_adapter()
    bluetooth_adapter.enable()
    time.sleep(3)
    assert bluetooth_adapter.is_enabled()
    bluetooth_adapter.disable()
    time.sleep(3)
    assert not bluetooth_adapter.is_enabled()


def bluetooth_discoverable():
    controller = RemoteController("0000")
    bluetooth_adapter = controller.get_bluetooth_adapter()
    bluetooth_adapter.enable()
    time.sleep(3)
    assert bluetooth_adapter.is_enabled()
    bluetooth_adapter.start_discoverable(120)
    time.sleep(3)
    assert bluetooth_adapter.is_discoverable()
    assert bluetooth_adapter.get_scan_mode() == ScanMode.SCAN_MODE_CONNECTABLE_DISCOVERABLE
    bluetooth_adapter.stop_discoverable()
    assert not bluetooth_adapter.is_discoverable()
    assert bluetooth_adapter.get_scan_mode() == ScanMode.SCAN_MODE_NONE
    bluetooth_adapter.disable()
    time.sleep(3)
    assert not bluetooth_adapter.is_enabled()


def bluetooth_change_name():
    controller = RemoteController("0000")
    bluetooth_adapter = controller.get_bluetooth_adapter()
    bluetooth_adapter.enable()
    time.sleep(3)
    assert bluetooth_adapter.is_enabled()
    prev_name = bluetooth_adapter.get_name()
    bluetooth_adapter.set_name("Name with space")
    time.sleep(3)
    assert bluetooth_adapter.get_name() == "Name with space"
    bluetooth_adapter.set_name("Name-with#!!@#$%^&&**(()")
    time.sleep(3)
    assert bluetooth_adapter.get_name() == "Name-with#!!@#$%^&&**(()"
    time.sleep(3)
    bluetooth_adapter.set_name(prev_name)
    assert bluetooth_adapter.get_name() == prev_name


def bluetooth_discovery_device():
    controller = RemoteController("0000")
    bluetooth_adapter = controller.get_bluetooth_adapter()
    bluetooth_adapter.enable()
    time.sleep(3)
    assert bluetooth_adapter.is_enabled()
    bluetooth_adapter.start_discovery()
    time.sleep(60)
    bluetooth_adapter.cancel_discovery()
    for device in bluetooth_adapter.get_discovered_devices():
        device.get_pair_state()
        device.get_bluetooth_class()
        device.get_name()
        device.get_type()
        print('------------------------')
    bluetooth_adapter.disable()
    time.sleep(3)
    assert not bluetooth_adapter.is_enabled()


def bluetooth_profile():
    controller = RemoteController("0000")
    bluetooth_adapter = controller.get_bluetooth_adapter()
    bluetooth_adapter.enable()
    time.sleep(3)
    assert bluetooth_adapter.is_enabled()
    for profile in ProfileType:
        bluetooth_adapter.get_profile_connected_state(profile)
    bluetooth_adapter.disable()
    time.sleep(3)
    assert not bluetooth_adapter.is_enabled()


if __name__ == '__main__':
    # bluetooth_enable_disable()
    # bluetooth_discoverable()
    # bluetooth_change_name()
    bluetooth_discovery_device()
    # bluetooth_profile()
