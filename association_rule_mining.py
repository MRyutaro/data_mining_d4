import os
import sys

import pandas as pd


def encode_onehot(df: pd.DataFrame) -> pd.DataFrame:
    """
    one-hotエンコーディングを行う

    Parameters
    ----------
    df : pd.DataFrame
        元のデータ

    Returns
    -------
    pd.DataFrame
        one-hotエンコーディング後のデータ
    """
    assert isinstance(df, pd.DataFrame), "dfはpd.DataFrame型にしてください"

    # nan以外の値を抽出する
    item_list = df.values.flatten()
    item_list = [x for x in item_list if pd.notnull(x)]

    # item_listから重複を除いたリストを作成する
    item_list = list(set(item_list))
    # item_listをabc順にソートする
    item_list.sort()

    # item_listをcolumns、indexはdfと同じ、値はFalseのDataFrameを作成する
    one_hot_df = pd.DataFrame(False, columns=item_list, index=df.index)

    # dfの各行でforループを回す
    for row_index, row in df.iterrows():
        # 中身のあるセルを抽出する
        items = [x for x in row if pd.notnull(x)]
        for item in items:
            for column in one_hot_df.columns:
                if item == column:
                    one_hot_df.loc[row_index, column] = True

    test_encode_onehot(df, one_hot_df)

    return one_hot_df


def test_encode_onehot(df: pd.DataFrame, one_hot_df: pd.DataFrame) -> None:
    """
    encode_onehot関数のテストを行う

    Parameters
    ----------
    df : pd.DataFrame
        元のデータ

    one_hot_df : pd.DataFrame
        one-hotエンコーディング後のデータ
    """
    assert isinstance(df, pd.DataFrame), "dfはpd.DataFrame型にしてください"
    assert isinstance(one_hot_df, pd.DataFrame), "one_hot_dfはpd.DataFrame型にしてください"
    assert df.index.equals(one_hot_df.index), "dfとone_hot_dfのindexが異なります"

    # dfの各行でforループを回す
    for row_index, row in df.iterrows():
        # 中身のあるセルを抽出する
        a_items = [x for x in row if pd.notnull(x)]
        # one_hot_dfの行を抽出する
        b_items = one_hot_df.loc[row_index, :]
        # Trueの値を抽出する
        b_items = b_items[b_items == True]
        # indexを抽出する
        b_items = b_items.index.values
        # a_itemsとb_itemsが一致するか確認する
        assert set(a_items) == set(b_items), "one-hotエンコーディングが正しく行われていません"


def load_onehot(file_path: str) -> pd.DataFrame:
    """
    one-hotエンコーディング後のデータを読み込む

    Parameters
    ----------
    file_path : str
        ファイルパス

    Returns
    -------
    pd.DataFrame
        one-hotエンコーディング後のデータ
    """
    assert os.path.exists(file_path), "ファイルが存在しません"
    assert isinstance(file_path, str), "file_pathはstr型にしてください"
    assert file_path.endswith(".csv"), "CSVファイルを指定してください"

    # onehotデータがある場合はそれを読み込む
    if os.path.exists(f"{file_path}.onehot.csv"):
        one_hot_df = pd.read_csv(f"{file_path}.onehot.csv", header=0)
    else:
        # CSVファイルからデータを読み込む
        # 1行目にはヘッダがあるので、ヘッダを指定する
        df = pd.read_csv(file_path, header=0)
        # print(df)
        # print(type(df))

        # one-hotエンコーディングを行う
        one_hot_df = encode_onehot(df)
        # print(one_hot_df)

        # one-hotエンコーディング後のデータをCSVファイルに書き込む
        one_hot_df.to_csv(f"{file_path}.onehot.csv", index=False)

    return one_hot_df


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    file_path = sys.argv[1]

    one_hot_df = load_onehot(file_path)

    print(one_hot_df)
