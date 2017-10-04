import numpy
import pandas as pd


def expand_index(df: pd.DataFrame, start: int, stop: int) -> pd.DataFrame:
    """
    Takes a DataFrame and fills in any holes between start and stop, inclusive,
        in the index with default values.
    :param df: DataFrame to fill in
    :param start: Beginning of the index range
    :param stop: End of the index range
    :return: New DataFrame that is a copy of `df` with the filled in rows
    """
    nan_types = {int, float, numpy.int64, numpy.float64}
    populated = set(df.index)
    unpopulated = [i for i in range(start, stop+1) if i not in populated]
    types = [type(df[col][df[col].index[0]]) for col in df.columns]
    data = [[numpy.NaN if t in nan_types else t() for t in types] for i in unpopulated]
    new_df = pd.DataFrame(data=data, columns=df.columns, index=unpopulated)
    new_df = pd.concat([df, new_df]).sort_index()
    return new_df


def merge(df1: pd.DataFrame, *args):
    """
    Merges two DataFrames into a new one by summing the contents of overlapping cells.
    :param df1: The left hand DataFrame
    :param args: A list of DataFrames to use as the right hand side
    :return: The merged DataFrame
    """
    for df2 in args:
        idxs = set(df1.index.values) | set(df2.index.values)
        df2 = expand_index(df2, min(idxs), max(idxs))
        rsuffix = "_df2"
        merged = df1.join(df2, rsuffix=rsuffix, how="outer")
        merge_columns = [col for col in set(df1.columns.values) & set(df2.columns.values)]
        for col in merge_columns:
            merged[col] = merged[col] + merged[f"{col}{rsuffix}"]
            merged = merged.drop([f"{col}{rsuffix}"], axis=1)
        df1 = merged
    return df1
