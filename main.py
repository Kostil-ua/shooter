from pygame import *
from random import randint
from time import time as timer

goal = 20
    
# фонова музика
mixer.init()
mixer.music.load('gimn-ljuftvaffe.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
# шрифти і написи
font.init()
font1 = font.Font(None, 60)
win = font1.render('Вітаю сало твоє!', True, (255, 255, 255))
lose = font1.render('сало було вкрадено!', True, (180, 0, 0))
font2 = font.Font(None, 36)




# нам потрібні такі картинки:
img_back = "pole-1.jpg"  # фон гри
img_hero = "tank.png"  # герой
img_bullet = "bullet.png" # куля
img_enemy = "kamikadze.png"  # ворог
img_ast = "images-removebg-preview (1).png" # астероїд
 
score = 0  # збито кораблів
lost = 0  # пропущено кораблів
max_lost = 30 # програли, якщо пропустили стільки
life = 60
# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed 
        if keys[K_UP] and self.rect.y > 5:
            self.rect.yd -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - self.rect.height:
            self.rect.y += self.speed 

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed


    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 5, 20, -15)
        bullets.add(bullet)
        
 
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 20):
    monster = Enemy(img_enemy, randint(     
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
bullets = sprite.Group()


asteroids = sprite.Group()
for i in range(1, 5):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

rel_time = False
# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна

num_fire = 0

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
            
                if num_fire >= 10 and  rel_time == False:
                    last_time = timer()
                    rel_time = True
        if e.type == MOUSEBUTTONDOWN:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
            
                if num_fire >= 10 and  rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))
 
        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()


        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False




        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            moster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        """
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))"""

        if score >= goal:
            finish =True
            window.blit(win, (200, 200))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        

        if life >= 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
 

















 
        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)

