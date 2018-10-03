# Effects by Skorpio: https://opengameart.org/content/sci-fi-effects
# Projectile models by Tatermand: https://opengameart.org/content/2d-shooter-effects-alpha-version
# Music by Oblidivm: https://opengameart.org/content/space-shooter-music
# Background by Falcosun: https://opengameart.org/content/loopable-hd-nebulas

import pygame
import random
import time
import math
from os import path

# Image, sound, and stats directories
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
stats_dir = path.join(path.dirname(__file__), "stats")

# Screen resolution
WIDTH = 1366
HEIGHT = 768
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Font used in-game
font_name = pygame.font.match_font("arial")

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Displays text in-game
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Spawn a new asteroid
def new_ast():
    spawnx = random.randint(100, 1200)
    ast = Asteroid(spawnx, 0)
    all_sprites.add(ast)
    astGrp.add(ast)

# Display player health
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100 )* BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Display boss health
def draw_shield_bar_Boss(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 900 )* BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Display lives left
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

#Write hits taken by player to text file
def playerHits(value):
    with open(path.join(stats_dir, "hitstaken.txt"), 'w') as f:
        f.write(str(value))

# Allows rotation around center
def rotate(image, rect, angle):
    # Rotate the image while keeping its center.
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect

# Display blink's cooldown
def displayCD(self):
    draw_text(screen, str(15 - math.floor((pygame.time.get_ticks() - self.warptimer) / 1000)),
                46, 150, HEIGHT - 150)
    pygame.display.flip()

    if math.floor((pygame.time.get_ticks() - self.warptimer) / 1000) == 15:
        player.boolean = 0

#Display timer on asteroid field in boss stage 2
def asteroidFieldTimer(self):
    draw_text(screen, 'Survive for: ' + str(60 - math.floor((pygame.time.get_ticks() - self.asteroidsTimer) / 1000)) + ' Seconds',
        24, WIDTH / 2, 30)
    pygame.display.flip()

    # Stage 2 lasts 60 seconds
    if pygame.time.get_ticks() - self.asteroidsTimer > 60000:
        self.stage = 3
        self.state = 0

def mainMenu(value):
    # Move selection in main menu
    screen_show = value
    background_screen = ["Menu.png", "paused.png", "stats.png"]
    background = pygame.image.load(path.join(img_dir, background_screen[value])).convert_alpha()
    background = pygame.transform.scale(background, (1366, 768))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    if screen_show == 0 or screen_show == 1:
        draw_text(screen, "Press Enter to Select an Option", 18, WIDTH / 2, HEIGHT - 80)

    else:
        draw_text(screen, "Press Enter to Return to Main Menu", 18, WIDTH / 2, HEIGHT - 80)

    pygame.display.flip()

def end_game(value):
    # Show end game screen
    background_screen = "Loading.png"
    background = pygame.image.load(path.join(img_dir, "Loading.png")).convert_alpha()
    background = pygame.transform.scale(background, (1366, 768))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    if value == 0:
        draw_text(screen, "Press Enter to Continue", 18, WIDTH / 2, HEIGHT - 80)
        draw_text(screen, "You beat the game in:", 36, WIDTH / 2, HEIGHT / 2)

        ending = round((pygame.time.get_ticks() - start_timer) / 1000, 1)
        draw_text(screen, str(ending) + " seconds", 36, WIDTH / 2, HEIGHT / 2 + 40)

        with open(path.join(stats_dir, "timer.txt"), 'r+') as f:
            try:
                end_timer = float(f.read())
            except:
                end_timer = "N/A"

        if end_timer == "N/A":
            end_timer = float(ending)
            with open(path.join(stats_dir, "timer.txt"), 'w') as f:
                f.write(str(end_timer))

        elif float(ending) < end_timer:
            end_timer = float(ending)
            with open(path.join(stats_dir, "timer.txt"), 'w') as f:
                f.write(str(end_timer))

        draw_text(screen, "Your best time is: " + str(end_timer) + " seconds", 36, WIDTH / 2, HEIGHT / 2 + 120)

        pygame.display.flip()

        with open(path.join(stats_dir, "completions.txt"), 'r+') as f:
            try:
                com = int(f.read())
            except:
                com = 0
        com += 1
        with open(path.join(stats_dir, "completions.txt"), 'w') as f:
            f.write(str(com))


    else:
        draw_text(screen, "Press Enter to Continue", 18, WIDTH / 2, HEIGHT - 80)
        draw_text(screen, "Game Over", 36, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def show_go_screen():
    # Main menu
    mainMenu(0)

    pygame.mixer.music.load(path.join(snd_dir, "Skyfire (Title Screen).ogg"))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)

    screen.blit(select_img, (213, HEIGHT / 2 - 100 ))
    pygame.display.flip()
    boolean = 0
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keystate = pygame.key.get_pressed()

            if boolean == 0:
                mainMenu(0)
                screen.blit(select_img, (213, HEIGHT / 2 - 100))
                pygame.display.flip()

            if boolean == 1:
                mainMenu(0)
                screen.blit(select_img, (304, HEIGHT / 2 + 25))
                pygame.display.flip()

            if boolean == 2:
                mainMenu(0)
                screen.blit(select_img, (391, HEIGHT / 2 + 157))
                pygame.display.flip()

            if keystate[pygame.K_RETURN] and boolean == 0:
                waiting = False

            if keystate[pygame.K_RETURN] and boolean == 1:
                stats()

            if keystate[pygame.K_RETURN] and boolean == 2:
                pygame.quit()

            if keystate[pygame.K_DOWN] and boolean == 0:
                boolean = 1

            elif keystate[pygame.K_DOWN] and boolean == 1:
                boolean = 2

            if keystate[pygame.K_UP] and boolean == 1:
                boolean = 0

            elif keystate[pygame.K_UP] and boolean == 2:
                boolean = 1

def lose_live():
    player_die_sound.play()
    death_explosion = Explosion(player.rect.center, 'player')
    all_sprites.add(death_explosion)
    player.hide()
    player.lives -= 1
    player.shield = 100
    player.immune = 1

def loadingScreen():
    # Loading screen window
    screen.fill(BLACK)
    background = pygame.image.load(path.join(img_dir, "Loading.png")).convert_alpha()
    background = pygame.transform.scale(background, (1366, 768))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    draw_text(screen, "WASD or Arrow Keys to Move, Spacebar to Shoot, C to Blink", 24, WIDTH / 2, HEIGHT / 2 + 170)
    pygame.display.flip()
    waiting = True
    timer = pygame.time.get_ticks()
    frame = 0
    image = loadBar[frame]
    while waiting:
        if pygame.time.get_ticks() - timer > 200:
            timer = pygame.time.get_ticks()
            image = loadBar[frame]
            frame += 1
            screen.blit(loadBar[frame], (WIDTH / 2 - 230, 530))
            pygame.display.flip()

        if frame == 20:
            waiting = False

def stats():
    # Pause screen
    mainMenu(2)

    pygame.display.flip()
    paused = True

    while paused:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            with open(path.join(stats_dir, "shotsfired.txt"), 'r+') as f:
                try:
                    shots = f.read()
                except:
                    shots = 0

            with open(path.join(stats_dir, "timer.txt"), 'r+') as f:
                try:
                    end_timer = f.read()
                except:
                    end_timer = "N/A"

            with open(path.join(stats_dir, "powersused.txt"), 'r+') as f:
                try:
                    powers = f.read()
                except:
                    powers = 0

            with open(path.join(stats_dir, "hitstaken.txt"), 'r+') as f:
                try:
                    hits_taken = f.read()
                except:
                    hits_taken = 0

            with open(path.join(stats_dir, "attempts.txt"), 'r+') as f:
                try:
                    att = f.read()
                except:
                    att = 0

            with open(path.join(stats_dir, "completions.txt"), 'r+') as f:
                try:
                    com = f.read()
                except:
                    com = 0

            draw_text(screen, "Shots Fired: " + str(shots), 26, WIDTH / 3, HEIGHT / 2 - 50)
            draw_text(screen, "Powerups Used: " + str(powers), 26, WIDTH / 3, HEIGHT / 2 - 100)
            draw_text(screen, "Hits Taken: " + str(hits_taken), 26, WIDTH / 3 * 2, HEIGHT / 2 - 100)
            draw_text(screen, "Fastest Time: " + str(end_timer) + " seconds", 26, WIDTH / 3 * 2, HEIGHT / 2 - 50)
            draw_text(screen, "Number of Attempts: " + str(att), 26, WIDTH / 3, HEIGHT / 2)
            draw_text(screen, "Number of Completions: " + str(com), 26, WIDTH / 3 * 2, HEIGHT / 2)

            pygame.display.flip()

            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_ESCAPE] or keystate[pygame.K_RETURN]:
                paused = False

def pause():
    # Pause screen
    mainMenu(1)

    screen.blit(select_img, (246, HEIGHT / 2 - 59))
    pygame.display.flip()
    boolean = 0
    paused = True

    while paused:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keystate = pygame.key.get_pressed()

            if boolean == 0:
                mainMenu(1)
                screen.blit(select_img, (246, HEIGHT / 2 - 59))
                pygame.display.flip()

            if boolean == 1:
                mainMenu(1)
                screen.blit(select_img, (306, HEIGHT / 2 + 119))
                pygame.display.flip()

            if keystate[pygame.K_RETURN] and boolean == 0:
                paused = False

            if keystate[pygame.K_RETURN] and boolean == 1:
                pygame.quit()

            if keystate[pygame.K_DOWN]:
                boolean = 1

            if keystate[pygame.K_UP]:
                boolean = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(self.image, (55, 60))
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 100
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        self.posX = WIDTH / 2
        self.posY = self.rect.centery
        self.move = True
        self.warptimer = pygame.time.get_ticks()
        self.state = 0
        self.cooldown = False
        self.CDtimer = pygame.time.get_ticks()
        self.nowImmune = pygame.time.get_ticks()
        self.boolean = 0
        self.immune = 0
        self.load_data()

    def load_data(self):
        with open(path.join(stats_dir, "shotsfired.txt"), 'r+') as f:
            try:
                self.shots = int(f.read())
            except:
                self.shots = 0

    def Power(self):
        self.power = 2
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        if self.immune == 1:
            self.immune = 2
            self.nowImmune = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.nowImmune > 2500:
            self.immune = 0

        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = HEIGHT - 100
            self.posX = WIDTH / 2
            self.posY = player.rect.y
            self.hidden = False

        if pygame.time.get_ticks() - self.warptimer > 15000:
            self.cooldown = False

        if self.move == False and pygame.time.get_ticks() - self.warptimer > 300:
            if self.state == 1:
                self.rect.center = (self.posX - 330, self.posY)
                self.posX = self.posX -330
                self.posY = self.posY

            if self.state == 2:
                self.rect.center = (self.posX + 330, self.posY)
                self.posX = self.posX + 330
                self.posY = self.posY

            if self.state == 3:
                self.rect.center = (self.posX, self.posY - 330)
                self.posX = self.posX
                self.posY = self.posY - 330

            if self.state == 4:
                self.rect.center = (self.posX, self.posY + 330)
                self.posX = self.posX
                self.posY = self.posY + 330

            warp = Warp(self.rect.centerx, self.rect.centery)
            all_sprites.add(warp)
            self.move = True
            self.state = 0

        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and self.move == True:
            self.speedx = -5
            self.posX -= 5
            if keystate[pygame.K_c] and self.cooldown == False:
                self.getRect = self.rect.center
                self.state = 1
                self.warpPlayer()

        if (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and self.move == True:
            self.speedx = 5
            self.posX += 5
            if keystate[pygame.K_c] and self.cooldown == False:
                self.getRect = self.rect.center
                self.state = 2
                self.warpPlayer()

        if (keystate[pygame.K_UP] or keystate[pygame.K_w]) and self.move == True:
            self.speedy = -5
            self.posY -= 5
            if keystate[pygame.K_c] and self.cooldown == False:
                self.getRect = self.rect.center
                self.state = 3
                self.warpPlayer()

        if (keystate[pygame.K_DOWN] or keystate[pygame.K_s]) and self.move == True:
            self.speedy = 5
            self.posY += 5
            if keystate[pygame.K_c] and self.cooldown == False:
                self.getRect = self.rect.center
                self.state = 4
                self.warpPlayer()

        elif keystate[pygame.K_c] and self.cooldown == False:
            self.getRect = self.rect.center
            self.state = 3
            self.warpPlayer()

        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH and self.hidden == False and self.move == True:
            self.rect.right = WIDTH
            self.posX = WIDTH - 35

        if self.rect.left < 0 and self.hidden == False and self.move == True:
            self.rect.left = 0
            self.posX = 35

        if self.rect.top < 0 and self.hidden == False and self.move == True:
            self.rect.top = 0
            self.posY = 60

        if self.rect.bottom > HEIGHT and self.hidden == False and self.move == True:
            self.rect.bottom = HEIGHT
            self.posY = HEIGHT - 60

        self.mask = pygame.mask.from_surface(self.image)


    def shoot(self):
        if self.power == 2:
            bullet = [Bullet(self.rect.right, self.rect.centery, -10, 0, 0), Bullet(self.rect.left + 1, self.rect.centery, -10, 0, 0)]
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                self.shots += 2
                with open(path.join(stats_dir, "shotsfired.txt"), 'w') as f:
                    f.write(str(self.shots))

            if pygame.time.get_ticks() - self.power_timer > 5000:
                self.power = 1

        else:
            bullet = [Bullet(self.rect.centerx + 1, self.rect.top, -10, 0, 0)]
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                self.shots += 1
                with open(path.join(stats_dir, "shotsfired.txt"), 'w') as f:
                    f.write(str(self.shots))

    def hide(self):
        # Hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (-1000, -1000)

    def warpPlayer(self):
        self.move = False
        self.warptimer = pygame.time.get_ticks()
        self.CDtimer = pygame.time.get_ticks()
        warp = Warp(self.rect.centerx, self.rect.centery)
        all_sprites.add(warp)
        self.rect.center = (-1000, -1000)
        self.cooldown = True
        self.boolean = 1
        anim = CooldownWarp(150, HEIGHT - 130)
        all_sprites.add(anim)

class CooldownWarp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = cdAnim[0]
        self.rect = self.image.get_rect()
        self.timer = pygame.time.get_ticks()
        self.frame = 1
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        if pygame.time.get_ticks() - self.timer > 50:
            self.timer = pygame.time.get_ticks()
            self.image = cdAnim[self.frame]
            self.frame += 1

        if self.frame == 29:
            self.frame = 0

        if player.boolean == 0:
            self.kill()

class Warp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = warpAnim[0]
        self.rect = self.image.get_rect()
        self.timer = pygame.time.get_ticks()
        self.frame = 0
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        if pygame.time.get_ticks() - self.timer > 50:
            self.timer = pygame.time.get_ticks()
            self.frame += 1
            self.image = warpAnim[self.frame]

        if self.frame == 7:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, speedx, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img[color]
        self.image = pygame.transform.scale(laser_img[color], (35, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy
        self.speedx = speedx

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Kill it if it moves off the top or bottom of the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)

class BulletOrig(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        pygame.sprite.Sprite.__init__(self)
        self.image = Origin[kind]
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer > 250:
            self.kill()

        self.speedx = 0

        if boss.state == 0:
            if player.rect.centerx > boss.rect.centerx:
                self.speedx += 3
                self.rect.centerx += self.speedx

            if player.rect.centerx < boss.rect.centerx:
                self.speedx -= 3
                self.rect.centerx += self.speedx

            if player.rect.centerx == boss.rect.centerx:
                self.speedx = 0
                self.rect.centerx += self.speedx

        if boss.state == 1 or boss.state == 2:
            if boss.rect.centerx < WIDTH / 2:
                self.speedx += 3
                self.rect.centerx += self.speedx

            if boss.rect.centerx > WIDTH / 2:
                self.speedx -= 3
                self.rect.centerx += self.speedx

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 70

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()

            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, randomize):
        pygame.sprite.Sprite.__init__(self)
        #self.type = random.choice(pu_img[0], pu_imgb[0])
        self.type = randomize
        self.image = self.type[0]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centery = -20
        self.rect.centerx = random.randint(200, 1100)
        self.speedy = 3
        self.timer = pygame.time.get_ticks()
        self.counter = 1

    def update(self):
        self.rect.y += self.speedy

        if pygame.time.get_ticks() - self.timer > 50:
            self.timer = pygame.time.get_ticks()
            self.counter += 1
            if self.counter == 6:
                self.counter = 0
            else:
                center = self.rect.center
                self.image = self.type[self.counter]
                self.rect = self.image.get_rect()
                self.rect.center = center

        # Kill it if it moves out of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class BG(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = backgrounds[number]
        self.image = pygame.transform.scale(self.image, (1366, 768))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        self.rect.y += 1

        # Enables background image loop
        if self.rect.top > HEIGHT:
            self.rect.top = -768

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = miss_img
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (65, 95))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.step = 0

    def update(self):
        self.speedy = 8
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.kill()

        self.rect.centerx += math.sin(self.step) * 3 + 0.4
        self.step += 0.2

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, spin):
        pygame.sprite.Sprite.__init__(self)
        self.turn = direction
        self.image = pygame.transform.rotate(radar_img, self.turn)
        self.oldimg = self.image
        self.rect = self.image.get_rect()
        self.oldrect = self.rect
        self.rect.centerx = x
        self.rect.centery = y
        self.timer = pygame.time.get_ticks()
        self.start = pygame.time.get_ticks()
        self.spinning = spin
        self.degree = 0
        self.end = False

    def update(self):
        laser_sound.play()
        # Timer to begin rotating
        if pygame.time.get_ticks() - self.start > 1250:
            if pygame.time.get_ticks() - self.timer > 10:
                self.timer = pygame.time.get_ticks()
                self.image, self.rect = rotate(self.oldimg, self.oldrect, self.degree)
                self.degree += self.spinning

            if self.degree >= 90 or self.degree <= -90:
                self.kill()

            self.rect.centerx += 1

            self.mask = pygame.mask.from_surface(self.image)

class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ellipse_img
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.oldimg = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.degree = 0
        self.timer = pygame.time.get_ticks()
        self.speedx = random.randint(-6, 6)
        self.speedy = random.randint(5, 13)

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        if pygame.time.get_ticks() - self.timer > 10:
            self.timer = pygame.time.get_ticks()
            self.image, self.rect = rotate(self.oldimg, self.rect, self.degree)
            self.degree += 1

        if self.degree == 360:
            self.degree = 0

        if self.rect.top > HEIGHT:
            self.kill

class Vortex(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = vortex_img
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.rect = self.image.get_rect()
        self.oldimg = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.degree = 0
        self.timer = pygame.time.get_ticks()
        self.end = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer > 10:
            self.timer = pygame.time.get_ticks()
            self.image, self.rect = rotate(self.oldimg, self.rect, self.degree)
            self.degree += 1

        if self.degree == 360:
            self.degree = 0

        if pygame.time.get_ticks() - self.end > 1200:
            for n in range(8):
                ell = Ellipse(self.rect.centerx, self.rect.centery)
                all_sprites.add(ell)
                ellipseGrp.add(ell)

            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_img
        self.scale = random.randint(80, 280)
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.radius = self.scale / 2
        self.oldimg = self.image
        self.rect = self.image.get_rect()
        self.oldrect = self.rect
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 0
        self.degree = 0
        self.timer = pygame.time.get_ticks()
        self.speed = random.randint(4, 8)

    def update(self):
        self.speedy = self.speed
        self.rect.centery += self.speedy

        if self.rect.top > HEIGHT and boss.stage == 2:
            self.kill()
            new_ast()

        if pygame.time.get_ticks() - self.timer > 10:
            self.timer = pygame.time.get_ticks()
            self.image, self.rect = rotate(self.oldimg, self.rect, self.degree)
            self.degree += 1

        if self.degree == 360:
            self.degree = 0

        self.mask = pygame.mask.from_surface(self.image)

class Special(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = specialImg[0]
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.frame = 1
        self.timer = pygame.time.get_ticks()
        self.rect.centerx = x
        self.rect.centery = y
        self.shootTimer = pygame.time.get_ticks()
        self.count = 0

    def update(self):
        player1 = Player()

        if pygame.time.get_ticks() - self.timer > 50:
            self.timer = pygame.time.get_ticks()
            self.image = specialImg[self.frame]
            self.image = pygame.transform.scale(self.image, (90, 90))
            self.frame += 1

        if self.frame == 19:
            self.frame = 0

        # Shoots fireball aimed at player's position
        if pygame.time.get_ticks() - self.shootTimer > 1000:
            self.shootTimer = pygame.time.get_ticks()

            locX = player.posX - self.rect.centerx
            locY = player.posY - self.rect.centery
            if locY >= locX:
                if locX == 0:
                    locX = 0.001

                ratio1 = locY / locX
                ratio2 = locX / locY

                if ratio2 > ratio1 and ratio1 >= 0:
                    ratio2 = ratio1

                elif ratio2 < ratio1 and ratio1 < 0:
                    ratio1 = ratio1

                fire = Fireball(self.rect.centerx, self.rect.centery, 15, ratio2 * 15, math.degrees(math.atan(locX / locY)))
                specials_sound.play()
                self.count += 1

            if locX < 0 and abs(locX) >= locY:
                if locX == 0:
                    locX = 0.001

                ratio1 = locY / locX
                ratio2 = locX / locY

                if ratio2 > ratio1 and ratio1 >= 0:
                    ratio2 = ratio2

                elif ratio2 < ratio1 and ratio1 < 0:
                    ratio1 = ratio1

                if locY < 0:
                    angle = math.degrees(math.atan(locX / locY)) + 180

                else:
                    angle = math.degrees(math.atan(locX / locY))

                fire = Fireball(self.rect.centerx, self.rect.centery, -ratio1 * 15, -15, angle)
                specials_sound.play()
                self.count += 1

            if locX > locY:
                if locY == 0:
                    locY = 0.001

                ratio1 = locX / locY
                ratio2 = locY / locX

                if ratio2 > ratio1 and ratio1 >= 0:
                    ratio2 = ratio2

                elif ratio2 < ratio1 and ratio1 < 0:
                    ratio1 = ratio2

                if locY < 0:
                    angle = math.degrees(math.atan(locX / locY)) + 180

                else:
                    angle = math.degrees(math.atan(locX / locY))

                fire = Fireball(self.rect.centerx, self.rect.centery, ratio2 * 15, 15, angle)
                specials_sound.play()
                self.count += 1

            all_sprites.add(fire)
            specialsGrp.add(fire)

            if self.count == 10:
                self.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, speedx, rot):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(fireball_img, 180)
        self.image = pygame.transform.scale(self.image, (70, 150))
        self.image = pygame.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Kill it if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = 150
        self.shield = 3
        self.shootTimer = pygame.time.get_ticks()
        self.missTimer = pygame.time.get_ticks()
        self.laserTimer = pygame.time.get_ticks()
        self.specialTimer = pygame.time.get_ticks()
        self.state = 0
        self.posX = self.rect.centerx
        self.stateTimer = pygame.time.get_ticks()
        self.speedy = 0
        self.stage = 3
        self.beginTimer = False
        self.asteroidsTimer = 0

    def update(self):
        if self.stage == 1:
            if self.state == 3 and pygame.time.get_ticks() - self.timer1 > 3000:
                self.stateTimer = pygame.time.get_ticks()
                self.state = 0

            if self.state == 4 and pygame.time.get_ticks() - self.timer1 > 14500:
                self.stateTimer = pygame.time.get_ticks()
                self.state = 0

            if self.state == 0:
                if pygame.time.get_ticks() - self.stateTimer > 15000 and self.shield > 500:
                    self.stateTimer = pygame.time.get_ticks()
                    self.state = random.randint(1, 2)

                self.speedx = 0

                self.posX = self.rect.centerx

                # Move Boss to match Player's X-axis
                if player.rect.centerx > self.rect.centerx:
                    self.speedx += 3
                    self.rect.centerx += self.speedx

                if player.rect.centerx < self.rect.centerx:
                    self.speedx -= 3
                    self.rect.centerx += self.speedx

                if player.rect.centerx == self.rect.centerx:
                    self.speedx = 0
                    self.rect.centerx += self.speedx

                if pygame.time.get_ticks() - self.shootTimer > 1500:
                    self.shootTimer = pygame.time.get_ticks()
                    bullet1 = [Bullet(self.rect.centerx, self.rect.centery + 30, 12, 0, 1),
                                Bullet(self.rect.centerx + 45, self.rect.centery + 80, 12, 0, 1),
                                Bullet(self.rect.centerx - 42, self.rect.centery + 80, 12, 0, 1)]

                    splash1 = [BulletOrig(self.rect.centerx + 1, self.rect.centery + 20, 1),
                                BulletOrig(self.rect.centerx + 45, self.rect.centery + 60, 1),
                                BulletOrig(self.rect.centerx - 42, self.rect.centery + 60, 1)]

                    all_sprites.add(bullet1)
                    all_sprites.add(splash1)
                    bullets1.add(bullet1)
                    shoot_soundBoss.play()

                if pygame.time.get_ticks() - self.missTimer > 2500:
                    self.missTimer = pygame.time.get_ticks()
                    miss = [Missile(self.rect.left + 20, self.rect.centery + 9),
                            Missile(self.rect.right - 23, self.rect.centery + 9)]

                    splash2 = [BulletOrig(self.rect.left + 23, self.rect.centery + 100, 0),
                                BulletOrig(self.rect.right - 22, self.rect.centery + 100, 0)]

                    all_sprites.add(miss)
                    all_sprites.add(splash2)
                    missileGrp.add(miss)
                    shoot_soundMiss.play()

            if self.state == 1:
                if self.posX < WIDTH / 2:
                    self.speedx = 3
                    self.rect.centerx += self.speedx
                    if self.rect.centerx >= WIDTH / 2:
                        self.speedx = 0
                        self.rect.centerx = WIDTH / 2

                if self.posX > WIDTH / 2:
                    self.speedx = 3
                    self.rect.centerx -= self.speedx
                    if self.rect.centerx <= WIDTH / 2:
                        self.speedx = 0
                        self.rect.centerx = WIDTH / 2

                if self.rect.centerx == WIDTH / 2:
                    # self.state = 3 disables repeated calls to self.state = 1
                    self.timer1 = pygame.time.get_ticks()
                    self.state = 3
                    self.laser()

            if self.state == 2:
                self.moveTimer = pygame.time.get_ticks()
                if self.posX < WIDTH / 2:
                    self.speedx = 3
                    self.rect.centerx += self.speedx
                    if self.rect.centerx >= WIDTH / 2:
                        self.speedx = 0
                        self.rect.centerx = WIDTH / 2

                if self.posX > WIDTH / 2:
                    self.speedx = 3
                    self.rect.centerx -= self.speedx
                    if self.rect.centerx <= WIDTH / 2:
                        self.speedx = 0
                        self.rect.centerx = WIDTH / 2

                if self.rect.centerx == WIDTH / 2:
                    # self.state = 3 disables repeated calls to self.state = 2
                    self.timer1 = pygame.time.get_ticks()
                    self.state = 4
                    self.special()

        if self.stage == 2:
            # Begins stage 2 timer
            if self.beginTimer == False:
                self.beginTimer = True
                self.asteroidsTimer = pygame.time.get_ticks()

            self.rect.centery -= 4
            if self.rect.centery < -200:
                self.rect.centery = -200

        if self.stage == 3:
            self.rect.centery += 4
            if self.rect.centery >= 90:
                self.rect.centery = 90

            if self.state == 0:
                if pygame.time.get_ticks() - self.stateTimer > 7500:
                    self.stateTimer = pygame.time.get_ticks()
                    self.state = 1

                self.speedx = 0

                self.posX = self.rect.centerx

                # Move Boss to match Player's X-axis
                if player.rect.centerx > self.rect.centerx:
                    self.speedx += 3
                    self.rect.centerx += self.speedx

                if player.rect.centerx < self.rect.centerx:
                    self.speedx -= 3
                    self.rect.centerx += self.speedx

                if player.rect.centerx == self.rect.centerx:
                    self.speedx = 0
                    self.rect.centerx += self.speedx

                if pygame.time.get_ticks() - self.shootTimer > 1200:
                    self.shootTimer = pygame.time.get_ticks()
                    bullet1 = [Bullet(self.rect.centerx, self.rect.centery + 30, 12, 0, 1),
                                Bullet(self.rect.centerx + 45, self.rect.centery + 80, 12, 0, 1),
                                Bullet(self.rect.centerx - 42, self.rect.centery + 80, 12, 0, 1)]

                    splash1 = [BulletOrig(self.rect.centerx + 1, self.rect.centery + 20, 1),
                                BulletOrig(self.rect.centerx + 45, self.rect.centery + 60, 1),
                                BulletOrig(self.rect.centerx - 42, self.rect.centery + 60, 1)]

                    all_sprites.add(bullet1)
                    all_sprites.add(splash1)
                    bullets1.add(bullet1)
                    shoot_soundBoss.play()

                if pygame.time.get_ticks() - self.missTimer > 2200:
                    self.missTimer = pygame.time.get_ticks()
                    miss = [Missile(self.rect.left + 20, self.rect.centery + 9),
                            Missile(self.rect.right - 23, self.rect.centery + 9)]

                    splash2 = [BulletOrig(self.rect.left + 23, self.rect.centery + 100, 0),
                                BulletOrig(self.rect.right - 22, self.rect.centery + 100, 0)]

                    all_sprites.add(miss)
                    all_sprites.add(splash2)
                    missileGrp.add(miss)
                    shoot_soundMiss.play()

            if self.state == 1:
                vor = [Vortex(self.rect.centerx + 200, player.posY - 180),
                            Vortex(self.rect.centerx - 200, player.posY - 180)]

                all_sprites.add(vor)
                self.state = 0

        self.mask = pygame.mask.from_surface(self.image)

    def special(self):
        # Use special ability
        specials = [Special(self.rect.left + 169, self.rect.centery + 160)]

        all_sprites.add(specials)

    def laser(self):
        # Use laser ability
        lasers = [Laser(self.rect.left + 110, self.rect.bottom - 12, 90, 4),
            Laser(self.rect.right - 105, self.rect.bottom - 22, -90, -4)]

        all_sprites.add(lasers)
        lasersGrp.add(lasers)

# Load all game graphics
backgrounds = [pygame.image.load(path.join(img_dir, "n1-bottom@3x.png")).convert(),
                pygame.image.load(path.join(img_dir, "n1-top@3x.png")).convert()]
player_img = pygame.image.load(path.join(img_dir, "player.png")).convert_alpha()
boss_img = pygame.image.load(path.join(img_dir, "boss1.png")).convert_alpha()
select_img_orig = pygame.image.load(path.join(img_dir, "icon_frame1.png")).convert_alpha()
select_img = pygame.transform.scale(select_img_orig, (130, 130))
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
miss_img = pygame.image.load(path.join(img_dir, "missile.png")).convert_alpha()
radar_img = pygame.image.load(path.join(img_dir, "radar1.png")).convert_alpha()
fireball_img = pygame.image.load(path.join(img_dir, "fireball.png")).convert_alpha()
asteroid_img = pygame.image.load(path.join(img_dir, "asteroid.png")).convert_alpha()
vortex_img = pygame.image.load(path.join(img_dir, "vortex.png")).convert_alpha()
ellipse_img = pygame.image.load(path.join(img_dir, "ellipse.png")).convert_alpha()

Origin = []
miss_orig = pygame.image.load(path.join(img_dir, "missOrig.png")).convert_alpha()
Origin.append(miss_orig)
bull_orig = pygame.image.load (path.join(img_dir, "VLaserOrig.png")).convert_alpha()
Origin.append(bull_orig)

laser_img = []
laser_imgPlayer = pygame.image.load(path.join(img_dir, "laser.png")).convert_alpha()
laser_img.append(laser_imgPlayer)
laser_imgBoss = pygame.image.load(path.join(img_dir, "projV.png")).convert_alpha()
laser_imgBoss = pygame.transform.rotate(laser_imgBoss, 180)
laser_img.append(laser_imgBoss)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(1, 8):
    filename = '000{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    explosion_anim['player'].append(img)

pu_img = []
for x in range (1, 7):
    filename = "frame {}.png".format(x)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img2 = pygame.transform.scale(img1, (25, 25))
    img2.set_colorkey(BLACK)
    pu_img.append(img2)

pu_imgb = []
for x in range (1, 7):
    filename = "frame {}b.png".format(x)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img2 = pygame.transform.scale(img1, (25, 25))
    img2.set_colorkey(BLACK)
    pu_imgb.append(img2)

warpAnim = []
for x in range(8):
    filename = "warp{}.png".format(x)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img1 = pygame.transform.scale(img1, (150, 140))
    warpAnim.append(img1)

cdAnim = []
for x in range(29):
    filename = "LoadingBarPractice{}.png".format(x)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img1 = pygame.transform.scale(img1, (150, 140))
    cdAnim.append(img1)

loadBar = []
for x in range(21):
    filename = "loading_bar{}.png".format(x)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img1 = pygame.transform.scale(img1, (450, 200))
    loadBar.append(img1)

specialImg = []
for x in range(19):
    filename = "{}.png".format(x)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    specialImg.append(img1)

# Load all game sounds
pu_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup.wav"))
laser_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup16.wav"))
specials_sound = pygame.mixer.Sound(path.join(snd_dir, "Explosion21.wav"))
hit_sound = pygame.mixer.Sound(path.join(snd_dir, "Hit_hurt42.wav"))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "laser_shoot5.wav"))
shoot_soundBoss = pygame.mixer.Sound(path.join(snd_dir, "laser_shoot4.wav"))
shoot_soundMiss = pygame.mixer.Sound(path.join(snd_dir, "Randomize34.wav"))
expl_sounds = []
for snd in ['explosion.wav', 'explosion8.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))

# Game loop
game_on = True
running = True
while running:
    if game_on:
        show_go_screen()
        game_on = False
        all_sprites = pygame.sprite.Group()
        loadingScreen()

        #Write attempt to text file
        with open(path.join(stats_dir, "attempts.txt"), 'r+') as f:
            try:
                att = int(f.read())
            except:
                att = 0
        att += 1
        with open(path.join(stats_dir, "attempts.txt"), 'w') as f:
            f.write(str(att))

        start_timer = pygame.time.get_ticks()
        missileGrp = pygame.sprite.Group()
        astGrp = pygame.sprite.Group()
        ellipseGrp = pygame.sprite.Group()
        specialsGrp = pygame.sprite.Group()
        lasersGrp = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullets1 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        explosionGrp = pygame.sprite.Group()
        background1 = BG(WIDTH / 2, 0, 1)
        background2 = BG(WIDTH / 2, 940, 0)
        player = Player()
        boss = Boss(WIDTH / 2, 90)
        asty = Asteroid(WIDTH / 2, HEIGHT / 2)
        all_sprites.add(background1)
        all_sprites.add(background2)
        all_sprites.add(boss)
        all_sprites.add(player)
        powerup_timer = pygame.time.get_ticks()

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, powerups, True)

    for hit in hits:
        pu_sound.play()
        if hit.type == pu_imgb:
            player.shield += random.randrange(40, 60)

            if player.shield >= 100:
                player.shield = 100

        if hit.type == pu_img:
            player.Power()

        with open(path.join(stats_dir, "powersused.txt"), 'r+') as f:
            try:
                powers = int(f.read())
            except:
                powers = 0

        powers += 1
        with open(path.join(stats_dir, "powersused.txt"), 'w') as f:
            f.write(str(powers))

    with open(path.join(stats_dir, "hitstaken.txt"), 'r+') as f:
        try:
            hitstaken = int(f.read())
        except:
            hitstaken = 0

    hits = pygame.sprite.spritecollide(player, enemies, True)

    for hit in hits:
        player.shield -= random.randrange(40, 60)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if player.shield <= 0:
            lose_live()
        newenemy()
        hitstaken += 1
        playerHits(hitstaken)

    hits = pygame.sprite.groupcollide(astGrp, bullets, False, True, pygame.sprite.collide_mask)

    hits = pygame.sprite.spritecollide(player, ellipseGrp, True, pygame.sprite.collide_mask)

    for hit in hits:
        if player.immune == 0:
            player.shield -= random.randrange(50, 80)
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            if player.shield <= 0:
                lose_live()
            hitstaken += 1
            playerHits(hitstaken)

    hits = pygame.sprite.spritecollide(player, astGrp, True, pygame.sprite.collide_mask)

    for hit in hits:
        if player.immune == 0:
            player.shield -= (asty.radius * 0.75)
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if player.shield <= 0:
                lose_live()
            hitstaken += 1
            playerHits(hitstaken)

    hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_mask)

    for hit in hits:
        hit_sound.play()
        boss.shield -= 1
        if boss.shield <= 450 and boss.stage == 1:
            boss.stage = 2
            for n in range (10):
                new_ast()

        if boss.shield <= 0 and boss.stage == 3:
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'player')
            all_sprites.add(expl)
            boss.kill()
            end_game(0)
            game_on = True

    hits = pygame.sprite.collide_circle(player, boss)

    if hits == True and player.immune == 0:
        random.choice(expl_sounds).play()
        player.shield = 0
        lose_live()
        hitstaken += 1
        playerHits(hitstaken)

    hits = pygame.sprite.spritecollide(player, specialsGrp, True, pygame.sprite.collide_mask)

    for hit in hits:
        if player.immune == 0:
            lose_live()
            hitstaken += 1
            playerHits(hitstaken)

    hits = pygame.sprite.spritecollide(player, missileGrp, True, pygame.sprite.collide_mask)

    for hit in hits:
        if player.immune == 0:
            lose_live()
            hitstaken += 1
            playerHits(hitstaken)

    hits = pygame.sprite.spritecollide(player, lasersGrp, True, pygame.sprite.collide_mask)

    for hit in hits:
        if player.immune == 0:
            lose_live()
            hitstaken += 1
            playerHits(hitstaken)

    hits = pygame.sprite.spritecollide(player, bullets1, True, pygame.sprite.collide_mask)

    for hit in hits:
        if player.immune == 0:
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            player.shield -= random.randrange(40, 60)
            if player.shield <= 0:
                lose_live()
            hitstaken += 1
            playerHits(hitstaken)

    # If the player died and the explosion is finished
    death_explosion = Explosion(player.rect.center, 'player') # Load Explosion
    if player.lives == 0 and not death_explosion.alive():
        player.lives = 3
        player.shield = 100
        end_game(1)
        game_on = True

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        pause()

    all_sprites.draw(screen)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_shield_bar_Boss(screen, WIDTH - 110, 5, boss.shield)
    draw_lives(screen, 10, 20, player.lives, player_mini_img)

    if player.boolean == 1:
        displayCD(player)

    if boss.stage == 2:
        asteroidFieldTimer(boss)

    pygame.display.flip()

    if pygame.time.get_ticks() - powerup_timer > 15000:
        powerup_timer = pygame.time.get_ticks()
        choice = random.choice([pu_img, pu_imgb])
        pow = Pow(choice)
        all_sprites.add(pow)
        powerups.add(pow)

pygame.quit()
