import enum
from remote_controller.shells.shell import Shell
from remote_controller.utils.logger import Logger
from remote_controller.adapters.bluetooth.bluetooth_class import BluetoothClass


class PairState(enum.Enum):
    NONE = 10
    PAIRING = 11
    PAIRED = 12


class Type(enum.Enum):
    DEVICE_TYPE_UNKNOWN = 0
    DEVICE_TYPE_CLASSIC = 1
    DEVICE_TYPE_LE = 2
    DEVICE_TYPE_DUAL = 3


class BluetoothDevice:
    __bluetooth_remote = "com.github.remotesdk.BLUETOOTH_REMOTE"

    __broadcast = "am broadcast -a"
    __bluetooth_broadcast = f"{__broadcast} {__bluetooth_remote}"

    __get_pair_state = f"getPairState"
    __get_device_name = f"getDeviceName"
    __get_device_type = f"getDeviceType"
    __get_device_class = f"getDeviceClass"
    __disconnect = f"DisconnectDeviceProfile"
    __connect = f"ConnectDeviceProfile"

    def __init__(self,
                 shell: Shell,
                 address: str):
        self.shell = shell
        self.address = address
        self.logger = Logger(scope_name=f"{shell.serial}] [{BluetoothDevice.__name__}]")

    def get_pair_state(self) -> PairState:
        result = PairState(
            int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                             self.__get_pair_state,
                                             self.address)))
        self.logger.log(message=f"get bluetooth device [{self.address}] pair state return [{result.name}]")
        return result

    def get_name(self) -> str:
        result = self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                              self.__get_device_name,
                                              self.address)
        self.logger.log(message=f"get bluetooth device [{self.address}] name return [{result}]")
        return result

    def get_type(self) -> str:
        result = Type(
            int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                             self.__get_device_type,
                                             self.address)))
        self.logger.log(message=f"get bluetooth device [{self.address}] type return [{result.name}]")
        return result

    def get_bluetooth_class(self) -> BluetoothClass:
        result = BluetoothClass(
            int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                             self.__get_device_class,
                                             self.address)))
        self.logger.log(
            message=f"get bluetooth device [{self.address}] class return [{result}]")
        return result

    def __str__(self):
        return self.address
