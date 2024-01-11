#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 2点間の距離を計算する関数
double distance(double x1, double y1, double x2, double y2)
{
	// (x1, y1)と(x2, y2)の距離を返す
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
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
            int num = 0;
            for (int j = 0; j < data_num; j++)
            {
                if (distance(data[i][0], data[i][1], data[j][0], data[j][1]) < eps)
                {
                    num++;
                }
            }

            // 半径eps内にmin_points個のデータがあれば
            if (num >= min_points)
            {
                // クラスタ番号をつける
                cluster++;

                // 自身をクラスタに追加
                label[i] = cluster;

                // 自身の半径eps内にあるデータをクラスタに追加
                for (int j = 0; j < data_num; j++)
                {
                    if (distance(data[i][0], data[i][1], data[j][0], data[j][1]) < eps)
                    {
                        label[j] = cluster;
                    }
                }
            }
        }

        printf("%d: (%lf, %lf) %d\n", i, data[i][0], data[i][1], label[i]);
    }
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
    double eps = 0.5;
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
