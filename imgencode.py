#!/usr/bin/python
import PIL
from PIL import Image
import math, wave, array, sys, getopt, glob
from generate_EFP import gen_images, gen_vertical

import subprocess


def start(inputfile, outputfile, duration):
    im = Image.open(inputfile)
    width, height = im.size
    rgb_im = im.convert('RGB')

    durationSeconds = float(duration)
    tmpData = []
    maxFreq = 0
    data = array.array('h')
    sampleRate = 44100
    channels = 1
    dataSize = 2

    numSamples = int(sampleRate * durationSeconds)
    samplesPerPixel = math.floor(numSamples / width)

    C = 20000 / height

    for x in range(numSamples):
        rez = 0

        pixel_x = int(x / samplesPerPixel)
        if pixel_x >= width:
            pixel_x = width -1

        for y in range(height):
            r, g, b = rgb_im.getpixel((pixel_x, y))
            s = r + g + b

            volume = s * 100 / 765

            if volume == 0:
                continue

            freq = int(C * (height - y + 1))

            rez += getData(volume, freq, sampleRate, x)

        tmpData.append(rez)
        if abs(rez) > maxFreq:
            maxFreq = abs(rez)

    for i in range(len(tmpData)):
        data.append(32767 * tmpData[i] / maxFreq)

    f = wave.open(outputfile, 'w')
    f.setparams((channels, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
    f.writeframes(data.tostring())
    f.close()

def getData(volume, freq, sampleRate, index):
    return int(volume * math.sin(freq * math.pi * 2 * index /sampleRate))

def make_video():
    bkg_img = glob.glob('images/bkg/*.png')
    sig_img = glob.glob('images/sig/*.png')
    for i in range(len(bkg_img)):
        input_video = Input('')


if __name__ == '__main__':
    #gen_images(N_images=50, dpi=10)


    gen_images(N_images=50, dpi=200)
    bkg_files = glob.glob('images/bkg/*.png')
    sig_files = glob.glob('images/sig/*.png')

    for i in range(len(bkg_files)):
        print "sonifying bkg %0.f/%0.f" %(i+1, len(bkg_files))
        start(inputfile=bkg_files[i], outputfile="output/bkg/bkg_%0.f.wav" %(i+1), duration='3')
    for i in range(len(sig_files)):
        print "sonifying sig %0.f/%0.f" %(i+1, len(sig_files))
        start(inputfile=sig_files[i], outputfile="output/sig/sig_%0.f.wav" %(i+1), duration='3')


    rc = subprocess.call("./videos.sh")
