import logging
import sys
import threading
from signalrcore.hub_connection_builder import HubConnectionBuilder

from RaspPiCamera import CameraOptions


def onReceivedMessage(message):
    print("item: ", message[0])
    print("command: ", message[1])


def on_error(error):
    print("connection closed")
    print(error)


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


class SignalRCommands(threading.Thread):
    server_url = "wss://deepbuzz-project.azurewebsites.net/commandHub"

    username = "jeff"

    def __init__(self, threadID, name, counter):
        super().__init__()
        print(" SignalRCommands: __init__")
        self.hub_connection = HubConnectionBuilder() \
            .with_url(self.server_url) \
            .configure_logging(logging.DEBUG) \
            .with_automatic_reconnect({
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 5
                })\
            .build()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        self.setup_connection(onReceivedMessage)

    def setup_connection(self, onReceivedCommand):
        print("SignalRCommands: setup_connection")

        self.hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
        self.hub_connection.on_close(lambda: print("connection closed"))

        self.hub_connection.on("SendCommand", onReceivedMessage)
        self.hub_connection.on("SendCommand", onReceivedCommand)
        self.hub_connection.start()
        message = None

        while message != "exit()":
            message = input(">> ")
            if message is not None and message is not "" and message is not "exit()":
                self.hub_connection.send("SendMessage", [self.username, message])

    def close_connection(self):
        self.hub_connection.stop()

        sys.exit(0)

    @staticmethod
    def onReceivedCommand(message):
        print("item: ", message[0])
        print("command: ", message[1])

        if message[0] == 'camera':
            if message[1] == 'start':
                print("starting camera")
                cameraOptions.multiple_image_capture()
            else:
                print("stopping camera")
                cameraOptions.stop_capture()
        elif message[1] == 'video':
            if message[1] == 'start':
                print("starting video")
                count = 5

                print("count: " + str(count))
                cameraOptions.multiple_video_capture(count)
            else:
                print("stopping video")
                cameraOptions.stop_capture()


cameraOptions = CameraOptions()

commandsHub = SignalRCommands(1, "Thread-1", 1)
commandsHub.start()
commandsHub.run()

# server_url = "wss://deepbuzz-project.azurewebsites.net/commandHub"
#
# username = "jeff"
#
# hub_connection = HubConnectionBuilder() \
#     .with_url(server_url) \
#     .configure_logging(logging.DEBUG) \
#     .with_automatic_reconnect({
#     "type": "raw",
#     "keep_alive_interval": 10,
#     "reconnect_interval": 5,
#     "max_attempts": 5
# }).build()
#
# hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
# hub_connection.on_close(lambda: print("connection closed"))
#
# hub_connection.on("SendCommand", onReceivedMessage)
# hub_connection.start()
# message = None
#
# # Do login
#
# while message != "exit()":
#     message = input(">> ")
#     if message is not None and message is not "" and message is not "exit()":
#         hub_connection.send("SendMessage", [username, message])
#
# hub_connection.stop()
#
# sys.exit(0)
