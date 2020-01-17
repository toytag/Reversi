CC=gcc
STD=-std=c99
CFLAGS=-fopenmp -march=native -Ofast -Wpedantic -Wall -Wextra -Werror

all: libreversi.so test

libreversi.so: reversi.h reversi.c
	$(CC) $(STD) $(CFLAGS) -fPIC -shared reversi.c -o libreversi.so

.PHONY: test clean

test: test.c libreversi.so
	$(CC) $(STD) $(CFLAGS) test.c -L. -lreversi -o test && ./test

clean:
	rm -rf libreversi.so test
