import speech_recognition as sr

# Instaniate recognizer class
recognizer = sr.Recognizer()

def transcribe(audio_file):
    res = sr.AudioFile(audio_file)
    with res as source:
        audio = recognizer.record(source)
    # Transcribe speech using Google web API
    return recognizer.recognize_google(audio_data=audio, language='en-US')
    
print(transcribe('result.wav'))