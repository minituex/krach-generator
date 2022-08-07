#! /usr/bin/env python3

from genericpath import isdir
import os
import random
import importlib
import argparse
from playsound import playsound


class Krach:
    def setupGPIO(self, mode, pin: int) -> None:
        if self.haz_gpio:
            GPIO.setwarnings(False) # Ignore warning for now
            GPIO.setmode(mode) # Use physical pin numbering: GPIO.BOARD
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

    def getSoundFiles(self) -> list:
        if not os.path.isdir(self.sounddir):
            return []
        return os.listdir(self.sounddir)

    def __init__(self, sounddir:str, pin) -> None:
        self.sounddir = sounddir
        self.soundfiles = self.getSoundFiles()
        if self.soundfiles == []:
            print("No sounds to play - exiting...")
            exit(0)

        gpio_spec = importlib.util.find_spec("RPi")
        self.haz_gpio = gpio_spec is not None
        if self.haz_gpio:
            import RPi.GPIO as GPIO
            self.setupGPIO(GPIO.BOARD, pin)
    
    def playsound(self, snd_file:str) -> None:
        print("soundfile: " + str(snd_file))
        playsound(self.sounddir + os.sep + snd_file)
        
    def mainloop(self):
        
        while True:
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
    parser = argparse.ArgumentParser(description='Bring the noise')
    parser.add_argument('-s','--sounds', default=os.getcwd()+os.sep+"sounds", help="Sound directory (Default: cwd/sounds")
    parser.add_argument('-p', '--pin', default=10, help="Raspberry pi GPIO Pin Number (Default:10)")
    args = parser.parse_args()

    gerausch = Krach(os.path.abspath(args.sounds), args.pin)
    gerausch.mainloop()

if __name__ == '__main__':
    main()