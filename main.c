#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 2点間の距離を計算する関数
double distance(double x1, double y1, double x2, double y2)
{
	// (x1, y1)と(x2, y2)の距離を返す
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

// k-meansを実行する関数. dataは2次元配列, labelは1次元配列. kはクラスタ数
void k_means(double **data, int *label, int k)
{
	// centerを2次元配列として扱うためのポインタ配列を確保
	double **center = (double **)malloc(sizeof(double *) * k);
	// center2の各要素に1次元配列を確保
	for (int i = 0; i < k; i++)
	{
		center[i] = (double *)malloc(sizeof(double) * 2);
	}
	// dataの配列の大きさを取得
	int size = sizeof(data) / sizeof(data[0]);
	// size個の中からk個の中心点をランダムに選ぶ
	for (int i = 0; i < k; i++)
	{
		// 0 ~ size-1の乱数を生成
		int r = rand() % size;
		// data[r]をcenter[i]にコピー
	}
	// centerをprintfで確認
	for (int i = 0; i < k; i++)
	{
		printf("(%f, %f)\n", center[i][0], center[i][1]);
	}
}

int main(int argc, char *argv[])
{
	FILE *fp_in, *fp_out;
	int input;
	int count = 0;
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
	k_means((double **)data, label, 3);
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
