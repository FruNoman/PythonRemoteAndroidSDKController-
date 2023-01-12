import re
import time
import subprocess
from appium import webdriver
from remote_controller.shells.shell import Shell


class AppiumShell(Shell):
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.serial = self.driver.execute_script("mobile: shell", {'command': 'getprop ro.boot.serialno'}).strip()

    def execute(self, command: str) -> str:
        try:
            return self.driver.execute_script("mobile: shell", {'command': f'{command}'})
        except Exception as e:
            return ''

    def execute_broadcast(self, broadcast, command, *parameters) -> str:
        command_line = f'{broadcast} --es command {command}'
        for index, param in enumerate(parameters):
            command_line = command_line + f" --es param{index} '{param}'"
        if self.remote_package not in self.execute("pm list packages -3"):
            install = f"adb -s {self.serial} install -g {self.get_apk()}".split()
            result = subprocess.check_output(install, timeout=60)
            time.sleep(5)
        if self.remote_package not in self.execute("ps -A"):
            self.execute(f"am start -n {self.remote_package}/.MainActivity")
            time.sleep(5)
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