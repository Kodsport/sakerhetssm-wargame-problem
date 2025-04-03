import wave
import socket
import sys
import queue

try:
    import sounddevice as sd
except ImportError:
    traceback.print_exc()
    print(
        'Du har inte installerat sounddevice. Du kan göra det genom att köra "python -m pip install sounddevice"'
    )


# Du behöver inte förstå vad den här filen gör för att lösa uppgiften. Kort sagt kopplar den upp sig till servern och streamar ljud från den samtidigt som den skickar upp ljud från din mikrofon. På vissa datorer kan det här funka mindre bra, om du stöter på problem som du inte lyckas fixa försök då med den andra klienten, på en annan dator eller fråga en lagkamrat att testa på sin egen.

# för att ändra input/output enheter ändra dessa till ints som representerar indexet
default_input = None
default_output = None

devices = sd.query_devices()

pulseindex = None
for device in devices:
    if device["name"] == "pulse":
        pulseindex = device["index"]
        break
if not default_output and pulseindex is not None:
    default_output = pulseindex
if not default_input and pulseindex is not None:
    default_input = pulseindex

sd.default.device = [default_output, default_input]

print("*" * 50)
print(devices)
print(
    f"Spelar in från: {devices[sd.default.device[1]]['index']} {devices[sd.default.device[1]]['name']}"
)
print(
    f"Spelar ljud på: {devices[sd.default.device[0]]['index']} {devices[sd.default.device[0]]['name']}"
)
print("För att ändra dessa enheter, redigera filen")
if pulseindex is not None:
    print("pulse brukar funka bäst på linux datorer")
print("*" * 50)

samplerate = 16000
blocksize = 600
blocksize_bytes = blocksize * 2

recv_audio = queue.Queue()


def better_send(socket, buf):
    while len(buf):
        sent = socket.send(buf)
        buf = buf[sent:]
    return buf


def better_recv(socket, bufsize):
    buf = b""
    while len(buf) < bufsize:
        res = socket.recv(bufsize - len(buf))
        buf += res
        if res == b"":
            break
    return buf


def callback(indata, outdata, frames, time, status):
    global s
    if status:
        print(status)

    data = recv_audio.get()
    if data == b"":
        raise sd.CallbackStop
    # print(frames, len(data))
    better_send(s, indata)
    outdata[:] = data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)
    s.connect((sys.argv[1], int(sys.argv[2])))

    with sd.RawStream(
        channels=1,
        dtype="int16",
        callback=callback,
        samplerate=samplerate,
        blocksize=blocksize,
    ) as stream:
        try:
            while True:
                data = better_recv(s, blocksize_bytes)
                if data == b"":
                    recv_audio.put(b"")
                    print("Audio stream ended, playing remaining and exiting...")
                    while not recv_audio.empty():
                        pass
                    stream.stop()
                    break
                recv_audio.put(data)
        except KeyboardInterrupt:
            print("exiting...")
            recv_audio.put(b"")
            stream.stop()
