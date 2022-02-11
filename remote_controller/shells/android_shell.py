import os
import subprocess
import re
import time
from shell import Shell


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

    def execute_broadcast(self, command) -> str:
        if self.remote_package not in self.execute("pm list packages -3"):
            install = f"adb -s {self.serial} install -g {os.path.abspath(self.controll_apk)}".split()
            subprocess.check_output(install, timeout=60)
        if self.remote_package not in self.execute("ps -A"):
            self.execute(f"am start -n {self.remote_package}/.MainActivity")
            time.sleep(10)
            self.execute("input keyevent KEYCODE_HOME")
        output = self.execute(command)
        if re.match(self.adapter_pattern, output):
            if f"result={str(self.error_code)}" in output:
                raise RuntimeError('Exception from broadcast')
            elif f"result={str(self.success_code)}" in output:
                return re.search(self.adapter_pattern, output).group(3)
            elif f"result={str(self.empty_code)}" in output:
                raise RuntimeError('Exception empty broadcast')
        # else:
        #     raise RuntimeError('Exception empty broadcast')
