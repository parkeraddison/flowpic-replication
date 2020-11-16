#!/usr/bin/env python

import sys
import json
import os

import src


def main(targets):

    if 'collect' in targets:
        raise NotImplementedError("This is a work in progress.")

        with open('config/data-generation-params.json') as f:
            generation_params = json.load(f)
            src.data.collect.get_data(generation_params)
        
    if 'data' in targets:
        # Load, clean, and preprocess data. Then store preprocessed data to
        # intermediate directory.

        print('Data target recognized.')

        with open('config/data-params.json', 'r') as f:
            data_params = json.load(f)
        print('Data configuration loaded.')
        
        print('Running ETL pipeline.')
        src.data.etl(**data_params)
        print('ETL pipeline complete.')

    if 'features' in targets:
        # Load preprocessed data, chunk each file into smaller windows of time,
        # then engineer features and write sets of features and labels to table.

        print('Features target recognized.')

        with open('config/features-params.json') as f:
            features_params = json.load(f)
        print('Features configuration loaded.')

        print('Engineering features.')
        src.features.apply_features(**features_params)
        print('Feature engineering complete.')

        

        # # Clean, preprocess, extend, and compute features for given data.
        # #
        # #! TODO: Doesn't have any data to run on yet -- this needs config and
        # #  would benefit from Viasat shifting to using the team directory.
        
        # # Load in example data -- should probably be handled with src.data.load
        # import pandas as pd
        # import glob
        # # Choose a vpn youtube file (data path is assumed)
        # DATADIR = feature_params['filepath']
        # #file = glob.glob(os.path.join(DATADIR, '*-youtube*-vpn*.csv'))[0]
        # #streamvpn = pd.read_csv(file)
        # fp_jq = 'jeq004_netflix_1080p_1x_vpn_mac_clean_20201101.csv'
        # streamvpn = pd.read_csv(fp_jq)

        # # Clean (get rid of traffic flows other than VPN)
        # cleaned = src.data.clean(streamvpn)
        
        # # Preprocess (extract packet measurements)
        # preprocessed = src.data.preprocess(cleaned)
        
        # # Extend (add inter-arrival time -- currently only extension)
        # extensions = [src.features.extending.inter_arrival_time]
        # extended = src.features.extend(preprocessed, *extensions)
        
        # # If we want to condition on direction, we should actually do:
        # extended = (
        #     preprocessed
        #     .groupby('pdir')
        #     .apply(src.features.extend, *extensions)
        # )

        # # Filter
        # downloading_only = src.features.filter(
        #     extended, src.features.filtering.download_pkts
        # )
        # uploading_only = src.features.filter(
        #     extended, src.features.filtering.upload_pkts
        # )
        
        # direction = feature_params['filter_direction']
        # rolling_col = feature_params['rolling_column']
        # rolling_window = feature_params['rolling_window']
        # if direction == 'download': 
        #     df_filtered = downloading_only 
        # else: 
        #     df_filtered = uploading_only
        # # Compute rolling features (currently only one column at a time)
        # import numpy as np
        # size_feats = src.features.roll(
        #     df_filtered, rolling_col, rolling_window, ['mean', 'count', np.sum]
        # )

        # # Proof that it worked
        # print(size_feats.describe())

        # # Run `python -i run.py features`
        # # then you can play with df
        # global df
        # df = size_feats

                  
    return
    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)