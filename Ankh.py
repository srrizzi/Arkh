#NewGame

#########################################
#                                       #
#          Autor: Carlos Rizzi          #
#                                       #
#########################################

import pygame
import random
from os import path


WIDTH = 530
HEIGHT = 930
FPS = 60
POWERUP_TIME = 1000


#cores

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


#PastaDosAssets
img_folder = path.join(path.dirname(__file__), "Imagens")
sound_folder = path.join(path.dirname(__file__), "Sons")


FontName = pygame.font.match_font('console')
FontName2 = pygame.font.match_font('console')

def DesenharTextoInicial(surf, text, size, x, y):
    font = pygame.font.Font(FontName2, 40)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def DesenharTexto(surf, text, size, x, y):
    font = pygame.font.Font(FontName, 30)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def NovoMob():
    m = Mob()
    Sprites.add(m)
    Mobs.add(m)

def DesenharHp(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 200
    BAR_HEIGT = 20
    fill = (pct / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGT)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def DesenharVidas(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40 * i
        img_rect.y = y + -19
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    #Sprite do Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (90, 90))
        self.image.set_colorkey(green)
        self.rect = self.image.get_rect()
        self.radius = 20
       # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hp = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.vidas = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        #Tempo para PowerUp de Dano
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        #voltar Após Morte
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.tiro() 

        self.rect.x += self.speedx
        if self.rect.right > 560:
            self.rect.right = 560
        if self.rect.left <- 24:
            self.rect.left = -24   
    

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    def tiro(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                Sprites.add(bullet)
                bullets.add(bullet)
                SomBullet.play()
            if  self.power >= 2:
                bullet1 = Bullet(self.rect.left + 20, self.rect.centery - 10)
                bullet2 = Bullet(self.rect.right - 20, self.rect.centery - 10)
                Sprites.add(bullet1)
                Sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                SomBullet.play()

    def hide(self):
        #esconde o jogador pós morte temporariamente
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mob_imgs)
        self.image_orig.set_colorkey(green)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 24
     #   pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange (WIDTH - self.rect.width) 
        self.rect.y = random.randrange (-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange (-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left <-100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange (WIDTH - self.rect.width) 
            self.rect.y = random.randrange (-100, -40)
            self.speedy = random.randrange (1, 8) 
            


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(green)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 20
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        #apagar ao sair da tela
        if self.rect.bottom < 0:
            self.kill()

    

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['PotHP', 'PotPow'])
        self.image = PowerUpImg[self.type]
        self.image.set_colorkey(green)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        #apagar ao sair da tela
        if self.rect.top > HEIGHT:
            self.kill()
        

class Explode(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = ExpAnimacao[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(ExpAnimacao[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = ExpAnimacao[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        
def TelaInicial():
    tela.blit(MenuInicial, MenuInicial_rect)
    # DesenharTextoInicial(tela, "Ankh!!!", 64, WIDTH / 2, HEIGHT / 30)
    # DesenharTextoInicial(tela, "Setas para movimentar", 22, WIDTH / 2, HEIGHT / 3)
    # DesenharTextoInicial(tela, "Espaço atira", 40, WIDTH / 2, HEIGHT / 4)
    # DesenharTextoInicial(tela, "Pressione para começar", 30, WIDTH/2 , HEIGHT / 2)
    pygame.display.flip()
    Esperar = True

    
    while Esperar:
        timer.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                Esperar = False
        

#Inicializar Pygame e Janela do jogo. 

pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ankh")
timer = pygame.time.Clock()


#Load das Imagens

MenuInicial = pygame.image.load(path.join(img_folder, "MenuImagem00.png")).convert()
MenuInicial_rect = MenuInicial.get_rect()
MenuInicial2 = pygame.image.load(path.join(img_folder, "MenuImagem01.png")).convert()
MenuInicial2_rect = MenuInicial2.get_rect()
background = pygame.image.load(path.join(img_folder, "darkPurple.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_folder, "Bixin1.png")).convert()
player_vida = pygame.transform.scale(player_img, (70, 70))
player_vida.set_colorkey(green)
bullet_img = pygame.image.load(path.join(img_folder, "Ammo2.png")).convert()

# player_img  = []
# player_list = ['Bixin1.png','Bixin2.png','Bixin3.png',"Bixin4.png"]
# for img in player_list:
#     player_img.append(pygame.image.load(path.join(img_folder, img)).convert())

mob_imgs = []
mob_list = ['Ghostin.png','Ghostin1.png','Phan1.png','Phan2.png', 'Slim1.png','Slim1-2.png', 'Slim2.png','Slim2-1.png']
for img in mob_list:
    mob_imgs.append(pygame.image.load(path.join(img_folder, img)).convert())
    
ExpAnimacao = {}
ExpAnimacao['lg'] = []
ExpAnimacao['sm'] = []
ExpAnimacao['Player'] = []
for i in range(8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    img_lg = pygame.transform.scale(img, (90, 90))
    ExpAnimacao['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (40, 40))
    ExpAnimacao['sm'].append(img_sm)
    filename = 'PlayerBoom0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    ExpAnimacao['Player'].append(img)
    
PowerUpImg = {}
PowerUpImg['PotHP'] = pygame.image.load(path.join(img_folder, 'PotHP.png')).convert_alpha()
PowerUpImg['PotPow'] = pygame.image.load(path.join(img_folder, 'PotPow.png')).convert_alpha()

#Carregar os sons
SomBullet = pygame.mixer.Sound(path.join(sound_folder, 'Laser.wav'))
PotHpSom = pygame.mixer.Sound(path.join(sound_folder, 'PotHP.wav'))
PotDamSom = pygame.mixer.Sound(path.join(sound_folder, 'PotDam.wav'))

SomHits = []
# for snd in ['Mob1.wav', 'Mob2.wav', 'Mob3.wav','Mob4.mp3'3]:
for snd in ['Mob1.wav', 'Mob2.wav', 'Mob3.wav']:
    SomHits.append(pygame.mixer.Sound(path.join(sound_folder, snd)))
SomMortePlayer = pygame.mixer.Sound(path.join(sound_folder, 'Death.wav'))
pygame.mixer.music.load(path.join(sound_folder, 'Music.wav'))
pygame.mixer.music.set_volume(0.10)
pygame.mixer.music.play(loops=-1)


#Loop Do Jogo 
GameOver = True
Rodando = True
while Rodando:
    if GameOver:
        TelaInicial()
        GameOver = False
        Sprites = pygame.sprite.Group()
        Mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        Sprites.add(player)
        for i in range(8):
            NovoMob()
        Score = 0
    #Rodar na velocidade certa
    timer.tick(FPS)
    #Inserir os processos (eventos)
    for event in pygame.event.get():
        #Check de fechar a janela
        if event.type == pygame.QUIT: 
            Rodando = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.tiro()

    #Update
    Sprites.update()

    #Checar Collide mob/tiro
    hits = pygame.sprite.groupcollide(Mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        Score +=  1
        random.choice(SomHits).play()
        boom = Explode(hit.rect.center, 'lg')
        Sprites.add(boom)
        if random.random() > 0.9:
            PowerUp = Pow(hit.rect.center)
            Sprites.add(PowerUp)
            powerups.add(PowerUp)

        NovoMob()
 

    #Checar Collide mob/player
    hits = pygame.sprite.spritecollide(player, Mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= 20
        NovoMob()
        if player.hp <= 0:
            SomMortePlayer.play()
            death_explode = Explode(player.rect.center, 'Player')
            Sprites.add(death_explode)
            player.hide()
            player.vidas -= 1
            player.hp = 100


    #Checar Collide com PowerUp

    hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit.type == 'PotHP':
            player.hp += 10
            PotHpSom.play()
            if player.hp >= 100:
                player.hp = 100
        if hit.type == 'PotPow':
            player.powerup()
            PotDamSom.play()


    #Quando o jogador morrer e a animação acabar também

    if player.vidas == 0 and not death_explode.alive():
        GameOver = True

    #Desenhar/Imagem
    tela.fill(blue) 
    tela.blit(background, background_rect)   
    Sprites.draw(tela)
    
    DesenharTexto(tela, str(Score), 18, WIDTH / 2, 10)
    DesenharHp(tela, 10, 5, player.hp)
    DesenharVidas(tela, WIDTH -150, 1, player.vidas, player_vida)

    #depois de desenhar tudo, dar um "flip"
    pygame.display.flip()

pygame.quit()