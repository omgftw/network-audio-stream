import socket
import sounddevice as sd
from time import sleep
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--device', default='CABLE Output (VB-Audio Virtual ')
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    sample_rate = 44100

    sd.default.samplerate = sample_rate
    sd.default.channels = 2
    sd.default.device = args.device

    with socket.socket() as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        print("Creating stream...")
        test = sd.RawInputStream()
        test.start()
        print('Stream created')

        while True:
            print('Waiting for connection...')
            conn, address = server_socket.accept()
            print('Client connected: {}:{}'.format(address[0], address[1]))
            print('Sending data...')
            while True:
                sleep(0.05)
                data = test.read(test.read_available)
                try:
                    conn.send(data[0])
                except ConnectionResetError:
                    print('Client disconnected...')
                    break
