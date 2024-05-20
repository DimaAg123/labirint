# Разработай свою игру в этом файле!
from pygame import *
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
win = transform.scale(image.load('win.png'), (win_width, win_height))
lose = transform.scale(image.load('lose.png'), (win_width, win_height))
back = (100,200,200)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__(player_image, player_x, player_y , size_x, size_y)
        self.speed = speed
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = speed

    def update(self):
        direction = 'left'
        if self.rect.x <= 480:
            self.direction = 'right'
        if self.rect.x >= 620:
                self.direction = 'left'
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

    


w1 = GameSprite('platform2.png', 150, 330, 300, 50)
w2 = GameSprite('platform2_v.png', 200, 170, 250, 50)
w3 = GameSprite('platform2.png', 400, 200, 50, 300)
w4 = Player('pngwing.com.png', 50, 50, 50, 50, 10)
final = GameSprite('platform2.png', 550, 430, 50, 50)
monster = Enemy('monster.png', 620, 200, 50, 50, 3)
barriers = sprite.Group()
monsters = sprite.Group()
monsters.add(monster)
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
bullets = sprite.Group()

run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            w4.fire()
    if not finish:
        window.fill(back)
        w1.reset()
        w2.reset()
        w3.reset()
        w4.reset()
        w4.update()
        final.reset()
        monsters.draw(window)
        monster.update()
        bullets.draw(window)
        bullets.update()


        if sprite.collide_rect(w4, final):
            finish = True
            window.blit(win, (0,0))
        if sprite.spritecollide(w4, monsters, False):
            finish = True
            window.blit(lose, (0,0))
        if sprite.spritecollide(w4, barriers, False):
            finish = True
            window.blit(lose, (0,0))
        if sprite.collide_rect(w4, monster):
            finish = True
            window.blit(lose, (0,0))
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)

        


    display.update()
    time.delay(20)