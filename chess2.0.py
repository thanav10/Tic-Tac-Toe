import pygame
import random
import copy

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two Player Chess (Bot + Check Rules)')
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

captured_pieces_white = []  # black pieces captured by white
captured_pieces_black = []  # white pieces captured by black

turn_step = 0               # 0: white select, 1: white dest, 2: black select, 3: black dest
selection = 100             # sentinel for "no selection"
valid_moves = []
flipped = False

# Bots
ai_enabled = True           # press 'B' to toggle
ai_side = 'black'           # press 'W' to switch AI side
ai_think_ms = 150

#Images
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
piece_list = ['rook', 'queen', 'knight', 'bishop', 'king', 'pawn']

# Piece values for the bot
PIECE_VAL = {'pawn': 100, 'knight': 320, 'bishop': 330, 'rook': 500, 'queen': 900, 'king': 0}

# Drawing

def draw_board():
    # Board squares
    for row in range(8):
        for col in range(8):
            x = col
            y = row
            if flipped:
                x = 7 - col
                y = 7 - row
            color = 'light gray' if (row + col) % 2 == 0 else 'dark gray'
            pygame.draw.rect(screen, color, [x * 100, y * 100, 100, 100])

    # Panels
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'black', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'black', [800, 0, 200, HEIGHT], 5)

    # Status text
    status_text = [
        'White: select a piece',
        'White: select a destination',
        'Black: select a piece',
        'Black: select a destination'
    ]

    # Check indicator
    white_in_check = side_in_check_now('white')
    black_in_check = side_in_check_now('black')

    msg = status_text[turn_step]
    if (turn_step < 2 and white_in_check) or (turn_step >= 2 and black_in_check):
        msg += '  — CHECK!'

    screen.blit(big_font.render(msg, True, 'black'), (20, 820))

    # AI indicator / controls
    ai_label = f"AI: {'Off' if not ai_enabled else ai_side.title()}"
    screen.blit(font.render(ai_label, True, 'black'), (820, 820))

    # Grid lines
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

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

def draw_valid(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for x, y in moves:
        if flipped:
            x, y = 7 - x, 7 - y
        pygame.draw.circle(screen, color, (x * 100 + 50, y * 100 + 50), 5)

def draw_captured():
    for i, captured_piece in enumerate(captured_pieces_white):  # black pieces captured by white
        index = piece_list.index(captured_piece)
        screen.blit(black_images_small[index], (825, 5 + 50 * i))
    for i, captured_piece in enumerate(captured_pieces_black):  # white pieces captured by black
        index = piece_list.index(captured_piece)
        screen.blit(white_images_small[index], (925, 5 + 50 * i))


# Move generators 
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

def check_valid_moves():
    options_list = white_options if turn_step < 2 else black_options
    if 0 <= selection < len(options_list):
        return options_list[selection]
    return []

def check_rook(position, color):
    moves_list = []
    friends_list = white_locations if color == 'white' else black_locations
    enemies_list = black_locations if color == 'white' else white_locations
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in directions:
        chain = 1
        while True:
            nx, ny = position[0] + chain * dx, position[1] + chain * dy
            if 0 <= nx <= 7 and 0 <= ny <= 7 and (nx, ny) not in friends_list:
                moves_list.append((nx, ny))
                if (nx, ny) in enemies_list:
                    break
                chain += 1
            else:
                break
    return moves_list

def check_bishop(position, color):
    moves_list = []
    friends_list = white_locations if color == 'white' else black_locations
    enemies_list = black_locations if color == 'white' else white_locations
    for dx, dy in [(1, -1), (-1, -1), (1, 1), (-1, 1)]:
        chain = 1
        while True:
            nx, ny = position[0] + chain * dx, position[1] + chain * dy
            if 0 <= nx <= 7 and 0 <= ny <= 7 and (nx, ny) not in friends_list:
                moves_list.append((nx, ny))
                if (nx, ny) in enemies_list:
                    break
                chain += 1
            else:
                break
    return moves_list

def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if position[1] < 7 and (position[0], position[1] + 1) not in white_locations + black_locations:
            moves_list.append((position[0], position[1] + 1))
        if position[1] == 1 and (position[0], position[1] + 2) not in white_locations + black_locations and \
           (position[0], position[1] + 1) not in white_locations + black_locations:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if position[1] > 0 and (position[0], position[1] - 1) not in white_locations + black_locations:
            moves_list.append((position[0], position[1] - 1))
        if position[1] == 6 and (position[0], position[1] - 2) not in white_locations + black_locations and \
           (position[0], position[1] - 1) not in white_locations + black_locations:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def check_knight(position, color):
    moves_list = []
    friends_list = white_locations if color == 'white' else black_locations
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for dx, dy in targets:
        nx, ny = position[0] + dx, position[1] + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7 and (nx, ny) not in friends_list:
            moves_list.append((nx, ny))
    return moves_list

def check_king(position, color):
    moves_list = []
    friends_list = white_locations if color == 'white' else black_locations
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for dx, dy in targets:
        nx, ny = position[0] + dx, position[1] + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7 and (nx, ny) not in friends_list:
            moves_list.append((nx, ny))
    return moves_list

def check_queen(position, color):
    moves_list = check_bishop(position, color)
    moves_list += check_rook(position, color)
    return moves_list

# Check / legality helpers
def find_king(side, w_pieces, w_locs, b_pieces, b_locs):
    if side == 'white':
        idx = w_pieces.index('king')
        return w_locs[idx]
    else:
        idx = b_pieces.index('king')
        return b_locs[idx]

def gen_pawn_attacks(position, side):
    x, y = position
    atks = []
    if side == 'white':
        for dx in (-1, 1):
            nx, ny = x + dx, y + 1
            if 0 <= nx <= 7 and 0 <= ny <= 7:
                atks.append((nx, ny))
    else:
        for dx in (-1, 1):
            nx, ny = x + dx, y - 1
            if 0 <= nx <= 7 and 0 <= ny <= 7:
                atks.append((nx, ny))
    return atks

def gen_knight_attacks(position):
    x, y = position
    atks = []
    for dx, dy in [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:
            atks.append((nx, ny))
    return atks

def gen_king_attacks(position):
    x, y = position
    atks = []
    for dx, dy in [(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:
            atks.append((nx, ny))
    return atks

def gen_sliding_attacks(position, deltas, friends, enemies):
    x, y = position
    atks = []
    for dx, dy in deltas:
        chain = 1
        while True:
            nx, ny = x + chain*dx, y + chain*dy
            if not (0 <= nx <= 7 and 0 <= ny <= 7):
                break
            if (nx, ny) in friends:
                break
            atks.append((nx, ny))
            if (nx, ny) in enemies:
                break
            chain += 1
    return atks

def all_attacks_by(side, w_pieces, w_locs, b_pieces, b_locs):
    atks = set()
    if side == 'white':
        friends, enemies = set(w_locs), set(b_locs)
        for p, pos in zip(w_pieces, w_locs):
            if p == 'pawn':
                atks.update(gen_pawn_attacks(pos, 'white'))
            elif p == 'knight':
                atks.update(gen_knight_attacks(pos))
            elif p == 'king':
                atks.update(gen_king_attacks(pos))
            elif p == 'rook':
                atks.update(gen_sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)], friends, enemies))
            elif p == 'bishop':
                atks.update(gen_sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)], friends, enemies))
            elif p == 'queen':
                atks.update(gen_sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)], friends, enemies))
    else:
        friends, enemies = set(b_locs), set(w_locs)
        for p, pos in zip(b_pieces, b_locs):
            if p == 'pawn':
                atks.update(gen_pawn_attacks(pos, 'black'))
            elif p == 'knight':
                atks.update(gen_knight_attacks(pos))
            elif p == 'king':
                atks.update(gen_king_attacks(pos))
            elif p == 'rook':
                atks.update(gen_sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)], friends, enemies))
            elif p == 'bishop':
                atks.update(gen_sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)], friends, enemies))
            elif p == 'queen':
                atks.update(gen_sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)], friends, enemies))
    return atks

def is_in_check(side, w_pieces, w_locs, b_pieces, b_locs):
    king_sq = find_king(side, w_pieces, w_locs, b_pieces, b_locs)
    opp = 'black' if side == 'white' else 'white'
    opp_atks = all_attacks_by(opp, w_pieces, w_locs, b_pieces, b_locs)
    return king_sq in opp_atks

def simulate_apply(side, piece_index, dest, w_pieces, w_locs, b_pieces, b_locs):
    # Deep copy lists
    wP, wL = w_pieces[:], w_locs[:]
    bP, bL = b_pieces[:], b_locs[:]
    if side == 'white':
        if dest in bL:
            j = bL.index(dest)
            bP.pop(j)
            bL.pop(j)
        wL[piece_index] = dest
    else:
        if dest in wL:
            j = wL.index(dest)
            wP.pop(j)
            wL.pop(j)
        bL[piece_index] = dest
    return wP, wL, bP, bL

def filter_legal_options(side):
    global white_pieces, white_locations, black_pieces, black_locations
    raw = check_options(white_pieces if side=='white' else black_pieces,
                        white_locations if side=='white' else black_locations,
                        side)
    legal = []
    for i, moves in enumerate(raw):
        ok = []
        for dest in moves:
            wP, wL, bP, bL = simulate_apply(side, i, dest,
                                            white_pieces, white_locations,
                                            black_pieces, black_locations)
            if not is_in_check(side, wP, wL, bP, bL):
                ok.append(dest)
        legal.append(ok)
    return legal

def update_all_legal_options():
    global white_options, black_options
    white_options = filter_legal_options('white')
    black_options = filter_legal_options('black')

def side_in_check_now(side):
    return is_in_check(side, white_pieces, white_locations, black_pieces, black_locations)

# Helpers 
def handle_promotion(color):
    global white_pieces, black_pieces
    if color == 'white':
        for i, p in enumerate(white_pieces):
            if p == 'pawn' and white_locations[i][1] == 7:
                white_pieces[i] = 'queen'
    else:
        for i, p in enumerate(black_pieces):
            if p == 'pawn' and black_locations[i][1] == 0:
                black_pieces[i] = 'queen'

def apply_move(side, piece_index, dest):
    global white_pieces, white_locations, black_pieces, black_locations
    global captured_pieces_white, captured_pieces_black

    if side == 'white':
        # Move piece
        white_locations[piece_index] = dest
        # Capture?
        if dest in black_locations:
            j = black_locations.index(dest)
            captured_pieces_white.append(black_pieces[j])
            black_pieces.pop(j)
            black_locations.pop(j)
        handle_promotion('white')
    else:
        black_locations[piece_index] = dest
        if dest in white_locations:
            j = white_locations.index(dest)
            captured_pieces_black.append(white_pieces[j])
            white_pieces.pop(j)
            white_locations.pop(j)
        handle_promotion('black')


# The Bot (greedy + simple prefs) — now uses LEGAL moves only

def score_move_for(side, piece_name, start, dest):
    # capture value
    capture_bonus = 0
    if side == 'white':
        if dest in black_locations:
            cap_piece = black_pieces[black_locations.index(dest)]
            capture_bonus += PIECE_VAL[cap_piece] * 10
    else:
        if dest in white_locations:
            cap_piece = white_pieces[white_locations.index(dest)]
            capture_bonus += PIECE_VAL[cap_piece] * 10

    # center preference & pawn advancement
    center_bonus = 3 if dest in {(3,3),(3,4),(4,3),(4,4)} else 0
    adv_bonus = 0
    if piece_name == 'pawn':
        adv_bonus = (dest[1] if side=='white' else (7 - dest[1])) * 2
        if (side=='white' and dest[1]==7) or (side=='black' and dest[1]==0):
            capture_bonus += PIECE_VAL['queen'] * 10

    jitter = random.uniform(0, 1)
    return capture_bonus + center_bonus + adv_bonus + jitter

def ai_play(side='black'):
    """Make a move for the AI on 'white' or 'black' side (legal, check-aware)."""
    global turn_step, selection, valid_moves

    # Build legal options
    options = filter_legal_options(side)

    pieces = white_pieces if side == 'white' else black_pieces
    locs = white_locations if side == 'white' else black_locations

    best_score = -1e9
    candidates = []  # (piece_index, dest, score)

    for i, moves in enumerate(options):
        for dest in moves:
            s = score_move_for(side, pieces[i], locs[i], dest)
            if s > best_score - 1e-6:
                if s > best_score + 1e-6:
                    candidates = []
                    best_score = s
                candidates.append((i, dest, s))

    # no legal moves -> stalemate or checkmate; just pass turn
    if not candidates:
        turn_step = 2 if side == 'white' else 0
        return

    piece_index, dest, _ = random.choice(candidates)

    pygame.time.wait(ai_think_ms)
    apply_move(side, piece_index, dest)

    # refresh options and pass the turn
    update_all_legal_options()
    if side == 'white':
        turn_step = 2  # black to move
    else:
        turn_step = 0  # white to move

    selection = 100
    valid_moves = []


# Initialize LEGAL options

update_all_legal_options()


# Main game loop

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

    # If it's the AI's turn, let it play immediately
    if ai_enabled and ((ai_side == 'black' and turn_step == 2) or (ai_side == 'white' and turn_step == 0)):
        ai_play(ai_side)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flipped = not flipped
            if event.key == pygame.K_b:
                ai_enabled = not ai_enabled
            if event.key == pygame.K_w:
                ai_side = 'white' if ai_side == 'black' else 'black'

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            if flipped:
                x_coord = 7 - x_coord
                y_coord = 7 - y_coord
            click_coords = (x_coord, y_coord)

            # ---- White human move ----
            if (not ai_enabled or ai_side != 'white') and turn_step <= 1:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                elif click_coords in valid_moves and selection != 100:
                    # apply white move (already legal by construction)
                    apply_move('white', selection, click_coords)
                    update_all_legal_options()
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            # ---- Black human move ----
            elif (not ai_enabled or ai_side != 'black') and turn_step > 1:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                elif click_coords in valid_moves and selection != 100:
                    apply_move('black', selection, click_coords)
                    update_all_legal_options()
                    turn_step = 0
                    selection = 100
                    valid_moves = []

    pygame.display.flip()

pygame.quit()
