import openai
import speech_recognition as sr
import os
from playsound import playsound
from gtts import gTTS


# set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# initialize the recognizer
r = sr.Recognizer()

# define the microphone as source
mic = sr.Microphone()

# get the device index of your microphone
mic_index = None
for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
    if "Scarlett Solo USB: Audio (hw:1,0)" in microphone_name:
        mic_index = i
        break

# if your microphone was not found, raise an error
if mic_index is None:
    raise Exception("Microphone not found.")

# define the microphone as source
mic = sr.Microphone(device_index=mic_index)

# adjust for ambient noise
# with mic as source:
#     r.adjust_for_ambient_noise(source)


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
    myobj.save("computer_voice.mp3")

    # Playing the converted file
    playsound("computer_voice.mp3")


# start listening for speech
with mic as source:
    while True:
        # recognize speech using Google Speech Recognition
        try:
            print("Listening ...")
            audio = r.listen(source, timeout=10)
            text = r.recognize_google(audio)
            print(f"You said: {text}")

            # call OpenAI GPT-3 API to generate response
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                max_tokens=100,
                n=1,
                stop=".",
                temperature=0.7,
                top_p=1,
            )

            # output the response from ChatGPT
            print("ChatGPT:", response.choices[0].text.strip())
            speak(response.choices[0].text.strip())

        except AssertionError:
            print("Could not understand audio.")
            continue
        except sr.WaitTimeoutError:
            print("Could not understand audio.")
            continue
        except sr.UnknownValueError:
            print("Could not understand audio.")
            continue
        except sr.RequestError as e:
            print(f"Error: {e}")
