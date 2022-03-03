import pygame
import numpy as np

pygame.init()

def draw_board(screen, BLACK: tuple):
  pygame.draw.line(screen, BLACK, (100, 0), (100, 300))
  pygame.draw.line(screen, BLACK, (200, 0), (200, 300))
  pygame.draw.line(screen, BLACK, (0, 100), (300, 100))
  pygame.draw.line(screen, BLACK, (0, 200), (300, 200))

def draw_symbol(screen, turn: int, x: int, y: int):
  if turn % 2:
    pygame.draw.line(screen, (0, 0, 255), (x-25, y-25), (x+25, y+25), width=10)
    pygame.draw.line(screen, (0, 0, 255), (x+25, y-25), (x-25, y+25), width=10)
  else:
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 40, 10)
  
  pygame.display.flip()

def check(board: list, turn: int, r: int, c: int):
  p = 2 - turn % 2
  row = list(board[r])
  column = list(board[:,c])
  diag1 = list(np.diagonal(board))
  diag2 = list(np.rot90(board).diagonal())
  w = [p, p, p]
  
  if p == 1:
    winner = "X"
  else:
    winner = "O"
  
  if w == row:
    return winner, "h"
  elif w == column:
    return winner, "v"
  elif w == diag1:
    return winner, "d1"
  elif w == diag2:
    return winner, "d2"
  elif not 0 in board:
    return "Tie", "T"

  return False, None

def win_text(screen, win: str):      
  font = pygame.font.Font('freesansbold.ttf', 20)

  if win != "T":
    text = font.render(f'{win} wins! Click to play again!', True, (0, 0, 0))
  else:
    text = font.render("Tie! Click to play again!", True, (0, 0, 0))

  tRect = text.get_rect()
  tRect.center = (150, 150)
  screen.blit(text, tRect)


def main():
  SCRN_W, SCRN_H = 300, 300
  BG_COLOR = (255, 255, 255)
  BLACK = (0, 0, 0)

  screen = pygame.display.set_mode((SCRN_W, SCRN_H))
  screen.fill(BG_COLOR)
  draw_board(screen, BLACK)
  pygame.display.flip()
  pygame.display.set_caption('TicTacToe')

  turn = 1
  
  board = np.array([[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]])
  board = board.reshape(3, 3)

  running = True
  win = False
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if win == False:
        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = event.pos
          column = x // 100
          row = y // 100

          if board[row][column] != 0:
            print("Spot taken!")
            continue

          draw_symbol(screen, turn, column*100+50, row*100+50)
          
          board[row][column] = 2 - turn%2

          win, t = check(board, turn, row, column)
          if win:
            if t == "h":
              pygame.draw.ellipse(screen, (255,215,0), ((0, row*100), (300, 100)), 10)
            elif t == "v":
              pygame.draw.ellipse(screen, (255,215,0), ((column*100, 0), (100, 300)), 10)
            elif t == "d1":
              pygame.draw.line(screen, (255, 215, 0), (0, 0), (300, 300), 10)
            elif t == "d2":
              pygame.draw.line(screen, (255, 215, 0), (300, 0), (0, 300), 10)
            elif t == "T":
              win_text(screen, t)
              pygame.display.flip()
              continue

            win_text(screen, win)

          pygame.display.flip()
          turn += 1
      else:
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          main()

if __name__ == "__main__":
  main()