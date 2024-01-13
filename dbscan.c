#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 2点間の距離を計算する関数
double distance(double x1, double y1, double x2, double y2)
{
	// (x1, y1)と(x2, y2)の距離を返す
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

// 与えられた点のε近傍点を探索する．
void get_neighbors(double data[][2], int data_num, int i, double eps, int neighbors[], int *neighbors_num)
{
    // 近傍点の数を0に初期化
    *neighbors_num = 0;
    // 各データについて
    for (int j = 0; j < data_num; j++)
    {
        // 自身以外のデータで
        if (i != j)
        {
            // 距離がeps以下なら
            if (distance(data[i][0], data[i][1], data[j][0], data[j][1]) < eps)
            {
                // 近傍点に追加
                neighbors[*neighbors_num] = j;
                (*neighbors_num)++;
            }
        }
    }

    // neighborsを昇順にソート
    for (int j = 0; j < *neighbors_num - 1; j++)
    {
        for (int k = *neighbors_num - 1; k > j; k--)
        {
            // 距離を比較
            double dist_1 = distance(data[i][0], data[i][1], data[neighbors[k]][0], data[neighbors[k]][1]);
            double dist_2 = distance(data[i][0], data[i][1], data[neighbors[k - 1]][0], data[neighbors[k - 1]][1]);
            if (dist_1 < dist_2)
            {
                // 交換
                int tmp = neighbors[k];
                neighbors[k] = neighbors[k - 1];
                neighbors[k - 1] = tmp;
            }
        }
    }
}

// クラスタを拡張する関数。再帰的に呼び出される。
void expand_cluster(double data[][2], int data_num, int i, int label[], int cluster, double eps, int min_points, int neighbors[], int neighbors_num)
{
    // 近傍点の数だけ繰り返す
    for (int j = 0; j < neighbors_num; j++)
    {
        // 未分類のデータのみ処理
        if (label[neighbors[j]] == -1)
        {
            // 近傍点をクラスタに追加
            label[neighbors[j]] = cluster;

            // 近傍点の近傍点を取得
            int neighbors2[data_num];
            int neighbors2_num;
            get_neighbors(data, data_num, neighbors[j], eps, neighbors2, &neighbors2_num);

            // 近傍点がmin_points以上ならば
            if (neighbors2_num >= min_points)
            {
                // 近傍点の近傍点をクラスタに追加
                expand_cluster(data, data_num, neighbors[j], label, cluster, eps, min_points, neighbors2, neighbors2_num);
            }
        }
    }
}

// DBSCANを実行する関数
void dbscan(double data[][2], int data_num, double eps, int min_points, int label[])
{
    // ラベルの初期化
    for (int i = 0; i < data_num; i++)
    {
        label[i] = -1;
    }

    // クラスタ番号
    int cluster = 0;

    // 各データについて
    for (int i = 0; i < data_num; i++)
    {
        // 未分類のデータのみ処理
        if (label[i] == -1)
        {
            // 半径eps内に含まれるデータ数を数える
            int neighbors[data_num];
            int neighbors_num;
            get_neighbors(data, data_num, i, eps, neighbors, &neighbors_num);

            // 半径eps内にmin_points個のデータがあれば
            if (neighbors_num >= min_points)
            {
                // 自身をクラスタに追加
                label[i] = cluster;
                // クラスタを拡張していく
                expand_cluster(data, data_num, i, label, cluster, eps, min_points, neighbors, neighbors_num);
                // クラスタが切れたら次のクラスタ番号へ
                cluster++;
            }
        }

        // printf("%d: (%lf, %lf) %d\n", i, data[i][0], data[i][1], label[i]);
    }

    // クラスタ数を表示
    printf("cluster: %d\n", cluster);
}

int main(int argc, char *argv[])
{
	FILE *fp_in, *fp_out;
	int input;
	int count = 0;
	int data_num = 200;
	double data[200][2]; // the number of data is 200
	int label[200];

	// Input//
	fp_in = fopen(argv[1], "r");
	if (fp_in == NULL)
	{
		printf("fail: cannot open the input-file. Change the name of input-file. \n");
		return -1;
	}

	while ((input = fscanf(fp_in, "%lf,%lf", &data[count][0], &data[count][1])) != EOF)
	{
		// printf("%lf %lf\n", data[count][0], data[count][1]);
		count++;
	}

	// DBSCAN//
    double eps = 0.1;
    int min_points = 5;
    dbscan(data, data_num, eps, min_points, label);
	//

	///////////

	// Output//
	fp_out = fopen(argv[2], "w");
	if (fp_out == NULL)
	{
		printf("fail: cannot open the output-file. Change the name of output-file.  \n");
		return -1;
	}

	for (int i = 0; i < 200; i++)
	{
		fprintf(fp_out, "%lf,%lf,%d\n", data[i][0], data[i][1], label[i]);
	}
	return 0;
}
