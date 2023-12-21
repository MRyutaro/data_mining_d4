#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// 2点間の距離を計算する関数
double distance(double x1, double y1, double x2, double y2)
{
	// (x1, y1)と(x2, y2)の距離を返す
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

// k-meansを実行する関数
void k_means(double data[][2], int label[], int data_num, int k)
{
	double old_center[k][2];
	double center[k][2];
	int flag = 1;
	float eps = 0.0001;

	// 乱数の初期化
	srand((unsigned)time(NULL));
	// size個の中からk個の中心点をランダムに選ぶ
	for (int i = 0; i < k; i++)
	{
		// 0 ~ size-1の乱数を生成
		int r = rand() % data_num;
		// data[r]をcenter[i]にコピー
		center[i][0] = data[r][0];
		center[i][1] = data[r][1];
		// printf("init:\tcenter[%d] = (%lf, %lf)\n", i, center[i][0], center[i][1]);
	}

	while (flag)
	{
		// 各点を最も近い中心点に割り当てる
		for (int i = 0; i < data_num; i++)
		{
			double min_dist = INFINITY;
			for (int j = 0; j < k; j++)
			{
				double dist = distance(data[i][0], data[i][1], center[j][0], center[j][1]);
				if (dist < min_dist)
				{
					min_dist = dist;
					label[i] = j;
				}
			}
			// printf("label[%d] = %d\n", i, label[i]);
		}

		// 中心点を再計算する
		for (int i = 0; i < k; i++)
		{
			double sum_x = 0;
			double sum_y = 0;
			int count = 0;
		
			for (int j = 0; j < data_num; j++)
			{
				if (label[j] == i)
				{
					sum_x += data[j][0];
					sum_y += data[j][1];
					count++;
				}
			}
			old_center[i][0] = center[i][0];
			old_center[i][1] = center[i][1];
			center[i][0] = sum_x / count;
			center[i][1] = sum_y / count;
			// printf("old_center[%d] = (%lf, %lf), center[%d] = (%lf, %lf)\n", i, old_center[i][0], old_center[i][1], i, center[i][0], center[i][1]);
		}

		// 中心点が変化しなくなったら終了
		int count = 0;
		for (int i = 0; i < k; i++)
		{
			if (center[i][0] - old_center[i][0] < eps && center[i][1] - old_center[i][1] < eps)
			{
				count++;
			}
		}
		if (count == k)
		{
			flag = 0;
		}
		// printf("count = %d, flag = %d\n", count, flag);
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

	// k-means//
	int k = 3;
	k_means(data, label, data_num, k);
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
