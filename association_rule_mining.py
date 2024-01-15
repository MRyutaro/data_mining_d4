import os
import sys

import pandas as pd


class OneHotEncoder:
    def __init__(self) -> None:
        pass

    def encode_onehot(self, df: pd.DataFrame) -> pd.DataFrame:
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

        self.test_encode_onehot(df, one_hot_df)

        return one_hot_df


    def test_encode_onehot(self, df: pd.DataFrame, one_hot_df: pd.DataFrame) -> None:
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


    def load_onehot(self, file_path: str) -> pd.DataFrame:
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
            one_hot_df = self.encode_onehot(df)
            # print(one_hot_df)

            # one-hotエンコーディング後のデータをCSVファイルに書き込む
            one_hot_df.to_csv(f"{file_path}.onehot.csv", index=False)

        return one_hot_df


class AssociationRuleMining:
    def __init__(self) -> None:
        pass

    def __check_one_hot_df(self, one_hot_df: pd.DataFrame) -> None:
        """
        one_hot_dfのチェックを行う

        Parameters
        ----------
        one_hot_df : pd.DataFrame
            one-hotエンコーディング後のデータ
        """
        assert isinstance(one_hot_df, pd.DataFrame), "one_hot_dfはpd.DataFrame型にしてください"
        assert one_hot_df.dtypes.unique() == [bool], "one_hot_dfの中身はTrue/Falseにしてください"
        assert len(one_hot_df.columns) > 0, "one_hot_dfにcolumnsがありません"

    def calc_freq_and_ratio_of_each_items(self, one_hot_df: pd.DataFrame) -> pd.DataFrame:
        """
        各商品の頻度と割合を計算する

        Parameters
        ----------
        one_hot_df : pd.DataFrame
            one-hotエンコーディング後のデータ

        Returns
        -------
        pd.DataFrame
            各商品の頻度と割合
        """
        self.__check_one_hot_df(one_hot_df)

        # 各商品の頻度を計算する
        frequency_of_items = one_hot_df.sum(axis=0)
        # print(frequency_of_items)

        # 各商品の割合を計算する
        ratio_of_items = frequency_of_items / len(one_hot_df)
        # print(ratio_of_items)

        # 各商品の頻度と割合を結合する
        freq_and_ratio_of_items = pd.concat([frequency_of_items, ratio_of_items], axis=1)
        freq_and_ratio_of_items.columns = ["frequency", "ratio"]
        # print(freq_and_ratio_of_items)
        # print(type(freq_and_ratio_of_items))

        return freq_and_ratio_of_items

    def calc_support(self):
        pass

    def calc_confidence(self):
        pass

    def calc_association_rule(self):
        pass


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    file_path = sys.argv[1]

    one_hot_df = OneHotEncoder().load_onehot(file_path)
    # print(one_hot_df)

    freq_and_ratio_of_items = AssociationRuleMining().calc_freq_and_ratio_of_each_items(one_hot_df)
    print(freq_and_ratio_of_items)
