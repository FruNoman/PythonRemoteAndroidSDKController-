import os
import subprocess
import re
import time
from src.remote_controller.shells.shell import Shell
import importlib.resources


class AndroidShell(Shell):

    def __init__(self, serial):
        self.serial = serial

    def execute(self, command: str) -> str:
        try:
            command = f"adb -s {self.serial} shell {command}".split()
            out = subprocess.check_output(command, timeout=60).decode()
            return out
        except subprocess.CalledProcessError:
            return ""

    def execute_broadcast(self, broadcast, command, *parameters) -> str:
        command_line = f'{broadcast} --es command {command}'
        for index, param in enumerate(parameters):
            command_line = command_line + f" --es param{index} '{param}'"
        if self.remote_package not in self.execute("pm list packages -3"):
            install = f"adb -s {self.serial} install -g {os.path.abspath(self.get_apk())}".split()
            subprocess.check_output(install, timeout=60)
        if self.remote_package not in self.execute("ps -A"):
            self.execute(f"am start -n {self.remote_package}/.MainActivity")
            time.sleep(10)
            self.execute("input keyevent KEYCODE_HOME")
        output = self.execute(command_line)
        if re.match(self.adapter_pattern, output):
            if f"result={str(self.error_code)}" in output:
                raise RuntimeError(re.search(self.adapter_pattern, output).group(1))
            elif f"result={str(self.success_code)}" in output:
                return re.search(self.adapter_pattern, output).group(1)
        elif f"result={str(self.error_code)}" in output:
            raise RuntimeError('Exception empty broadcast')
        elif f"result={str(self.success_code)}" in output and "data=" not in output:
            return ""
