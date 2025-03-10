import pyttsx4
import pygame
import random

engine = pyttsx4.init()
voices = engine.getProperty('voices')

#for voice in engine.getProperty('voices'):
#    if 'Eva' in voice.name:  # Adjust based on the specific voice name format
#        engine.setProperty('voice', voice.id)
#        break
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def searchingSounds():
    sounds = ["aiAffirmative.mp3", "aiCameraSound.mp3", "aiSearch.mp3", "aiSwap.mp3"]
    sound = random.choice(sounds)
    play_sound(sound)

def play_sound(file_path):
    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Play the sound
    pygame.mixer.music.play()

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Check every 10ms if the music has finished