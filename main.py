from SoundFetcher import SoundFetcher
from morse_text_decoder import MorseDecoder

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

morse = MorseDecoder()
sounds = SoundFetcher()


def on_translate():
    user_input = input_alphabet.get()
    morse.translate(user_input, morse_output_results_field)


def play():
    sounds.downloading_files()
    morse.play()


if __name__ == '__main__':
    # set up window
    window = tk.Tk()
    window.title("Morse Code Translator")
    window.config(padx=20, pady=20)

    # Create a Canvas for the image
    canvas = Canvas(width=200, height=200)

    original_image = Image.open("morse-code.png")
    resized_image = original_image.resize((100, 100), Image.LANCZOS)

    lock_img = ImageTk.PhotoImage(resized_image)
    canvas.create_image(100, 100, image=lock_img)
    canvas.grid(column=1, row=0)

    # text
    alphabet_text = Label(text="Alphabet input:", font=("Calibri", 10))
    alphabet_text.grid(column=0, row=1)

    morse_output_text = Label(text="morse code output:", font=("Calibri", 10))
    morse_output_text.grid(column=0, row=2, sticky="w")

    morse_output_results_field = Label(text="", font=("Calibri", 10))
    morse_output_results_field.grid(column=1, row=2, sticky="w")

    # inputs
    input_alphabet = Entry(width=30)
    input_alphabet.focus()
    input_alphabet.grid(column=1, row=1, columnspan=2, sticky="w")

    # buttons
    generate_morse_button = Button(text="Generate morse code", width=25, command=on_translate)
    generate_morse_button.grid(column=2, row=1, sticky="w")

    morse_sound = Button(text="listen to sound", width=8, command=play)
    morse_sound.grid(column=1, row=4, columnspan=4, sticky="ew")

    window.mainloop()