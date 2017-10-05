import copy
import numpy
import pandas as pd
from typing import Optional


def expand_index(df: pd.DataFrame, start: int, stop: int, propagate: Optional[str] = None) -> pd.DataFrame:
    """
    Takes a DataFrame and fills in any holes between start and stop, inclusive,
        in the index with default values.
    :param df: DataFrame to fill in
    :param start: Beginning of the index range
    :param stop: End of the index range
    :param propagate: Describes how value propagation should work.
                        "forward" for copying previous values
                        "backward" for copying future values
                        "none"/None for no copying
    :return: New DataFrame that is a copy of `df` with the filled in rows
    """
    nan_types = {int, float, numpy.int64, numpy.float64}
    populated = set(df.index)
    unpopulated = [i for i in range(start, stop+1) if i not in populated]
    types = [type(df[col][df[col].index[0]]) for col in df.columns]
    data = []
    for i in unpopulated:
        if propagate is None:
            data.append([numpy.NaN if t in nan_types else t() for t in types])
        elif propagate == "forward":
            last_pop = filter(lambda x: x < i, populated)
            print(populated, i, [p for p in last_pop])
            data.append(df.loc[max(last_pop)])
        elif propagate == "backward":
            next_pop = filter(lambda x: x > i, populated)
            data.append(df.loc[max(next_pop)])
    new_df = pd.DataFrame(data=data, columns=df.columns, index=unpopulated)
    new_df = pd.concat([df, new_df]).sort_index()
    return new_df


def merge(*args, propagate: Optional[str] = None):
    """
    Merges two DataFrames into a new one by summing the contents of overlapping cells.
    :param args: A list of DataFrames to merge
    :param propagate: Describes how value propagation should work in expand_index.
                        "forward" for copying previous values
                        "backward" for copying future values
                        "none"/None for no copying
    :return: The merged DataFrame
    """
    if len(args) == 0:
        return pd.DataFrame()
    df1 = args[0]
    if len(args) > 1:
        for df2 in args[1:]:
            idxs = set(df1.index.values) | set(df2.index.values)
            df2 = expand_index(df2, min(idxs), max(idxs), propagate)
            rsuffix = "_df2"
            merged = df1.join(df2, rsuffix=rsuffix, how="outer")
            merge_columns = [col for col in set(df1.columns.values) & set(df2.columns.values)]
            for col in merge_columns:
                merged[col] = merged[col] + merged[f"{col}{rsuffix}"]
                merged = merged.drop([f"{col}{rsuffix}"], axis=1)
            df1 = merged
    return df1
