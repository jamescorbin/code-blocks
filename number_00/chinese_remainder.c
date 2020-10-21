#include "euclid_algorithm.h"
#include "stdio.h"

// parameters:
// 		- ${a}: pointer to integer array of length ${dim}
// 			$a = {a_1, ..., a_d}$
// 			where ${a_i} is smallest positive residual
// 			of system of congruence relations.
// 		- ${n}: pointer to integer array of length ${dim}
// 			$n = {n_1, ..., n_d}$
// 			where ${n_i} is modulus of give 
// 			congruence relation.
// 			Each ${n_i}$ is pairwise coprime.
int* chinese_remainder(int* a, int* n, int dim) {
	enum arr_dim {out_dim=2, N=3};
	static int ret_val[out_dim];
	if (dim == 1) {
			ret_val[0] = a[0];
			ret_val[1] = n[0];
	}
	else {
			int a1 = a[dim-2];
			int a2 = a[dim-1];
			int n1 = n[dim-2];
			int n2 = n[dim-1];

			int* var = extended_euclid(n1, n2);
			int m1 = var[1];
			int m2 = var[2];

			int n_comb = n1*n2;
			int a_comb = (a1*m2*n2 + a2*m1*n1) % n_comb;

			a[dim-2] = a_comb;
			n[dim-2] = n_comb;
			dim--;

			int* tmp = chinese_remainder(a, n, dim);
			ret_val[0] = *tmp;
			ret_val[1] = *(tmp+1);
	}
	return ret_val;
}

int main() {
		int dim = 3;
		enum arr_dim {N = 3};
		int n[N] = {3, 5, 7};
		int a[N] = {1, 2, 6};
		printf("The system is \n");
		for (int i=0; i<dim; i++) {
			printf("x = %d (mod %d)\n", a[i], n[i]);
		}
		int* ans = chinese_remainder(a, n, dim);
		printf("The system reduces to: x = %d (mod %d)\n", ans[0], ans[1]);
}

