#! /usr/bin/env python3

import os
import glob
import random
import importlib
import argparse
from playsound import playsound
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewAudioFileHandler(FileSystemEventHandler):
    """
    Watch for changs in sounddir and update the list if files are changed
    """
    def __init__(self, gerausch):
        self.krach = gerausch

    def on_any_event(self, event):
        events = ['created', 'deleted', 'modified', 'moved']
        if event.event_type in events:
            print("Files in sound direcotry changed - updateing")
            self.krach.updateSoundFiles()
            print("\t...done")
class Krach:
    """
    Class to play a random sound from a direcotry on the press of a key/button.
    """

    def setupGPIO(self, mode, pin: int) -> None:
        """
        Initializes the GPIO if we are on a raspberry pi.
        By default pin 10 is used, initialy pulled low, with the GPIO.BOARD numbering scheme.

        Parameters:
        -----------
        mode = Pin numbering scheme for the GPIO (Default: GPIO.BOARD)
        pin:int = Pin number to use (Default: 10)
        """
        if self.haz_gpio:
            GPIO.setwarnings(False) # Ignore warning for now
            GPIO.setmode(mode) # Use physical pin numbering: GPIO.BOARD
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

    def getSoundFiles(self) -> list:
        """
        Returns a list of audio files in a directory.
        Supported files are: mp3, wav , flac and ogg
        To add file types, extend the formats list.
        Do we want to make the formats configurable?
        If we want this to be recursive, add an recursive:true to the glob.

        Returns:
        -------
        list<str> = A list of all audio filepaths of that directory as string.
        """
        file_list = []
        if not os.path.isdir(self.sounddir):
            return file_list
        formats=["*.mp3", "*.wav", "*.flac", "*.ogg"]
        for extension in formats:
            file_list = file_list + glob.glob(self.sounddir + os.sep + extension)
        return file_list

    def updateSoundFiles(self):
        self.updateFileList = True
        self.soundfiles = []
        self.soundfiles = self.getSoundFiles()
        self.updateFileList = False

    def __init__(self, sounddir:str, pin:int) -> None:
        """
        Initialise the Krach-object.

        Parameters:
        -----------
        sounddir:str = Path to the directory with the audio files.
        pin:int = Raspberry pi GPIO pin to use
        """
        print("Sounddir: " + sounddir)
        self.sounddir = sounddir
        self.updateSoundFiles()
        if self.soundfiles == []:
            print("No sounds to play - exiting...")
            exit(0)
        
        self.observer = Observer()
        self.handler = NewAudioFileHandler(self)
        self.observer.schedule(self.handler, self.sounddir)
        self.observer.start()

        gpio_spec = importlib.util.find_spec("RPi")
        self.haz_gpio = gpio_spec is not None
        if self.haz_gpio:
            import RPi.GPIO as GPIO
            print("Rasperry pi detected:\n\tusing pin: " + str(pin))
            self.setupGPIO(GPIO.BOARD, pin)
    
    def __del__(self):
        """
        Make sure we clan up the watchdog
        """
        self.observer.stop()
        self.observer.join(timeout=1)
    
    def playsound(self, snd_file:str) -> None:
        """
        Wrapper around playsound. Plays the given file.

        Parameters:
        -----------

        snd_file:str = File name of the file to play.
        """
        print("playing: " + os.path.basename(snd_file))
        playsound(snd_file)
        
    def mainloop(self) -> None:
        """
        Main loop: Check if enter is pressed or, if we have a pi, a button was pressed.
        If so, we play a random file from the file list.
        If we do use the keyboard as input (no pi), we also test if q was pressed
        and then quit.
        """
        while True:
            if self.updateFileList:
                continue
            snd_file = random.choice(self.soundfiles)
            if self.haz_gpio:
                if GPIO.input(10) == GPIO.HIGH:
                    self.playsound(snd_file)
            else:
                inputstr = input("Press any key, q to quit:\n")
                if inputstr.startswith("q"):
                    exit(0)
                self.playsound(snd_file)
            
def main():
    """
    Main function if we use krgen.py not as lib.
    In this case we gather some command line options and
    initialize Krach-object with them, then run the main loop.
    """
    parser = argparse.ArgumentParser(description='Bring the noise')
    parser.add_argument('-s','--sounds', default=os.getcwd()+os.sep+"sounds", help="Sound directory (Default: cwd/sounds")
    parser.add_argument('-p', '--pin', default=10, help="Raspberry pi GPIO Pin Number (Default:10)")
    args = parser.parse_args()

    gerausch = Krach(os.path.abspath(args.sounds), args.pin)
    gerausch.mainloop()

if __name__ == '__main__':
    main()