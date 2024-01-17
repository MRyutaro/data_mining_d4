import os
import sys

import numpy as np
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
    def __init__(self, one_hot_df: pd.DataFrame, item_num: int = 10) -> None:
        """
        コンストラクタ
        
        Parameters
        ----------
        one_hot_df : pd.DataFrame
            one-hotエンコーディング後のデータ

        item_num : int(default=10)
            商品の数

        Returns
        -------
        None
        """
        self.__check_one_hot_df(one_hot_df)
        one_hot_df = one_hot_df.iloc[:, :item_num]
        # すべてFalseの行を削除する
        one_hot_df = one_hot_df[~(one_hot_df == False).all(axis=1)]
        # indexを振り直す
        self.one_hot_df = one_hot_df.reset_index(drop=True)
        # print(self.one_hot_df)

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

    def __create_itemsets(self, items: list, num: int) -> list:
        """
        itemsからnum個の商品を選ぶすべての組み合わせを作成する

        Parameters
        ----------
        items : list
            商品のリスト

        num : int
            商品の数

        Returns
        -------
        list
            商品の組み合わせのリスト
        """
        assert isinstance(items, list), "itemsはlist型にしてください"
        assert isinstance(num, int), "numはint型にしてください"
        assert num > 0, "numは1以上にしてください"

        itemsets = []
        # itemsからnum個の商品を選ぶすべての組み合わせを作成する
        for i in range(len(items)):
            if num == 1:
                itemsets.append([items[i]])
            else:
                # items[i+1:]からnum-1個の商品を選ぶすべての組み合わせを作成する
                for itemset in self.__create_itemsets(items[i+1:], num-1):
                    itemsets.append([items[i]] + itemset)

        return itemsets

    def __calc_support(self, itemset: list) -> pd.DataFrame:
        """
        itemsetのsupportを計算する

        Parameters
        ----------
        itemset : list
            商品の組み合わせ

        Returns
        -------
        pd.DataFrame
            supportのデータ
        """
        assert isinstance(itemset, list), "itemsetはlist型にしてください"
        assert len(itemset) > 0, "itemsetに商品がありません"

        # itemsetの商品の列を抽出する
        columns = self.one_hot_df[itemset]
        # print(columns)

        # itemsetの商品がすべてTrueの行を抽出する
        rows = columns.all(axis=1)
        # print(rows)

        # itemsetの商品がすべてTrueの行の割合を計算する
        support = rows.sum() / len(rows)
        # print(support)

        # supportのデータを作成する
        support_df = pd.DataFrame([[itemset, support]], columns=["itemset", "support"])

        return support_df

    def calc_support(self) -> pd.DataFrame:
        """
        self.one_hot_dfの商品のすべての組み合わせのsupportを計算する

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            supportのデータ
        """
        # supportのデータを格納するDataFrameを作成する
        supports_df = pd.DataFrame(columns=["itemset", "support"])
        # itemのリストを作成する
        items: list = list(self.one_hot_df.columns)
        # print(items)

        # 1から(商品数-1)までのforループを回す
        for i in range(1, len(items)):
            # i個の商品の全ての組み合わせを作成する
            itemsets: list = self.__create_itemsets(items, i)
            # print(len(itemsets))

            # itemsetsのsupportを計算する
            for itemset in itemsets:
                support_df: pd.DataFrame = self.__calc_support(itemset)
                # print(support_df)
                # supportが0の場合は追加しない
                if support_df["support"].values[0] == 0:
                    continue
                # supportのデータを追加する
                supports_df = pd.concat([supports_df, support_df], ignore_index=True)

        # supportの降順にソートする
        supports_df = supports_df.sort_values("support", ascending=False, ignore_index=True)

        return supports_df

    def calc_confidence(self) -> pd.DataFrame:
        pass

    def calc_association_rule(self) -> pd.DataFrame:
        pass


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    file_path = sys.argv[1]

    one_hot_df = OneHotEncoder().load_onehot(file_path)
    # print(one_hot_df)

    arm = AssociationRuleMining(one_hot_df)
    supports_df = arm.calc_support()
    print(supports_df)
