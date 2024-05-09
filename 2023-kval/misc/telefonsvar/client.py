#!/usr/bin/env python3
import wave
import socket
import sys
import queue
import traceback
import threading

try:
    import pyaudio
except ImportError:
    traceback.print_exc()
    print(
        'Du har inte installerat PyAudio. Du kan göra det genom att köra "python -m pip install pyaudio"'
    )

# Du behöver inte förstå vad den här filen gör för att lösa uppgiften. Kort sagt kopplar den upp sig till servern och streamar ljud från den samtidigt som den skickar upp ljud från din mikrofon. På vissa datorer kan det här funka mindre bra, om du stöter på problem som du inte lyckas fixa försök då på en annan dator eller fråga en lagkamrat att testa på sin egen.

# för att ändra input/output enheter ändra dessa till ints som representerar indexet
default_input = None
default_output = None

p = pyaudio.PyAudio()
devices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]

pulseindex = None
for device in devices:
    if device["name"] == "pulse":
        pulseindex = device["index"]
        break
if not default_output and pulseindex is not None:
    default_output = pulseindex
if not default_input and pulseindex is not None:
    default_input = pulseindex

print("*" * 50)
for device in devices:
    print(device["index"], device["name"])

if default_input:
    device_input = p.get_device_info_by_index(default_input)
else:
    device_input = p.get_default_input_device_info()

if default_output:
    device_output = p.get_device_info_by_index(default_output)
else:
    device_output = p.get_default_output_device_info()

print()
print("Spelar in från:", device_input["index"], device_input["name"])
print("Spelar ljud på:", device_output["index"], device_output["name"])
print("För att ändra dessa enheter, redigera filen")
if pulseindex is not None:
    print("pulse brukar funka bäst på linux datorer")
print("*" * 50)

samplerate = 16000
blocksize = 600
blocksize_bytes = blocksize * 2

recv_audio = queue.Queue()
send_queue = []

n_recv = 0
n_sent = 0


def better_send(socket, buf):
    while len(buf):
        sent = socket.send(buf)
        buf = buf[sent:]
    return buf


def better_recv(socket, bufsize):
    try:
        buf = b""
        while len(buf) < bufsize:
            buf += socket.recv(bufsize - len(buf))
        return buf
    except ConnectionResetError:
        return b""


def callback(indata, frame_count, time_info, status):
    global send_queue

    try:
        if status:
            print("error:", status)

        send_queue.extend(indata)

        audio = []
        for _ in range(frame_count * 2):
            d = recv_audio.get()
            if d is None:
                print("out of data!")
                return bytes([]), pyaudio.paAbort

            audio.append(d)

        return bytes(audio), pyaudio.paContinue
    except:
        traceback.print_exc()


def send_blocks_to_server(s):
    global send_queue, n_sent

    try:
        while send_queue is not None:
            if len(send_queue) > blocksize_bytes:
                block = send_queue[:blocksize_bytes]
                send_queue = send_queue[blocksize_bytes:]

                # print("Sending block: ", n_recv - n_sent)
                better_send(s, bytes(block))
                n_sent += len(block)
    except:
        traceback.print_exc()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)
    s.connect((sys.argv[1], int(sys.argv[2])))

    try:
        stream = p.open(
            format=p.get_format_from_width(2),
            channels=1,
            rate=samplerate,
            input=True,
            output=True,
            frames_per_buffer=blocksize,
            stream_callback=callback,
            input_device_index=device_input["index"],
            output_device_index=device_output["index"],
        )
    except OSError:
        traceback.print_exc()
        print(
            "Något gick fel vid initialisering av audio. Testa byta audioenheter så kanske det löser sig. Läs texten mellan stjärnorna för mer info om hur man gör det."
        )
        exit(1)

    t = threading.Thread(target=send_blocks_to_server, args=(s,))
    t.start()

    while stream.is_active():
        try:
            while True:
                data = better_recv(s, blocksize_bytes)
                n_recv += len(data)
                # print("got", len(data))
                if data == b"":
                    recv_audio.put(None)
                    print("Audio stream ended, playing remaining and exiting...")
                    while not recv_audio.empty():
                        pass
                    break

                for b in data:
                    recv_audio.put(b)

        except KeyboardInterrupt:
            print("exiting...")
            recv_audio.put(None)
            send_queue = None
            t.join()

            break
