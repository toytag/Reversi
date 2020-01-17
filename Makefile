CC=gcc
CFLAGS=-std=c99 -fopenmp -march=native -Ofast -Wpedantic -Wall -Wextra -Werror

all: libreversi.so

libreversi.so: reversi.h reversi.c
	$(CC) $(CFLAGS) -fPIC -shared reversi.c -o libreversi.so

.PHONY: test clean

test: test.c libreversi.so
	$(CC) $(CFLAGS) test.c -Wl,-rpath=. -L. -lreversi -o test && ./test

clean:
	rm -rf reversi.o libreversi.so test
