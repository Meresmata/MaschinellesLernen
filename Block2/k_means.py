from pandas import read_csv
from einfuehrung.Labor_2_Clustering import k_means, distance_euklid

if __name__ == '__main__':
    df = read_csv('telematik_agg_v2.csv')
    df_2 = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0', 'driving_skill'])
    clusters = k_means(df_2, 5, distance_euklid)
