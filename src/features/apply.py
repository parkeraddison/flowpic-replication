import src.features

import pandas as pd
import glob
import os

import scipy.signal

def apply_features(source, outdir, outfile, chunk_length):

    #! NOTE: There is some sloppy/temporary code in here :) Need to re-examine
    #  how to support adding more features in general, e.g. through config.
    #
    #  Will do later.

    print("Chunk length not yet supported!")

    preprocessed = glob.glob(os.path.join(source, "*"))

    total_files = len(preprocessed)

    frame = pd.DataFrame(columns=[
        'file',
        'activity',
        'mean_packet_size',
        'mean_inter_packet_delay',
        'send_receive_ratio',
        # 'std_packet_size',
        # 'min_packet_size',
        # 'max_packet_size',
        # 'std_inter_packet_delay',
        # 'min_inter_packet_delay',
        # 'max_inter_packet_delay',
        'count_peaks',
        'mean_inter_peak_delay',
        'std_inter_peak_delay'
    ], index=range(total_files))

    for i, file in enumerate(preprocessed):

        print(f"Feature engineering {file}")

        # All preprocessed files follow the same naming convention -- either
        # streaming-<originalfilename>.csv or browsing-<original>.csv
        fname = os.path.basename(file)
        splitted = fname.split('-')
        activity = splitted[0]
        originalfilename = '-'.join(splitted[1:])

        # Chunk into bins, make a set of features for each bin. This ensures
        # equal length.
        #
        #! TODO
        # df['ptime'] = pd.to_timedelta(df.ptime)
        # df = df.set_index('ptime')

        # binned = df.resample('160s')

        df = pd.read_csv(file)

        mean_packet_size = src.features.computing.mean_packet_size(df)
        mean_inter_packet_delay = src.features.computing.mean_inter_packet_delay(df)
        send_receive_ratio = src.features.computing.send_receive_ratio(df)

        # Resample-related features
        df['ptime'] = pd.to_timedelta(df.ptime)
        df = df.set_index('ptime')

        bytes_per_second = df.resample('1s').psize.sum()

        def threshold(ser):
            return ser.mean() + ser.min()

        peaks, props = scipy.signal.find_peaks(
            bytes_per_second, threshold(bytes_per_second)
        )

        count_peaks = len(peaks)
        peak_delays = df.index[peaks].total_seconds().to_series().diff()
        mean_inter_peak_delay = peak_delays.mean()
        std_inter_peak_delay = peak_delays.std()


        row = pd.Series({
            'file': originalfilename,
            'activity': activity,
            'mean_packet_size': mean_packet_size,
            'mean_inter_packet_delay': mean_inter_packet_delay,
            'send_receive_ratio': send_receive_ratio,
            'count_peaks': count_peaks,
            'mean_inter_peak_delay': mean_inter_peak_delay,
            'std_inter_peak_delay': std_inter_peak_delay
        })

        frame.iloc[i] = row

    # Make sure outdir exists
    os.makedirs(outdir, exist_ok=True)

    outpath = os.path.join(outdir, outfile)
    print(f"Writing features to {outpath}")
    frame.dropna().to_csv(outpath, index=False)