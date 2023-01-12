import importlib_resources


class Shell(object):
    remote_package = "com.github.remotesdk"
    adapter_pattern = '.*\n?.*data="(.*\n?.*)".*\n?.*'
    error_code = 123
    success_code = 373
    empty_code = 0
    serial = ''

    def execute(self, command: str) -> str:
        pass

    def execute_broadcast(self, broadcast, command, *parameters) -> str:
        pass

    def get_serial(self) -> str:
        pass

    def get_apk(self) -> str:
        my_resources = importlib_resources.files("remote_controller.resources")
        return (my_resources / "app-debug.apk")
