import socket
import sounddevice as sd
from time import sleep
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--samplerate', type=int, default=44100)
    parser.add_argument('--channels', type=int, default=2)
    parser.add_argument('--blocksize', type=int, default=8)
    parser.add_argument('--device', default='CABLE Output (VB-Audio Virtual ')
    args = parser.parse_args()

    sd.default.samplerate = args.samplerate
    sd.default.channels = args.channels
    sd.default.device = args.device
    sd.default.blocksize = args.blocksize

    global connection
    global stream

    def callback(indata, frame_count, time_info, status):
        if status:
            print(status)
        try:
            global connection
            connection.sendall(indata)

        except Exception as e:
            print(e)
            stream.stop()
            accept_connection()

    def accept_connection():
        print('Waiting for connection...')
        global connection
        connection, address = server_socket.accept()
        print('Client connected: {}'.format(address[0]))
        print('Streaming audio...')
        stream.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((args.host, args.port))
        server_socket.listen(1)
        global stream
        stream = sd.RawInputStream(callback=callback)
        accept_connection()

        # Lazy mechanism to keep the app from closing
        while True:
            sleep(100)
