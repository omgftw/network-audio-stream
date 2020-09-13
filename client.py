import socket
import sounddevice as sd
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--device', default=None)
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    sample_rate = 44100

    sd.default.samplerate = sample_rate
    sd.default.channels = 2

    with socket.socket() as client_socket:
        while True:
            print('Connecting to {}:{}...'.format(HOST, PORT))
            client_socket.connect((HOST, PORT))
            print('Connected')

            print('Creating stream')
            test = sd.RawOutputStream()
            test.start()
            print('Stream started...')
            print("Getting data...")
            while True:
                try:
                    data = client_socket.recv(8)
                    test.write(data)
                except ConnectionResetError:
                    print('Server closed. Attempting to reconnect...')
                    break
