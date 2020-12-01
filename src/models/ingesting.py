# Functions to load in data in tensorflow.
import src

import os
import numpy as np
import tensorflow as tf

def data_generator(file_list, batch_size, dimensions_to_use):
    """
    
    See:
    https://biswajitsahoo1111.github.io/post/reading-multiple-files-in-tensorflow-2/

    """
    i = 0
    while True:
        if i*batch_size >= len(file_list):
            i = 0
            np.random.shuffle(file_list)
        else:
            file_chunk = file_list[i*batch_size:(i+1)*batch_size] 
            data = []
            labels = []
            for file in file_chunk:
                # Only take the desired dimensions
                arr = np.load(file)[:,:,dimensions_to_use]
                data.append(arr.reshape(src.INPUT_SHAPE))
                labels.append(os.path.dirname(file).endswith(b'streaming'))
            data = np.asarray(data).reshape(-1,*src.INPUT_SHAPE)
            labels = np.asarray(labels)
            yield data, labels
            i = i + 1

def generator_for_prediction(file_list, batch_size, dimensions_to_use):
    i = 0
    while i <= (len(file_list)/batch_size):
        if i == np.floor(len(file_list)/batch_size):
            file_chunk = file_list[i*batch_size:len(file_list)]
            if len(file_chunk)==0:
                break
        else:
            file_chunk = file_list[i*batch_size:(i+1)*batch_size] 
        data = []
        for file in file_chunk:
            arr = np.load(file)[:,:,dimensions_to_use]
            data.append(arr.reshape(src.INPUT_SHAPE)) 
        data = np.asarray(data).reshape(-1,*src.INPUT_SHAPE)
        yield data
        i = i + 1

def get_dataset(file_list, batch_size, dimensions_to_use, for_prediction=False):
    """
    Takes a list of *.npy filepaths and returns a TensorFlow dataset built on
    a generator, and the steps required for a single epoch.
    """
    
    if for_prediction:
        dataset = tf.data.Dataset.from_generator(
            generator_for_prediction, args=(file_list, batch_size, dimensions_to_use),
            output_types=(tf.float32), output_shapes=(None, *src.INPUT_SHAPE)
        )
    else:
        dataset = tf.data.Dataset.from_generator(
            data_generator, args=(file_list, batch_size, dimensions_to_use),
            output_types=(tf.float32, tf.bool),
            output_shapes=((None, *src.INPUT_SHAPE), (None,))
        )

    steps_per_epoch = np.int(np.ceil(len(file_list) / batch_size))

    return dataset, steps_per_epoch
