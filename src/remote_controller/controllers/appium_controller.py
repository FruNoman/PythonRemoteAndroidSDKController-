from appium import webdriver
from remote_controller.shells.appium_shell import AppiumShell
from remote_controller.adapters.bluetooth.bluetooth_adapter import BluetoothAdapter


class AppiumRemoteController:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.shell = AppiumShell(self.driver)

    def get_bluetooth_adapter(self) -> BluetoothAdapter:
        return BluetoothAdapter(self.shell)
