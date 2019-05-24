import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google_images_download import google_images_download
import pyaudio
import wave

# Instantiates a client
client = speech.SpeechClient()


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME_PREFIX = "resources/output"

j = 0

while True:

	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)

	print("*recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("*done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME_PREFIX + str(j) + ".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	# The name of the audio file to transcribe
	file_name = os.path.join(
	    os.path.dirname(__file__),
	    'resources',
	    'output' + str(j) + '.wav')

	# Loads the audio into memory
	with io.open(file_name, 'rb') as audio_file:
	    content = audio_file.read()
	    audio = types.RecognitionAudio(content=content)

	config = types.RecognitionConfig(
	    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
	    sample_rate_hertz=44100,
	    language_code='en-US')

	# Detects speech in the audio file
	response = client.recognize(config, audio)

	for result in response.results:
	    print('Transcript: {}'.format(result.alternatives[0].transcript))

	arguments = {
	        "keywords": result.alternatives[0].transcript,
	        "limit": 5,
	        "print_urls": False
	    }

	response = google_images_download.googleimagesdownload()
	absolute_image_paths = response.download(arguments)
	j += 1