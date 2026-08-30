# Remote Android SDK Controller (Python)

Python port of
[`JavaRemoteAndroidSDKController`](https://github.com/FruNoman/JavaRemoteAndroidSDKController).

Drive an Android device's internals — Bluetooth, Wi‑Fi, audio, telephony, location,
media, file system — **from an external Python test process**, instead of writing an
on‑device instrumentation test per case. Built for hardware‑in‑the‑loop
automotive‑infotainment automation.

## How it works

A thin shell abstraction runs commands and broadcasts on the device. The privileged
work is done on‑device by the companion app
([`RemoteAndroidApk`](https://github.com/FruNoman/RemoteAndroidApk)), invoked over
`am broadcast`. Two transports:

| Controller | Transport |
|---|---|
| `remote_controller.controllers.remote_controller.RemoteController` | `adb` (by device serial) |
| `remote_controller.controllers.appium_controller.AppiumRemoteController` | Appium `mobile: shell` |

## Install

```bash
git clone https://github.com/FruNoman/python-remote-android-sdk-controller
cd python-remote-android-sdk-controller
pip install .
```

or build a wheel: `python3 setup.py bdist_wheel` → `dist/*.whl`.

## Usage

```python
import time
from remote_controller.controllers.remote_controller import RemoteController

controller = RemoteController("<device-serial>")   # from `adb devices`
bluetooth = controller.get_bluetooth_adapter()

bluetooth.enable()
time.sleep(3)
assert bluetooth.is_enabled()

bluetooth.set_name("Bench unit 7")
for dev in bluetooth.get_paired_devices():
    print(dev)
```

With Appium instead:

```python
from remote_controller.controllers.appium_controller import AppiumRemoteController

controller = AppiumRemoteController(driver)   # an existing appium webdriver.Remote
controller.get_bluetooth_adapter().disable()
```

Runnable examples: `tests/bluetooth_tests.py`, `tests/appium_bluetooth_tests.py`.

## Status

The `BluetoothAdapter` is fully ported (enable/disable, discovery, discoverable mode,
naming, pairing, paired/discovered devices, profiles, connection state, factory
reset). The **Java project is the reference implementation** and additionally covers
wifi, audio, avrcp, location, telephony, sms, player, usb and the file system.

## Requirements

- Python 3.8+
- `adb` on `PATH`
- Companion app able to hold system/privileged permissions (userdebug/eng build,
  rooted device, or installed as a privileged app)

## License

MIT — see [LICENSE](LICENSE).
