##### [УПРАВЛЕНИЕ] #####                ##### [НЕ УДАЛЯТЬ ДАЖЕ КОММЕНТЫ, А ТО ВСЁ ПОСЫПЕТСЯ] #####
# WASD - ХОДЬБА
# ПРОБЕЛ - СТРЕЛЬБА
# R - ПЕРЕЗАРЯДКА
# вроде всё

from pygame import *
from random import randint
mixer.init()
font.init()


####### [ ООП ] #######
class Base():
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(sprite.Sprite, Base):
    def __init__(self):
        self.image = transform.scale(image.load("player.png"), (160, 110))
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.y = 15
        self.speedx = 0
        self.speedy = 0
        self.ang = 90
        self.hpline = 3

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
    def fire(self):
        global timer, mag
        sfire.play()
        bullet = Bullet()
        bullets.add(bullet)
        timer = 7
        mag -= 1

class Enemy(sprite.Sprite, Base):
    def __init__(self, way, axis, p, x, y):
        super().__init__()
        self.image = transform.scale(image.load("enemy.png"), (150, 110))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hpline = randint(10, 20)
        self.axis = axis
        self.p1, self.p2, self.p = x, y, p
        self.timer = -1
        self.direct = "f"

        if way == "w":
            self.speedx, self.speedy = 0, -2
            self.image = transform.rotate(self.image, 90)
        if way == "s":
            self.speedx, self.speedy = 0, 2
            self.image = transform.rotate(self.image, -90)
        if way == "a":
            self.speedx, self.speedy = -2, 0
            self.image = transform.rotate(self.image, 180)
        if way == "d":
            self.speedx, self.speedy = 2, 0

    def update(self):
        if self.timer < 0:
            
            if self.direct == "f":
                self.rect.x += self.speedx
                self.rect.y += self.speedy
            if self.direct == "r":
                self.rect.x += self.speedx
                self.rect.y += self.speedy
            
            if self.axis == "x":
                if self.rect.x == self.p or self.rect.x == self.p1:
                    if self.direct == "f":
                        self.direct == "r"
                        self.timer = 180
                        self.speedx = -self.speedx
                    if self.direct == "r":
                        self.direct == "f"
                        self.timer = 180
                        self.speedx = -self.speedx

            if self.axis == "y" and self.timer <= 0:
                if self.rect.y == self.p or self.rect.y == self.p2:
                    if self.direct == "f":
                        self.direct == "r"
                        self.timer = 180
                        self.speedy = -self.speedy
                    if self.direct == "r":
                        self.direct == "f"
                        self.timer = 180
                        self.speedy = -self.speedy
            

        else:
            self.timer -= 1

        if self.timer == 0:
            self.image = transform.rotate(self.image, 180)
        
        if self.hpline < 1:
            self.rect.x = -200
            self.movement = False
            self.kill()

class Wall(sprite.Sprite, Base):
    def __init__(self, x, y, width, heigth):
        self.image = Surface((width, heigth))
        self.rect = self.image.get_rect()
        self.image.fill((50, 50, 50))
        self.rect.x = x
        self.rect.y = y
    
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = transform.scale(image.load("bullet.png"), (15, 20))
        self.rect = self.image.get_rect()

        if player.ang == 0:
            self.speedx, self.speedy = 0, -30
            self.rect.x = player.rect.x + 75
            self.rect.y = player.rect.y - 30
        if player.ang == 90:
            self.speedx, self.speedy = 30, 0
            self.image = transform.rotate(self.image, -90)
            self.rect.x = player.rect.x + 170
            self.rect.y = player.rect.y + 75
        if player.ang == 180:
            self.speedx, self.speedy = 0, 30
            self.image = transform.rotate(self.image, -180)
            self.rect.x = player.rect.x + 20
            self.rect.y = player.rect.y + 165
        if player.ang == 270:
            self.speedx, self.speedy = -30, 0
            self.image = transform.rotate(self.image, 90)
            self.rect.x = player.rect.x - 30
            self.rect.y = player.rect.y + 20

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x < -10 or self.rect.x > 1280 or self.rect.y < -10 or self.rect.y > 730:
            self.kill()
        if sprite.collide_rect(self, wall1) or sprite.collide_rect(self, wall2) or sprite.collide_rect(self, wall3) or sprite.collide_rect(self, wall4):
            self.kill()

        if sprite.collide_rect(self, enemy1):
            self.kill()
            enemy1.hpline -= 1
        if sprite.collide_rect(self, enemy2):
            self.kill()
            enemy2.hpline -= 1
        if sprite.collide_rect(self, enemy3):
            self.kill()
            enemy3.hpline -= 1
        if sprite.collide_rect(self, enemy4):
            self.kill()
            enemy4.hpline -= 1
        if sprite.collide_rect(self, enemy5):
            self.kill()
            enemy5.hpline -= 1
        if sprite.collide_rect(self, enemy6):
            self.kill()
            enemy6.hpline -= 1


####### [САМАЯ ТАКАЯ БАЗА] #######
window = display.set_mode((1280, 720))
display.set_caption("Dying Light 3")
bg = transform.scale(image.load("background.jpg"), (1280, 720))


####### [ОБЪЕКТЫ] #######
player = Player()
enemy1 = Enemy("a", "x", 0, 1100, 30)
enemy2 = Enemy("w", "y", 150, 1140, 500)
enemy3 = Enemy("d", "x", 950, 200, 260)
enemy4 = Enemy("s", "y", 550, 60, 230)
enemy5 = Enemy("d", "x", 890, 280, 480)
enemy6 = Enemy("a", "x", 200, 900, 600)


####### [СТЕНЫ] #######
wall1 = Wall(0, 170, 1100, 50)
wall2 = Wall(1050, 420, 50, 350)
wall3 = Wall(250, 420, 800, 50)
wall4 = Wall(250, 420, 50, 150)


####### [МУЗЫКА] #######
mixer.music.load("ost.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.55)

smiss = mixer.Sound("miss.mp3")
smiss.set_volume(0.4)
sfire = mixer.Sound("fire.mp3")
sfire.set_volume(0.25)
sreload = mixer.Sound("reload.mp3")
sreload.set_volume(0.4)
hit = mixer.Sound("hit.mp3")
hit.set_volume(0.4)


####### [ШРИФТЫ И НАДПИСИ] #######
font_ammo = font.Font("Frula.ttf", 56)
font_wl = font.Font("Frula.ttf", 200)
twin = font_wl.render("WIN", 1, (255, 255, 255))
tlose = font_wl.render("LOSE", 1, (255, 255, 255))


####### [ГРУППЫ СПРАЙТОВ] #######
bullets = sprite.Group()
monsters = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)
monsters.add(enemy6)


####### [ПАРАМЕТРЫ ПЕРЕД ЦИКЛОМ] #######
timer = 0
timerr = 0
timerm = 0
timerhp = 0
r = False
res = 180
mag = 30
magch = 0
reload = False
speedxc = 0
speedyc = 0
win = False
finish = False
clock = time.Clock()
game = True


####### [ЦИКЛ] #######
while game:


    ####### [ПРОВЕРКА НА ЗАКРЫТИЕ] #######
    for e in event.get():
        if e.type == QUIT:
            game = False
    

    ###### [ЦИКЛ ОТРИСОВКИ] #######
    if not finish:


    ####### [ОТРИСОВАКА BACKGROUND] #######
        window.blit(bg, (0, 0))


    ####### [ОТРИСОВКА ИГРОКА] #######
        player.update()
        player.reset()

    ####### [ОТРИСОВКА ВРАГОВ] #######
        monsters.draw(window)
        monsters.update()


    ####### [ОТРИСОВКА ПУЛЬ] #######
        bullets.draw(window)
        bullets.update()


    ####### [ОТРИСОВКА СТЕН] #######
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()


    ####### [ОТРИСОВКА HUD] #######
        hud = font_ammo.render(f"{mag}   {res}", 1, (255, 255, 255))
        window.blit(hud, (1050, 670))
        hp = font_ammo.render(f"{player.hpline} HP", 1, (255, 255, 255))
        window.blit(hp, (1140, 600))
    

    ####### [ФИКС АВТОХОДЬБЫ] #######
        player.speedx, player.speedy = 0, 0


    ####### [УПРАВЛЕНИЕ] #######
    keys = key.get_pressed()
    if keys[K_w] and player.rect.y > -5:
        player.speedx, player.speedy = 0, -5
        if player.ang != 0:
            player.image = transform.rotate(player.image, player.ang)
            player.ang = 0
    if keys[K_s] and player.rect.y < 600:
        player.speedx, player.speedy = 0, 5
        if player.ang != 180:
            player.image = transform.rotate(player.image, player.ang)
            player.ang = 180
            player.image = transform.rotate(player.image, -player.ang)
    if keys[K_a] and player.rect.x > -10:
        player.speedx, player.speedy = -5, 0
        if player.ang != 270:
            player.image = transform.rotate(player.image, player.ang)
            player.ang = 270
            player.image = transform.rotate(player.image, -player.ang)
    if keys[K_d] and player.rect.x < 1150:
        player.speedx, player.speedy = 5, 0
        if player.ang != 90:
            player.image = transform.rotate(player.image, player.ang)
            player.ang = 90
            player.image = transform.rotate(player.image, -player.ang)
    if keys[K_SPACE] and reload != True and finish != True:
        if timer <= 0 and mag >= 1:
            player.fire()
        if mag == 0 and timerm <= 0:
            smiss.play()
            timerm = 7
    if keys[K_r] and mag != 30 and reload != True and res > 0 and finish != True:
        sreload.play()
        magch = mag
        reload = True
        timerr = 220


    ###### [ФИЗИКА ПЕРЕЗАРЯДКИ] #######
    if timerr > 0:
        timerr -= 1
    elif timerr == 0:
        if res >= 30:
            reload = False
            mag = 30
            res -= mag - magch
            timerr = -1
        else:
            reload = False
            mag = res
            res = 0
            timerr = -1
    

    ###### [ФИЗИКА СТЕН] #######
    if sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall4):
        if r == True:
            pass
        else:
            speedxc = player.speedx
            speedyc = player.speedy
        if player.ang == 0:
            player.rect.y += -speedyc + 10
        if player.ang == 90:
            player.rect.x -= speedxc + 10
            r = True
        if player.ang == 180:
            player.rect.y -= speedyc + 10
            r = True
        if player.ang == 270:
            player.rect.x += -speedxc + 10
            r = True
    else:
        r = False


    ###### [НАНЕСЕНИЕ УРОНА ИГРОКУ И ПРОЗРАЧНОСТЬ СПРАЙТА] #######
    if sprite.collide_rect(player, enemy1) or sprite.collide_rect(player, enemy2) or sprite.collide_rect(player, enemy3) or sprite.collide_rect(player, enemy4) or sprite.collide_rect(player, enemy5) or sprite.collide_rect(player, enemy6):
        if timerhp <= 0:
            hit.play()
            player.hpline -= 1
            timerhp = 180
            player.image.set_alpha(100)
    if timerhp <= 0:
        player.image.set_alpha(255)
    

    ###### [ОБНОВЛЕНИЕ ТАЙМЕРОВ] #######
    timerm -= 1
    timer -= 1
    timerhp -= 1


    ###### [ПОБЕДА] #######
    if enemy1.rect.x < 0 and enemy2.rect.x < 0 and enemy3.rect.x < 0 and enemy4.rect.x < 0 and enemy5.rect.x < 0 and enemy6.rect.x < 0:
        window.fill((0, 0, 0))
        window.blit(twin, (465.5, 291.5))
        finish = True
    

    ####### [ПОРАЖЕНИЕ] #######
    if player.hpline <= 0:
        player.rect.y = -200
        window.fill((0, 0, 0))
        window.blit(tlose, (349, 289.5))
        finish = True


    ###### [ОБНОВЛЕНИЕ] #######
    clock.tick(60)
    display.update()