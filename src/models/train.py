import src
from src.models.ingesting import get_dataset

import os

import numpy as np

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score, confusion_matrix

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, layers

def train(source, outdir, outfile, batch_size, epochs, validation_size):

    os.makedirs(outdir, exist_ok=True)

    # Get both streaming/*.npy and browsing/*.npy files, the label will be
    # parsed by the dataset generator.
    all_files = glob.glob(os.path.join(source, '*/*.npy'))
    # Create shuffled train and validation sets
    train_files, val_files = train_test_split(all_files, test_size=validation_size)

    train, train_steps = get_dataset(train_files, batch_size)
    val, val_steps = get_dataset(val_files, batch_size)

    # Prefetch the data for a slight performance boost
    # See: https://www.tensorflow.org/guide/data_performance#prefetching
    train = train.prefetch(tf.data.experimental.AUTOTUNE)
    val = val.prefetch(tf.data.experimental.AUTOTUNE)

    # Building a LeNet-esque model, as defined in "FlowPic: Encrypted Internet
    # Traffic Classification is as Easy as Image Recognition" by Tal Shapira and
    # Yuval Shavitt.
    model = models.Sequential(name="FlowPic")
    # Args: filters, kernel_size, strides
    model.add(layers.Conv2D(10, (10,10), (5,5), activation='relu', input_shape=src.INPUT_SHAPE))
    # Args: pool_size, strides (defaults to pool)
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Conv2D(20, (10,10), (5,5), activation='relu'))
    model.add(layers.Dropout(0.25))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.5))
    # Binary classification, turn into probabilities
    model.add(layers.Dense(1, activation='sigmoid'))

    model.summary()

    # Start training!
    #
    # We'll save checkpoints with a callback every time we get a new-best on the
    # validation data. Then we'll load those weights again and save the model at
    # the end.
    #
    # Also providing an early stopping if the model doesn't improve validation
    # score for a handful of epochs.
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.binary_crossentropy,
        metrics=['accuracy']
    )

    checkpoint_path = os.path.join(outdir, 'checkpoint')
    checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=True,
        monitor='val_loss',
        mode='max',
        save_best_only=True
    )
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3
    )

    history = model.fit(
        train, steps_per_epoch=train_steps
        validation_data=valid, validation_steps=val_steps,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=[checkpoint_cb, early_stopping_cb]
    )

    model.load_weights(checkpoint_path)
    model.save(os.path.join(outdir, outfile))

    return history

    # Evaluate on test (validation) data
    # preds = (model.predict(X_test) > 0.5).astype('int32')

    # from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
    # print('Accuracy:', accuracy_score(preds, y_test))
    # print('F1:      ', f1_score(preds, y_test))
    # print('ROC AUC: ', roc_auc_score(preds, y_test))
    # print('')
    # print('Predicted Browsing / Streaming ->')
    # print('True Browsing / Streaming v')
    # print(confusion_matrix(y_test, preds))
