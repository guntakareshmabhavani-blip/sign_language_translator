import pyttsx3

engine = pyttsx3.init()

engine.say("Hello")
engine.runAndWait()

engine.say("Second")
engine.runAndWait()

engine.say("Third")
engine.runAndWait()

print("Done")