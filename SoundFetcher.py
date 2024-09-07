import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MP3_LOCATION = 'morse_mp3_files'
ALPHABET = 'ABCDBCDEFGHIJKLMNOPRSTUVWXYZ'

class SoundFetcher:

    def __init__(self):
        self.folder_setup()

        #set up chrome options
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.prefs = {"download.default_directory": self.folder_path}
        self.chrome_options.add_argument("--disable-search-engine-choice-screen")
        self.chrome_options.add_experimental_option("prefs", self.prefs)



    def folder_setup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))  # gets directory of where script is located
        self.folder_path = os.path.join(current_dir, MP3_LOCATION)  # full path of file to create

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f'folder created at {self.folder_path}')
        else:
            print(f'folder already exists at {self.folder_path}')

    def downloading_files(self):
        # initialize driver
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 5)

        download_progress = '' #replace dots with #
        display_threshold = 5

        if not os.listdir(self.folder_path):
            print(f'Downloading sounds from wikipedia...')

            for letter in ALPHABET:
                self.driver.get(f'https://commons.wikimedia.org/wiki/File:Morse-{letter}.ogg')
                link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@title='Download file']")))
                link.click()

                #Download_bar
                percent = round((len(download_progress) / len(ALPHABET)) * 100)
                download_progress += '#'

                if percent >= display_threshold:
                    print(f'Download currently at: {percent}%\n{download_progress}')

                    if display_threshold < 100:
                        display_threshold += 15

            self.driver.close()

        else:
            print(f'Sounds already present in folder')