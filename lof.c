#include <stdio.h>
#include <math.h>


// 2点間の距離を計算する関数
double distance(double x1, double y1, double x2, double y2)
{
	// (x1, y1)と(x2, y2)の距離を返す
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

// LOFを実行する関数
void lof(double data[][2], int label[], int data_num, int k)
{
	// k個の近傍点を格納する配列
	int k_nearest[k];

	for (int i = 0; i < data_num; i++)
	{
		printf("data[%d] = (%lf, %lf)\t", i, data[i][0], data[i][1]);
		// data[i]からの距離を計算する
		double distances[data_num];
		for (int j = 0; j < data_num; j++)
		{
			distances[j] = distance(data[i][0], data[i][1], data[j][0], data[j][1]);
		}
		// data[i]のk近傍点を求める
		for (int j = 0; j < k; j++)
		{
			// distancesの中で最小の値を探す
			double min = 1000000;
			int min_index = -1;
			for (int l = 0; l < data_num; l++)
			{
				// 自身は除く
				if (l == i)
				{
					continue;
				}
				else if (distances[l] < min)
				{
					min = distances[l];
					min_index = l;
				}
			}
			// 最小の値をk_nearestに格納する
			k_nearest[j] = min_index;
			// distancesの最小値を大きな値に変更する
			distances[min_index] = 1000000;
		}
		// k_nearestを出力する
		for (int j = 0; j < k; j++)
		{
			printf("%d ", k_nearest[j]);
		}
		printf("\n");
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

	// LOF//
	int k = 3;
	lof(data, label, data_num, k);
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
