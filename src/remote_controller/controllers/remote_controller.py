from remote_controller.shells.android_shell import AndroidShell
from remote_controller.adapters.bluetooth.bluetooth_adapter import BluetoothAdapter


class RemoteController:
    def __init__(self, serial: str):
        self.serial = serial
        self.shell = AndroidShell(self.serial)

    def get_bluetooth_adapter(self) -> BluetoothAdapter:
        return BluetoothAdapter(self.shell)
