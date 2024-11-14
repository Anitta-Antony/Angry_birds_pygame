################################### PHASE 1 ###############################

import pygame
import sys
import random
import math
 
pygame.init()
 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")
 
 
player_bird_image = pygame.image.load("Images/player_bird.png")
enemy_bird_image1 = pygame.image.load("Images/enemy_bird.png")
enemy_bird_image2 = pygame.image.load("Images/enemy_bird2.png")
enemy_bird_image3 = pygame.image.load("Images/enemy_bird3.png")
background_image = pygame.image.load("Images/background1.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
sling_image = pygame.image.load("Images/shooter.png")
heart_image = pygame.image.load("Images/red_heart.png")
 
 
class Bird(pygame.sprite.Sprite):
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
        # pygame.mixer.music.load("sounds/sounds_swoosh.wav")  # Replace "path_to_music_file.mp3" with the actual path to your music file
        # pygame.mixer.music.play(0)  # Play the music once
 
    def hit_enemy(self):
        global score
        score += 100  
        print(f"Enemy hit! Score: {score}")
         
 
 
 
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
 
 
 
 
 
def homepage():
 
    # clock = pygame.time.Clock()
    home_image = pygame.image.load("Images/homepage2.png")
    play_button_image = pygame.image.load("Images/play.png")
   
    play_button = Button(565, 490, play_button_image, "play")
    # pygame.mixer.music.load("sounds/sounds_bgmusic.mp3") 
    while True:  # Add a while loop to keep the function running until an event occurs
        screen.blit(home_image, (0, 0))
        screen.blit(play_button.image, play_button.rect)
         # Replace "path_to_music_file.mp3" with the actual path to your music file
        # pygame.mixer.music.play(0) 
        mouse_pos = pygame.mouse.get_pos()
        play_button.update(mouse_pos)
        play_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.MOUSEBUTTONUP:
                if play_button.rect.collidepoint(event.pos):
                    mainloop()
 
        pygame.display.flip()
        # clock.tick(60)
 
 
def mainloop():
    button_margin = 10
    button_top = button_margin
    button_left = button_margin
    button_spacing = 5
   
   
    score = 0
    score_position = (970, 10)
   
   
    quit_button_image = pygame.image.load("Images/quit_button.png")
    refresh_button_image = pygame.image.load("Images/refresh_button.png")
   
    quit_button = Button(button_left, button_top, quit_button_image, "quit")
    refresh_button = Button(button_left + quit_button_image.get_width() + button_spacing, button_top, refresh_button_image, "refresh")
   
    #game loop
    clock = pygame.time.Clock()
    try_again_counter = 0
    max_try_again = 3
    level_cleared = False
    game_over = False
    count=3
    refresh=False
   
    player_birds = [Bird(100, SCREEN_HEIGHT // 1.48, player_bird_image) for _ in range(4)]
    player_bird_index = 0
    player_bird = player_birds[player_bird_index]
    list = [enemy_bird_image3, enemy_bird_image1, enemy_bird_image2]
    sling = Bird(100, SCREEN_HEIGHT // 1.3, sling_image)
   
    x=700
    y=20
    hearts = pygame.sprite.Group()
    for _ in range(4):
        x = x+40
        heart = Bird(x, y, heart_image)
        hearts.add(heart)
        
    enemy_birds = pygame.sprite.Group()
    for _ in range(5):
        x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        enemy_bird_image = random.choice(list)
        enemy_bird = Bird(x, y, enemy_bird_image)
        enemy_birds.add(enemy_bird)
   
    while True:
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
                    
               
               
   
                    enemy_birds.empty()
                    for _ in range(5):
                        x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
                        y = random.randint(50, SCREEN_HEIGHT - 50)
                        enemy_bird_image = random.choice(list)
                        enemy_bird = Bird(x, y, enemy_bird_image)
                        enemy_birds.add(enemy_bird)
                        

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
   
   
   
        hits = pygame.sprite.spritecollide(player_bird, enemy_birds, True)
   
        if hits:
            # pygame.mixer.music.load("sounds/sounds_hit.wav")  # Replace "path_to_music_file.mp3" with the actual path to your music file
            # pygame.mixer.music.play(0) 
            for hit_enemy in hits:
                # hit_enemy.hit_enemy()
                score += 100  
                print(f"Enemy hit! Score: {score}")
 
   
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
        score_text = score_font.render(f"level 1 Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, score_position) # Display score at specified position
   
        # Draw buttons
        screen.blit(quit_button.image, quit_button.rect)
        screen.blit(refresh_button.image, refresh_button.rect)
   
   
    # Display "Level Cleared" if score is 500
        if score >= 500:
            level_cleared_text = font.render("LEVEL CLEARED", True, (0, 0, 0))
            text_rect = level_cleared_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(level_cleared_text, text_rect)
            level_cleared = True # Update the level_cleared flag
   
        
            
        if game_over:
            game_over_text = font.render("GAME OVER - REPLAY", True, (0, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
       
   
            # Update the game_over flag
   
        pygame.display.flip()
        clock.tick(60)
   
    pygame.quit()
 
homepage()
 