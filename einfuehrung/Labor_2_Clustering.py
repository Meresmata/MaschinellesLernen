#!/usr/bin/env python
# coding: utf-8

from pprint import pprint
from dataclasses import dataclass
from pandas import read_csv, DataFrame, Series
import numpy as np
from math import inf


cluster_df = read_csv('cluster_table.csv')
real_cluster_df = cluster_df.drop(columns='Cluster label')


@dataclass
class Point:
    x: float
    y: float
    z: float


def distance(p1: Point, p2: Point):
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2


k = 5
centroids = real_cluster_df.sample(5)
pprint(centroids)


def average(df: DataFrame, f: list[int]) -> tuple[float, float, float]:
    loc_df = df.loc[f].copy()
    return tuple(loc_df.mean().values)


# key: centroid index, values list of point index
label_point_dict: dict[int, list[int]] = {j: [j, ] for j in centroids.index}
best_label_series = Series(data=np.zeros(len(real_cluster_df)), index=real_cluster_df.index, dtype='uint')
label_count_dict = {k: len(v) for k, v in label_point_dict.items()}


for h in range(len(real_cluster_df)):
    print(f'run number is {h}')
    for s_idx in real_cluster_df.index:
        best_distance = inf
        best_c_idx = np.random.choice(centroids.index)
        for c_idx in centroids.index:
            if best_distance > (dist := distance(Point(*(real_cluster_df.loc[s_idx])), Point(*(centroids.loc[c_idx])))):
                best_distance = dist
                best_c_idx = c_idx

        best_label_series.loc[s_idx] = best_c_idx

        for _idx in centroids.index:
            if s_idx in label_point_dict[_idx]:
                label_point_dict[_idx].remove(s_idx)
                break  # stop removal, Point can only be in one class
        label_point_dict[best_c_idx].append(s_idx)

        centroids.loc[best_c_idx] = average(real_cluster_df, label_point_dict[best_c_idx])

    # stop when solution is stable
    local_label_count_dict = {k: len(v) for k, v in label_point_dict.items()}
    if local_label_count_dict == label_count_dict:
        break
    else:
        label_count_dict = local_label_count_dict
    pprint(label_count_dict)

    # pprint(centroids)

real_cluster_df['label'] = best_label_series
