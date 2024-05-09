import wave
import socket
import threading
import logging
import time
import random
from pathlib import Path
import numpy as np

samplerate = 16000
blocksize = 600
sample_dtype = np.int16
blocksize_bytes = sample_dtype().nbytes * blocksize
calculation_dtype = np.float64

dtmf_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
dtmf_chars = {  # key is indicies of frequencies above
    frozenset([0, 4]): "1",
    frozenset([1, 4]): "4",
    frozenset([2, 4]): "7",
    frozenset([3, 4]): "S",
    frozenset([0, 5]): "2",
    frozenset([1, 5]): "5",
    frozenset([2, 5]): "8",
    frozenset([3, 5]): "0",
    frozenset([0, 6]): "3",
    frozenset([1, 6]): "6",
    frozenset([2, 6]): "9",
    frozenset([3, 6]): "P",
    frozenset([0, 7]): "A",
    frozenset([1, 7]): "B",
    frozenset([2, 7]): "C",
    frozenset([3, 7]): "D",
}
exponentials = [
    np.exp(
        np.complex64(
            [-1j * (1 / samplerate * freq) * (2 * np.pi * n) for n in range(blocksize)]
        )
    )
    for freq in dtmf_freqs
]

# format: {location: ([**wav_names], choice_wav, [**next_locations])}
# when arriving at a path, all wav names will be played, after which choice_wav
# will follow 3 times with a delay at the end. if everything is played, the
# connection times out. if invalid input is detected, choice_wav will be played
# again 3 times. If at any time the None wav file is played, the worker will exit
paths = {
    "meny": (["meny"], "meny_val", ["tåg", "papegoja"]),
    # "papegoja": (["papegoja"], []),
    "tåg": (["1-tåget"], "1-tåget_val", ["borås", "campus", "hunger"]),
    "borås": (["1.1-borås"], None, []),
    "hunger": (["1.3-hunger"], None, []),
    "campus": (["2-campus"], "2-campus_val", ["bar", "lindholmen", "gu"]),
    "lindholmen": (["2.2-alkoholförgiftning"], None, []),
    "gu": (["2.3-GU"], None, []),
    "bar": (["3-bar"], "3-bar_val", ["vasa", "kajsa", "mc2", "basen", "eta"]),
    "vasa": (["3.1-vasa"], None, []),
    "mc2": (["3.3-mc2"], None, []),
    "basen": (["3.4-haskell"], None, []),
    "eta": (None, None, []),
    "kajsa": (["4-vandrarhem"], "4-vandrarhem_val", ["tid", "sen"]),
    "tid": (["4.1-i_tid", "5-ctf"], "5-ctf_val", ["dtmf", "gcd"]),
    "sen": (["4.2-sena", "5-ctf"], "5-ctf_val", ["dtmf", "gcd"]),
    "gcd": (["5.1-gcd"], None, []),
    # "dtmf": (None, "5.2-dtmf", []),
    "fel": (None, None, []),
    "rätt": (["5.2.2-rätt", "5.2.2.1-grattis"], None, []),
}


def read_wav(path):
    with wave.open(path.open("rb")) as wf:
        assert wf.getsampwidth() == sample_dtype().nbytes
        # print(wf.getframerate(), samplerate)
        assert wf.getframerate() == samplerate
        return np.frombuffer(wf.readframes(wf.getnframes()), dtype=sample_dtype)


wavs = {
    path.name.removesuffix(".wav"): read_wav(path) for path in Path("wavs").iterdir()
}
wavs["choice_pause"] = np.random.normal(0, 10, samplerate * 5).astype(sample_dtype)
wavs["papegoja_pause"] = np.random.normal(0, 10, int(samplerate * 0.5)).astype(
    sample_dtype
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(threadName)s] - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)


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


def conn_worker(conn, addr):
    logger.info(f"worker started, serving {addr}")

    conn.settimeout(5)

    ## navigation vars
    location = "meny"
    next_location = None

    ## audio vars
    # send a few blocks of audio ahead of time to avoid underflows in the client
    next_audio_time = time.time() - 0.5
    wavfile_name = paths["meny"][0] + [paths["meny"][1], "choice_pause"] * 3
    audio_progress = 0

    ## dtmf vars
    last_verified_char = ""
    last_char = ""
    char_repetitions = 0
    required_repetitions = 0.2 // (blocksize / samplerate)  # require some time of dtmf
    last_verified_char_time = 0
    message = ""

    iteration = 0

    with conn:
        while True:  # main worker loop
            iteration += 1
            # None wav means exit immediately
            if not wavfile_name[0]:
                break
            ## transmit. recieve and decode audio
            if next_audio_time < time.time():
                if wavfile_name and audio_progress < len(wavs[wavfile_name[0]]):
                    # continue sending wav file
                    data = wavs[wavfile_name[0]][
                        audio_progress : audio_progress + blocksize
                    ]
                    better_send(conn, np.pad(data, (0, blocksize - len(data))))
                    audio_progress += blocksize
                else:
                    # send 0's since audio is done
                    better_send(conn, np.zeros(blocksize, dtype=sample_dtype))

                next_audio_time += blocksize / samplerate

                # continue in order to have a few audio samples in the buffer
                if iteration <= 0.5 // (blocksize / samplerate):
                    continue

                # if audio needs transmitting, client audio also needs recieving
                indata = np.frombuffer(
                    better_recv(conn, blocksize_bytes), dtype=sample_dtype
                )
                # detect dtmf
                indata = indata.astype(calculation_dtype)
                energy = np.sum(np.power(indata, 2)) / blocksize
                if energy:
                    indata = indata / np.sqrt(energy)  # normalized energy
                else:
                    indata = indata * 0

                detected = set()
                for i, e in enumerate(exponentials):
                    amp = np.abs(np.sum(e * indata))
                    if amp > 40:
                        detected.add(i)

                # dtmf char logic
                detected = frozenset(detected)
                cur_char = dtmf_chars.get(detected, "")

                if cur_char == last_char:
                    char_repetitions += 1
                else:
                    char_repetitions = 0

                if (
                    char_repetitions >= required_repetitions
                    and last_verified_char != cur_char
                ):
                    if cur_char:
                        message += cur_char
                    last_verified_char = cur_char
                    last_verified_char_time = time.time()

                last_char = cur_char

            ## menu logic
            # if a message is ready
            if (
                message
                and last_char == ""
                and time.time() - last_verified_char_time > 1.5
            ):
                logger.info(f"got message {message}")
                match location:
                    case "papegoja":
                        if (
                            wavfile_name[0] == "choice_pause"
                            or wavfile_name[0] == "papegoja"
                        ):
                            wavfile_name = (
                                [
                                    item
                                    for c in message
                                    for item in [c, "papegoja_pause"]
                                ]
                                + ["choice_pause"]
                                + ["papegoja", "choice_pause"] * 3
                            )
                            audio_progress = 0
                    case "dtmf":
                        if message == "2356":
                            next_location = "rätt"
                        else:
                            location = "fel"
                            wavfile_name = (
                                ["invalid1"]
                                + [
                                    item
                                    for c in message
                                    for item in [c, "papegoja_pause"]
                                ]
                                + ["5.2.1-fel", None]
                            )
                            audio_progress = 0
                    case _:
                        if len(paths[location][2]):  # if  selections are available
                            try:
                                selection = int(message)
                                assert 1 <= selection <= len(paths[location][2])
                                next_location = paths[location][2][selection - 1]
                            except (ValueError, AssertionError):
                                wavfile_name = (
                                    ["invalid1"]
                                    + [
                                        item
                                        for c in message
                                        for item in [c, "papegoja_pause"]
                                    ]
                                    + ["invalid2"]
                                    + [paths[location][1], "choice_pause"] * 3
                                )
                                audio_progress = 0

                message = ""

            # if swiching locations
            if next_location:
                logger.info(f"navigating to {next_location}")
                match next_location:
                    case "papegoja":
                        wavfile_name = ["papegoja", "choice_pause"] * 3
                    case "dtmf":
                        wavfile_name = ["5.2-dtmf", "choice_pause"] * 10
                    case "mc2":
                        wavfile_name = (
                            paths["mc2"][0] + [paths["tåg"][1], "choice_pause"] * 3
                        )
                        next_location = "tåg"
                    case "eta":
                        wavfile_name = [
                            random.choice(
                                [
                                    "3.5.1-eta_ålder",
                                    "3.5.2-ETA_natriumpersulfanta",
                                    "3.5.3-simons_kretskort",
                                ]
                            ),
                            None,
                        ]
                    case _:
                        wavfile_name = (
                            paths[next_location][0]
                            + [paths[next_location][1], "choice_pause"] * 3
                        )

                audio_progress = 0
                location = next_location
                next_location = None

            # if audio is finished playing
            if wavfile_name and audio_progress >= len(wavs[wavfile_name[0]]):
                wavfile_name.pop(0)
                audio_progress = 0

            # timeout
            if not wavfile_name:
                if location == "timeout":
                    break
                logger.info("timing out")
                location = "timeout"
                wavfile_name = ["timeout"]
                audio_progress = 0

            # anti resource hugging sleep
            time.sleep(blocksize / samplerate * 0.1)

    logger.info(f"worker finished")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 1337))
    s.listen(1)
    logger.info("startup complete, listening...")
    while True:
        conn, addr = s.accept()
        logger.info(f"accepted connection from {addr}, starting worker...")
        thread = threading.Thread(target=conn_worker, args=(conn, addr), daemon=True)
        thread.start()
