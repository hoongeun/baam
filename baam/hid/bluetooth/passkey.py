from typing import Callable
from micropython import const


ACTION_INPUT = const(2)
ACTION_DISP = const(3)
ACTION_NUMCMP = const(4)


class PassKeyActor:
    def __init__(self):
        self.passkey_input_handler = None
        self.passkey = ""

    def handle_action(self, ble, data):
        conn_handle, action, passkey = data
        if action == ACTION_NUMCMP.value():  # Do we accept this connection?
            accept = False
            if self.passkey_input_handler is not None:  # Is callback function set?
                accept = self.passkey_input_handler()  # Call callback for input
            ble.gap_passkey(conn_handle, action, accept)
        elif action == ACTION_DISP.value():  # Show our passkey
            ble.gap_passkey(conn_handle, action, self.passkey)
        elif action == ACTION_INPUT.value():  # Enter passkey
            passkey = None
            if self.passkey_input_handler is not None:  # Is callback function set?
                passkey = self.passkey_input_handler()  # Call callback for input
            ble.gap_passkey(conn_handle, action, passkey)
        else:
            ValueError("unknown passkey action")