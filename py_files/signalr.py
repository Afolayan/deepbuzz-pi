from signalr_aio import Connection
from base64 import b64decode
from zlib import decompress, MAX_WBITS
import json


def process_message(message):
    deflated_msg = decompress(b64decode(message), -MAX_WBITS)
    return json.loads(deflated_msg.decode())


# Create debug message handler.
async def on_debug(**msg):
    # In case of 'queryExchangeState'
    if 'R' in msg and type(msg['R']) is not bool:
        decoded_msg = process_message(msg['R'])
        print(decoded_msg)


# Create error handler
async def on_error(msg):
    print("error is {0}".format(msg))
    print(msg)


# Create hub message handler
async def on_message(msg):
    print("message is {0}".format(msg))
    decoded_msg = process_message(msg[0])
    print(decoded_msg)


if __name__ == "__main__":
    # Create connection
    # Users can optionally pass a session object to the client, e.g a cfscrape session to bypass cloudflare.
    # connection = Connection('https://beta.bittrex.com/signalr', session=None)
    connection = Connection('http://localhost:5001', session=None)

    # Register hub
    # hub = connection.register_hub('c2')
    hub = connection.register_hub('chatHub')

    # Assign debug message handler. It streams unfiltered data, uncomment it to test.
    connection.received += on_debug

    # Assign error handler
    connection.error += on_error

    # Assign hub message handler
    hub.client.on('ReceiveMessage', on_message)
    # hub.client.on('uS', on_message)

    # Send a message
    hub.server.invoke('SendMessage1', 'BTC-ETH')
    # hub.server.invoke('SubscribeToSummaryDeltas')
    # hub.server.invoke('queryExchangeState', 'BTC-NEO')

    print(connection.hub)
    print(connection.url)
    # Start the client
    connection.start()
