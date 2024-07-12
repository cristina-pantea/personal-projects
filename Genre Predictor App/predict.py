import librosa
import statistics
import os
import pandas as pd
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from collections.abc import Iterable
import matplotlib.pyplot as plt
import pyaudio
import wave


def record_audio():
    os.remove("recording.wav")
    time.sleep(3)
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = 10
    filename = "recording.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def predict_genre():
    # start_time = time.time()
    df = pd.read_csv('Data/features_3_sec.csv', low_memory=True)
    list = []
    for i in range(0, 9990):
        if i % 10 != 0:
            list.append(i)
    df = df.drop(df.index[list])
    df.rename(columns={'chroma_stft_mean': 'chroma_stft_mean1'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    chroma_stft_mean1 = df["chroma_stft_mean1"]

    df2 = pd.read_csv('Data/features_30_sec.csv', low_memory=True)
    df2.rename(columns={'chroma_stft_mean': 'chroma_stft_mean2'}, inplace=True)
    df2 = df2.drop(df2.index[999])
    chroma_stft_mean2 = df2[["chroma_stft_mean2", "label", "tempo"]]
    chroma_stft = pd.concat([chroma_stft_mean1, chroma_stft_mean2], axis=1)

    model = LinearRegression()
    model.fit(chroma_stft[['chroma_stft_mean1']], chroma_stft['chroma_stft_mean2'])
    y_2 = model.predict(chroma_stft[['chroma_stft_mean1']])
    chroma_stft['chroma_predicted'] = y_2

    hop_length = 512
    file = os.path.join('recording.wav')
    y, sr = librosa.load(file)
    duration = librosa.get_duration(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo = "{:.2f}".format(tempo)
    duration = time.strftime("%H:%M:%S", time.gmtime(duration))
    chroma_test = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_test = chroma_test.tolist()
    chroma_test = flatten(chroma_test)
    chroma_test_mean = statistics.mean(chroma_test)

    value = find_nearest(chroma_stft['chroma_predicted'], value=chroma_test_mean)
    for i in range(0, 998):
        if chroma_stft['chroma_predicted'][i] == value:
            genre = chroma_stft['label'][i]
    return genre, tempo, duration

