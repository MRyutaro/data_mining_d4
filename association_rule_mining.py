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
        self.__check_onehot_df(one_hot_df)
        one_hot_df = one_hot_df.iloc[:, :item_num]
        # すべてFalseの行を削除する
        one_hot_df = one_hot_df[~(one_hot_df == False).all(axis=1)]
        # indexを振り直す
        self.one_hot_df = one_hot_df.reset_index(drop=True)
        # print(self.one_hot_df)
        self.items = list(self.one_hot_df.columns)
        # print(self.items)
        # supportのデータを格納するDataFrameを作成する
        self.supports_df = pd.DataFrame(columns=["itemset", "support"])                    
        # confidenceのデータを格納するDataFrameを作成する
        self.confidence_df = pd.DataFrame(columns=["X", "Y", "X_support", "Y_support", "X_and_Y_support", "confidence"])

    def __check_onehot_df(self, one_hot_df: pd.DataFrame) -> None:
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
        # 1から(商品数-1)までのforループを回す
        for i in range(1, len(self.items)):
            # i個の商品の全ての組み合わせを作成する
            itemsets: list = self.__create_itemsets(self.items, i)
            # print(len(itemsets))

            # itemsetsのsupportを計算する
            for itemset in itemsets:
                support_df: pd.DataFrame = self.__calc_support(itemset)
                # print(support_df)
                # supportが0の場合は追加しない
                if support_df["support"].values[0] == 0:
                    continue
                # supportのデータを追加する
                self.supports_df = pd.concat([self.supports_df, support_df])

        # supportの降順にソートする
        self.supports_df = self.supports_df.sort_values("support", ascending=False, ignore_index=True)

        return self.supports_df

    def __get_support(self, itemset: list) -> float:
        """
        itemsetのsupportを取得する

        Parameters
        ----------
        itemset : list
            商品の組み合わせ

        Returns
        -------
        float
            support
        """
        assert isinstance(itemset, list), "itemsetはlist型にしてください"
        assert len(itemset) > 0, "itemsetに商品がありません"
        assert not self.supports_df.empty, "self.supports_dfが空です"

        # itemsetを含む行を抽出し、その行の"support"列の値を取得
        support = self.supports_df[self.supports_df["itemset"].apply(lambda x: set(itemset) == set(x))]["support"].values
        if len(support) == 0:
            return 0
        else:
            return support[0]

    def calc_confidence(self) -> pd.DataFrame:
        """
        X->Yのconfidenceを計算する。ただし、XとYはself.listの商品の組み合わせである。

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            confidenceのデータ
        """
        # もしself.supports_dfが空の場合は、self.calc_support()を実行する
        if self.supports_df.empty:
            self.calc_support()

        itemsets = []
        for i in range(1, len(self.items)):
            itemset = self.__create_itemsets(self.items, i)
            # print(itemset)  # 2次元配列
            # print(len(itemset))  # 10, 45, 120, 210, ...
            itemsets += itemset

        # print(itemsets)
        # print(len(itemsets))

        # itemsetsからX,Yを選ぶ
        for X in itemsets:
            for Y in itemsets:
                # XとYが重複する場合はスキップする
                if set(X) & set(Y):
                    continue
                # print(X, Y)

                # Xのsupportを取得する
                X_support = self.__get_support(X)
                if X_support == 0:
                    continue
                # Yのsupportを取得する
                Y_support = self.__get_support(Y)
                # XかつYのsupportを取得する
                X_and_Y_support = self.__get_support(X + Y)
                if X_and_Y_support == 0:
                    continue

                # confidenceを計算する
                confidence = X_and_Y_support / X_support
                # print(confidence)

                # confidenceのデータを作成する
                confidence_df = pd.DataFrame(
                    [[X, Y, X_support, Y_support, X_and_Y_support, confidence]],
                    columns=["X", "Y", "X_support", "Y_support", "X_and_Y_support", "confidence"]
                )
                # print(confidence_df)
                # confidenceのデータを追加する
                self.confidence_df = pd.concat([self.confidence_df, confidence_df])

        # confidenceの降順にソートする
        self.confidence_df = self.confidence_df.sort_values("confidence", ascending=False, ignore_index=True)

        return self.confidence_df


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    file_path = sys.argv[1]

    one_hot_df = OneHotEncoder().load_onehot(file_path)
    # print(one_hot_df)

    arm = AssociationRuleMining(one_hot_df)
    # supports_df = arm.calc_support()
    # print(supports_df)

    confidence_df = arm.calc_confidence()
    print(confidence_df)
    confidence_df.to_csv(fr"data\output\{os.path.basename(file_path)}.confidence.csv", index=False)
