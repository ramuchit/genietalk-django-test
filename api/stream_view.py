from rest_framework.views import APIView
from rest_framework.response import Response
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import time
import numpy as np
import os
from django.contrib.staticfiles.storage import staticfiles_storage


class StreamView(APIView):

    def post(self, request, *args):
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        audio_path= os.path.join(static_path, 'audio.wav')
        self.record_voice(path=audio_path)
        self.start_convertion(path=audio_path, output_path=os.path.join(static_path, 'audio.txt'))
        return Response(staticfiles_storage.url('audio.txt'))

    def start_convertion(self, path='output.wav', output_path='audio.txt', lang='en-IN'):
        time.sleep(12)
        with sr.AudioFile(path) as source:
            print('Fetching File')
            # Initialize the recognizer
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            audio_text = r.record(source)
            try:
                # using google speech recognition
                print('Converting audio transcripts into text ...')
                text = r.recognize_google(audio_text)
                with open(output_path, 'w+') as f:
                    f.write(text)
                os.remove(path)
            except:
                print('Sorry.. run again...')

    def record_voice(self, path="audio.wav"):
        fs = 44100
        second = 10
        print('Recording...')
        data = sd.rec(int(fs * second), samplerate=fs, channels=2)
        sd.wait()
        y = (np.iinfo(np.int32).max * (data / np.abs(data).max())).astype(np.int32)
        write(path, fs, y)