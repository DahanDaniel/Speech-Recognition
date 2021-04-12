import speech_recognition as sr
import pyaudio as pa
import pygame

pygame.mixer.quit()
pygame.mixer.init()

speech_on = pygame.mixer.Sound(r'speech on.wav')
speech_off = pygame.mixer.Sound(r'speech off.wav')

r = sr.Recognizer()
mic = sr.Microphone()

keyWord1 = 'hey computer'
keyWord2 = 'hey Jarvis'

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:

        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 400
        audio = recognizer.listen(source,timeout=3)
    
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)#,language='pl-PL')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response["transcription"]

while True:
    try:
        text = recognize_speech_from_mic(r, mic)
        if (keyWord1.lower() in text.lower()) or (keyWord2.lower() in text.lower()):
            speech_on.play()
            print('Keyword detected in the speech.')
            message = recognize_speech_from_mic(r, mic)
            print(message)
            speech_off.play()
    except Exception:
        # print('Please speak again.')
        pass