import enum
import re
from typing import List
from remote_controller.shells.shell import Shell
from remote_controller.utils.logger import Logger
from remote_controller.adapters.bluetooth.bluetooth_device import BluetoothDevice
from remote_controller.adapters.bluetooth.bluetooth_device import PairState
from remote_controller.adapters.bluetooth.bluetooth_profile import ProfileType
from remote_controller.adapters.bluetooth.bluetooth_profile import ConnectedState


class State(enum.Enum):
    STATE_OFF = 10
    STATE_TURNING_ON = 11
    STATE_ON = 12
    STATE_TURNING_OFF = 13


class ScanMode(enum.Enum):
    SCAN_MODE_NONE = 20
    SCAN_MODE_CONNECTABLE = 21
    SCAN_MODE_CONNECTABLE_DISCOVERABLE = 23


class BluetoothAdapter:
    __bluetooth_address_pattern = "[\\s\\S]*address:[\\s\\S](.*)[\\s\\S]*"
    __bluetooth_remote = "com.github.remotesdk.BLUETOOTH_REMOTE"

    __broadcast = "am broadcast -a"
    __bluetooth_broadcast = f"{__broadcast} {__bluetooth_remote}"

    __error_test = "ERROR_TEST"
    __get_address = "dumpsys bluetooth_manager"
    __enable = "enable"
    __disable = "disable"
    __get_state = "getState"
    __discoverable = "discoverable"
    __set_name = "setName"
    __get_name = "getName"
    __start_discovery = "startDiscovery"
    __cancel_discovery = "cancelDiscovery"
    __pair_device = "pairDevice"
    __get_discovered_devices = "getDiscoveredDevices"
    __set_pairing_confirmation = "setPairingConfirmation"
    __get_scan_mode = "getScanMode"
    __get_bonded_devices = "getBondedDevices"
    __get_remote_device = "getRemoteDevice"
    __is_enabled = "isEnabled"
    __factory_reset = "factoryReset"
    __get_bluetooth_class = "getBluetoothClass"
    __set_scan_mode = "setScanMode"
    __get_discoverable_timeout = "getDiscoverableTimeout"
    __set_discoverable_timeout = "setDiscoverableTimeout"
    __is_discovering = "isDiscovering"
    __get_connection_state = "getConnectionState"
    __get_profile_connection_state = "getProfileConnectionState"
    __remove_bond = "removeBond"
    __get_pair_state = "getPairState"
    __get_device_name = "getDeviceName"
    __get_device_type = "getDeviceType"
    __get_connected_profiles = "getConnectedProfiles"
    __device_cancel_pairing = "deviceCancelPairing"

    def __init__(self,
                 shell: Shell
                 ):
        self.shell = shell
        self.logger = Logger(scope_name=f"{BluetoothAdapter.__name__} [{shell.serial}")

    def enable(self) -> None:
        self.shell.execute_broadcast(self.__bluetooth_broadcast, self.__enable)
        self.logger.log(message="enable")

    def disable(self) -> None:
        self.shell.execute_broadcast(self.__bluetooth_broadcast, self.__disable)
        self.logger.log(message="disable")

    def is_enabled(self) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__is_enabled).title())
        self.logger.log(message=f"is enabled return [{str(result)}]")
        return result

    def get_state(self) -> State:
        result = State(int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                        self.__get_state)))
        self.logger.log(message=f"get state return [{result.name}]")
        return result

    def get_address(self) -> str:
        result = self.shell.execute(self.__get_address)
        if re.match(self.__bluetooth_address_pattern, result):
            address = re.search(self.__bluetooth_address_pattern, result).group(1)
            self.logger.log(message=f"get address return [{address}]")
            return address
        else:
            return ""

    def get_scan_mode(self) -> ScanMode:
        result = ScanMode(int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                           self.__get_scan_mode)))
        self.logger.log(message=f"get scan mode return [{result.name}]")
        return result

    def set_scan_mode(self,
                      scan_mode: ScanMode,
                      time: int
                      ) -> bool:
        result = eval(
            self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                         self.__set_scan_mode,
                                         scan_mode.value,
                                         time).title())
        self.logger.log(message=f"set scan mode [{str(scan_mode.name)}] return [{result}]")
        return result

    def start_discoverable(self,
                           time: int
                           ) -> None:
        self.shell.execute_broadcast(self.__bluetooth_broadcast, self.__discoverable, time)
        self.logger.log(message="start discoverable")

    def cancel_discoverable(self) -> None:
        self.set_scan_mode(ScanMode.SCAN_MODE_NONE, 0)
        self.logger.log(message="cancel discoverable")

    def is_discoverable(self) -> bool:
        result = self.get_scan_mode() is ScanMode.SCAN_MODE_CONNECTABLE_DISCOVERABLE
        self.logger.log(message=f"is discoverable return [{result}]")
        return result

    def get_name(self) -> str:
        result = self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                              self.__get_name)
        self.logger.log(message=f"get name return [{result}]")
        return result

    def set_name(self,
                 name: str
                 ) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__set_name,
                                                   name).title())
        self.logger.log(message=f"set name [{name}] return [{result}]")
        return result

    def start_discovery(self) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__start_discovery).title())
        self.logger.log(message=f"start discovery return [{result}]")
        return result

    def cancel_discovery(self) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__cancel_discovery).title())
        self.logger.log(message=f"cancel discovery return [{result}]")
        return result

    def is_discovering(self) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__is_discovering).title())
        self.logger.log(message=f"is discovering return [{result}]")
        return result

    def pair(self,
             address: str
             ) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__pair_device,
                                                   address).title())
        self.logger.log(message=f"pair device [{address}] return [{result}]")
        return result

    def get_discovered_devices(self) -> List[BluetoothDevice]:
        devices = []
        result = self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                              self.__get_discovered_devices)
        for address in result.split(","):
            if address:
                devices.append(BluetoothDevice(
                    self.shell,
                    address
                ))
        self.logger.log(message="get discovered devices")
        return devices

    def get_paired_devices(self) -> List[BluetoothDevice]:
        devices = []
        result = self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                              self.__get_bonded_devices)
        for address in result.split(","):
            if address:
                devices.append(BluetoothDevice(
                    self.shell,
                    address
                ))
        self.logger.log(message="get paired devices")
        return devices

    def factory_reset(self) -> bool:
        result = eval(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                                   self.__factory_reset).title())
        self.logger.log(message=f"factory reset return [{result}]")
        return result

    def remove_pair(self,
                    address: str
                    ) -> bool:
        result = eval(
            self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                         self.__remove_bond,
                                         address).title())
        self.logger.log(message=f"remove pair [{address}] return [{result}]")
        return result

    def remove_all_paired_devices(self) -> None:
        for device in self.get_paired_devices():
            self.remove_pair(device.address)

    def get_pair_state(self,
                       address: str
                       ) -> PairState:
        result = PairState(
            int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                             self.__get_pair_state,
                                             address)))
        self.logger.log(message=f"get device [{address}] pair state return [{result.name}]")
        return result

    def get_connected_profiles(self) -> List[ProfileType]:
        profiles = []
        result = self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                              self.__get_connected_profiles)
        for profile in result.split(","):
            if profile:
                profiles.append(ProfileType(int(profile)))
        self.logger.log(message="get connected profiles")
        return profiles

    def get_profile_connected_state(self,
                                    profile: ProfileType
                                    ) -> ConnectedState:
        result = ConnectedState(
            int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                             self.__get_profile_connection_state,
                                             profile.value)))
        self.logger.log(message=f"get profile [{profile.name}] connected state return [{result.name}]")
        return result

    def is_a2dp_sink_connected(self) -> bool:
        result = self.get_profile_connected_state(ProfileType.A2DP_SINK) == ConnectedState.STATE_CONNECTED
        self.logger.log(message=f"is A2DP_SINK connected [{str(result)}]")
        return result

    def get_connection_state(self) -> ConnectedState:
        result = ConnectedState(
            int(self.shell.execute_broadcast(self.__bluetooth_broadcast,
                                             self.__get_connection_state)))
        self.logger.log(message=f"get connection state return [{result.name}]")
        return result
