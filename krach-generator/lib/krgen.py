#! /usr/bin/env python3

from genericpath import isdir
import os
import random
import importlib
import argparse
from playsound import playsound


class Krach:
    def setupGPIO(self, mode, pin):
        if self.haz_gpio:
            GPIO.setwarnings(False) # Ignore warning for now
            GPIO.setmode(mode) # Use physical pin numbering: GPIO.BOARD
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

    def __init__(self) -> None:
        gpio_spec = importlib.util.find_spec("RPi")
        self.haz_gpio = gpio_spec is not None
        if self.haz_gpio:
            import RPi.GPIO as GPIO
            self.setupGPIO(GPIO.BOARD, 10)

    def getSoundFiles(self, sounddir: str) -> list:
        if not os.path.isdir(sounddir):
            return []
        return os.listdir(sounddir)
    
    def playsound(self, sounddir, snd_file):
        print("soundfile: " + str(snd_file))
        playsound(sounddir + os.sep + snd_file)
        
    def mainloop(self, sounddir : str):
        file_paths = self.getSoundFiles(sounddir)
        if file_paths == []:
            print("No sounds to play - exiting...")
            exit(0)
        
        while True:
            snd_file = random.choice(file_paths)
            if self.haz_gpio:
                if GPIO.input(10) == GPIO.HIGH:
                    self.playsound(sounddir, snd_file)
            else:
                keypressed = input("Press any key")
                self.playsound(sounddir, snd_file)
            
def main():
    parser = argparse.ArgumentParser(description='Bring the noise')
    parser.add_argument('-s','--sounds', default=os.getcwd()+os.sep+"sounds", help="Sound directory (Default: cwd/sounds")
    args = parser.parse_args()

    gerausch = Krach()
    gerausch.mainloop(os.path.abspath(args.sounds))

if __name__ == '__main__':
    main()