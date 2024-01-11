import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor


def calculate_lof(file_path, k):
    # CSVファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None, names=["x", "y"])

    # LOFの計算
    lof = LocalOutlierFactor(n_neighbors=k)
    lof.fit_predict(df)
    df['label'] = -lof.negative_outlier_factor_

    print(df)

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

    calculate_lof(file_path, 3)
