import wave
import sounddevice as sd
import numpy as np

sd.default.device = [
    None,
    None,
]  # Change these to ints, first one for playback and second for recording
sd.default.device = 6  # TODO remove

samplerate = 16000
blocksize = 600
sample_dtype = np.int16
calculation_dtype = np.float64

dtmf_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
dtmf_avg = [0]*8
dtmf_avg_multiplier = 0.7
dtmf_chars = {  # key is indicies of frequencies above
    frozenset([0, 4]): "1",
    frozenset([1, 4]): "4",
    frozenset([2, 4]): "7",
    frozenset([3, 4]): "*",
    frozenset([0, 5]): "2",
    frozenset([1, 5]): "5",
    frozenset([2, 5]): "8",
    frozenset([3, 5]): "0",
    frozenset([0, 6]): "3",
    frozenset([1, 6]): "6",
    frozenset([2, 6]): "9",
    frozenset([3, 6]): "#",
    frozenset([0, 7]): "A",
    frozenset([1, 7]): "B",
    frozenset([2, 7]): "C",
    frozenset([3, 7]): "D",
}

# k = (1 / samplerate * 1209) * blocksize
# c1 = np.exp(
#     np.complex64([-1j * k * (2 * np.pi * n) / blocksize for n in range(blocksize)])
# )

exponentials = [
    np.exp(
        np.complex64(
            [-1j * (1 / samplerate * freq) * (2 * np.pi * n) for n in range(blocksize)]
        )
    )
    for freq in dtmf_freqs
]

devices = sd.query_devices()
print(devices)
print(f"Recording from {devices[sd.default.device[1]]['name']}")


last_verified_char = ""
last_char = ""
char_repetitions = 0
required_repetitions = 0.15 // (blocksize/samplerate) # require 0.5s dtmf

data0 = []
data1 = []
data2 = []
data3 = []
data4 = []
data5 = []
data6 = []
data7 = []


def callback(indata, frames, time, status):
    global last_verified_char, last_char, char_repetitions

    if status:
        print(status)

    indata = indata[:, 0]
    indata = indata.astype(calculation_dtype)
    energy = np.sum(np.power(indata, 2)) / blocksize
    indata = indata / np.sqrt(energy)

    # data.append(energy)
    # data2.append(np.sum(np.power(indata, 2)) / blocksize)

    # noise = sum(
    #     np.abs(np.sum(e * np.power(indata, 1))) for e in (noise_exponentials)
    # ) / (len(noise_exponentials))

    # vol = np.sum(np.abs(indata)) // blocksize
    # print("vol:", vol)
    # data.append(vol)
    # indata *= 2**28 // vol
    # data2.append(np.sum(np.abs(indata)) // blocksize)

    detected = set()
    for i, e in enumerate(exponentials):
        amp = np.abs(np.sum(e * indata))
        dtmf_avg[i] = dtmf_avg[i] * dtmf_avg_multiplier + amp
        if dtmf_avg[i] > 200:
            detected.add(i)

    data0.append(dtmf_avg[0])
    data1.append(dtmf_avg[1])
    data2.append(dtmf_avg[2])
    data3.append(dtmf_avg[3])
    data4.append(dtmf_avg[4])
    data5.append(dtmf_avg[5])
    data6.append(dtmf_avg[6])
    data7.append(dtmf_avg[7])
    # print(
    #     "snr:",
    #     np.abs(np.sum(exponentials[0] * np.power(indata, 1))) / noise,
    # )

    detected = frozenset(detected)
    cur_char = dtmf_chars.get(detected, "")

    if cur_char == last_char:
        char_repetitions += 1
    else:
        char_repetitions = 0
    
    if char_repetitions >= required_repetitions and last_verified_char != cur_char:
        print(cur_char)
        last_verified_char = cur_char

    last_char = cur_char
    # if dtmf_chars.get(detected, "") != last_char:
    #     print(dtmf_chars.get(detected, ""))
    #     last_char = dtmf_chars.get(detected, "")


with sd.InputStream(
    channels=1,
    dtype=sample_dtype,
    callback=callback,
    samplerate=samplerate,
    blocksize=blocksize,
) as stream:
    try:
        sd.sleep(int(5000 * 1000))
    except KeyboardInterrupt:
        pass


from matplotlib import pyplot as plt

plt.plot(data0)
plt.plot(data1)
plt.plot(data2)
plt.plot(data3)
plt.plot(data4)
plt.plot(data5)
plt.plot(data6)
plt.plot(data7)
plt.show()
