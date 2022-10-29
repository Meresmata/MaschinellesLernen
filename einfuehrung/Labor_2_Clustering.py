#!/usr/bin/env python
# coding: utf-8

from dataclasses import dataclass
from math import inf

import numpy as np
from pandas import read_csv, DataFrame, Series


@dataclass
class Point:
    x: float
    y: float
    z: float


def distance_euklid(p1: tuple, p2: tuple):
    assert len(p1) == len(p2)
    result = 0.0

    for i in range(len(p1)):
        result += (p1[i] - p2[i])**2
    return result


def k_means(_df: DataFrame, k: int, dist) -> Series:
    centroids = _df.sample(k)

    def average(df: DataFrame, f: list[int]) -> tuple[float, float, float]:
        loc_df = df.loc[f].copy()
        return tuple(loc_df.mean().values)

    # key: centroid index, values list of point index
    label_point_dict: dict[int, list[int]] = {j: [j, ] for j in centroids.index}
    best_label_series = Series(data=np.zeros(len(_df)), index=_df.index, dtype='uint')
    label_count_dict = {_k: len(_v) for _k, _v in label_point_dict.items()}

    for h in range(len(_df)):
        print(f'run number is {h}')
        for s_idx in _df.index:
            best_distance = inf
            best_c_idx = np.random.choice(centroids.index)
            for c_idx in centroids.index:
                if best_distance > (dist_measure := dist(_df.loc[s_idx], centroids.loc[c_idx])):
                    best_distance = dist_measure
                    best_c_idx = c_idx

            best_label_series.loc[s_idx] = best_c_idx

            for _idx in centroids.index:
                if s_idx in label_point_dict[_idx]:
                    label_point_dict[_idx].remove(s_idx)
                    break  # stop removal, Point can only be in one class
            label_point_dict[best_c_idx].append(s_idx)

            centroids.loc[best_c_idx] = average(_df, label_point_dict[best_c_idx])

        # stop when solution is stable
        local_label_count_dict = {_k: len(_v) for _k, _v in label_point_dict.items()}
        if local_label_count_dict == label_count_dict:
            return best_label_series
        else:
            label_count_dict = local_label_count_dict
    return best_label_series


if __name__ == '__name__':
    cluster_df = read_csv('cluster_table.csv')
    real_cluster_df = cluster_df.drop(columns='Cluster label')

    real_cluster_df['label'] = k_means(real_cluster_df, 5, distance_euklid)
