import json
from playsound import playsound

MORSE_JSON_FILES = 'morse.json'
MP3_LOCATION = 'morse_mp3_files'

class MorseDecoder:
    def __init__(self):
        self.morse_output = ''
        self.user_input = None

    def translate(self, user_input, morse_output_results_field):
        self.user_input = user_input

        with open('morse.json', 'r') as file:
            morse_dict = json.load(file)

        for letter in user_input.lower():
            if letter in morse_dict:
                self.morse_output += morse_dict[letter]

        # Update the label with the Morse code translation
        morse_output_results_field.config(text=f"{self.morse_output}")


    def play(self):
        letters = self.user_input
        for letter in letters:
            playsound(f'{MP3_LOCATION}\Morse-{letter}.ogg.mp3')