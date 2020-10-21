all: main.o rational.o euclid_algorithm.o
	c++ -std=c++11 main.o rational.o euclid_algorithm.o -o test_rational
euclid_algorithm.o: euclid_algorithm.c euclid_algorithm.h
	c++ -std=c++11 -c -g euclid_algorithm.c
rational.o: rational.cpp rational.h euclid_algorithm.h
	c++ -std=c++11 -c -g rational.cpp
main.o: main.cpp rational.h
	c++ -std=c++11 -c -g main.cpp
clean:
	rm -f *.o 
