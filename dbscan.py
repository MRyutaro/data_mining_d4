import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN


def calculate_dbscan(file_path, eps, min_samples):
    # CSVファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None, names=["x", "y"])

    # DBSCANクラスの初期化
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)

    # データを学習させクラスタリングを行う
    clusters = dbscan.fit_predict(df)
    df['label'] = clusters

    # labelが-1の数をカウント
    n_noise = list(clusters).count(-1)
    print(f"count: {len(clusters) - n_noise}")
    # labelごとの数をカウント
    print(df.groupby('label').count().iloc[:, 0])

    # クラスタリングの結果をプロット
    plt.scatter(
        df['x'], df['y'], c=df['label'], cmap='viridis', marker='o')

    # グラフの設定
    plt.xlabel('x')
    plt.ylabel('y')

    plt.savefig(r"data\output\dbscan-py-crater.pdf", format="pdf")

    # グラフを表示
    # plt.show()


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    # file_path = sys.argv[1]
    file_path = r"data\input\crater.csv"

    eps = 0.5
    min_samples = 5
    calculate_dbscan(file_path)
