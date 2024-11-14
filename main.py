import pygame
import sys
import random
import math
import time
 
pygame.init()

# Set up the display
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")
 
# Load images 
player_bird_image = pygame.image.load("Images/player_bird.png")
enemy_bird_image1 = pygame.image.load("Images/enemy_bird.png")
enemy_bird_image2 = pygame.image.load("Images/enemy_bird2.png")
enemy_bird_image3 = pygame.image.load("Images/enemy_bird3.png")
enemy_bird_image4 = pygame.image.load("Images/enemy_bird4.png")
enemy_bird_image5 = pygame.image.load("Images/enemy_bird5.png")

background_image = pygame.image.load("Images/background1.png")
background_image2 = pygame.image.load("Images/background2.png")
background_image3 = pygame.image.load("Images/background3.png")
background_image4 = pygame.image.load("Images/background4.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
sling_image = pygame.image.load("Images/shooter.png")
heart_image = pygame.image.load("Images/red_heart.png")
 
# Define the Bird class
class Bird(pygame.sprite.Sprite):
    # Initialize the Bird class
    def __init__(self, x, y, image, drag_limit=100):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]  # [horizontal_velocity, vertical_velocity]
        self.dragging = False
        self.drag_start_pos = (0, 0)
        self.drag_limit = drag_limit
        self.gravity = 0.1  
        self.is_launched = False  
    
    # Update the Bird position based on the dragging and launching
    def update(self):
        if self.dragging:
           
            mouse_pos = pygame.mouse.get_pos()
            drag_distance = math.sqrt((mouse_pos[0] - self.drag_start_pos[0]) ** 2 +
                                       (mouse_pos[1] - self.drag_start_pos[1]) ** 2)
           
            if drag_distance > self.drag_limit:
                direction = math.atan2(mouse_pos[1] - self.drag_start_pos[1],
                                        mouse_pos[0] - self.drag_start_pos[0])
                self.rect.centerx = self.drag_start_pos[0] + self.drag_limit * math.cos(direction)
                self.rect.centery = self.drag_start_pos[1] + self.drag_limit * math.sin(direction)
            else:
               
                self.rect.centerx = mouse_pos[0]
                self.rect.centery = mouse_pos[1]
 
        else:
           
            if self.is_launched:
                self.velocity[1] += self.gravity  
                self.rect.x += self.velocity[0]
                self.rect.y += self.velocity[1]
    
    def start_drag(self):
        self.dragging = True
        self.drag_start_pos = self.rect.center
 
    def end_drag(self):
        self.dragging = False
        mouse_pos = pygame.mouse.get_pos()
        direction = math.atan2(self.drag_start_pos[1] - mouse_pos[1],
                                self.drag_start_pos[0] - mouse_pos[0])
        speed = 12  
        self.velocity = [speed * math.cos(direction), speed * math.sin(direction)]
        self.is_launched = True
        pygame.mixer.music.load("sounds/sounds_swoosh.wav")  # Replace "path_to_music_file.mp3" with the actual path to your music file
        pygame.mixer.music.play(0)  # Play the music once
    
    def hit_enemy(self):
        global score
        score += 100  # Increase the score by 100
         
# Define the Button class 
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action
       
        self.hovered = False
 
    def update(self, mouse_pos):
        # Check if the mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
 
 
    def draw(self, screen):
        if self.hovered:
           enlarged_image = pygame.transform.scale(self.image, (160, 113))  # Increase the size of the image
           enlarged_rect = enlarged_image.get_rect(center=self.rect.center)  # Center the enlarged image
           screen.blit(enlarged_image, enlarged_rect)
        else:
            screen.blit(self.image, self.rect)
 
# Define the homepage of the game 
def homepage():
 
    home_image = pygame.image.load("Images/homepage2.png")
    play_button_image = pygame.image.load("Images/play.png")
   
    play_button = Button(565, 490, play_button_image, "play")
    
    pygame.mixer.music.load("sounds/sounds_bg.mp3") 
    pygame.mixer.music.play(-1)  # Set -1 to loop the music indefinitely

    # Set up the game loop
    while True: 
        screen.blit(home_image, (0, 0))
        screen.blit(play_button.image, play_button.rect)
        
        mouse_pos = pygame.mouse.get_pos()
        play_button.update(mouse_pos)
        play_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.MOUSEBUTTONUP:
                if play_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    mainloop()
 
        pygame.display.flip()
 
# Define the levels of the game
levels = [
    {"num_enemies": 5, "enemy_images": [enemy_bird_image1, enemy_bird_image3], "lvl_score": 100,"background_image":background_image},
    {"num_enemies": 7, "enemy_images": [enemy_bird_image1, enemy_bird_image2, enemy_bird_image3, enemy_bird_image4], "lvl_score": 100,"background_image":background_image2},
    {"num_enemies": 10, "enemy_images": [enemy_bird_image1, enemy_bird_image2, enemy_bird_image3, enemy_bird_image4, enemy_bird_image5], "lvl_score": 100,"background_image":background_image4},]

def load_level(level_index):
   
    print("Level_index while loading: ", level_index)
    level = levels[level_index]
    lscore=level["lvl_score"]
    background_image=level["background_image"]
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    enemy_birds = pygame.sprite.Group()
    for _ in range(level["num_enemies"]):
        x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        enemy_bird_image = random.choice(level["enemy_images"])
        enemy_bird = Bird(x, y, enemy_bird_image)
        enemy_birds.add(enemy_bird)
    return enemy_birds,background_image,lscore
 

def mainloop():
    button_margin = 10
    button_top = button_margin
    button_left = button_margin
    button_spacing = 5
   
    level_index = 0
    level = levels[level_index]
    max_levels = len(levels)
    global score
    score = 0
    score_position = (970, 10)
   
   
    quit_button_image = pygame.image.load("Images/quit_button.png")
    refresh_button_image = pygame.image.load("Images/refresh_button.png")
   
    quit_button = Button(button_left, button_top, quit_button_image, "quit")
    refresh_button = Button(button_left + quit_button_image.get_width() + button_spacing, button_top, refresh_button_image, "refresh")
   
    clock = pygame.time.Clock()
    try_again_counter = 0
    level_cleared = False
    game_over = False
   
    player_birds = [Bird(100, SCREEN_HEIGHT // 1.48, player_bird_image) for _ in range(4)]
    player_bird_index = 0
    player_bird = player_birds[player_bird_index]
    sling = Bird(100, SCREEN_HEIGHT // 1.3, sling_image)
   
    x=700
    y=20
    hearts = pygame.sprite.Group()
    for _ in range(4):
        x = x+40
        heart = Bird(x, y, heart_image)
        hearts.add(heart)
        
    enemy_birds,background_image,lscore = load_level(level_index)
    
    # Set up the game loop
    while True:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
   
                elif refresh_button.rect.collidepoint(event.pos):
                    player_birds = [Bird(100, SCREEN_HEIGHT // 1.48, player_bird_image) for _ in range(4)]
                    player_bird_index=0
                    player_bird=player_birds[player_bird_index]
                    level = levels[level_index]
                    enemy_birds.empty() 
                    enemy_birds,background_image,lscore = load_level(level_index)
                    
                    hearts = pygame.sprite.Group()
                    x=700
                    y=20
                    for _ in range(4):
                      x = x+40
                      heart = Bird(x, y, heart_image)
                      hearts.add(heart)
   
                    # Reset flags
                    level_cleared = False
                    game_over = False
                    try_again_counter = 0
                    score = 0
               
                elif player_bird.rect.collidepoint(event.pos):
                    player_bird.start_drag()
   
            elif event.type == pygame.MOUSEBUTTONUP:
                if player_bird.dragging:
                    player_bird.end_drag()
               
                    if not hits:
                        try_again_counter += 1
               
                else:
                    break
   
        # Check for collisions
        hits = pygame.sprite.spritecollide(player_bird, enemy_birds, True)
   
        if hits:
            pygame.mixer.music.load("sounds/sounds_hit.wav")  # Replace "path_to_music_file.mp3" with the actual path to your music file
            pygame.mixer.music.play(0) 
            for hit_enemy in hits:
                # hit_enemy.hit_enemy()
                score += 100  
            
        # Check if the player bird is out of bounds
        if (player_bird.rect.left > SCREEN_WIDTH  or player_bird.rect.top > SCREEN_HEIGHT) and  level_cleared==False:
            if player_bird_index<=2:
                if hearts:
                    heart = hearts.sprites()[0]
                print(player_bird_index)
                player_bird.kill()             
                player_bird = None 
                heart.kill()
                heart=None
                player_bird_index+=1
                
                player_bird=player_birds[player_bird_index]
            else:
                if hearts:
                    heart = hearts.sprites()[0]
                    heart.kill()
                game_over = True
   
        # Check if the enemy birds are out of bounds
        for enemy_bird in enemy_birds:
            if enemy_bird.rect.right < 0:
                enemy_bird.rect.left = SCREEN_WIDTH
                enemy_bird.rect.top = random.randint(50, SCREEN_HEIGHT - 50)

        # Clear the screen and draw the background
        screen.blit(background_image, (0, 0))
      
        player_bird.update()
        screen.blit(player_bird.image, player_bird.rect)
        screen.blit(sling.image, sling.rect)
   
        # Update and draw enemy birds
        enemy_birds.update()
        enemy_birds.draw(screen)
        hearts.update()
        hearts.draw(screen)     
   
        # Display font
        font = pygame.font.Font(None, 50)
   
        # Score font
        score_font = pygame.font.Font(None, 36)
   
        # Draw and update player's score
        score_text = score_font.render(f"level {level_index+1}  Score: {score}", True, (200, 0, 0))
        screen.blit(score_text, score_position) # Display score at specified position
   
        # Draw buttons
        screen.blit(quit_button.image, quit_button.rect)
        screen.blit(refresh_button.image, refresh_button.rect)
   
   
        # Display "Level Cleared" if score is 500
        if score >= lscore and (player_bird.rect.left > SCREEN_WIDTH  or player_bird.rect.top > SCREEN_HEIGHT):
            print(level["lvl_score"])
            if level_index<2:
                level_cleared_text = font.render("LEVEL CLEARED", True, (0, 0, 0))
                text_rect = level_cleared_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(level_cleared_text, text_rect)
                pygame.display.flip()
                time.sleep(3)  # Delay for 5 seconds

            level_cleared = True # Update the level_cleared flag
            player_birds = None
            player_bird_index = 0
        
            # Load the next level
            if level_index<max_levels-1:
                level_index += 1
                enemy_birds,background_image,lscore = load_level(level_index)
                player_bird_index=0
                player_birds = [Bird(100, SCREEN_HEIGHT // 1.48, player_bird_image) for _ in range(4)]
                player_bird = player_birds[player_bird_index]
                hearts = pygame.sprite.Group()
                x=700
                y=20
                for _ in range(4):
                    x = x+40
                    heart = Bird(x, y, heart_image)
                    hearts.add(heart)
                score = 0
                level_cleared = False
                game_over = False
            
            else:
                pygame.mixer.music.load("sounds/sounds_won.mp3")  
                pygame.mixer.music.play(0)

                game_over_text = pygame.font.Font(None, 60).render("U WON!", True, (200, 0, 0))
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(game_over_text, text_rect)
                pygame.display.flip()
                time.sleep(3) 
                
        # Display "Game Over" if score is less than level score
        if score < level["lvl_score"]  and player_bird_index>=4 and level_cleared==False:  
            game_over = True
        
        if game_over:
            game_over_text = font.render("GAME OVER - REPLAY", True, (0, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
   
        pygame.display.flip()
        clock.tick(60)
   
    pygame.quit()
 
homepage()
 