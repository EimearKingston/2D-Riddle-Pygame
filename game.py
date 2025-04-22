#PYGAME IMPLEMENTED PLAT-FORM CHARACTER, RIDDLE-BASED ADVENTURE GAME
"""TEAM PROJECT SPECIFICATION: -no web interfaces
                               -system should take some input upon which it acts
                               -system should generate some output"""

#IMPORT MODULES
import pygame 
from pygame.locals import *
from pygame.sprite import *

pygame.init() #initialize game
clock = pygame.time.Clock() #frame rate for game (allows game to run at same rate regardless of device)
fps = 60 #frames per second
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SOFTWARE PROJECT by Peace & Eimear")

#GAME VARIABLES
tile_size = 50 #50 pixels for tile size, screen -> 20*16 grid format
game_over = 0
main_menu = True
level = 1
max_levels = 4

#Define colors and font 
PINK = (255, 0, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
font = pygame.font.Font(None, 26)


#LOAD GAME IMAGES
bg_img = pygame.image.load('bg.jpg') #background image
bg_image = pygame.transform.scale(bg_img, (width, height))
start_img = pygame.image.load('start_button.png') #start button image
start_img = pygame.transform.scale(start_img, (150, 50))
restart_img = pygame.image.load('restart_button.png') #restart button image (for when the player loses)
restart_img = pygame.transform.scale(restart_img,(150,50))

#FUNCTION TO DISPLAY GAME INSTRUCTIONS
def display_instructions():
    instructions_text = font.render("Game Instructions:", True, PINK)
    instruction1 = font.render("- Use arrow keys to move.", True, PINK)
    instruction2 = font.render("- Press space to jump.", True, PINK)
    game_about = font.render("Run around to find the wizard, answer his riddles to move on to the next level", True, PINK)
    game_about2 = font.render("And watch out for the enemies!!!", True, PINK)

    screen.blit(instructions_text, (50, 50))
    screen.blit(instruction1, (50, 100))
    screen.blit(instruction2, (50, 150))
    screen.blit(game_about, (50, 200))
    screen.blit(game_about2, (50, 250))

#FUNCTION TO RESET LEVEL AFTER LEVEL COMPLETION
def reset_level(level):
    player.reset(100, height - 130)
    ghost_group.empty()
    lava_group.empty()
    wizard_group.empty()
    #level data and create world
    if level == 1:
        world = World(world_data)
    elif level == 2:
        world = World(world_data2)
    elif level == 3:
        world = World(world_data3)
    elif level == 4:
        world = World(world_data4)
    else:
        print("invalid level number")
    return world

class Button():
    def __init__(self, x, y, image):
        """Initializes buttons used in the game"""
        self.image = image
        self.rect = self.image.get_rect() #create rect object of image
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        """function to draw the button onto the screen and handle mouse clicks
            returns True or False depending on whether the button is clicked or not
        """
        action = False #whether button has been clicked
        pos = pygame.mouse.get_pos() #get mouse position

        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            #check for click, left mouse click is at index 0 of get_pressed
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button to screen
        screen.blit(self.image, self.rect)
        return action

class World():
    def __init__(self, data:list):
        """used to initialize world tile data, in form of a list of tuples
            input: list of tile reference numbers in grid pattern
            output: list of world tile data as list of tuples
        """
        self.tile_list = []
        #load in images needed
        #CAN ADD MORE TILE BLOCKS TO DESIGN THE GAME SCREEN
        grass_img = pygame.image.load('grass.png') #assigned number: 1
        dirt_img = pygame.image.load('dirt.png')#Assigned number: 2

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_img,(tile_size, tile_size)) #scale image to fit tile size
                    img_rect = img.get_rect() #creates the pygame rect object of the image
                    #each tile position is dependent on tis row and column in the input data list
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)#store tile data
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(dirt_img,(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile) #store tile data
                if tile == 3:
                    wizard = Wizard(col_count * tile_size, row_count * tile_size - (tile_size //2))
                    wizard_group.add(wizard) # add to sprite group
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count* tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 5:
                    ghost = Enemy(col_count * tile_size, row_count* tile_size)
                    ghost_group.add(ghost)
                col_count += 1
            row_count += 1

    def draw(self):
        """used to draw the tiles onto the game screen, in the given grid pattern"""
        for tile in self.tile_list:
            #tile data stored as image in index 0, and rect data in index 1 of the tuple
            screen.blit(tile[0], tile[1])

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.images_right = []#images used to animate movement to the right
        self.images_left = []#images used to animate left
        self.index = 0#corresponds to images in list
        self.counter = 0 #speed at which images are changed for animation
        for num in range(1, 9):
            #load images, each num corresponds to image
            img_right = pygame.image.load(f'bunny{num}.png')
            img_right = pygame.transform.scale(img_right, (40,80))
            img_left = pygame.transform.flip(img_right, True, False)#true for x axis flip (opposite direction)
            self.images_right.append(img_right)#append images to list
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('death1.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (40,80))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()# create rect object
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0 #velocity in the y direction, for gradual jump
        self.jumped = False #can't hold the space bar for a long jump
        self.direction = 0 # direction 1->right, -1->left
        self.in_air = True
        self.textbox=None
    
    def jump(self, key):
        """JUMP, with gravity, can only jump once (jump if not already in air)"""
        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            #when space key is released
            self.jumped = False
        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        return self.vel_y
    
    def move(self, key, dx):
        """MOVE, left & right"""
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        #animation stops if keys not pressed
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        return dx
    
    def handle_animation(self):
        walk_cooldown = 5
        """handle ANIMATION of character"""
        if self.counter > walk_cooldown:
            self.counter = 0 #counter increases when arrow keys are pressed
            self.index += 1 #increase index
            #prevent index from going over the length of the list
            if self.index >= len(self.images_right):
                self.index = 0
            #check direction 
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
    
    def check_collision_with_tiles(self, dx, dy):
        """check for collision"""
        self.in_air = True
        for tile in world.tile_list:
            #check for collision in with tiles, x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0 #can't move further
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below ground ie. jumping and hit head on block
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above ground ie. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False #has landed onto something
        return dx, dy
    
    def update(self, game_over):
        """steps: find player position -> check for collision-> move player position"""
        """add player movement/ animation"""
        #values for player position change/ movement
        dx = 0
        dy = 0

        #game is active
        if game_over == 0:
            #get key presses, for player movement
            key = pygame.key.get_pressed()
            #CALL SEPARATE FUNCTIONS
            dy += self.jump(key)
            dx += self.move(key, dx)
            self.handle_animation()
            dx, dy = self.check_collision_with_tiles(dx, dy)
            
            riddles=["I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?", "The more you take, the more you leave behind. What am I?", "I can be cracked, made, told, and played. What am I?", "I have keys but no locks. I have space but no room. You can enter, but you can't go inside. What am I?"] 
            answers=[["Echo", "Whisper", "Thunder"], ["Time", "Memories", "Footsteps"], ["Code",  "Joke", "Puzzle"],["Keyboard", "Cloud", "Maze"]]
            
            """update player position"""
            self.rect.x += dx
            self.rect.y += dy

            """check for collision with lava"""
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1 #player has lost
            
            """check for collision with enemies"""
            if pygame.sprite.spritecollide(self, ghost_group, False):
                game_over = -1 #player has died

            """check for collision with wizard"""
            if pygame.sprite.spritecollide(self, wizard_group, False):
                if self.textbox is None or self.textbox.result: 
                    wizard_height = wizard_group.sprites()[0].rect.height  # Assuming there's only one wizard in the group
                    textbox_y = wizard_group.sprites()[0].rect.y - wizard_height - 30  # Adjust the value (-20) as needed 
                    textbox_width = 100  # Adjust the textbox width as needed
                    textbox_x = wizard_group.sprites()[0].rect.x - textbox_width // 2
 
                    textbox=TextBox(550, 30, 400, 70, riddles[level-1], answers[level-1])
                textbox.draw(screen) 
                textbox.display_options() 
                select=textbox.handle_event()
                if select=="Win":
                    game_over=1
                elif select == "Lose":
                    game_over = -1
                    textbox.result=""
                else:
                    # No option selected yet, continue the game
                    game_over = 0

        #GAME IS OVER/ NOT ACTIVE
        elif game_over == -1:
            self.image = self.dead_image
            self.image = pygame.transform.scale(self.dead_image, (40,50))
            if self.rect.y > 50:
                self.rect.y -= 5 

        """draw player unto screen"""
        self.draw()

        return game_over
    
    def draw(self):
        screen.blit(self.image, self.rect)

class Wizard(pygame.sprite.Sprite):
    #Sprites used in pygame to manage and manipulate graphical elements in a game
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #inherit from super class
        image = pygame.image.load('wizard.png')
        self.image = pygame.transform.scale(image, (70,90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call to inherit from super class
        image = pygame.image.load('lava.png')#need to find enemy image
        self.image = pygame.transform.scale(image,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call to inherit from super class
        image = pygame.image.load('ghost.png')#need to find enemy image
        self.image = pygame.transform.scale(image,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction #move to the right
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1 #change direction
            self.move_counter *= -1 #flip counter, opposite direction

class TextBox():
    def __init__(self, x, y, width, height, text, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = text
        self.read_only = True 
        self.visible=False 
        self.options=options
        self.option_rects = [] 
        self.button_clicked=False  
        option_x=550
        option_y=y+75
        option_width=100 
        option_height=40 
        if level==1:
            self.answer= options[0]
        elif level==2:
            self.answer= options[2]
        elif level==3: 
            self.answer= options[1] 
        elif level==4:
            self.answer= options[0]
        self.result=""
        for i, option in enumerate(options):
            rect = pygame.Rect(option_x+i*option_width+i, option_y, option_width, option_height)
            self.option_rects.append(rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Split the text into lines that fit within the width of the textbox
        lines = self.wrap_text(font, self.text, self.rect.width - 10)  # Adjust padding as needed

        # Render and draw each line
        y_offset = 5
        for line in lines:
            text_surface = font.render(line, True, BLACK)
            surface.blit(text_surface, (self.rect.x + 5, self.rect.y + y_offset))
            y_offset += text_surface.get_height() 
    
    def display_options(self):
        for i, rect in enumerate(self.option_rects): 
            
            pygame.draw.rect(screen, GRAY, rect) 
            pygame.draw.rect(screen, BLACK, rect, 3)
            # x_position = i * (150 + 10)
            text_surface = font.render(self.options[i], True, BLACK)
            screen.blit(text_surface, (rect.x + 10, rect.y+10))
    
    def wrap_text(self, font, text, max_width):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = current_line + [word]
            test_width, _ = font.size(' '.join(test_line))

            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))
        return lines 
    
    def handle_event(self):
        if pygame.mouse.get_pressed()[0] and not self.button_clicked:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(pygame.mouse.get_pos()):
                
                    pygame.draw.rect(screen, WHITE, rect)
                    text_surface = font.render(self.options[i], True, BLACK)
                    screen.blit(text_surface, (rect.x+10, rect.y+10))
                    if self.options[i]==self.answer:
                        self.result="Win"
                    else:
                        self.result="Lose"
                    print(f"Selected Option: {self.options[i]} - "+ self.result) 
                    self.button_clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.button_clicked = False
        return self.result
    
#WORLD DATA IN FORM OF LIST AND A REFERENCE NUMBER TO EACH IMAGE
# 1 -> grass image
# 2 -> dirt block image
# 3 -> wizard sprite character
# 4 -> lava image
# 5 -> ghost enemy image
world_data = [
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world_data2 = [
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2],
    [2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
world_data3 = [
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2],
    [2, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 2],
    [2, 0, 0, 0, 0, 0, 1, 1, 1, 4, 4, 4, 4, 4, 1, 1, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
world_data4 = [
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2],
    [2, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
    [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 2],
    [2, 0, 0, 0, 0, 1, 1, 1, 1, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

#create class instances
player = Player(100, height -130)
wizard_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
world = World(world_data)

#create buttons
start_button = Button((width // 2)-50, (height //2), start_img)
restart_button = Button((width // 2)-50, (height //2), restart_img)

#GAME LOOP
running = True
while running:
    clock.tick(fps) #set frame rate
    screen.blit(bg_image, (0,0)) #draw background image unto screen
    #draw game variables onto the screen
    #MAIN MENU SCREEN BEFORE GAME STARTS
    if main_menu == True:
        display_instructions() #display instructions to screen
        if start_button.draw(): #clicked
            main_menu = False
    #GAME SCREEN
    else:
        world.draw() #draw world image onto screen
        if game_over == 0:
            ghost_group.update()#continue enemy movement during the game
        wizard_group.draw(screen)
        lava_group.draw(screen)
        ghost_group.draw(screen)
        game_over = player.update(game_over) #update function returns game_over value

        if game_over == -1: #player has died
            if restart_button.draw(): #returns True or False
                player.reset(100, height - 130) #reset player
                game_over = 0 #no longer game over condition

        if game_over == 1:
            #player has completed level
            level += 1 #move to next level
            if level <= max_levels:
                #prevent the game from going on to undefined levels
                world = reset_level(level)
                game_over = 0 #reset game over variable
            else:
                #once all levels complete return to first level
                #may change this code to display a WIN SCREEN ONLY??
                text = font.render("YOU WIN!!, restart from level1?", True, PINK, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (width //2, 50)
                screen.blit(text, text_rect)
                if restart_button.draw():
                    level = 1
                    world = reset_level(level)
                    game_over = 0

    #EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
