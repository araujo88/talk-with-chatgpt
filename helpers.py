import time
import os
from playsound import playsound
from gtts import gTTS
from pydub import AudioSegment


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    print('Time is up!')


def speak(text):
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("audio.mp3")

    # Load the audio file using pydub
    # audio = AudioSegment.from_file("audio.mp3")

    # Speed up the audio by 1.5 times
    # audio_faster = audio.speedup(playback_speed=1.5)

    # Export the sped up audio file to a temporary file
    # temp_file = "temp_file.mp3"
    # audio_faster.export(temp_file, format="mp3")

    # Playing the converted file
    playsound("audio.mp3")

    # Delete the temporary file
    # os.remove(temp_file)
