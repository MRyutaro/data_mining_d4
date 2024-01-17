import sys

import matplotlib.pyplot as plt
import pandas as pd


def plot_csv_data(file_path):
    # CSVファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None, names=["x", "y", "label"])

    print(df)

    # もしラベルがない場合は、全て0とする
    if df['label'].isnull().all():
        df['label'] = 0
    # データをプロット
    plt.scatter(
        df['x'], df['y'], c=df['label'], cmap='viridis', marker='o')

    # グラフの設定
    plt.xlabel('x')
    plt.ylabel('y')
    # カラーバーを表示
    # plt.colorbar()

    # データ番号を表示
    # for i, txt in enumerate(range(0, len(df))):
    #     plt.annotate(txt, (df['x'][i], df['y'][i]), textcoords="offset points", xytext=(0, 5), ha='center')

    # labelが-1の数をカウント
    n_noise = list(df['label']).count(-1)
    print(f"count: {len(df) - n_noise}")
    # labelごとの数をカウント
    print(df.groupby('label').count().iloc[:, 0])

    output_file_path = file_path.replace(".csv", ".pdf")
    plt.savefig(output_file_path, format="pdf")
    # グラフを表示
    plt.show()


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    # file_path = sys.argv[1]
    file_path = r"data\output\dbscan-c-three-island.csv"

    # CSVファイルからデータを読み込み、プロットする
    plot_csv_data(file_path)
