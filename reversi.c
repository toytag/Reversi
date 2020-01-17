#include <stdlib.h>
#include <memory.h>
#include <time.h>
#include <omp.h>
#include "reversi.h"

// --- constant ---
const uint8_t EMPTY = 0;
const uint8_t BLACK = 1;
const uint8_t WHITE = 2;
const uint8_t BOTH  = 3;
const float   INF   = 1/0.0;
const uint8_t DEFAULT_MOVE = 3 * 8 + 3; // continue the game when one has 0 avl position
// ----------------

// --- REVERSI related funtions ---
void init(REVERSI *env) {
    memset(env->chess_board, EMPTY, 64);
    memset(env->avl_board, EMPTY, 64);
    env->black_count = 0;
    env->black_avl_count = 0;
    env->white_count = 0;
    env->white_avl_count = 0;
    env->round_count = 0;
    env->chess_board[3][3] = WHITE;
    env->chess_board[3][4] = BLACK;
    env->chess_board[4][3] = BLACK;
    env->chess_board[4][4] = WHITE;
    check_status(env);
}
bool put_chess(REVERSI *env, uint8_t x, uint8_t y, uint8_t player) {
    uint8_t avl_count = player == BLACK ? env->black_avl_count : env->white_avl_count;
    // if player has no available position
    if (avl_count == 0) {
        env->round_count += 1;
        return true;
    }
    // if (x,y) is avl, then put the chess
    if (env->avl_board[x][y] == player || env->avl_board[x][y] == BOTH) {
        env->chess_board[x][y] = player;
        flip(env, x, y, player, false);
        env->round_count += 1;
        return true;
    } else {
        return false;
    }
}
// lots of room for improvements
bool flip(REVERSI *env, uint8_t x, uint8_t y, uint8_t player, bool check) {
    // if check is true, return true or false and don't change chess_board
    // if check is talse, flip the chess

    // vertial up
    for (int i = 1; x-i >= 0; i++) {
        if (env->chess_board[x-i][y] == EMPTY) break;
        if (env->chess_board[x-i][y] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x-j][y] = player;
            }
            break;
        }
    }
    // vertial down
    for (int i = 1; x+i < 8; i++) {
        if (env->chess_board[x+i][y] == EMPTY) break;
        if (env->chess_board[x+i][y] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x+j][y] = player;
            }
            break;
        }
    }

    // horizontal left
    for (int i = 1; y-i >= 0; i++) {
        if (env->chess_board[x][y-i] == EMPTY) break;
        if (env->chess_board[x][y-i] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x][y-j] = player;
            }
            break;
        }
    }
    // horizontal right
    for (int i = 1; y+i < 8; i++) {
        if (env->chess_board[x][y+i] == EMPTY) break;
        if (env->chess_board[x][y+i] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x][y+j] = player;
            }
            break;
        }
    }

    // slash back
    for (int i = 1; (x-i >= 0) && (y-i >= 0); i++) {
        if (env->chess_board[x-i][y-i] == EMPTY) break;
        if (env->chess_board[x-i][y-i] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x-j][y-j] = player;
            }
            break;
        }
    }
    // slash forward
    for (int i = 1; (x+i < 8) && (y+i < 8); i++) {
        if (env->chess_board[x+i][y+i] == EMPTY) break;
        if (env->chess_board[x+i][y+i] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x+j][y+j] = player;
            }
            break;
        }
    }

    // backslash back
    for (int i = 1; (x-i >= 0) && (y+i < 8); i++) {
        if (env->chess_board[x-i][y+i] == EMPTY) break;
        if (env->chess_board[x-i][y+i] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x-j][y+j] = player;
            }
            break;
        }
    }
    // backslash forward
    for (int i = 1; (x+i < 8) && (y-i >= 0); i++) {
        if (env->chess_board[x+i][y-i] == EMPTY) break;
        if (env->chess_board[x+i][y-i] == player) {
            if (i != 1) {
                if (check) return true;
                for (int j = 1; j < i; j++)
                    env->chess_board[x+j][y-j] = player;
            }
            break;
        }
    }

    return false;
}
void check_status(REVERSI *env) {
    // reset avl_board, 
    // black_count, black_avl_count
    // white_count, white_avl_count
    memset(env->avl_board, EMPTY, 64);
    env->black_count = 0;
    env->black_avl_count = 0;
    env->white_count = 0;
    env->white_avl_count = 0;

    // update avl_board, 
    // black_count, black_avl_count
    // white_count, white_avl_count
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (env->chess_board[i][j] == BLACK) {
                env->black_count += 1;
            } else if (env->chess_board[i][j] == WHITE) {
                env->white_count += 1;
            } else {
                if (flip(env, i, j, BLACK, true)) {
                    // rely on BLACK + WHITE = BOTH
                    env->avl_board[i][j] += BLACK;
                    env->black_avl_count += 1;
                }
                if (flip(env, i, j, WHITE, true)) {
                    // rely on BLACK + WHITE = BOTH
                    env->avl_board[i][j] += WHITE;
                    env->white_avl_count += 1;
                }
            }
        }
    }

}
bool is_end(REVERSI env) {
    if (env.black_avl_count == 0 && env.white_avl_count == 0)
        return true;
    else
        return false;
}
// naive evaluation
float score(REVERSI env, uint8_t player) {
    if (player == BLACK)
        return 1.5 * (env.black_count - env.white_count) + env.black_avl_count;
    else
        return 1.5 * (env.white_count - env.black_count) + env.white_avl_count;
}
void possible_move(REVERSI env, uint8_t player, uint8_t (*dst)[2]) {
    uint8_t count = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (env.avl_board[i][j] == player || env.avl_board[i][j] == BOTH) {
                dst[count][0] = i;
                dst[count][1] = j;
                count += 1;
            }
        }
    }
    // shuffle algorithm
    srand(time(NULL));
    for (int i = 0; i < count; i++) {
        int random_index = rand() % count;
        // swap
        uint8_t tmp[2] = {dst[i][0], dst[i][1]};
        dst[i][0] = dst[random_index][0];
        dst[i][1] = dst[random_index][1];
        dst[random_index][0] = tmp[0];
        dst[random_index][1] = tmp[1];
    }
}
float minimax(REVERSI env, uint8_t depth, uint8_t player, float alpha, float beta, bool maximizing) {
    // termination condition
    if (depth == 0 || is_end(env)) {
        /* always return the score relevent to the original player (first pass)
        if minimax(env, depth, WHITE, alpha, beta, true), then no matter what depth it is at,
        WHITE is with maximizing==true, BLACK is with false.
        if minimax(env, depth, BLACK, alpha, beta, true), then no matter what depth it is at,
        BLACK is with maximizing==true, WHITE is with false.
        In this way, we can determine whose optimal move we are trying to find without passing any additional param */
        return maximizing ? score(env, player) : score(env, OPPONENT(player));
    }
    // get avl_count for current player
    uint8_t avl_count = player == BLACK ? env.black_avl_count : env.white_avl_count;
    if (maximizing) {
        // initialze max_score to store the max eval
        float max_score = -INF;
        // initalize moves to store possible moves (avoid memory control)
        uint8_t moves[avl_count+1][2];
        possible_move(env, player, moves);
        /* length of moves is avl_count+1, the last one is DEFAULT_MOVE
        when avl_count > 0, DEFAULT_MOVE won't be evaluated, 
        thanks to the `continue` in the for loop.
        when avl_count = 0, DEFAULT_MOVE is the only one,
        it will be used to continue the game. */
        moves[avl_count][0] = DEFAULT_MOVE / 8;
        moves[avl_count][1] = DEFAULT_MOVE % 8;
        // explore possible moves, with length = avl_count+1
        for (int i = 0; i < avl_count+1; i++) {
            // copy env
            REVERSI child_env;
            memcpy(&child_env, &env, sizeof(REVERSI));
            // put chess at avl position
            if (!put_chess(&child_env, moves[i][0], moves[i][1], player)) continue;
            // check status, update avl_board
            check_status(&child_env);
            // eval current situation with depth-1
            // recursion
            float new_score = minimax(child_env, depth-1, OPPONENT(player), alpha, beta, false);
            // update the max_score
            max_score = MAX(max_score, new_score);
            // alpha-beta pruning
            alpha = MAX(alpha, new_score);
            if (beta <= alpha) break;
        }
        return max_score;
    } else {
        float min_score = +INF;
        uint8_t moves[avl_count+1][2];
        possible_move(env, player, moves);
        moves[avl_count][0] = DEFAULT_MOVE / 8;
        moves[avl_count][1] = DEFAULT_MOVE % 8;
        for (int i = 0; i < avl_count+1; i++) {
            REVERSI child_env;
            memcpy(&child_env, &env, sizeof(REVERSI));
            if (!put_chess(&child_env, moves[i][0], moves[i][1], player)) continue;
            check_status(&child_env);
            float new_score = minimax(child_env, depth-1, OPPONENT(player), alpha, beta, true);
            min_score = MIN(min_score, new_score);
            beta = MIN(beta, new_score);
            if (beta <= alpha) break;
        }
        return min_score;
    }
}
uint8_t minimax_parallel(REVERSI env, uint8_t depth, uint8_t player) {
    /* depth should be at least 1, otherwise it doesn't make sense
    depth == 0 means return the current evaluation of the situation
    and just looking at the CURRENT evaluation is not sufficient
    to determine the move that will lead to the NEXT best situation */

    uint8_t avl_count = player == BLACK ? env.black_avl_count : env.white_avl_count;
    // if no avl pos, just go DEFAULT_MOVE
    if (avl_count == 0) return DEFAULT_MOVE;

    uint8_t moves[avl_count][2];
    possible_move(env, player, moves);
    float scores[avl_count];

    int num_threads = omp_get_max_threads();
    omp_set_num_threads(MIN(num_threads, avl_count));
    #pragma omp parallel for
    for (int i = 0; i < avl_count; i++) {
        REVERSI child_env;
        memcpy(&child_env, &env, sizeof(REVERSI));
        if (!put_chess(&child_env, moves[i][0], moves[i][1], player)) continue;
        check_status(&child_env);
        scores[i] = minimax(child_env, depth-1, OPPONENT(player), -INF, +INF, false);
    }

    // best_move shouldn't be DEFAULT_MOVE when returned, unless ... bug
    uint8_t best_move = DEFAULT_MOVE;
    float max_score = -INF;
    for (int i = 0; i < avl_count; i++) {
        if (scores[i] > max_score) {
            max_score = scores[i];
            best_move = moves[i][0] * 8 + moves[i][1];
        }
    }
    return best_move;
}
// --------------------------------
