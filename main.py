import openai
import speech_recognition as sr
import os
import threading
from helpers import countdown, speak

# Parameters
timeout = 5

# set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# initialize the recognizer
r = sr.Recognizer()

# define the microphone as source
mic = sr.Microphone()

# get the device index of your microphone
mic_index = None
microphone_names = sr.Microphone.list_microphone_names()
while True:
    for i, microphone_name in enumerate(microphone_names):
        print(f"{i}: {microphone_name}")
    selected_index = input("Please select a microphone index: ")
    if selected_index.isdigit() and int(selected_index) < len(microphone_names):
        mic_index = int(selected_index)
        print(f"Selected microphone: {microphone_names[mic_index]}")
        break
    else:
        print("Invalid input.")

# if your microphone was not found, raise an error
if mic_index is None:
    raise Exception("Microphone not found.")

# define the microphone as source
mic = sr.Microphone(device_index=mic_index)

# adjust for ambient noise
with mic as source:
    r.adjust_for_ambient_noise(source)

history = []

# start listening for speech
with mic as source:
    while True:
        # recognize speech using Google Speech Recognition
        try:
            print("Listening ...")
            # threading.Thread(countdown(timeout))
            audio = r.listen(source, timeout=timeout)
            text = r.recognize_whisper(audio)
            history.append(text)
            print(f"You said: {text}")

            # call OpenAI GPT-3 API to generate response
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="\n".join(history),
                max_tokens=100,
                n=1,
                # stop=".",
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
