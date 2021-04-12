import speech_recognition as sr
import pyaudio as pa
import pygame

pygame.mixer.quit()
pygame.mixer.init()
# ding = pygame.mixer.Sound(r'ding.wav')
speech_on = pygame.mixer.Sound(r'speech on.wav')
speech_off = pygame.mixer.Sound(r'speech off.wav')

r = sr.Recognizer()
mic = sr.Microphone()

# print(sr.Microphone.list_microphone_names())
# with mic as source:
#     audio = r.listen(source)

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        print('Wait. Adjusting for ambient noise.')
        recognizer.adjust_for_ambient_noise(source,duration=1)
        print('Done')
        speech_on.play()
        audio = recognizer.listen(source)
        speech_off.play()
    
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio,language='pl-PL')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

text = recognize_speech_from_mic(r, mic)["transcription"]
print(text)

# text = r.recognize_google(audio)
# print(text)

# words = text.split()
# print(words)

# # numbers = ['zero','one','two','three','four','five','six','seven','eight','nine','ten']
# matchers_addition = ['+']
# matching = [word for word in words if any(match in word for match in matchers_addition)]

# nums = [float(word) for word in words if word.replace('.','',1).isdigit()]

# print(nums)

# nums = list_2 = [i for i in list_1 if isinstance(i, (int, float))]

# if matching