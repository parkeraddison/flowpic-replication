# DSC180A Senior Capstone - Viasat VPN Analysis

- [Purpose](#purpose)
- [Running](#running)
  - [Target `collect`](#target-collect)
  - [Target `data`](#target-data)
  - [Target `features`](#target-features)
  - [Example](#example)
- [Responsibilities](#responsibilities)

## Purpose

Our goal is to predict whether a user is streaming video on a VPN by analyzing their network traffic traits such as video signatures, interpacket intervals, packet size, etc. through a machine learning classifier, then repeat the analysis with other noise present on the network. 

Our data collection process uses the network-stats script from Viasat, which will output packet data on a per-second, per-connection basis from any given network interface. This tool was designed to focus more on connection-to-connection data rather than individual packet data. Once running, network-stats will output the time, source, destination, and protocol of the packets sent within any connection, as well as the count, size, time, and direction of each packet’s arrival at the destination. 


## Running

The following targets can be run by calling `python run.py <target_name>`. These targets perform various aspects of the data collection, cleaning, engineering, and training pipeline.

In DSMLP, first run `launch-180.sh -i parkeraddison/capstone-dev -G B05_VPN_XRAY`, then inside of the container nagivate to `cd /home/jovyan/data-science-capstone`.

### Target `collect`
**WIP**

Uses [`network-stats`](https://github.com/Viasat/network-stats) to collect your local machine's network activity for use in training. Labels must be provided.

To stop data capturing, press `CTRL-C` in the terminal.

### Target `data`
**WIP**

Loads data from a source directory then performs cleaning and preprocessing steps on each file. Saves the preprocessed data to a intermediate directory.

See `config/data-params.json` for configuration:
| Key | Description |
| --- | --- |
| source | Path to directory containing raw data. Default: `data/raw/` |
| outdir | Path to store preprocessed data. Default: `data/preprocessed/` |
| pattern | Glob pattern. Only copy and preprocess data matching this pattern. Default: `null` |

### Target `features`
**WIP**

Loads all preprocessed data and summarizes each file into sets of features and labels, each set containing a configurable number of seconds of data. Saves a table of all features and labels to a file to be used for model training.

See `config/features-params.json` for configuration:
| Key | Description |
| --- | --- |
| source | Path to directory containing preprocessed data. Default: `data/preprocessed/` |
| outdir | Path to directory to store feature engineered data. Default: `data/features/` |
| outfile | File name to store feature engineered data. Must be a csv. Default: `features.csv` |
| chunk_length | Time in seconds to chunk data into when computing features. Default: `60` |

### Example

```bash
ssh dsmlp

launch-180.sh -i parkeraddison/capstone-dev -P Always -G B05_VPN_XRAY

cd /home/jovyan/data-science-capstone

python run.py data

python run.py features

cat data/features/features.csv
```

## Responsibilities

* Group member 1 (Jerry) Initial work on introduction. Wrote run.py, set up data generation environment through network-stats and configured data-generation-params to be used with run.py. Work on methods report.
* Group member 2 (Parker) Initial work on data generation environment. Wrote introduction. Edit methods report. Create preprocessing and feature piplines, targets.

