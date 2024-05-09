import csv
import datetime
from pathlib import Path
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import pytz

# Disclaimer: Jag kan typ inte frekvensgrejer, så den här koden är mycket söligare än vad den skulle kunna vara. Jag lyckades dock komma på den genom att googla lite.

sample_rate, data = wavfile.read("brumm.wav")

segment_multiplier = 1000
segment_size = sample_rate

data = data[: -(len(data) % segment_size)]

fftfreqs = np.fft.fftfreq(segment_size * segment_multiplier, d=1 / sample_rate)
freqs = []

print("Processing FFT...")
iterations = len(data) // segment_size
for i in range(iterations):
    # vår chunk som vi kör FFT på paddas med 99.9% nollor för att få tillräckligt med precision ut från FFTn för att lösa uppgiften. om den inte hade paddats, och med en segmentstorlek på sample_size hade precisionen vart 1Hz alltså skulle scriptet alltid säga 50Hz. Det är just det här som är ooptimerat, för vi får ut väldigt exakta frekvenser för hela frekvensbandet som vi inte behöver. Jonathans lösning (jupyter notebooken) är bättre på det sättet och går mycket snabbare, men har också matte man typ inte kan förstå
    chunk = np.concatenate(
        [
            data[i * segment_size : (i + 1) * segment_size],
            np.zeros((segment_multiplier - 1) * segment_size),
        ]
    )
    fft = np.fft.fft(chunk)
    # få ut frekvensen med högst amplitud, det är lyckligtvis vår ~50Hz signal i alla fall då den är så högljud
    freq = abs(fftfreqs[np.argmax(np.abs(fft))])
    freqs.append(freq)
    print(f"{i+1}/{iterations}")

print("Loading fingrid data...")
dirty_source_freqs = []
for freqfile in sorted(Path("freqs").iterdir()):
    print(freqfile)
    with freqfile.open() as f:

        reader = csv.reader(f)
        next(reader)

        for row in reader:
            timestamp = (
                pytz.timezone("EET")
                .localize(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
                .timestamp()
            )

            if not timestamp.is_integer():
                continue

            dirty_source_freqs.append(
                [
                    timestamp,
                    float(row[1]),
                ]
            )

# fingrid lyckas missa några sekunder då och då så vi fyller dem med 50Hz
print("Patching holes in data...")
dirty_source_freqs.sort()
source_freqs = []
counter = 0
jan_1 = (
    pytz.timezone("EET").localize(datetime.datetime(2022, 1, 1, 0, 0, 0)).timestamp()
)
for i in range(31 * 24 * 3600):
    if dirty_source_freqs[counter][0] > i + jan_1:
        source_freqs.append(50)
        continue
    source_freqs.append(dirty_source_freqs[counter][1])
    counter += 1

print("Calculating best matching time...")

freqs = np.float32(freqs)
source_freqs = np.float32(source_freqs)

scores = []

# för varje sekund i månaden kollar vi på skillnaden mellan ljudfilen och väggfrekvensen då, tar summan av den arrayen och kollar vilken sekund som är minst för att lista ut när inspelningen hände. det här är förvånandsvärt snabbt i python
for i in range(len(freqs), 31 * 24 * 3600 - len(freqs)):
    scores.append(np.sum(np.abs(source_freqs[i : i + len(freqs)] - freqs)))

found_timestamp = (
    jan_1 + len(freqs) + scores.index(min(scores)) + 3 * 60 + 31
)  # offset för när jonathan knäpper fingrarna

print(found_timestamp)
print(datetime.datetime.fromtimestamp(found_timestamp))

plt.plot(freqs)
plt.plot(
    source_freqs[
        len(freqs)
        + scores.index(min(scores)) : len(freqs)
        + scores.index(min(scores))
        + len(freqs)
    ]
)
plt.show()
