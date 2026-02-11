import speech_recognition as sr

def listen_for_command(language="en-US") -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (say your command)")
        r.adjust_for_ambient_noise(source, duration=0.6)
        audio = r.listen(source, phrase_time_limit=6)

    try:
        text = r.recognize_google(audio, language=language)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("Voice service unavailable (internet issue).")
        return ""
