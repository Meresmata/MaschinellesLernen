from pandas import DataFrame, read_csv
import numpy as np

from einfuehrung.Labor_2_Clustering import Point, distance_euklid


def find_nearest_neighbor(df, k: int, dist) -> list:
    category_list = []
    for current_idx in df.index:
        distances = dict({'index': [],
                     'distance': [],
                     'category': []})

        for other_idx in df.index:
            distances['index'].append(other_idx)
            distances['distance'].append(dist(Point(*(df.loc[current_idx][:3])),
                                              Point(*(df.loc[other_idx][:3]))))
            distances['category'].append(df.loc[other_idx, 'Cluster label'])
        distances = DataFrame(distances)
        distances = distances.loc[distances['index'] != current_idx]
        distances = distances.sort_values(by='distance')
        distances = distances[:k]

        category_list.append(distances['category'].mode()[0].astype('uint8'))
    return category_list


if __name__ == '__main__':
    cluster_df = read_csv('cluster_table.csv')
    for i in reversed((15, 30, 45)):
        cluster_df[f'k_{i}'] = find_nearest_neighbor(cluster_df, i, distance_euklid)
        print(f"Übereinstimmung für k={i}: {100*np.mean(cluster_df[f'k_{i}'] == cluster_df['Cluster label']):3.1f} %.")

