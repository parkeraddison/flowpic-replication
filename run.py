#!/usr/bin/env python

import sys
import json
import os

import src

global df
df = None

# sys.path.insert(0, 'src/data')

# from collect import get_data

def main(targets):

    if 'data' in targets:
        with open('config/data-generation-params.json') as f:
            generation_params = json.load(f)
            src.data.collect.get_data(generation_params)

    if 'features' in targets:
        with open('config/feature-params.json') as f:
            feature_params = json.load(f)
        # Clean, preprocess, extend, and compute features for given data.
        #
        #! TODO: Doesn't have any data to run on yet -- this needs config and
        #  would benefit from Viasat shifting to using the team directory.
        
        # Load in example data -- should probably be handled with src.data.load
        import pandas as pd
        import glob
        # Choose a vpn youtube file (data path is assumed)
        DATADIR = feature_params['filepath']
        #file = glob.glob(os.path.join(DATADIR, '*-youtube*-vpn*.csv'))[0]
        #streamvpn = pd.read_csv(file)
        fp_jq = 'jeq004_netflix_1080p_1x_vpn_mac_clean_20201101.csv'
        streamvpn = pd.read_csv(fp_jq)

        # Clean (get rid of traffic flows other than VPN)
        cleaned = src.data.clean(streamvpn)
        
        # Preprocess (extract packet measurements)
        preprocessed = src.data.preprocess(cleaned)
        
        # Extend (add inter-arrival time -- currently only extension)
        extensions = [src.features.extending.inter_arrival_time]
        extended = src.features.extend(preprocessed, *extensions)
        
        # If we want to condition on direction, we should actually do:
        extended = (
            preprocessed
            .groupby('pdir')
            .apply(src.features.extend, *extensions)
        )

        # Filter
        downloading_only = src.features.filter(
            extended, src.features.filtering.download_pkts
        )
        uploading_only = src.features.filter(
            extended, src.features.filtering.upload_pkts
        )
        
        direction = feature_params['filter_direction']
        rolling_col = feature_params['rolling_column']
        rolling_window = feature_params['rolling_window']
        if direction == 'download': 
            df_filtered = downloading_only 
        else: 
            df_filtered = uploading_only
        # Compute rolling features (currently only one column at a time)
        import numpy as np
        size_feats = src.features.roll(
            df_filtered, rolling_col, rolling_window, ['mean', 'count', np.sum]
        )

        # Proof that it worked
        print(size_feats.describe())

        # Run `python -i run.py features`
        # then you can play with df
        global df
        df = size_feats

                  
    return
    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)