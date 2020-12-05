import src.features

import pandas as pd
import numpy as np
import glob
import os

import multiprocessing
import time


def _engineer_file(args):
    return engineer_file(*args)
def engineer_file(file, outdir):

    fname = os.path.basename(file)
    activity = fname.split('-')[0]

    # Load in the preprocessed chunk file
    df = pd.read_csv(file)

    # Calculate the flowpic and save it as a numpy file in the proper directory
    h = src.features.flowpic(df)
    np.save(os.path.join(outdir, activity, fname.rstrip('.csv')), h)

    return True

def pipeline(source, outdir):

    preprocessed = glob.glob(os.path.join(source, "*"))
    print(f'{len(preprocessed)} preprocessed files found.')

    # Make sure outdir exists with streaming and browsing directories
    os.makedirs(os.path.join(outdir, 'streaming'), exist_ok=True)
    os.makedirs(os.path.join(outdir, 'browsing'), exist_ok=True)

    args = [
        (file, outdir)
        for file in preprocessed
    ]

    workers = multiprocessing.cpu_count()
    print(f'Starting a processing pool of {workers} workers.')
    start = time.time()
    pool = multiprocessing.Pool(processes=workers)
    results = pool.map(_engineer_file, args)
    print(f'Time elapsed: {round(time.time() - start)} seconds.')

    results = np.array(list(results))
    print(f'{sum(results)} input chunks successfully feature engineered.')
    print(f"{sum(~results)} files couldn't be procesed.")
    

# def _get_signal(args):
#     """
#     A helper to be called with the ProcessorPool -- takes all arguments as a
#     single input, a tuple of arguments.
#     """
#     return get_signal(file=args[0], chunk_length=args[1], resample_length=args[2], rolling_length=args[3])
# def get_signal(file, chunk_length='90s', resample_length='100ms', rolling_length='1s'):

#     print(f"Feature engineering {file}")

#     # All preprocessed files follow the same naming convention -- either
#     # streaming-<originalfilename>.csv or browsing-<original>.csv
#     fname = os.path.basename(file)
#     splitted = fname.split('-')
#     activity = splitted[0]
#     originalfilename = '-'.join(splitted[1:])

#     df = pd.read_csv(file, index_col='ptime')
#     df.index = pd.to_timedelta(df.index)
#     df = src.features.extend(df, src.features.extending.inter_arrival_time)
#     resampled = df.resample(resample_length).sum().reset_index()
#     slice_indices = np.argwhere(
#         resampled.ptime.isin(
#             pd.timedelta_range(resampled.ptime.min(), resampled.ptime.max(), freq=chunk_length)
#         )
#         .values
#     ).ravel()
#     chunks = np.split(resampled, slice_indices)[1:-1]

#     signals = []

#     for chunk in chunks:
#         signal = chunk.rolling(rolling_length, on='ptime').psize.sum().values
#         # Also normalize to (0-1)
#         #
#         # Note: This removes information that could be used in quality detection
#         signal = (signal - signal.min())
#         signal = signal / signal.max()
#         signals.append((originalfilename, activity, tuple(signal)))

#     return signals or [None, None, None]


# def pipeline(source, outdir, outfile, chunk_length, resample_length, rolling_length):

#     #! NOTE: There is some sloppy/temporary code in here :) Need to re-examine
#     #  how to support adding more features in general, e.g. through config.
#     #
#     #  Will do later.

#     preprocessed = glob.glob(os.path.join(source, "*"))
#     args = zip(preprocessed, [chunk_length]*len(preprocessed), [resample_length]*len(preprocessed), [rolling_length]*len(preprocessed))

#     with concurrent.futures.ProcessPoolExecutor(5) as executor:
#         signals = executor.map(_get_signal, args)
    
#     frame = pd.DataFrame(np.vstack(list(signals))).dropna()
#     frame.columns = ['file', 'activity', 'signal']


    # total_files = len(preprocessed)

    # frame = pd.DataFrame(columns=[
    #     'file',
    #     'activity',
    #     'mean_packet_size',
    #     'mean_inter_packet_delay',
    #     'send_receive_ratio',
    #     # 'std_packet_size',
    #     # 'min_packet_size',
    #     # 'max_packet_size',
    #     # 'std_inter_packet_delay',
    #     # 'min_inter_packet_delay',
    #     # 'max_inter_packet_delay',
    #     'count_peaks',
    #     'mean_inter_peak_delay',
    #     'std_inter_peak_delay'
    # ], index=range(total_files))

    # for i, file in enumerate(preprocessed):

    #     print(f"Feature engineering {file}")

    #     # All preprocessed files follow the same naming convention -- either
    #     # streaming-<originalfilename>.csv or browsing-<original>.csv
    #     fname = os.path.basename(file)
    #     splitted = fname.split('-')
    #     activity = splitted[0]
    #     originalfilename = '-'.join(splitted[1:])

    #     # Chunk into bins, make a set of features for each bin. This ensures
    #     # equal length.
    #     #
    #     #! TODO
    #     # df['ptime'] = pd.to_timedelta(df.ptime)
    #     # df = df.set_index('ptime')

    #     # binned = df.resample('160s')

    #     df = pd.read_csv(file)

    #     mean_packet_size = src.features.computing.mean_packet_size(df)
    #     mean_inter_packet_delay = src.features.computing.mean_inter_packet_delay(df)
    #     send_receive_ratio = src.features.computing.send_receive_ratio(df)

    #     # Resample-related features
    #     df['ptime'] = pd.to_timedelta(df.ptime)
    #     df = df.set_index('ptime')

    #     bytes_per_second = df.resample('1s').psize.sum()

    #     def threshold(ser):
    #         return ser.mean() + ser.min()

    #     peaks, props = scipy.signal.find_peaks(
    #         bytes_per_second, threshold(bytes_per_second)
    #     )

    #     count_peaks = len(peaks)
    #     peak_delays = df.index[peaks].total_seconds().to_series().diff()
    #     mean_inter_peak_delay = peak_delays.mean()
    #     std_inter_peak_delay = peak_delays.std()


    #     row = pd.Series({
    #         'file': originalfilename,
    #         'activity': activity,
    #         'mean_packet_size': mean_packet_size,
    #         'mean_inter_packet_delay': mean_inter_packet_delay,
    #         'send_receive_ratio': send_receive_ratio,
    #         'count_peaks': count_peaks,
    #         'mean_inter_peak_delay': mean_inter_peak_delay,
    #         'std_inter_peak_delay': std_inter_peak_delay
    #     })

    #     frame.iloc[i] = row

    
    # outpath = os.path.join(outdir, outfile)
    # print(f"Writing features to {outpath}")
    # frame.dropna().to_csv(outpath, index=False)
