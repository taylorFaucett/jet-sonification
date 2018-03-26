import sys
sys.path.insert(0, '/Users/taylor/Dropbox/Research/EFP/packages/')

from data_generator import output_data
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import itertools
from scipy.signal import argrelextrema
plt.style.use('dark_background')

def gen_images(N_images, dpi):
    bkg_counter, sig_counter = 0, 0
    for i in range(N_images):
        plt.figure(figsize=(32,32))
        #plt.axis('off')
        events, target = output_data(h5file = '/Users/taylor/Dropbox/Research/RENN/RENN_jets/RENN_training/data/jets/images/test_no_pile_5000000.h5', start=i, stop=i+1)
        plt.imshow(events[0].T, cmap='inferno', interpolation='nearest', origin='lower') #lanczos
        plt.xlim([0,32])
        plt.ylim([0,32])
        plt.tight_layout()
        plt.rcParams['figure.facecolor'] = 'black'

        if target[0]==0:
            plt.savefig('images/bkg_basic/bkg_%0.f.png' %bkg_counter, bbox_inches='tight', pad_inches=0, dpi=dpi)
            bkg_counter = bkg_counter + 1
        elif target[0]==1:
            plt.savefig('images/sig_basic/sig_%0.f.png' %sig_counter, bbox_inches='tight', pad_inches=0, dpi=dpi)
            sig_counter = sig_counter + 1
        plt.clf()

def gen_vertical(N_images, dpi):
    bkg_counter, sig_counter = 0, 0
    for i in range(N_images):
        plt.figure(figsize=(10,10))
        plt.axis('off')
        events, target = output_data(h5file = '/Users/taylor/Dropbox/Research/RENN/RENN_jets/RENN_training/data/jets/images/test_no_pile_5000000.h5', start=i, stop=i+1)
        flat = events.flatten()
        flat = np.trim_zeros(flat)
        #flat = flat[flat!=0]
        flat = np.vstack((flat))

        max_event = max(flat)
        np.asarray(flat)
        flat = np.flip(flat,0)
        argrelextrema(flat, np.greater)
        flat[flat < (0.8*max_event[0])] = 0

        plt.imshow(flat, cmap='gist_gray', interpolation='lanczos', origin='lower') #lanczos
        plt.xlim([0,1])
        plt.tight_layout()
        plt.rcParams['figure.facecolor'] = 'black'
        if target[0]==0:
            bkg_counter = bkg_counter + 1
            plt.savefig('images/bkg/bkg_%0.f.png' %bkg_counter, bbox_inches='tight', pad_inches=0, dpi=dpi)
            print bkg_counter
        elif target[0]==1:
            sig_counter = sig_counter + 1
            plt.savefig('images/sig/sig_%0.f.png' %sig_counter, bbox_inches='tight', pad_inches=0, dpi=dpi)
        plt.clf()