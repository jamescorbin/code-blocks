int euclid(int a, int b) {
		int new_a, new_b;
		int ret_val;
		if ((a < 0) || (b < 0) || (b > a)) {
				new_a = (a < 0) ? -a : a;
				new_b = (b < 0) ? -b : b;
				if (new_b > new_a) {
						new_b = new_b + new_a;
						new_a = new_b - new_a;
						new_b = new_b - new_a;
				}
				ret_val = euclid(new_a, new_b);
		}
		else if ((b==0) && (a > 0)) {
				ret_val = a;
		}
		else if ((b!=0) && (a!=0)) {
				new_a = b;
				new_b = a - (a / b) * b;
				ret_val = euclid(new_a, new_b);
		}
		else 
				ret_val = 0;
		return ret_val;
}

int* extended_euclid_aux(int a, int b, int* s, int* t) {
		int new_a, new_b, tmp;
		int* ret_val;
		if ((b==0) && (a > 0)) {
				int var[3] = {a, s[0], t[0]};
				ret_val = var;
		}
		else if ((b!=0) && (a!=0)) {
				new_a = b;
				new_b = a - (a / b) * b;
				tmp = s[0] - (a / b) * s[1];
				*s = *(s+1);
				*(s+1) = tmp;
				tmp = t[0] - (a / b) * t[1];
				*t = *(t+1);
				*(t+1) = tmp;
				ret_val = extended_euclid_aux(new_a, new_b, s, t);
		}
		else {
				int var[3] = {0, 0, 0};
				ret_val = var;
		}
		return ret_val;
}

int* extended_euclid(int a, int b) {
		enum LEN { LEN=3 };
		static int val[LEN];
		int s_init[2] = {1, 0};
		int* s = s_init;
		int t_init[2] = {0, 1};
		int* t = t_init;
		int* tmp;
		int swtch = 0;

		int new_a = (a < 0) ? -a : a;
		int new_b = (b < 0) ? -b : b;
		if (new_b > new_a) {
				new_b = new_b + new_a;
				new_a = new_b - new_a;
				new_b = new_b - new_a;
				swtch = 1;
		}

		tmp = extended_euclid_aux(new_a, new_b, s, t);
		for(int i=0; i<LEN; i++) {
				val[i] = tmp[i];
		}
		if (swtch) {
				val[1] = val[1] + val[2];
				val[2] = val[1] - val[2];
				val[1] = val[1] - val[2];
		}
		if (a < 0)
				val[1] = -val[1];
		if (b < 0)
				val[2] = -val[2];
				
		return val;
}
