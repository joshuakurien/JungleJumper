import pygame, random

class App:
    """Container for app with multiple scenes"""
    scenes = []
    screen_width = 500
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    def __init__(self, caption):
        #initialize pygame
        pygame.init()
        pygame.display.set_caption(caption)
        pygame.mixer.init()
        pygame.font.init()

        #screen sizing
        self.running = True

        initial_scene = Home()
        self.run(initial_scene)

    def run(self, current_scene):
        #game loop
        while self.running:
            #waits for events and pressed keys
            pressed_keys = pygame.key.get_pressed()
            scene_events = []

            for event in pygame.event.get():
                #quits game
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                else:
                    scene_events.append(event)

            current_scene.ProcessInput(scene_events, pressed_keys)
            current_scene.Update()
            current_scene.Render()

            current_scene = current_scene.next
        

class Scene:
    """Scene Base Class"""
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, keys):
        pass
    
    def Update(self):
        pass
    
    def Render(self):
        pass

    def SwitchToScene(self, next_scene):
        #used to change scenes
        self.next = next_scene

class Home(Scene):
    """Home screen scene"""
    def __init__(self):
        super().__init__()
        self.background_music = pygame.mixer.Sound("./media/we_three_kings.OGG")
        self.clicking_sound = pygame.mixer.Sound("./media/clicks.WAV")
        self.background_music.play(10)

        self.background = [pygame.image.load('./media/F{}.jpg'.format(number)).convert() for number in range(1, 9)]
        self.thunder = [pygame.image.load('./media/thunder{}.png'.format(number)) for number in range(1, 10)]
        #counters used to alternate between background and thunder images
        self.background_counter = 0
        self.thunder_counter = 0
        self.title = pygame.image.load('./media/JungleJumper.png')

        #these variables are required for button animation
        self.start_button = pygame.image.load('./media/Start.png')
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.topleft = (178,120)
        self.start_button_alternate = pygame.image.load('./media/Start2.png')

        #these variables are required for button animation
        self.how_to_play = pygame.image.load('./media/HowtoPlay.png')
        self.how_to_play_alternate = pygame.image.load('./media/HowtoPlayDark.png')        
        self.how_to_play_rect = self.how_to_play.get_rect()
        self.how_to_play_rect.topleft = (117, 240)

        #these variables are required to recognize if user is clicking scroll
        self.scroll = pygame.image.load('./media/scroll.png')
        self.scroll_rect = self.scroll.get_rect()
        self.scroll_rect.topleft = (50,10)

        #used to indicate if scroll is being displayed or not
        self.how_to_play_bool = False

    def ProcessInput(self, events, keys):
        for event in events:
            #used to indicate if mouse is over button and then animate by changing image
            if event.type == pygame.MOUSEMOTION:
                if self.start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.start_button = self.start_button_alternate
                else:
                    self.start_button = pygame.image.load('./media/Start.png')
                if self.how_to_play_rect.collidepoint(pygame.mouse.get_pos()):
                    self.how_to_play = self.how_to_play_alternate
                else:
                    self.how_to_play = pygame.image.load('./media/HowtoPlay.png')
                if not self.scroll_rect.collidepoint(pygame.mouse.get_pos()):
                    #checks if user is still looking at how to play
                    self.how_to_play_bool = False     

            #detects user clicking start button or how to play button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.how_to_play_rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicking_sound.play()
                    self.how_to_play_bool = True
                if self.start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicking_sound.play()
                    self.start_button = self.start_button_alternate
                    self.background_music.stop()
                    self.next = Game()
                    
    #updates counter and makes sure background animations aren't too fast
    def Update(self):
        pygame.time.delay(100)
        self.background_counter = (self.background_counter+1)%8
        self.thunder_counter = random.randint(0, 8)

    #displays on screen
    def Render(self):
        if not self.how_to_play_bool:
            App.screen.blit(self.background[self.background_counter], [0, 0])
            App.screen.blit(self.thunder[self.thunder_counter], [200, 50])
            App.screen.blit(self.title, (38,40))
            App.screen.blit(self.start_button, self.start_button_rect)
            App.screen.blit(self.how_to_play, self.how_to_play_rect)
        else:
            App.screen.blit(self.background[self.background_counter], [0, 0])
            App.screen.blit(self.thunder[self.thunder_counter], [200, 50])
            App.screen.blit(self.title, (38,40))
            App.screen.blit(self.start_button, self.start_button_rect)
            App.screen.blit(self.how_to_play, self.how_to_play_rect)
            App.screen.blit(self.scroll, self.scroll_rect)

        pygame.display.update()

class Game(Scene):
    """Game scene"""
    def __init__(self):
        super().__init__()
        self.clicking_sound = pygame.mixer.Sound("./media/clicks.WAV")
        self.background = pygame.image.load('./media/background.jpg')

        self.score = 0

        self.jungle_jumper_img = pygame.image.load('./media/JungleJumper.png')

        self.pause_button = pygame.image.load('./media/pausebutton2.png')
        self.pause_button_rect = self.pause_button.get_rect()
        self.pause_button_rect.topleft = (400, 15)

        self.pause_button_screen = pygame.image.load('./media/pausebutton.png')
        self.pause_button_screen_rect = self.pause_button_screen.get_rect()
        self.pause_button_screen_rect.topleft = (188, 140)

        self.quit_button = pygame.image.load('./media/quit.png')
        self.quit_button_alternate = pygame.image.load('./media/DarkQuit.png')
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.topleft = (160,320)

        #instantiating player and platforms for the game
        self.user = Player()
        self.platforms = Platforms()

        #used to indicate if pause screen is present or not
        self.pause_bool = False


    def ProcessInput(self, events, keys):
        #processing defers based on whether pause displayed or not
        #no key inputs are taken if pause screen displayed so user cannot play when pause displayed
        if not self.pause_bool:
            self.user.movement(keys)
            self.collision_check(keys)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.clicking_sound.play()
                        self.pause_bool = True
        else:
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    if self.quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.quit_button = self.quit_button_alternate
                    else:
                        self.quit_button = pygame.image.load('./media/quit.png')
            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_screen_rect.collidepoint(pygame.mouse.get_pos()):
                        self.clicking_sound.play()
                        self.pause_bool = False
                    if self.quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.clicking_sound.play()
                        self.next = Home()

    def Update(self):
        #does not update if pause screen displayed
        if not self.pause_bool:
            self.user.moving_counter = (self.user.moving_counter+1)%8
            self.user.idle_counter = (self.user.idle_counter+1)%12
            self.screen_move()
            self.platforms.add_new(self.score)
            if self.user.rect.top >= App.screen_height:
                self.next = Quit(self.score)

    def Render(self):
        #display varies based on whether pause screen is displayed
        if not self.pause_bool:
            App.screen.blit(self.background, (0, -500))
            self.platforms.update()
            App.screen.blit(self.pause_button, (400, 15))
            self.text_render()
            self.user.update()

        else:
            App.screen.blit(self.background, (0, 0))
            App.screen.blit(self.jungle_jumper_img, (38,40))
            App.screen.blit(self.quit_button, (160,320))
            App.screen.blit(self.pause_button_screen, (188, 140))
        pygame.display.update()

    
    def collision_check(self, keys):
        if self.user.vel.y > 0:
            for plat in self.platforms.good:
                if self.user.rect.colliderect(plat):
                    #math involved with how player is placed on a good platform
                    image = pygame.Surface((plat[2],plat[3]))
                    image_rect = image.get_rect(topleft=(plat[0],plat[1]))
                    self.user.pos.y = image_rect.top - self.user.rect.height 
                    self.user.vel.y = 0
                    #player only able to jump when they have collided with a platforms
                    self.user.jump(keys)
            
            for plat in self.platforms.dangerous:
                #if player collides with a dangerous platerform game ends
                if self.user.rect.colliderect(plat):
                    self.next = Quit(self.score)  

    def text_render(self):
        #used for displaying score
        font = pygame.font.SysFont('Cambria', 50)
        text = font.render(str(self.score), False, (204, 204, 0))
        text_rect = text.get_rect(center=(App.screen_width / 2, App.screen_height - 470))  
        App.screen.blit(text, text_rect)

    def screen_move(self):
        #moves screen and updates score so player has more platforms to jump on
        if self.user.rect.top <= App.screen_height * 0.25:
            if self.user.pos.y != self.user.prev_y:
                self.score += 10
            #updates player position for effect of moving screen
            self.user.pos.y += abs(self.user.vel.y)
            self.user.prev_y = self.user.pos.y

            #updates good platforms for effect of moving screen
            for plat_counter, plat in enumerate(self.platforms.good):
                self.platforms.good.remove(plat)
                moved_plat = (plat[0], plat[1] + abs(self.user.vel.y), plat[2], plat[3])
                self.platforms.good.insert(plat_counter, moved_plat)
                image = pygame.Surface((moved_plat[2],moved_plat[3]))
                image_rect = image.get_rect(topleft=(moved_plat[0],moved_plat[1]))
                if image_rect.top >= App.screen_height:
                    self.platforms.good.remove(moved_plat)

            #updates dangerous platforms for effect of moving screen
            for plat_counter, plat in enumerate(self.platforms.dangerous):
                self.platforms.dangerous.remove(plat)
                moved_plat = (plat[0], plat[1] + abs(self.user.vel.y), plat[2], plat[3])
                self.platforms.dangerous.insert(plat_counter, moved_plat)
                image = pygame.Surface((moved_plat[2],moved_plat[3]))
                image_rect = image.get_rect(topleft=(moved_plat[0],moved_plat[1]))
                if image_rect.top >= App.screen_height:
                    self.platforms.dangerous.remove(moved_plat)

class Quit(Scene):
    """Scene for game end"""
    def __init__(self, score):
        super().__init__()
        self.music = pygame.mixer.Sound('./media/fails.WAV')
        self.music.play()
        self.clicking_sound = pygame.mixer.Sound("./media/clicks.WAV")

        self.score = str(score)
        self.background = pygame.image.load('./media/background.jpg')
        self.score_image = pygame.image.load('./media/your score.png')

        self.quit_button = pygame.image.load('./media/quit.png')
        self.quit_button_alternate = pygame.image.load('./media/DarkQuit.png')
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.topleft = (160,380)

        self.replay_button = pygame.image.load('./media./replay.png')
        self.replay_button_alternate = pygame.image.load('./media/Darkreplay.png')
        self.replay_button_rect = self.replay_button.get_rect()
        self.replay_button_rect.topleft = (140, 287)

    def ProcessInput(self, events, keys):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.quit_button = self.quit_button_alternate
                else:
                    self.quit_button = pygame.image.load('./media/quit.png')
                if self.replay_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.replay_button = self.replay_button_alternate
                else:
                    self.replay_button = pygame.image.load('./media./replay.png')
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicking_sound.play()
                    self.next = Home()
                if self.replay_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicking_sound.play()
                    self.music.stop()
                    #allows user to start a new game
                    self.next = Game()

    def Render(self):
        App.screen.blit(self.background,(0, 0))
        App.screen.blit(self.score_image, (88,40))
        App.screen.blit(self.quit_button, (160,380))
        App.screen.blit(self.replay_button, (140, 287))
        self.text_render()
        pygame.display.update()
        
    def text_render(self):
        font = pygame.font.SysFont('Cambria', 100)
        text = font.render(self.score, False, (0, 153, 51))
        text_rect = text.get_rect(center=(App.screen_width/2, (App.screen_height/2) - 50)) 
        App.screen.blit(text, text_rect)

class Player:
    """Class for player in game"""
    def __init__(self):
        cor_x_initial = App.screen_width * 0.5
        cor_y_initial = App.screen_height - 40
        #coordinates requirement for player movement math and collision detection
        self.prev_y = cor_y_initial
        self.pos = pygame.math.Vector2(cor_x_initial, cor_y_initial)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.img = pygame.image.load('./media/idle.gif')
        self.rect = self.img.get_rect(topleft=(int(cor_x_initial), int(cor_y_initial)))

        #images for player movements
        self.player_idle_imgs = [pygame.image.load('./media/still1.png'), pygame.image.load('./media/still2.png'),
               pygame.image.load('./media/still3.png'), pygame.image.load('./media/still4.png'),
               pygame.image.load('./media/still5.png'), pygame.image.load('./media/still6.png'),
               pygame.image.load('./media/still7.png'), pygame.image.load('./media/still8.png'),
               pygame.image.load('./media/still9.png'), pygame.image.load('./media/still10.png'),
               pygame.image.load('./media/still11.png'), pygame.image.load('./media/still12.png')]
        self.move_right_imgs = [pygame.image.load('./media/RR_1.png'), pygame.image.load('./media/RR_2.png'),
                pygame.image.load('./media/RR_3.png'), pygame.image.load('./media/RR_4.png'),
                pygame.image.load('./media/RR_5.png'), pygame.image.load('./media/RR_6.png'),
                pygame.image.load('./media/RR_7.png'), pygame.image.load('./media/RR_8.png')]
        self.move_left_imgs = [pygame.image.load('./media/RL_1.png'), pygame.image.load('./media/RL_2.png'),
                    pygame.image.load('./media/RL_3.png'), pygame.image.load('./media/RL_4.png'),
                    pygame.image.load('./media/RL_5.png'), pygame.image.load('./media/RL_6.png'),
                    pygame.image.load('./media/RL_7.png'), pygame.image.load('./media/RL_8.png')]
        self.jump_imgs = pygame.image.load('./media/jump_right.png')
        self.jumping_sounds = pygame.mixer.Sound('./media/jumpSounds.WAV')

        #booleans for player movement affecting animations and what player does on screen
        self.moving_left = False
        self.moving_right = False
        self.jumping = False

        #used to determine what image is displayed of player for animation
        self.moving_counter = 0
        self.idle_counter = 0

    def movement(self, keys):
        #math processing for player moving including moving right, left and jumping
        self.acc = pygame.math.Vector2(0, 0.8)
        if keys[pygame.K_LEFT]: 
            self.acc.x = -0.7
            self.moving_left = True
            self.moving_right = False
        elif keys[pygame.K_RIGHT]:
            self.acc.x = 0.7
            self.moving_left = False
            self.moving_right = True
        else:
            self.moving_left = False
            self.moving_right = False
                    
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
                
        if self.pos.x > App.screen_width:
            self.pos.x  = 0
        if self.pos.x < 0:
            self.pos.x = App.screen_width

        self.rect.topleft = self.pos
    
    def jump(self, keys):
        #defines player jumping movement
        App.clock.tick(45)
        if keys[pygame.K_UP]:
            self.jumping = True
            self.jumping_sounds.play()
            self.vel.y = -20
        else:
            self.jumping = False

    def update(self):
        if self.moving_left:
            App.screen.blit(self.move_left_imgs[self.moving_counter], (self.pos))
        elif self.moving_right:
            App.screen.blit(self.move_right_imgs[self.moving_counter], (self.pos))
        elif self.jumping:
            App.screen.blit(self.jump_imgs, (self.pos))
        else:
            App.screen.blit(self.player_idle_imgs[self.idle_counter], (self.pos))

class Platforms:
    """Class for game platforms"""
    def __init__(self):
        #lists used to store good and dangerous platforms of a game
        self.dangerous = [(80, 400, 100, 20),(300, 50, 80, 20)]
        self.good = [(0, App.screen_height - 40, App.screen_width, 40), (App.screen_width/2, App.screen_height * .7, 120, 20),
             (125, 190, 100, 20), (320, 120, 100, 20), (175, 60, 50, 20)]

    def add_new(self, score):
        #adds new platforms when there aren't enough platforms on the screen
        #platform sizes become smaller as player score increases
        while len(self.good) < 6:
            if score > 5000:
                width = random.randrange(30, 50)
            elif score > 2500:
                width = random.randrange(40, 65)
            else:
                width = random.randrange(55, 85)

            cor_y = random.randrange(-40, 0)
            for plat in self.good:
                while abs(cor_y - plat[1]) < 20:
                    cor_y = random.randrange(-40, 0)
            self.good.append((random.randrange(0, App.screen_width-width),cor_y, width, 20))
            
        while len(self.dangerous) < 4:
            if score > 10000:
                width = random.randrange(60, 85)
            elif score> 5000:
                width = random.randrange(50, 70)
            else:
                width = random.randrange(40, 65)

            cor_y = random.randrange(-40, 0)
            for plat in self.good:
                while abs(cor_y - plat[1]) < 20:
                    cor_y = random.randrange(-40, 0)
            self.dangerous.append((random.randrange(0, App.screen_width-width), cor_y, width, 20))

    def update(self):
        #displays platforms
        for plat in self.good:
            picture = pygame.image.load('./media/platform_1.png')
            picture = pygame.transform.scale(picture, (plat[2], plat[3]))
            rect = picture.get_rect()
            rect = rect.move((plat[0], plat[1]))
            App.screen.blit(picture, rect)

        for plat in self.dangerous:
            picture = pygame.image.load('./media/platform_2.png')
            picture = pygame.transform.scale(picture, (plat[2], plat[3]))
            rect = picture.get_rect()
            rect = rect.move((plat[0], plat[1]))
            App.screen.blit(picture, rect)

def start_app():
    #function used to instantiate app
    app = App("Jungle Jumper")

start_app()