#include "rational.h"
#include <iostream>

int main() {
		Rational x(10, 2), y(-1, 4), z;

		Rational t(x);
		t.add(y);
		std::cout << x.to_string() << " + " << y.to_string() << " = "
				<< t.to_string() << "\n";

		Rational s(x);
		s.add(z);
		std::cout << x.to_string() << " + " << z.to_string() << " = "
				<< s.to_string() << "\n";

		Rational u(x);
		u.diff(y);
		std::cout << x.to_string() << " - " << y.to_string() << " = "
				<< u.to_string() << "\n";

		Rational v(x);
		v.mult(y);
		std::cout << x.to_string() << " * " << y.to_string() << " = "
				<< v.to_string() << "\n";

		Rational w(x);
		w.div(y);
		std::cout << x.to_string() << " / " << y.to_string() << " = "
				<< w.to_string() << "\n";

		Rational sum =  x + y;
		std::cout << x.to_string() << " + " << y.to_string() << " = "
				<< sum.to_string() << "\n";

		return 0;
}
