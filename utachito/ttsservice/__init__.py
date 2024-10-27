from __future__ import annotations

import threading
from typing import Generator, Iterable

from pyht.client import Client, TTSOptions, Language
import os

from pydub import AudioSegment
from pydub.playback import play

class TTSService:
    def __init__(self):
        self.user_id = os.getenv("PLAY_HT_USER_ID")
        self.api_key = os.getenv("PLAY_HT_API_KEY")
        self.client = Client(self.user_id, self.api_key)
        self.voice = "s3://voice-cloning-zero-shot/a93cf217-658d-43fd-b529-74ca6d3e1102/original/manifest.json"
        self.language = Language.SPANISH
        self.speed = 0.9


    def save_audio(self, data: Generator[bytes, None, None] | Iterable[bytes]):
        chunks: bytearray = bytearray()
        for chunk in data:
            chunks.extend(chunk)
        with open("utachito.wav", "wb") as f:
            f.write(chunks)

    def play_saved_audio(self):
        audio = AudioSegment.from_wav("utachito.wav")
        play(audio)


    def generate_audio(self, text: Iterable[str]):
        options = TTSOptions(voice=self.voice, language=Language(self.language), speed=self.speed)

        voice_engine = "Play3.0-mini-http"
        in_stream, out_stream = self.client.get_stream_pair(options, voice_engine=voice_engine)

        audio_thread = threading.Thread(None, self.save_audio, args=(out_stream,))
        audio_thread.start()

        for t in text:
            in_stream(t)
        in_stream.done()

        audio_thread.join()
        out_stream.close()

        metrics = self.client.metrics()
        print(str(metrics[-1].timers.get("time-to-first-audio")))

        self.client.close()
