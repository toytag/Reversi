#ifndef REVERSI_H
#define REVERSI_H

// --- boolean type ---
#include <stdbool.h>
// --------------------
// --- uint8_t type ---
typedef unsigned char uint8_t
// --------------------

// --- constant ---
extern const uint8_t EMPTY;
extern const uint8_t BLACK;
extern const uint8_t WHITE;
extern const uint8_t BOTH;
// ----------------

// --- general helper macros --- 
#define MAX(x, y) ((x) > (y) ? (x) : (y))
#define MIN(x, y) ((x) < (y) ? (x) : (y))
#define OPPONENT(player) ((player) == BLACK ? WHITE : BLACK)
// -----------------------------

// --- struct define ---
typedef struct REVERSI {
    uint8_t chess_board[8][8];
    uint8_t avl_board[8][8];
    uint8_t black_count;
    uint8_t black_avl_count;
    uint8_t white_count;
    uint8_t white_avl_count;
    uint8_t round_count;
} REVERSI;
// ---------------------

// --- REVERSI related funtions ---
// initalize reversi environment
void  init(REVERSI *env);
// put player's chess to x, y on the chess board
bool  put_chess(REVERSI *env, uint8_t x, uint8_t y, uint8_t player);
// flip the chess according to player and x, y position on the chess board
bool  flip(REVERSI *env, uint8_t x, uint8_t y, uint8_t player, bool check);
// check game status
void  check_status(REVERSI *env);
// check if the game has ended
bool  is_end(REVERSI env);
// give a evaluation of current status for player
float score(REVERSI env, uint8_t player);
// find the possible move for player, store to dst
void  possible_move(REVERSI env, uint8_t player, uint8_t (*dst)[2]);
// general minimax algorithm
float minimax(REVERSI env, uint8_t depth, uint8_t player, float alpha, float beta, bool maximizing);
// parallel minimax algorithm, instead of return score, it finds best move and save to dst
uint8_t minimax_parallel(REVERSI env, uint8_t depth, uint8_t player);
// --------------------------------

#endif
