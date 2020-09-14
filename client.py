import socket
import sounddevice as sd
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--samplerate', type=int, default=44100)
    parser.add_argument('--channels', type=int, default=2)
    parser.add_argument('--blocksize', type=int, default=8)
    parser.add_argument('--device', default=None)
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    sd.default.samplerate = args.samplerate
    sd.default.channels = args.channels

    while True:
        with socket.socket() as client_socket:
            print('Connecting to {}:{}...'.format(HOST, PORT))
            try:
                client_socket.connect((HOST, PORT))
            except Exception as e:
                print(e)
                continue
            print('Connected')

            print('Creating stream')
            with sd.RawOutputStream() as stream:
                stream.start()
                print('Stream started...')
                print("Getting data...")
                while True:
                    try:
                        data = client_socket.recv(args.blocksize)
                        stream.write(data)
                    except Exception as e:
                        print(e)
                        break
