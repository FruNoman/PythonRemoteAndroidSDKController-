class Shell(object):
    remote_package = "com.github.remotesdk"
    adapter_pattern = '.*\n?.*data="(.*\n?.*)".*\n?.*'
    error_code = 123
    success_code = 373
    empty_code = 0

    def execute(self, command: str) -> str:
        pass

    def execute_broadcast(self, command: str) -> str:
        pass

    def get_serial(self) -> str:
        pass
