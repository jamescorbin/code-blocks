#ifndef RATIONAL_H
#define RATIONAL_H

#include <string>

class Rational {
		public:
				explicit Rational(int n=0, int d=1);
				Rational(const Rational& q);
				int add(const Rational& x);
				int diff(const Rational& x);
				int mult(const Rational& x);
				int div(const Rational& x);
				std::string to_string();
				Rational operator+(const Rational& x);
				Rational operator-(const Rational& x);
				Rational operator*(const Rational& x);
				Rational operator/(const Rational& x);
				
		private:
				int numerator;
				int denominator;
				void reduce();
};
#endif

