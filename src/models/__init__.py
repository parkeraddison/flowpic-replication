# Do a bunch of stuff to supress annoying FutureWarnings and other warnings/logs
# set off by TensorFlow.
#
# NOTE: Turns out I don't need to do this -- I just need to activate the correct
# conda environment (ml-latest) first... *but* that environment doesn't have
# sklearn installed :(.
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from src.models.train import train

