#! /usr/bin/env python3

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Bring the noise')
    parser.add_argument('-s','--sounds', default=os.getcwd()+os.sep+"sounds", help="Sound directory (Default: cwd/sounds")

if __name__ == '__main__':
    main()