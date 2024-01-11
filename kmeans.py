import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


def calculate_kmeans(file_path, k):
    # CSVファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None, names=["x", "y"])

    # KMeansクラスの初期化
    kmeans = KMeans(n_clusters=k, init='random')

    # クラスタリングの計算を実行
    kmeans.fit(df)

    # クラスタリングの結果を元のデータフレームに追加
    df["label"] = kmeans.labels_

    # クラスタリングの結果をプロット
    plt.scatter(
        df['x'], df['y'], c=df['label'], cmap='viridis', marker='o')

    # グラフの設定
    plt.xlabel('x')
    plt.ylabel('y')

    # グラフを表示
    plt.show()


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    file_path = sys.argv[1]

    calculate_kmeans(file_path, 3)
