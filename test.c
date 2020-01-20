#include <stdio.h>
#include <assert.h>
#include "reversi.h"

// --- general helper functions ---

// print board to stdout for debugging
void print_board(uint8_t board[8][8]);

// print print print debug debug debug
void inspect(REVERSI env);

void print_board(uint8_t board[8][8]) {
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; ++j)
            printf("%d ", board[i][j]);
        printf("\n");
    }
}

void inspect(REVERSI env) {
    printf("\n");
    printf("chess_board:\n");
    print_board(env.chess_board);
    printf("avl_board:\n");
    print_board(env.avl_board);
    printf("black_count:\t %d\n", env.black_count);
    printf("black_avl_count: %d\t\n", env.black_avl_count);
    printf("white_count:\t %d\n", env.white_count);
    printf("white_avl_count: %d\n", env.white_avl_count);
    printf("round_count:\t %d\n", env.round_count);
    printf("\n");
}
// --------------------------------


int main() {
    
    REVERSI env;
    uint8_t x, y, player, best_move;
    init(&env);

    int skip_count = 0;

    while (!is_end(env)) {
        player = env.round_count % 2 == 0 ? BLACK : WHITE;
        best_move = minimax_parallel(env, 4, player);
        if (best_move == 27) skip_count += 1;
        x = best_move / 8; y = best_move % 8;
        put_chess(&env, x, y, player);
        check_status(&env);
        // inspect(env);
    }

    inspect(env);
    
    assert((env.black_count+env.white_count-4+skip_count) == env.round_count);
    printf("test success!\n");

    return 0;

}