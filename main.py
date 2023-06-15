from pygame import *
from random import randint


main_win = display.set_mode((700,500))
display.set_caption('Ам Ням')
back = transform.scale(image.load('box.jpg'), (700,500))


mixer.init()
mixer.music.load('menu_music.ogg')
mixer.music.play()
chewing = mixer.Sound('monster_chewing.ogg')
lose_sound = mixer.Sound('lose.ogg')
win_sound = mixer.Sound('win.ogg')

font.init()
font = font.Font(None,70)
lose = font.render('YOU LOSE!', True, (255,0,0))
win = font.render('YOU WIN!', True, (255,228,0))

s_counter = 0

class GameSprite(sprite.Sprite):
    def __init__(self,p_image,p_x,p_y,p_speed,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(size_x,size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if pressed_keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

class Sweet(GameSprite):
    def update(self):
        global s_counter
        self.rect.y += self.speed
        if sprite.spritecollide(nyam, sweets, False):
            self.rect.y = 0
            self.rect.x = randint(50,620)
            s_counter += 1
            chewing.play()
        if self.rect.y > 500:
            self.rect.y = 0 
            self.rect.x = randint(50,650)

class Spider(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0 
            self.rect.x = randint(50,650)

nyam = Player('am nyam.png', 350,400,10,125,100)
sweets = sprite.Group()
spiders = sprite.Group()

for _ in range(5):
    s = Sweet('candy.png',randint(50,650),0,randint(1,3),75,50)
    sweets.add(s)

for _ in range(4):
    sp = Spider('spider.png',randint(50,650),0,randint(1,2),50,50)
    spiders.add(sp)

finish = False
game = True
fps = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        main_win.blit(back,(0,0))
        nyam.reset()
        spiders.draw(main_win)
        sweets.draw(main_win)
        nyam.update()
        sweets.update()
        spiders.update()

        score = font.render('Счёт:' + str(s_counter), True, (255,255,255))
        main_win.blit(score, (10,10))

        if s_counter >= 10:
            finish = True
            main_win.blit(win, (250,250))
            win_sound.play()

        if sprite.spritecollide(nyam,spiders, False):
            finish = True
            lose_sound.play()
            main_win.blit(lose,(250,250))
    

    clock.tick(fps)
    display.update()