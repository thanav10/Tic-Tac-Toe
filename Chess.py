#Chess Game
'''
import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Two Player Chess')
font = pygame.font.Font('freesansbold.ttf',20)
big_font = pygame.font.Font('freesansbold.ttf',50)
timer = pygame.time.Clock()
fps = 60
#Game varieable/Images

white_pieces = ['rook','knight','bishop','king','queen','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
black_pieces = ['rook','knight','bishop','king','queen','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                   (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]
black_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                   (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 1000
valid_moves = []
'''
import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two Player Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# Game variables
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 1000
valid_moves = []
flipped = False
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('/Users/thanavamaravadi/Library/Mobile Documents/com~apple~CloudDocs/Projects/Chess/Pieces/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_rook, white_queen, white_knight, white_bishop, white_king, white_pawn]
white_images_small = [white_rook_small, white_queen_small, white_knight_small, white_bishop_small, white_king_small, white_pawn_small]
black_images = [black_rook, black_queen, black_knight, black_bishop, black_king, black_pawn]
black_images_small = [black_rook_small, black_queen_small, black_knight_small, black_bishop_small, black_king_small, black_pawn_small]
piece_list = ['rook','queen','knight','bishop','king','pawn'] 

'''
#Draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0,800,WIDTH,100])
        pygame.draw.rect(screen, 'black', [0,800,WIDTH,100],5)
        pygame.draw.rect(screen, 'black', [800,0,200,HEIGHT],5)
        status_text = ['White select a piece to move','White select a Destination','Black select a piece to move','Black select a Destination']
        screen.blit(big_font.render(status_text[turn_step],True,'black'),(20,820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0,100*i),(800,100*i), 2)
            pygame.draw.line(screen, 'black', (100*i,0),(100*i,800), 2)

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn,(white_locations[i][0] * 100 + 21 , white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index],(white_locations[i][0] * 100 + 10 , white_locations[i][1] * 100 + 10))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn,(black_locations[i][0] * 100 + 21 , black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index],(black_locations[i][0] * 100 + 10 , black_locations[i][1] * 100 + 10))

def draw_board():
    for row in range(8):
        for col in range(8):
            x = col
            y = row
            if flipped:
                x = 7 - col
                y = 7 - row
            if (row + col) % 2 == 0:
                color = 'light gray'
            else:
                color = 'dark gray'
            pygame.draw.rect(screen, color, [x * 100, y * 100, 100, 100])

    # Bottom UI bar
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'black', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'black', [800, 0, 200, HEIGHT], 5)
    status_text = ['White select a piece to move', 'White select a Destination',
                   'Black select a piece to move', 'Black select a Destination']
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))

    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

# Draw pieces based on perspective
'''
def draw_board():
    for row in range(8):
        for col in range(8):
            x = col
            y = row
            if flipped:
                x = 7 - col
                y = 7 - row
            color = 'light gray' if (row + col) % 2 == 0 else 'dark gray'
            pygame.draw.rect(screen, color, [x * 100, y * 100, 100, 100])

    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'black', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'black', [800, 0, 200, HEIGHT], 5)

    status_text = [
        'White select a piece to move',
        'White select a Destination',
        'Black select a piece to move',
        'Black select a Destination'
    ]
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))

    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
'''
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        x, y = white_locations[i]
        if flipped:
            x, y = 7 - x, 7 - y
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (x * 100 + 21, y * 100 + 30))
        else:
            screen.blit(white_images[index], (x * 100 + 10, y * 100 + 10))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        x, y = black_locations[i]
        if flipped:
            x, y = 7 - x, 7 - y
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (x * 100 + 21, y * 100 + 30))
        else:
            screen.blit(black_images[index], (x * 100 + 10, y * 100 + 10))
'''
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        x, y = white_locations[i]
        if flipped:
            x, y = 7 - x, 7 - y
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (x * 100 + 21, y * 100 + 30))
        else:
            screen.blit(white_images[index], (x * 100 + 10, y * 100 + 10))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        x, y = black_locations[i]
        if flipped:
            x, y = 7 - x, 7 - y
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (x * 100 + 21, y * 100 + 30))
        else:
            screen.blit(black_images[index], (x * 100 + 10, y * 100 + 10))



#Function to check all the valid moves for all the pieces
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        if piece == 'rook':
            moves_list = check_rook(location, turn)
        if piece == 'bishop':
            moves_list = check_bishop(location, turn)
        if piece == 'knight':
            moves_list = check_knight(location, turn)
        if piece == 'queen':
            moves_list = check_queen(location, turn)
        if piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

'''
#Draw Valid Moves
def draw_valid(moves):  
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
'''
# Draw valid moves with flipped support
'''
def draw_valid(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for x, y in moves:
        if flipped:
            x, y = 7 - x, 7 - y
        pygame.draw.circle(screen, color, (x * 100 + 50, y * 100 + 50), 5)
'''
def draw_valid(moves):  
    color = 'red' if turn_step < 2 else 'blue'
    for move in moves:
        x, y = move
        if flipped:
            x, y = 7 - x, 7 - y
        pygame.draw.circle(screen, color, (x * 100 + 50, y * 100 + 50), 5)


#Check valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options

    if 0 <= selection < len(options_list):
        return options_list[selection]
    else:
        return []
    valid_options = options_list[selection]
    return valid_options

    
#Valid Rook Moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations

    # Directions: up, down, left, right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # x, y movements for rook

    for direction in directions:
        x, y = direction
        path = True
        chain = 1

        while path:
            new_position = (position[0] + chain * x, position[1] + chain * y)
            if 0 <= new_position[0] <= 7 and 0 <= new_position[1] <= 7:
                if new_position not in friends_list:
                    moves_list.append(new_position)
                    if new_position in enemies_list:
                        path = False  # Stop if enemy piece is encountered
                    chain += 1
                else:
                    path = False  # Stop if a friendly piece is encountered
            else:
                path = False  # Stop if out of bounds

    return moves_list

#Check Bishop Moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

#Check Valid Pawn Moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0],position[1] + 1) not in white_locations and (position[0],position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0],position[1]+ 1))
        if (position[0],position[1] + 2) not in white_locations and (position[0],position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0],position[1]+ 2))
        if (position[0] + 1,position[1]+1) in black_locations:
            moves_list.append((position[0]+1,position[1] + 1))
        if (position[0] - 1,position[1]+1) in black_locations:
            moves_list.append((position[0] - 1,position[1] + 1))
    else:
        if (position[0],position[1] - 1) not in white_locations and (position[0],position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0],position[1]- 1))
        if (position[0],position[1] - 2) not in white_locations and (position[0],position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0],position[1]-2))
        if (position[0] + 1,position[1]-1) in white_locations:
            moves_list.append((position[0] + 1,position[1] - 1))
        if (position[0] - 1,position[1]-1) in white_locations:
            moves_list.append((position[0] - 1,position[1] - 1))
    return moves_list

# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list
        
             
#Draw Captured Pieces on the side of the screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(black_images_small[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(white_images_small[index], (925, 5 + 50 * i))
    


'''
#Main game loop
white_options = check_options(white_pieces, white_locations,'white')
black_options = check_options(black_pieces,black_locations,'black')
run = True 
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations,'black')
                    white_options = check_options(white_pieces,white_locations,'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(black_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    white_options = check_options(white_pieces, white_locations,'white')
                    black_options = check_options(black_pieces,black_locations,'black')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    
    pygame.display.flip()
pygame.quit()
'''
# Main game loop
white_options = check_options(white_pieces, white_locations, 'white')
black_options = check_options(black_pieces, black_locations, 'black')
run = True
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flipped = not flipped

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            if flipped:
                x_coord = 7 - x_coord
                y_coord = 7 - y_coord
            click_coords = (x_coord, y_coord)

            if turn_step <= 1:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                elif click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            else:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                elif click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    white_options = check_options(white_pieces, white_locations, 'white')
                    black_options = check_options(black_pieces, black_locations, 'black')
                    turn_step = 0
                    selection = 100
                    valid_moves = []

    pygame.display.flip()

pygame.quit()
