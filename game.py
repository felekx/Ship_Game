from livewires import games, color
import random, os


os.environ['SDL_VIDEO_CENTERED'] = '1'
games.init(screen_width = 770, screen_height = 630, fps = 50)


""""Definiuje efekt eksplozji"""
class Explosion(games.Animation):
    sound = games.load_sound("eksplozja.wav")
    images_big = ["expl1.bmp","expl2.bmp","expl3.bmp","expl4.bmp","expl5.bmp","expl6.bmp",
                "expl7.bmp","expl8.bmp","expl9.bmp"]
    images_small = ["expl1.bmp","expl2.bmp"]

    def __init__(self, x, y, nr):
        if nr == 'big':
            super(Explosion, self).__init__(images=Explosion.images_big,
                                            x=x, y=y,
                                            repeat_interval=6, n_repeats=1,
                                            is_collideable=False)
        elif nr == 'small':
            super(Explosion, self).__init__(images=Explosion.images_small,
                                            x=x, y=y,
                                            repeat_interval=6, n_repeats=1,
                                            is_collideable=False)

        Explosion.sound.play()




"""Statek sterowany przez komputer"""
class Statek_gora(games.Sprite):
    image = games.load_image("statek_gora.gif")
    DELAY_POCISKU = 55
    LIFE = 5

    def __init__(self, x, y):
        super(Statek_gora, self).__init__(image=Statek_gora.image, x=x, y=y, dx = 2, dy = 2 )
        self.wait_pocisku = 0

        "Obiekty serca - wskaznik zycia statku komputera"
        self.heart1 = Serce(x=18, y=33)
        games.screen.add(self.heart1)

        self.heart2 = Serce(x=40, y=33)
        games.screen.add(self.heart2)

        self.heart3 = Serce(x=62, y=33)
        games.screen.add(self.heart3)

        self.heart4 = Serce(x=84, y=33)
        games.screen.add(self.heart4)

        self.heart5 = Serce(x=106, y=33)
        games.screen.add(self.heart5)

    def die(self):
        if Statek_gora.LIFE == 5:
            self.heart5.die()
        elif Statek_gora.LIFE == 4:
            self.heart4.die()
        elif Statek_gora.LIFE == 3:
            self.heart3.die()
        elif Statek_gora.LIFE == 2:
            self.heart2.die()
        elif Statek_gora.LIFE == 1:
            new_explosion = Explosion(x=self.x, y=self.y, nr='big')
            games.screen.add(new_explosion)
            self.destroy()
            self.heart1.die()
            self.end_game()

        Statek_gora.LIFE -= 1

    def update(self):
        "Ustal czy kierunek ruchu statku musi zostac zmieniony na przeciwny"
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(50) == 0:
           self.dx = -self.dx

        if self.top < 0 or self.bottom > (games.screen.height/2) :
            self.dy = -self.dy
        elif random.randrange(50) == 0:
           self.dy = -self.dy

        # czas ktory musi minąć do ponownego wystrzelenia pocisku
        if self.wait_pocisku > 0:
            self.wait_pocisku -= 1

        self.shoot()

    #wystrzel pocisk
    def shoot(self):
        if self.wait_pocisku == 0:
            nowy_pocisk = Pocisk(self.x, self.y+40, dy=3.5)
            games.screen.add(nowy_pocisk)
            self.wait_pocisku = Statek_gora.DELAY_POCISKU

    #zakoncz grę
    def end_game(self):
        end_message = games.Message(value = "Koniec gry",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 50 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)




"""Statek sterowany przez gracza"""
class Statek_dol(games.Sprite):
    image = games.load_image("statek_dol.gif")
    DELAY_POCISKU = 60
    LIFE = 5


    def __init__(self, x, y):
        super(Statek_dol, self).__init__(image=Statek_dol.image, x=x, y=y)
        self.wait_pocisku = 0

        self.wait_lustra = random.randrange(50,200)

        "Obiekty serca - wskaznik zycia statku gracza"
        self.heart1 = Serce(x=games.screen.width-18, y=33)
        games.screen.add(self.heart1)

        self.heart2 = Serce(x=games.screen.width-40, y=33)
        games.screen.add(self.heart2)

        self.heart3 = Serce(x=games.screen.width-62, y=33)
        games.screen.add(self.heart3)

        self.heart4 = Serce(x=games.screen.width-84, y=33)
        games.screen.add(self.heart4)

        self.heart5 = Serce(x=games.screen.width-106, y=33)
        games.screen.add(self.heart5)


    def update(self):
        # wspolrzedne pobierane z myszy
        self.x = games.mouse.x
        self.y = games.mouse.y
        self.check_position()

        # czas ktory musi minąć do ponownego wystrzelenia pocisku
        if self.wait_pocisku > 0:
            self.wait_pocisku -= 1
        self.shoot()

        #czas ktory musi minąć do ponownego pojawienia się lustra
        if self.wait_lustra > 0:
            self.wait_lustra -= 1
        self.create_lustro()

    def create_lustro(self):
        if self.wait_lustra == 0:
            lustro = Lustro()
            games.screen.add(lustro)
            self.wait_lustra = random.randrange(50,500)

    # kontroluj pozycję statku jesli wyjdzie poza ekran gry
    def check_position(self):
        if self.top <= (games.screen.height/2):
            self.top = games.screen.height/2
        if self.bottom >= games.screen.height:
            self.bottom = games.screen.height
        if self.left <= 0:
            self.left = 0 - 7
        if self.right >= games.screen.width:
            self.right = games.screen.width + 7

    # wystrzel pocisk jeśli zostanie wcisniety lewy przycisk myszy
    def shoot(self):
        if games.mouse.is_pressed(0)==1 and self.wait_pocisku == 0:
            nowy_pocisk = Pocisk(self.x, self.y-40, dy=-3.5)
            games.screen.add(nowy_pocisk)
            self.wait_pocisku = Statek_dol.DELAY_POCISKU

    def die(self):
        if Statek_dol.LIFE == 5:
            self.heart5.die()
        elif Statek_dol.LIFE == 4:
            self.heart4.die()
        elif Statek_dol.LIFE == 3:
            self.heart3.die()
        elif Statek_dol.LIFE == 2:
            self.heart2.die()
        elif Statek_dol.LIFE == 1:
            new_explosion = Explosion(x=self.x, y=self.y, nr='big')
            games.screen.add(new_explosion)
            self.destroy()
            self.heart1.die()
            self.end_game()

        Statek_dol.LIFE -= 1

    # zakoncz grę
    def end_game(self):
        end_message = games.Message(value = "Koniec gry",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 50 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)




"""Reprezentuje wystrzeliwane pociski"""
class Pocisk(games.Sprite):
    sound = games.load_sound("pocisk.wav")
    image = games.load_image("pocisk.bmp")

    def __init__(self, statek_x, statek_y, dy):
        Pocisk.sound.play()
        super(Pocisk, self).__init__(image=Pocisk.image,
                                      x=statek_x, y=statek_y, dy = dy)

    def update(self):
        # sprawdź, czy pocisk zachodzi na jakiś inny obiekt
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self, expl='Yes'):
        if expl == 'Yes':
            new_explosion = Explosion(x = self.x, y = self.y, nr = 'small')
            games.screen.add(new_explosion)
            self.destroy()
        elif expl == 'No':
            self.destroy()




"""Obiekty serca - wskazniki zycia"""
class Serce(games.Sprite):
    image = games.load_image("serce.jpg")

    def __init__(self, x, y):
        super(Serce, self).__init__(image=Serce.image, x=x, y=y, is_collideable=False)

    def die(self):
        self.destroy()



"""Obiekt lustra - odbija pociski gracza"""
class Lustro(games.Sprite):
    image = games.load_image("lustro.jpg")

    def __init__(self):
        super(Lustro, self).__init__(image=Lustro.image, x=1, y=games.screen.height/2, dx = 1, is_collideable=False )

    def update(self):
        # sprawdź, czy pocisk zachodzi na lustro
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite,Pocisk):
                    sprite.die(expl='No')
                    self.shoot()

    def shoot(self):
        nowy_pocisk = Pocisk(self.x, self.y+50, dy=4)
        games.screen.add(nowy_pocisk)





"""Główna funkcja"""
def main():
    wall_image = games.load_image("tlo.jpg", transparent = False)
    games.screen.background = wall_image

    score1 = games.Text(value='Komputer', size=22,color=color.light_gray,x=45,y=15, is_collideable=False)
    score2 = games.Text(value='Gracz', size=24, color=color.light_gray, x=(games.screen.width-40), y=15, is_collideable=False)
    games.screen.add(score1)
    games.screen.add(score2)

    statek_gora = Statek_gora( x=350, y=30)
    games.screen.add(statek_gora)

    statek_dol = Statek_dol(x=games.mouse.x, y=games.mouse.y)
    games.screen.add(statek_dol)

    games.mouse.is_visible = False
    games.screen.event_grab = True

    games.screen.mainloop()

#Wywołanie funkcji main() - wystartuj !
main()







