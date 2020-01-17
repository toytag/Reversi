CC=gcc
CFLAGS=-std=c99 -fopenmp -march=native -Ofast -Wpedantic -Wall -Wextra -Werror

all: libreversi.so

reversi.o: reversi.h reversi.c
    $(CC) $(CFLAGS) -fPIC -c reversi.c -o reversi.o

libreversi.so: reversi.o
    $(CC) $(CFLAGS) -shared reversi.o -o libreversi.so

.PHONY: test clean

test: test.c libreversi.so
    $(CC) $(CFLAGS) test.c -L. -lreversi -o test && ./test

clean:
    rm -rf reversi.o libreversi.so test
