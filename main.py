import json
import os

import tkinter as tk
from tkinter import *
from playsound import playsound
from PIL import Image, ImageTk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MORSE_JSON_FILES =  'morse.json'
MP3_LOCATION = 'morse_mp3_files'

def morse_trans(user_input):
    with open(MORSE_JSON_FILES, 'r') as file:
        morse_dict = json.load(file)

    morse_output = " "

    for letter in user_input.lower():
        morse_output += morse_dict[letter]

    return morse_output


def mp3_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__)) #gets directory of where script is located
    folder_path = os.path.join(current_dir, MP3_LOCATION) #full path of file to create

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'folder created at {folder_path}')
    else:
        print(f'folder already exists at {folder_path}')

    return folder_path


def get_sounds():
    folder_path = mp3_folder()
    alphabet_morse = 'ABCDBCDEFGHIJKLMNOPRSTUVWXYZ'

    if not os.listdir(folder_path):
        print(f'Downloading sounds from wikipedia...')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        prefs = {"download.default_directory": folder_path}
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 5)

        for letter in alphabet_morse:
            driver.get(f'https://commons.wikimedia.org/wiki/File:Morse-{letter}.ogg')
            link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@title='Download file']")))
            link.click()


def on_translate():
    input_text = input_alphabet.get()
    output_text = morse_trans(input_text)
    morse_output_results.config(text=f"{output_text}")


def play():
    letters = input_alphabet.get()
    for letter in letters:
        playsound(f'{MP3_LOCATION}\Morse-{letter}.ogg.mp3')

if __name__ == '__main__':

    get_sounds() #Makes file and scrapes mp3 files from wikipedia

    #set up window
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

    #text
    alphabet_text = Label(text="Alphabet input:", font=("Calibri", 10))
    alphabet_text.grid(column=0, row=1)

    morse_output_text = Label(text="morse code output:", font=("Calibri", 10))
    morse_output_text.grid(column=0, row=2, sticky="w")

    morse_output_results = Label(text="", font=("Calibri", 10))
    morse_output_results.grid(column=1, row=2, sticky="w")

    #inputs
    input_alphabet = Entry(width=30)
    input_alphabet.focus()
    input_alphabet.grid(column=1, row=1, columnspan=2, sticky="w")

    #buttons
    generate_morse_button = Button(text="Generate morse code", width=25, command=on_translate)
    generate_morse_button.grid(column=2, row=1, sticky="w")

    morse_sound= Button(text="listen to sound", width=8, command=play)
    morse_sound.grid(column=1, row=4, columnspan=4, sticky="ew")

    window.mainloop()



