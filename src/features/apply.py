import src.features

import pandas as pd
import glob
import os

def apply_features(source, outdir, outfile, chunk_length):

    print("Chunk length not yet supported!")

    preprocessed = glob.glob(os.path.join(source, "*"))

    total_files = len(preprocessed)

    frame = pd.DataFrame(columns=[
        'activity',
        'mean_packet_size',
        'mean_inter_packet_delay',
        'send_receive_ratio'
    ], index=range(total_files))

    for i, file in enumerate(preprocessed):

        print(f"Feature engineering {file}")

        # All preprocessed files follow the same naming convention -- either
        # streaming-000n.csv or browsing-000n.csv.
        activity = os.path.basename(file).split('-')[0]

        df = pd.read_csv(file)

        mean_packet_size = src.features.computing.mean_packet_size(df)
        mean_inter_packet_delay = src.features.computing.mean_inter_packet_delay(df)
        send_receive_ratio = src.features.computing.send_receive_ratio(df)

        row = pd.Series({
            'activity': activity,
            'mean_packet_size': mean_packet_size,
            'mean_inter_packet_delay': mean_inter_packet_delay,
            'send_receive_ratio': send_receive_ratio
        })

        frame.iloc[i] = row

    # Make sure outdir exists
    os.makedirs(outdir, exist_ok=True)

    outpath = os.path.join(outdir, outfile)
    print(f"Writing features to {outpath}")
    frame.dropna().to_csv(outpath, index=False)
