''' Generates observable data '''

import math
import numpy as np
import h5py
import itertools

def output_data(h5file, start, stop):
    def data_generator(h5file, start, stop):
        batchsize=1
        stop = ((stop - start) // batchsize) * batchsize + start
        assert (stop - start) % batchsize == 0  # Batches will not exceed stop.

        with h5py.File(h5file, 'r') as f1:
            assert f1['features'].shape[0] >= stop
            assert f1['features'].shape[0] == f1['targets'].shape[0]
            iexample = start
            while True:
                assert iexample >= start
                assert iexample + batchsize <= stop
                batch = slice(iexample, iexample + batchsize)
                X = f1['features'][batch]  # Images.
                Y = f1['targets'][batch]
                yield {'input_0': X}, {'output': Y}
                iexample += batchsize
                if iexample >= stop:
                    assert iexample == stop
                    iexample = start


    print('importing file: %s' %h5file)
    #print('Calculating %0.f data points' %N)
    generator = data_generator(h5file, start=start, stop=stop)

    target_list = []
    pT_array = np.empty([0, 32])
    for x in range(start, stop, 1):
        inputs, outputs = next(generator)

        pT = inputs
        target = outputs
        target_val = outputs.get('output')[0]
        target_list.append(target_val[0])
        pT_val = pT.get('input_0')
        pT_val = pT_val[0]
        pT_matrix = pT_val[0]
        pT_array = np.vstack((pT_array, pT_matrix))
    return pT_array.reshape((start-stop, 32, 32)), target_list

