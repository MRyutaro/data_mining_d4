#include <stdio.h>
#include <math.h>

/*
 * マクロ定義
 */
#define max(A, B) ((A) > (B) ? (A) : (B))


// 2点間の距離を計算する関数
double distance(double x1, double y1, double x2, double y2)
{
	// (x1, y1)と(x2, y2)の距離を返す
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

// k_nearestを求める関数
void calculate_k_nearest(int i, int k, double data[][2], int data_num, int k_nearest[])
{
	// 1. data[i]からの距離を計算する
	double distances[data_num];
	for (int j = 0; j < data_num; j++)
	{
		distances[j] = distance(data[i][0], data[i][1], data[j][0], data[j][1]);
	}

	// 2. data[i]のk近傍点を求める
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
			if (distances[l] < min)
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
}

// reach_dist_kを求める関数
void calculate_reach_dist_k(int i, int k, double data[][2], int data_num, int k_nearest[], double reach_dist_k[])
{
	// reach_dist_k(i, j)を求める。ただし、jはk_nearestの要素。
	for (int j = 0; j < k; j++)
	{
		int k_nearest_j[k];
		calculate_k_nearest(k_nearest[j], k, data, data_num, k_nearest_j);
		// 表示
		// printf("\n");
		// printf("%d\t", k_nearest[j]);
		// for (int l = 0; l < k; l++)
		// {
		// 	printf("k_nearest_j[%d]=%d\t", l, k_nearest_j[l]);
		// }

		// reach_dist_k(i, j) = max{d(i, j), k-distances(j)}
		double d_ij = distance(data[i][0], data[i][1], data[k_nearest[j]][0], data[k_nearest[j]][1]);
		double k_dist_j = distance(data[k_nearest[j]][0], data[k_nearest[j]][1], data[k_nearest_j[k-1]][0], data[k_nearest_j[k-1]][1]);
		reach_dist_k[j] = max(d_ij, k_dist_j);
		// 表示
		// printf("\nk_nearest[%d]=%d, d(%d,%d)=%lf, d(%d,%d)=%lf, max=%lf", j, k_nearest[j], i, k_nearest[j], d_ij, k_nearest[j], k_nearest_j[k-1], k_dist_j, reach_dist_k[j]);
	}
}

// lrd_kを求める関数
double calculate_lrd_k(double reach_dist_k[], int k)
{
	// lrd_kを求める
	double lrd_k = 0;
	for (int j = 0; j < k; j++)
	{
		lrd_k += reach_dist_k[j];
	}
	lrd_k = k / lrd_k;
	// 表示
	// printf("\nlrd_k=%lf", lrd_k);

	return lrd_k;
}

// LOFを求める関数
void lof(double data[][2], double label[], int data_num, int k)
{
	for (int i = 0; i < data_num; i++)
	{
		printf("data[%d] = (%lf, %lf)\t", i, data[i][0], data[i][1]);

		// k_nearestを求める
		int k_nearest[k];
		calculate_k_nearest(i, k, data, data_num, k_nearest);

		// reach_dist_k(i, j)を求める。
		double reach_dist_k[k];
		calculate_reach_dist_k(i, k, data, data_num, k_nearest, reach_dist_k);

		// lrd_kを求める
		double lrd_k_i = calculate_lrd_k(reach_dist_k, k);
		double lof_i = 0;
		for (int j = 0; j < k; j++)
		{
			// k_nearest[j]のk_nearestを求める
			int k_nearest_j[k];
			calculate_k_nearest(k_nearest[j], k, data, data_num, k_nearest_j);
			// lrd_k_jを求める
			double reach_dist_k_j[k];
			calculate_reach_dist_k(k_nearest[j], k, data, data_num, k_nearest_j, reach_dist_k_j);
			double lrd_k_j = calculate_lrd_k(reach_dist_k_j, k);
			// printf("lrd_k_j[%d] = %lf\t", k_nearest[j], lrd_k_j);
			lof_i += lrd_k_j;
		}
		lof_i = lof_i / (k * lrd_k_i);
		printf("lof[%d] = %lf", i, lof_i);
		label[i] = lof_i;

		printf("\n");
	}
}

int main(int argc, char *argv[])
{
	FILE *fp_in, *fp_out;
	int input;
	int count = 0;
	int data_num = 200;
	double data[200][2];
	double label[200];

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
		fprintf(fp_out, "%lf,%lf,%lf\n", data[i][0], data[i][1], label[i]);
	}
	return 0;
}
