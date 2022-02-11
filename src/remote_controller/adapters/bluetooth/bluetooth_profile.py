import enum


class ProfileType(enum.Enum):
    HEADSET = 1
    A2DP = 2
    HEALTH = 3
    HID_HOST = 4
    PAN = 5
    PBAP = 6
    GATT = 7
    GATT_SERVER = 8
    MAP = 9
    SAP = 10
    A2DP_SINK = 11
    AVRCP_CONTROLLER = 12
    AVRCP = 13
    HEADSET_CLIENT = 16
    PBAP_CLIENT = 17
    MAP_CLIENT = 18
    HID_DEVICE = 19
    OPP = 20
    HEARING_AID = 21
    MAX_PROFILE_ID = 21


class ConnectedState(enum.Enum):
    STATE_DISCONNECTED = 0
    STATE_CONNECTING = 1
    STATE_CONNECTED = 2
    STATE_DISCONNECTING = 3
