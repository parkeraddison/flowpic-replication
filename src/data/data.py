import src.data

import pandas as pd
import numpy as np
import glob
import os
import re

import multiprocessing
import time

def _process_file(args):
    return process_file(*args)
def process_file(file, outdir, chunk_length, isolate_flow, dominating_threshold):

    # print(f"Processing {file}")
    fname = os.path.basename(file)
    fnlower = fname.lower()

    # Load in the raw data
    df = pd.read_csv(file)

    try:
        cleaned = src.data.clean(df)
        chunks = src.data.preprocess(cleaned, chunk_length, isolate_flow, dominating_threshold)
    except Warning as warn:
        # A warning may be raised by our preprocessing stage if we attempt to
        print(warn)
    # Extract labels from the file name and save as either a streaming or
    # browsing file.
    #
    # Support for metadata (like streaming provider, resolution, etc) is
    # still pending. Thinking about hdf5 format but not sure...
    streaming_providers = [
        "youtube", "hbomax", "disneyplus", "canvas", "amazonprime", "hulu",
        "vimeo", "netflix", "espnplus",
    ]
    browsing_words = [
        "novideo", "nostream", "general", "browsing", 
    ]
    is_streaming = re.search('|'.join(streaming_providers), fnlower)
    is_browsing = re.search('|'.join(browsing_words), fnlower)
    if not (is_streaming or is_browsing) or (is_streaming and is_browsing):
        print(f"File {fname} does not match naming conventions, cannot determine activity. Ignoring")
        return False

    # Save preprocessed file with new format:
    # {streaming | browswing }-<chunk number>-<original file name>.csv
    #
    # Notice we don't have index=False -- it's important to keep the index
    # since it is set to the packet arrival time.
    prefix = 'streaming' if is_streaming else 'browsing'
    for i, chunk in enumerate(chunks):
        chunk[['packet_times', 'packet_sizes']].to_csv(
            os.path.join(outdir, f'{prefix}-{i}-{fname}')
        )

    return True

def pipeline(source, outdir, pattern, chunk_length, isolate_flow, dominating_threshold):
    """
    Loads data files from source matching a glob pattern, then performs cleaning
    and preprocessing steps and saves each file to outdir.
    """

    # Make sure source exists. If not, then make soft links.
    if not os.path.exists(source):
        DATA_DIRECTORY = "/teams/DSC180A_FA20_A00/b05vpnxray/data/unzipped"
        print(f"Symlinking raw data from {DATA_DIRECTORY} into {source}")
        os.symlink(DATA_DIRECTORY, source)

    # Make sure outdir exists
    os.makedirs(outdir, exist_ok=True)

    # Clear outdir
    print(f"Removing existing files from `{outdir}`")
    to_remove = glob.glob(os.path.join(outdir, '*'))
    for file in to_remove:
        os.remove(file)

    # If a glob pattern is specified, only perform preprocessing on those files.
    # Otherwise, a null or empty pattern will default to preprocessing all.
    to_preprocess = glob.glob(os.path.join(source, pattern or "*"))
    # We're only interested in the vpn data
    to_preprocess = list(filter(lambda file: "novpn" not in file.lower(), to_preprocess))

    args = [
        (file, outdir, chunk_length, isolate_flow, dominating_threshold)
        for file in to_preprocess
    ]

    workers = multiprocessing.cpu_count()
    print(f'Starting a processing pool of {workers} workers.')
    start = time.time()
    pool = multiprocessing.Pool(processes=workers)
    results = pool.map(_process_file, args)
    print(f'Time elapsed: {round(time.time() - start)} seconds.')
    
    results = np.array(list(results))
    print(f'{sum(results)} input files successfully preprocessed.')
    print(f"{sum(~results)} files couldn't be procesed.")
    