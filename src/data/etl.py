import src.data

import pandas as pd
import glob
import os
import re

def etl(source, outdir, pattern, add_columns):
    """
    Loads data files from source matching a glob pattern, then performs cleaning
    and preprocessing steps and saves each file to outdir.
    """

    # Make sure source exists. If not, then make soft links.
    if not os.path.exists(source):
        DATA_DIRECTORY = "/teams/DSC180A_FA20_A00/b05vpnxray/personal_pgaddiso-jeq004/data/"
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
    # We're not interested in the novpn data
    to_preprocess = filter(lambda file: "novpn" not in file, to_preprocess)

    streaming_count = 0
    browsing_count = 0
    for file in to_preprocess:
        print(f"Processing {file}")

        # Load in the raw data
        df = pd.read_csv(file)

        # Cleaning and preprocessing (reformatting) of the data are file- and
        # config-agnostic.
        cleaned = src.data.clean(df)
        preprocessed = src.data.preprocess(cleaned)

        # Calculate additional columns for features to be engineered on.
        # Currently only inter arrival time is possible.
        column_map = {
            "inter_arrival_time": src.features.extending.inter_arrival_time
        }
        # Yeah yeah, this is related to features... whether or not it belongs in
        # the preprocessing step is questionable. I haven't even decided myself!
        extensions = [column_map[column] for column in add_columns]
        extended = src.features.extend(preprocessed, *extensions)

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
        is_streaming = re.search('|'.join(streaming_providers), file)
        is_browsing = re.search('|'.join(browsing_words), file)
        if not (is_streaming or is_browsing) or (is_streaming and is_browsing):
            print(f"File {file} does not match naming conventions, cannot determine activity. Ignoring")
            continue
        # meta = {
        #     'activity': 'streaming' if is_streaming else 'browsing',
        # }

        if is_streaming:
            extended.to_csv(os.path.join(outdir, f"streaming-{streaming_count:04d}.csv"), index=False)
            streaming_count += 1
        else:
            extended.to_csv(os.path.join(outdir, f"browsing-{browsing_count:04d}.csv"), index=False)
            browsing_count += 1
