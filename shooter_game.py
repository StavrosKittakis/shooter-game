from pygame import *
from random import randint

score = 0
missed_shots = 0

font.init()
font1 = font.Font(None, 50)
font2 = font.Font(None, 100)

window = display.set_mode((700, 500))
display.set_caption("pygame window")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

bullets = sprite.Group()
asteroids = sprite.Group()

class SpriteCharacter(sprite.Sprite):
    def __init__(self, image_path, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def render(self, window):
        window.blit(self.image, self.rect.topleft)
    
class Hero(SpriteCharacter):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x + 20, self.rect.y, 9)
        bullets.add(bullet)

class Asteroid(SpriteCharacter):
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > 1300:
            self.rect.y = 0
            self.rect.x = randint(0, 635)
            self.speed = 3

class UFO(SpriteCharacter):
    def update(self):
        global missed_shots
        self.rect.y += self.speed
        if self.rect.y > 500:  
            missed_shots += 1  
            self.rect.y = 0  
            self.rect.x = randint(0, 635)  
            self.speed = randint(2, 5)  

class Bullet(SpriteCharacter):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

enemies = sprite.Group()
for i in range(5):
    ufo = UFO("ufo.png", randint(100, 600), 10, randint(2, 5))
    enemies.add(ufo)

rocket = Hero("rocket.png", 350, 400, 6)
asteroid = Asteroid("asteroid.png", randint(100, 600), 10, 3)

game = True
game_over = False
clock = time.Clock()
FPS = 60

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.fire()



    if not game_over:
        rocket.move()
        window.blit(background, (0, 0))
        rocket.render(window)

        asteroid.render(window)
        asteroid.move()

        enemies.draw(window)
        enemies.update()

        bullets.draw(window)
        bullets.update()

        collisions = sprite.groupcollide(bullets, enemies, True, True)
        as_collisions = sprite.groupcollide(bullets, asteroids, True, False)

        if sprite.collide_rect(rocket, asteroid):
            score -= 10
            if score < 0:
                score = 0

        for p in collisions:
            score += 1
            ufo = UFO("ufo.png", randint(100, 600), 10, randint(2, 5))
            enemies.add(ufo)

        score_txt = font1.render("Score:" + str(score), True, (255, 255, 255))
        missed = font1.render("Missed:" + str(missed_shots), True, (255, 255, 255))
        window.blit(score_txt, (10, 10))
        window.blit(missed, (10, 40))

        if missed_shots >= 5:
            game_over = True
        elif score >= 50:
            game_over = True

    else:
        window.blit(background, (0, 0))
        if missed_shots >= 5:
            lose = font2.render("YOU LOSE", True, (255, 0, 0))
            window.blit(lose, (200, 200))
        elif score >= 50:
            win = font2.render("YOU WIN", True, (255, 255, 0))
            window.blit(win, (200, 200))

    clock.tick(FPS)
    display.update()


