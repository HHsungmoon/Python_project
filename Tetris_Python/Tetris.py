
import sys
from math import sqrt
from random import randint
import pygame
import random
import time
 
# 전역 변수
pygame.init() # 라이브러리 초기화를 하지 않으면 일부 기능이 정상적으로 작동하지 않을 수 있다.

pygame.display.set_caption("Tetris game - madeby HSM")  #화면 타이틀
SCREEN = pygame.display.set_mode((800, 800)) #화면 크기 설정

smallfont = pygame.font.SysFont(None, 36)
largefont = pygame.font.SysFont(None, 72)
 
pygame.key.set_repeat(30, 30)

clock = pygame.time.Clock()

# 가로 세로 블럭 갯수. 게임 테투리 크기
# 게임 진행동안 쌓인 블록이 저장될 보드, 점수
Game_Board = []
Game_Score = 0
Board_Width_num = 16
Board_Height_num = 24
INTERVAL = 40 #낙하 간격

# 색상
BLACK = (0,0,0)
AQUA = (0, 255, 255) # I
RED = (255, 0, 0) # Z
BLUE = (0, 0, 255) # J
ORENGE = (255, 165, 0) # L
GREEN = (0, 255, 0) # S
PURPLE = (255, 0, 255) # T
YELLOW = (255, 255, 0) # O
GRAY = (128, 128, 128) # 벽
WHITE = (255,255,255)

PIECE_SIZE = 24 # 24 x 24
PIECE_GRID_SIZE = PIECE_SIZE+1 # 블록간 간격 1로 설정

"""---------------------------------------------------------"""

# 블록 모양은 변하지 않는 값이기 때문에 튜플로 선언
# C++테트리스 에서는 4x4 배열로 4가지 타입 선언을 해 주었는데 파이썬 테트리스 에서는 2x2, 3x3, 4x4로 나눠서 만들어 보았다.

# 회전1, 2x2
Block_type_O = ((
        (1,1),
        (1,1) ),
    (
        (1,1),
        (1,1) ))

# 회전2, 4x4
Block_type_I = ((
        (0,0,0,0),
        (2,2,2,2),
        (0,0,0,0),
        (0,0,0,0) ),
    (
        (0,0,2,0),
        (0,0,2,0),
        (0,0,2,0),
        (0,0,2,0) ))

# 회전2, 3x3
Block_type_S = ((
        (0,3,3),
        (3,3,0),
        (0,0,0) ),
    (
        (3,0,0),
        (3,3,0),
        (0,3,0) ),)
Block_type_Z = ((
        (4,4,0),
        (0,4,4),
        (0,0,0) ),
    (
        (0,4,0),
        (4,4,0),
        (4,0,0) ),)

# 회전4, 3,3
Block_type_T = ((
        (0,5,0),
        (5,5,5),
        (0,0,0) ),
    (
        (0,5,0),
        (0,5,5),
        (0,5,0) ),
    (
        (0,0,0),
        (5,5,5),
        (0,5,0) ),
    (
        (0,5,0),
        (5,5,0),
        (0,5,0) ))
Block_type_L = ((
        (0,6,0),
        (0,6,0),
        (0,6,6) ),
    (
        (0,0,0),
        (6,6,6),
        (6,0,0) ),
    (
        (6,6,0),
        (0,6,0),
        (0,6,0) ),
    (
        (0,0,6),
        (6,6,6),
        (0,0,0) ))
Block_type_J = ((
        (0,7,0),
        (0,7,0),
        (7,7,0) ),
    (
        (7,0,0),
        (7,7,7),
        (0,0,0) ),
    (
        (0,7,7),
        (0,7,0),
        (0,7,0) ),
    (
        (0,0,0),
        (7,7,7),
        (0,0,7) ))

#위에 만든 블록 종류를 저장하는 튜플과 배열 순서에 맞춘 color. O타입 블록의 index가 1이기 때문에 color가 Yellow이다.
Block_Type = ( (), Block_type_O, Block_type_I, Block_type_S, Block_type_Z, Block_type_T, Block_type_L, Block_type_J)
Block_Color = ( WHITE, YELLOW, AQUA, GREEN, RED , PURPLE, ORENGE, BLUE)


class TBlock:
    def __init__(self, block_type_num):
        self.block_type = block_type_num # 7가지 블록 종류. index인 int타입
        self.rotate_type = int(len(Block_Type[block_type_num])) # 블록 로테이트 종류 1,2,4

        self.rotation = randint(0, self.rotate_type-1) 
        self.block_color = Block_Color[self.block_type]

        self.block_shape = Block_Type[self.block_type]# 블록데이터.  rotationx2x2, 3x3, 4x4

        self.size = int(len(self.block_shape[0])) # 블록 배열 한변의 길이
        self.x = int(Board_Width_num/2)-1
        self.y = 0
        self.down_speed = INTERVAL # 블록이 떨어지는 속도

    # 블록을 print 하는 함수
    def Print_Block(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.block_shape[self.rotation][y][x] == self.block_type:
                    p_x = PIECE_GRID_SIZE + (x + self.x)* PIECE_GRID_SIZE
                    p_y = PIECE_GRID_SIZE + (y + self.y)* PIECE_GRID_SIZE
                    pygame.draw.rect(SCREEN, self.block_color, (p_x, p_y, PIECE_SIZE, PIECE_SIZE))
                    pygame.display.flip()
    # 블록을 지우는 함수
    def Erase_Block(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.block_shape[self.rotation][y][x] == self.block_type:
                    p_x = PIECE_GRID_SIZE + (x + self.x)* PIECE_GRID_SIZE
                    p_y = PIECE_GRID_SIZE + (y + self.y)* PIECE_GRID_SIZE
                    pygame.draw.rect(SCREEN, BLACK, (p_x, p_y, PIECE_SIZE, PIECE_SIZE))
                    pygame.display.flip()
    
    # 블록이 회전 가능한지 체크하는 함수
    def Rotate_possible(self, next_rotation):
        block_data = self.block_shape[next_rotation]
        for y in range(0,self.size):
            for x in range(0, self.size):
                if block_data[y][x] == self.block_type:
                    if Game_Board[y+self.y][x+self.x] != 0:
                        return False
        return True

    # 블록이 오른쪽으로 회전 가능하면 rotation을 변경
    def Rotate_Right(self):
        tmp = (self.rotation+1) % self.rotate_type
        if self.Rotate_possible(tmp) == True:
            self.rotation = tmp
        return self.rotation

    # 블록이 왼쪽으로 회전 가능하면 rotation을 변경
    def Rotate_Left(self):
        if self.rotation == 0:
            tmp = self.rotate_type-1
        else:
            tmp = self.rotation-1

        if self.Rotate_possible(tmp) == True:
            self.rotation = tmp
        return self.rotation

    # 블록이 매개변수로 넘어온 방향으로 이동 가능한지 체크
    def Move_possible(self, px, py):
        block_data = self.block_shape[self.rotation]
        for y in range(0,self.size):
            for x in range(0, self.size):
                if block_data[y][x] == self.block_type:
                    if Game_Board[y+py][x+px] !=0:
                        return False
        return True

    def Move_down(self):
        if self.Move_possible(self.x, self.y+1) == True:
            return self.y+1
        return self.y

    def Move_Right(self):
        if self.Move_possible(self.x+1, self.y) == True:
            return self.x+1
        return self.x
    def Move_Left(self):
        if self.Move_possible(self.x-1, self.y) == True:
            return self.x-1
        return self.x

# 다음 블록이 어떤 종류인지 출력하는 함수
def Print_Next_Block(block: TBlock):
    block.x = Board_Width_num + 5
    block.y = 5
    block.Print_Block()

# 게임 보드를 만드는 함수. 좌우 아래 벽은 -1
def Create_Board():
    board = []
    for y in range(0, Board_Height_num):
        tmp = []
        for x in range(0, Board_Width_num):
            tmp.append(0)
        board.append(tmp)

    for y in range(2, Board_Height_num):
        board[y][0] = -1
        board[y][Board_Width_num-1] = -1
    for x in range(0, Board_Width_num):
        board[Board_Height_num-1][x] = -1
    return board

# 게임 보드를 출력하는 함수.좌우 아래 벽은 -1, 쌓인 블록 정보에 따라 색갈별로
def Print_Board():
    for y in range(0, Board_Height_num):
        for x in range(0, Board_Width_num):
            b_x = PIECE_GRID_SIZE + x*PIECE_GRID_SIZE
            b_y = PIECE_GRID_SIZE + y*PIECE_GRID_SIZE
            if Game_Board[y][x] == -1:
                pygame.draw.rect(SCREEN, GRAY, (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 1:
                pygame.draw.rect(SCREEN, Block_Color[1], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 2:
                pygame.draw.rect(SCREEN, Block_Color[2], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 3:
                pygame.draw.rect(SCREEN, Block_Color[3], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 4:
                pygame.draw.rect(SCREEN, Block_Color[4], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 5:
                pygame.draw.rect(SCREEN, Block_Color[5], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 6:
                pygame.draw.rect(SCREEN, Block_Color[6], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))
            elif Game_Board[y][x] == 7:
                pygame.draw.rect(SCREEN, Block_Color[7], (b_x, b_y, PIECE_SIZE, PIECE_SIZE))

    pygame.display.flip()
 
# 우측 상단에 점수 표시
def Print_Score():    
    score_str = str(Game_Score).zfill(3)
    score_image = smallfont.render(score_str, True, (0, 255, 0))
    SCREEN.blit(score_image, (500, 30))
    pygame.display.flip()

# 게임 종료 조건 체크
def Game_Over():
    global Game_Board
    for x in range(1, Board_Width_num-1):
        if Game_Board[2][x] != 0:
            return True
    return False

# 게임over 메시지 출력후 프로그램 종료 된다.
def Print_GameOver_Message():
    score_str = "Game is Over!"
    score_image = largefont.render(score_str, True, (0, 255, 0))
    SCREEN.blit(score_image, (250, 300))
    pygame.display.flip()

# 블록이 game보드에서 더이상 아래로 움직일 수 없을 때 보드에 블록 정보 저장
def Update_Game_Board(block):
    global Game_Board
    added_line = []
    for y in range(0, block.size):
        for x in range(0, block.size):
            if block.block_shape[block.rotation][y][x] != 0:
                Game_Board[block.y+y][block.x+x] = block.block_type
                added_line.append(block.y + y)
    return list(set(added_line))

# 게임 보드에서 매개변수로 받은 y줄의 한줄 완성 여부를 체크한다.                 
def Line_Full_check(y):
    global Game_Board
    for x in range(1,Board_Width_num-1):
        if Game_Board[y][x] == 0:
            return False
    return True

# Clear_line 함수 실행시 새로운 줄을 만들어 준다.
def Make_New_Line():
    line = []
    for x in range(0, Board_Width_num):
        line.append(0)
    line[0] = -1
    line[Board_Width_num-1]=-1
    return line

# 한줄 완성이 되었을 경우 해당 줄을 삭제하고 점수를 올려준다.
def Clear_Line(list_y):
    global Game_Board
    global Game_Score
    list_y.sort()
    for y in list_y:
        if Line_Full_check(y) == True:
            del Game_Board[y]
            Game_Board.insert(2, Make_New_Line())
            Game_Score += 1


def run_game():
    global Game_Board
    Game_Board = Create_Board()
    next_block_type = randint(1,7)
    Next_BLOCK = TBlock(next_block_type)
    
    while True:
        SCREEN.fill(BLACK)
        Print_Board()
        Print_Score()

        # 현재 블록은 next블록 과 같은 종류,rotation상태 이어야 한다.
        BLOCK = TBlock(Next_BLOCK.block_type)
        BLOCK.rotation = Next_BLOCK.rotation
        BLOCK.Print_Block()

        block_type = randint(1,7)
        Next_BLOCK = TBlock(block_type)
        Print_Next_Block(Next_BLOCK)
        
        while True:
            frame = 20
            clock.tick(frame)
            speed = 0.5    # 게임 진행 속도를 0.5초 로 잡았다. 
            #---------------------
            
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    BLOCK.Erase_Block()
                    if key == pygame.K_RIGHT:
                        BLOCK.x = BLOCK.Move_Right()
                    elif key == pygame.K_LEFT:
                        BLOCK.x = BLOCK.Move_Left()
                    elif key == pygame.K_DOWN:
                        BLOCK.y = BLOCK.Move_down()
                    elif key == pygame.K_a:
                        BLOCK.rotation = BLOCK.Rotate_Left()
                    elif key == pygame.K_d:
                        BLOCK.rotation = BLOCK.Rotate_Right()
                    BLOCK.Print_Block()
                    speed = speed - 0.2
                    time.sleep(0.2)
                    break;
                elif event.type == pygame.KEYUP:
                    key = None
            
            #---------------------
            pygame.event.clear()

            if BLOCK.Move_possible(BLOCK.x, BLOCK.y+1) == True:
                BLOCK.Erase_Block()
                BLOCK.y = BLOCK.Move_down()
                BLOCK.Print_Block()
                time.sleep(speed)
            else:
                added_line = Update_Game_Board(BLOCK)
                Clear_Line(added_line)
                time.sleep(speed)
                next_block_type = Next_BLOCK.block_type
                break

        if Game_Over() == True:
            Print_GameOver_Message()
            time.sleep(3)
            return 
            

run_game()
pygame.quit()