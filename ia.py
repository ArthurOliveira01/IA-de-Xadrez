import chess
tabuleiro = chess.Board()

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def evaluate_board(tabuleiro):
    if tabuleiro.is_checkmate():
        if tabuleiro.turn:
            return -9999
            
        else:
            return 9999
    if tabuleiro.is_stalemate():
        return 0
    if tabuleiro.is_insufficient_material():
        return 0

    material = MaterialScore().score(tabuleiro)

    pawnsq = sum([pawntable[i] for i in tabuleiro.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                          for i in tabuleiro.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i]
                   for i in tabuleiro.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                              for i in tabuleiro.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i]
                   for i in tabuleiro.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                              for i in tabuleiro.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i]
                 for i in tabuleiro.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                          for i in tabuleiro.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i]
                  for i in tabuleiro.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                            for i in tabuleiro.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i]
                 for i in tabuleiro.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                          for i in tabuleiro.pieces(chess.KING, chess.BLACK)])

    eval = pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if tabuleiro.turn:
        return eval - material
    else:
        return -eval - material


def alphabeta(tabuleiro, alpha, beta, depthleft):
    bestscore = -9999

    if (depthleft == 0):
        return quiesce(tabuleiro, alpha, beta)
    for move in new_legal_moves(tabuleiro):
        tabuleiro.push(move)
        score = -alphabeta(tabuleiro, -beta, -alpha, depthleft - 1)
        tabuleiro.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(tabuleiro, alpha, beta):
    stand_pat = evaluate_board(tabuleiro)
    if (stand_pat >= beta):
        return beta
    if (stand_pat > alpha):
        alpha = stand_pat

    for move in is_capture_moves(tabuleiro, tabuleiro.legal_moves):
      tabuleiro.push(move)
      score = -quiesce(tabuleiro, -beta, -alpha)
      tabuleiro.pop()
      if (score >= beta):
          return beta
      if (score > alpha):
          alpha = score
    return alpha

def is_capture_moves(tabuleiro, moves):
  return [move for move in moves if tabuleiro.is_capture(move)]

def new_legal_moves(tabuleiro):
    legal_moves = tabuleiro.legal_moves
    captures = is_capture_moves(tabuleiro, legal_moves)
    if len(captures) > 0:
      return captures
    return legal_moves
    

def selectmove(tabuleiro, depth):
    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    for move in new_legal_moves(tabuleiro):
        tabuleiro.push(move)
        boardValue = -alphabeta(tabuleiro, -beta, -alpha, depth - 1)
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move
        if boardValue > alpha:
            alpha = boardValue
        tabuleiro.pop()
    return bestMove


class Chess:
  def __init__(self):
    self.tabuleiro = chess.Board()
  def move(self, k):
    for i in range(k):
        move = selectmove(self.tabuleiro, 3)
        self.tabuleiro.push(move)
        print(self.tabuleiro)                                       #caso for rodar no colab.research para visualizar melhor o tabuleiro substituir o print por display
        print('\n')                                                
        if self.tabuleiro.can_claim_threefold_repetition():
            print("é um empate pela tripla ocorrência de posição")
            print(f'{i + 1}º jogada')
            break
        if self.tabuleiro.is_checkmate():
            print('Check-Mate')
            print(f'{i + 1}º jogada')
            break
    return self

class MaterialScore:
  def score(self, tabuleiro):
    wp = len(tabuleiro.pieces(chess.PAWN, chess.WHITE))
    bp = len(tabuleiro.pieces(chess.PAWN, chess.BLACK))
    wn = len(tabuleiro.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(tabuleiro.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(tabuleiro.pieces(chess.BISHOP, chess.WHITE))
    bb = len(tabuleiro.pieces(chess.BISHOP, chess.BLACK))
    wr = len(tabuleiro.pieces(chess.ROOK, chess.WHITE))
    br = len(tabuleiro.pieces(chess.ROOK, chess.BLACK))
    wq = len(tabuleiro.pieces(chess.QUEEN, chess.WHITE))
    bq = len(tabuleiro.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp + bp) + 320 * (wn + bn) + 330 * \
        (wb + bb) + 500 * (wr + br) + 900 * (wq + bq)
    return material
Chess().move(500)