#! /usr/bin/env python3

from genericpath import isdir
import os
import random
import argparse
from playsound import playsound

class Krach:
    def getSoundFiles(self, sounddir: str) -> list:
        if not os.path.isdir(sounddir):
            return []
        return os.listdir(sounddir)
        
    def mainloop(self, sounddir : str):
        file_paths = self.getSoundFiles(sounddir)
        if file_paths == []:
            print("No sounds to play - exiting...")
            exit(0)
        
        while True:
            snd_file = random.choice(file_paths)
            keypressed = input("Press any key")
            print("soundfile: " + str(snd_file))
            playsound(sounddir + os.sep + snd_file)

def main():
    parser = argparse.ArgumentParser(description='Bring the noise')
    parser.add_argument('-s','--sounds', default=os.getcwd()+os.sep+"sounds", help="Sound directory (Default: cwd/sounds")
    args = parser.parse_args()

    gerausch = Krach()
    gerausch.mainloop(os.path.abspath(args.sounds))

if __name__ == '__main__':
    main()