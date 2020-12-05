# DSC180A Senior Capstone - Viasat VPN Analysis

- [Purpose](#purpose)
- [Running](#running)
  - [~~Target `collect`~~](#target-collect)
  - [Target `data`](#target-data)
  - [Target `features`](#target-features)
  - [Target `train`](#target-train)
  - [Example](#example)

## TODO

- [x] Add packet direction as secondary channel to FlowPic
- [ ] Add `predict` target to take in a network-stats output and use a trained model to classify whether or not it contains video streaming
- [ ] Adjust the test data and `test` target now that FlowPic is being used -- mainly need to adjust the test config

## Purpose

Our goal is to predict whether or not network traffic which utilizes a VPN contains video streaming activity.

## FlowPic

This particular approach is an implementation and slight modification of the FlowPic model introduced in [FlowPic: Encrypted Internet Traffic Classification is as Easy as Image Recognition](https://ieeexplore.ieee.org/document/8845315) by Tal Shapira and Yuval Shavitt.

The basic premise: a short duration of network traffic is turned into a 2D histogram of Packet Size and Arrival Time. This histogram can be treated similar to an image -- a two-dimensional array with a value channel (in our case, bin density density remapped to range from 0 to 1).

The model has also been extended witha  second channel containing the proportion of packets in each bin that were downloaded.

## Running

The following targets can be run by calling `python run.py <target_name>`. These targets perform various aspects of the data collection, cleaning, engineering, training, and predicting pipeline.

In DSMLP, first run `launch-180.sh -i parkeraddison/capstone-dev -G B05_VPN_XRAY`, then inside of the container nagivate to `cd /home/jovyan/data-science-capstone`.

### ~~Target `collect`~~
**WIP - Hasn't been tested yet**

Uses [`network-stats`](https://github.com/Viasat/network-stats) to collect your local machine's network activity for use in training. Labels must be provided.

To stop data capturing, press `CTRL-C` in the terminal.

### Target `data`

Loads data from a source directory then performs cleaning and preprocessing steps on each file. Saves the preprocessed data to a intermediate directory.

See `config/data-params.json` for configuration:
| Key | Description |
| --- | --- |
| source | Path to directory containing raw data. Default: `data/raw/` |
| outdir | Path to store preprocessed data. Default: `data/preprocessed/` |
| pattern | Glob pattern. Only copy and preprocess data matching this pattern. Default: `null` |
| chunk_length | Time offset string. To augment the data and allow the classifier to work on short durations of data, every file is split into multiple non-overlapping files of this length. Default: `60s` |
| isolate_flow | Boolean. If true, each file will be filtered so that only the most frequent pair of IPs will remain, if possible. Default: `false` |
| dominating_threshold | Proportion. If isolate_flow is true and no pair of IPs has more than this proportion of communications in the file, then the file will be ignored as no dominant traffic flow could be found. Default: `0.9`.

### Target `features`

Loads all preprocessed data and computes a FlowPic for each, then saves each FlowPic to a streaming/ or browsing/ directory depending on the file's label.

See `config/features-params.json` for configuration:
| Key | Description |
| --- | --- |
| source | Path to directory containing preprocessed data. Default: `data/preprocessed/` |
| outdir | Path to directory to store feature engineered data. Default: `data/features/` |

### Target `train`

Trains a CNN model on FlowPics and saves the model.

See `config/train-params.json` for configuration:
| Key | Description |
| --- | --- |
| source | Path to directory containing feature engineered data (this folder should contain a streaming/ and browsing/ directory. Default: `data/features/` |
| outdir | Path to directory to save trained model. Default: `data/out/` |
| batch_size | Batch size to use when training the model. Default: `10` |
| epochs | Number of iterations over the training data that the model should undergo. Regardless of additional epochs, the saved model will be from the iteration with the lowest validation loss and training will stop after 3 iterations without any improvement to the lowest validation loss. Default: `20` |
| validation_size | Proportion. This amount of training data will be withheld as a validation set. Default: `0.2` |
| dimensions_to_use | List of channel indices [Histogram→0, Proportion downloaded→1] to use as part of the model. Default: `[0]`

### Example

```bash
ssh dsmlp

# Request container with proper image and group, and two GPUs.
launch-180.sh -i parkeraddison/capstone-dev -G B05_VPN_XRAY -g 2

# Navigate to the cloned repository
cd /home/jovyan/data-science-capstone

# Check out the proper branch
git checkout flowpic

# Run the preprocessing, feature engineering, and training.
python run.py data features train
```
