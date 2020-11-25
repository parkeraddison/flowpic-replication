import src.data
import src.features
import src.models
import src.charts
import src.utils

def pipeline(df, stop_after='filter', filters=[]):
    """
    Runs the cleaning, preprocessing, extending, computing pipeline on a table
    until the specified point.
    """

    cleaned = src.data.clean(df)
    if stop_after == 'clean':
        return cleaned
    
    preprocessed = src.data.preprocess(cleaned)
    if stop_after == 'preprocess':
        return preprocessed
    
    extended = src.features.extend(preprocessed, src.features.extending.inter_arrival_time)
    if stop_after == 'extend':
        return extended

    filtered = src.features.filter(extended, *filters)
    if stop_after == 'filter':
        return filtered
    
    # computed = src.data.compute(extended)
    # if stop_after == 'compute':
    #     return computed