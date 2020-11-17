import src.data

import pandas as pd
import glob
import os
import re

import multiprocessing

def etl(source, outdir, pattern, add_columns):
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
    to_preprocess = filter(lambda file: "novpn" not in file.lower(), to_preprocess)

    #! TODO: Parallelize
    #
    #  I attempted to do so, but ran into a NameError about half way through
    #  the data! (strange).
    for file in to_preprocess:

        print(f"Processing {file}")
        fname = os.path.basename(file)
        fnlower = fname.lower()

        # Load in the raw data
        df = pd.read_csv(file)

        # Cleaning and preprocessing (reformatting) of the data are file- and
        # config-agnostic.
        cleaned = src.data.clean(df)
        preprocessed = src.data.preprocess(cleaned)
        df = preprocessed

        # Calculate additional columns for features to be engineered on.
        # Currently only inter arrival time is possible.
        column_map = {
            "inter_arrival_time": src.features.extending.inter_arrival_time
        }
        # Yeah yeah, this is related to features... whether or not it belongs in
        # the preprocessing step is questionable. I haven't even decided myself!
        extensions = [column_map[column] for column in add_columns]
        extended = src.features.extend(preprocessed, *extensions)
        df = extended

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
            return
        # meta = {
        #     'activity': 'streaming' if is_streaming else 'browsing',
        # }

        # Save preprocessed file with new format:
        # {streaming | browswing }-<original file name>.csv
        #
        # Notice we don't have index=False -- it's important to keep the index
        # since it is set to the packet arrival time.
        if is_streaming:
            df.to_csv(os.path.join(outdir, f"streaming-{fname}"))
        else:
            df.to_csv(os.path.join(outdir, f"browsing-{fname}"))
    # pool = multiprocessing.Pool(4)
    # pool.map(process_file, to_preprocess)
    