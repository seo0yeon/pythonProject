import pygame
import sys
import random

class Snow(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, snow_image):
        super().__init__()
        self.image = pygame.image.load(snow_image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width) 
        self.rect.y = random.randint(-screen_height, 0) 
        self.speed = random.randint(1, 3)  
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600: 
            self.rect.y = random.randint(-600, 0) 
            self.rect.x = random.randint(0, 800)

#INTRO
class Intro:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("휴강이 필요해!")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.font = self.font = pygame.font.Font("impact.ttf", 40)

        self.img_intro_bg = pygame.image.load("start_bg.png")
        self.img_intro_explain = pygame.image.load("explain_intro.png")

        self.start_button = pygame.Rect(550, 290, 200, 60)
        self.exit_button = pygame.Rect(550, 370, 200, 60)
        self.info_button = pygame.Rect(550, 450, 200, 60)

        self.text_start = self.font.render("Start", True, (0, 0, 0))
        self.text_exit = self.font.render("Exit", True, (0, 0, 0))
        self.text_info = self.font.render("Explain", True, (0, 0, 0))
        self.text_start_rect = self.text_start.get_rect(center=self.start_button.center)
        self.text_exit_rect = self.text_exit.get_rect(center=self.exit_button.center)
        self.text_info_rect = self.text_info.get_rect(center=self.info_button.center)

        self.snow_group = pygame.sprite.Group()
        for _ in range(100):  
            snowflake = Snow(800, 600, "snowflake.png") 
            self.snow_group.add(snowflake)

    def render(self):
        current_screen_size = self.screen.get_size()
        is_fullscreen = pygame.FULLSCREEN & pygame.display.get_surface().get_flags()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
                        current_screen_size = self.screen.get_size()
                        is_fullscreen = True
                    if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode((800, 600))
                        current_screen_size = self.screen.get_size()
                        is_fullscreen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        return ("START", current_screen_size, is_fullscreen)
                    if self.exit_button.collidepoint(event.pos):
                        return ("EXIT", current_screen_size, is_fullscreen)
                    if self.info_button.collidepoint(event.pos):
                        result = self.intro_info(current_screen_size, is_fullscreen)
                        if result == "BACK":
                            if is_fullscreen:
                                self.screen = pygame.display.set_mode(current_screen_size, pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode(current_screen_size)
                            continue
                        return (result, current_screen_size, is_fullscreen)

            self.screen.blit(self.img_intro_bg, (0, 0))

            self.snow_group.update()
            self.snow_group.draw(self.screen)

            pygame.draw.rect(self.screen, (255, 255, 255), self.start_button)
            pygame.draw.rect(self.screen, (255, 255, 255), self.exit_button)
            pygame.draw.rect(self.screen, (255, 255, 255), self.info_button)

            self.screen.blit(self.text_start, self.text_start_rect)
            self.screen.blit(self.text_exit, self.text_exit_rect)
            self.screen.blit(self.text_info, self.text_info_rect)

            pygame.display.update()
            self.clock.tick(30)

    def intro_info(self, screen_size, is_fullscreen):
        back_button = pygame.Rect(0, 0, 100, 50)  

        if is_fullscreen:
            self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_size)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                    if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode(screen_size)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        return "BACK"
            
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.img_intro_explain, (0, 0))

            pygame.display.update()
            self.clock.tick(30)


#시나리오
class ScenarioSet:
    def __init__(self):
        self.scenario_sets = [
            {"images": ["scenario_intro1.png", "scenario_intro2.png", "scenario_intro3.png", "scenario_intro4.png"], "bgm": "introBGM.ogg"},
            {"images": ["scenario_battle1.png", "scenario_battle2.png"], "bgm": "scenarioBGM.ogg"},
            {"images": ["scenario_ending1.png", "scenario_ending2.png", "scenario_ending3.png"], "bgm": "endingBGM.ogg"},
        ]

    def get_scenario_set(self, index):
        return self.scenario_sets[index]

class Scenario:
    def __init__(self, images, bgm, screen_size, is_fullscreen):
        pygame.init()
        if is_fullscreen:
            self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        
        self.images = images
        self.img_wordballoon_intro1 = pygame.transform.scale(pygame.image.load("word_balloon_intro1.png"),(250, 125))
        self.img_wordballoon_intro2 = pygame.transform.scale(pygame.image.load("word_balloon_intro2.png"),(300, 150))
        self.img_chara_intro = pygame.transform.scale(pygame.image.load("lamb3_run.png"), (250, 250))
        self.wordballoon1_pos = (400, 300)
        self.wordballoon2_pos = (400, 250)
        self.chara_intro_pos = (150, 300)
        self.bgm = bgm

    def run(self):
        pygame.mixer.music.load(self.bgm)
        pygame.mixer.music.play(-1)

        for image_path in self.images:
            image = pygame.image.load(image_path).convert()
            image = pygame.transform.scale(image, self.screen.get_size())
            self.screen.blit(image, (0, 0))

            if "scenario_intro3.png" in image_path:
                self.screen.blit(self.img_wordballoon_intro1, self.wordballoon1_pos)
            elif "scenario_intro4.png" in image_path:
                self.screen.blit(self.img_chara_intro, self.chara_intro_pos)
                self.screen.blit(self.img_wordballoon_intro2, self.wordballoon2_pos)
            pygame.display.flip()

            waiting = True
            while waiting:  
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                        elif event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                           self.screen = pygame.display.set_mode(screen_size)
                        elif event.key == pygame.K_RETURN:
                            waiting = False 

#RUNNER GAME
class CharaRun(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(topleft=(-40, 250))
        self.initial_position = (-40, 250)
        self.mask = pygame.mask.from_surface(self.image)

        self.jump = False
        self.double_jump = False
        self.double_jump_allowed = False
        self.jump_progress = 0
        self.jump_height = 300
        self.jump_speed = 15
        self.animation_speed = 3
        self.frame = 0

    def update(self, tmr):
        if tmr % self.animation_speed == 0:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
        
        if self.jump:
            if self.jump_progress < self.jump_height:
                self.rect.y -= self.jump_speed
                self.jump_progress += self.jump_speed
            elif self.jump_progress < 2 * self.jump_height:
                self.rect.y += self.jump_speed
                self.jump_progress += self.jump_speed
            else:
                self.jump = False
                self.jump_progress = 0
                if self.double_jump: 
                    self.double_jump = False
                    self.double_jump_allowed = True
                    self.rect.topleft = self.initial_position  
                else:  
                    self.double_jump_allowed = True

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.jump = False
            self.double_jump = False
            self.double_jump_allowed = True

        
class EnemyRun(pygame.sprite.Sprite):
    def __init__(self, image1, image2):
        super().__init__()
        self.image1 = image1
        self.image2 = image2
        self.original_image = self.image1
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(800, 400))
        self.mask = pygame.mask.from_surface(self.image)
        self.count = 0
        self.spawn = True
        self.reset_time()

    def reset_time(self):
        if self.count < 9:
            self.spawn_time = random.randint(20, 60)
            self.rect.x = 800
            self.spawn = True
            self.set_random_size()
            self.set_random_obstacle()

    def set_random_size(self):
        scale_factor = random.uniform(0.5, 1.5)  
        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def set_random_obstacle(self):
        self.original_image = random.choice([self.image1, self.image2])
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed):
        if self.count >= 9:
            self.spawn = False
            return
        
        if self.spawn_time > 0:
            self.spawn_time -= 1
        elif self.spawn:
            self.rect.x -= speed
            if self.rect.right < 0:
                self.spawn = False
                self.count += 1
                self.reset_time()

class GameOverRun:
    def __init__(self, screen):
        self.screen = screen
        pygame.mixer.music.stop()
        self.background = pygame.image.load("Gameover.png")
        self.font = pygame.font.Font("BusanFont_Provisional.ttf", 18)
        self.button_text = self.font.render("Try Again!", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(400, 400))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, (100, 100, 100), self.button_rect)
        self.screen.blit(self.button_text, self.button_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    return True
        return None

    def run(self):
        while True:
            result = self.handle_events()
            if result is not None:
                return result
            self.draw()
            pygame.display.flip()


class RunGame:
    def __init__(self, screen_size, is_fullscreen):
        pygame.init()
        if is_fullscreen:
            self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.img_run_bg = pygame.transform.scale(pygame.image.load("run_bg.png"), screen_size)
        self.img_headband_bg = pygame.image.load("headband_run_bg.png")
        self.img_shalom_bg = pygame.image.load("shalom_run_bg.png")
        self.img_enemy1 = pygame.transform.scale(pygame.image.load("obstacle_run.png"), (190, 130))
        self.img_enemy2 = pygame.transform.scale(pygame.image.load("obstacle1_run.png"), (300, 200))
        self.img_chara =[
            pygame.transform.scale(pygame.image.load("lamb_run.png"), (300, 300)),
            pygame.transform.scale(pygame.image.load("lamb1_run.png"), (300, 300))
        ]
        self.img_hp = pygame.transform.scale(pygame.image.load("hp_run_pic.png"), (50, 50))

        pygame.mixer.init()
        pygame.mixer.music.load("run_bgm.ogg")
        pygame.mixer.music.play(-1)
        self.jump_sound = pygame.mixer.Sound("Jump.ogg")
        
        self.scroll_speed = 10
        self.scroll_offset = 0
        self.current_bg = "headband"
        self.run_count = 0
        self.bg_width = screen_size[0]
        self.enemy_count_reached = False

        self.hp = 3
        self.unbeatable = False 
        self.unbeatable_timer = 0  

        self.chara = CharaRun(self.img_chara)
        self.enemy = EnemyRun(self.img_enemy1, self.img_enemy2)
        self.all_sprites = pygame.sprite.Group(self.chara, self.enemy)

    def run(self):
        tmr = 0
        while True:
            tmr += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
                    if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode((800, 600))
                    if event.key == pygame.K_SPACE:
                        if not self.chara.jump:
                            self.chara.jump = True
                            self.jump_sound.play()
                        elif self.chara.double_jump_allowed and not self.chara.double_jump:
                            self.chara.double_jump = True
                            self.chara.jump = True
                            self.chara.jump_progress = 0
                            self.jump_sound.play()

            result = self.update_game_bg(tmr)
            if result == "GAMEOVER":
                return "GAMEOVER"
            elif result == "RUNCLEAR":
                self.render() 
                pygame.display.flip()
                return "RUNCLEAR"
            
            self.render()
            self.clock.tick(30)

    def update_game_bg(self, tmr):
        if self.current_bg == "headband":
            self.scroll_offset += self.scroll_speed
            if self.scroll_offset >= self.bg_width:
                    self.scroll_offset = 0
                    self.current_bg = "run"

        elif self.current_bg == "run":
            self.scroll_offset += self.scroll_speed
            if self.scroll_offset >= self.bg_width:
                self.scroll_offset = 0
                if self.enemy_count_reached:
                    self.run_count += 1
                    if self.run_count >= 2: 
                        self.current_bg = "shalom"
            if self.enemy.count >= 9 and not self.enemy_count_reached:
                self.enemy_count_reached = True

        elif self.current_bg == "shalom":
            return "RUNCLEAR"

        self.chara.update(tmr)
        self.enemy.update(self.scroll_speed)

        if self.unbeatable:
            self.unbeatable_timer -= 1
            if self.unbeatable_timer <= 0:
                self.unbeatable = False

        if not self.unbeatable and pygame.sprite.collide_mask(self.chara, self.enemy):
            self.hp -= 1
            self.unbeatable = True
            self.unbeatable_timer = 60

            if self.hp <= 0:
                return "GAMEOVER"
        
    def render(self):
        self.screen.fill((0, 0, 0))

        if self.current_bg == "headband":
            self.screen.blit(self.img_headband_bg, (-self.scroll_offset, 0))
            self.screen.blit(self.img_run_bg, (-self.scroll_offset + self.bg_width, 0))
        elif self.current_bg == "run":
            self.screen.blit(self.img_run_bg, (-self.scroll_offset, 0))
            self.screen.blit(self.img_run_bg, (-self.scroll_offset + self.bg_width, 0))
        elif self.current_bg == "shalom":
            self.screen.blit(self.img_shalom_bg, (0, 0))

        for i in range(self.hp):
            self.screen.blit(self.img_hp, (10 + i * 60, 10))

        self.all_sprites.draw(self.screen)

        pygame.display.update()



#SHOOTING GAME

class ShootingGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FPS = 60

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_path = "./BUSANFONT_PROVISIONAL.TTF"
        self.font = pygame.font.Font(self.font_path, 36)
        self.background_image = pygame.image.load("shootinggame_bg.png")
        self.intro_music = "scenarioBGM.ogg"
        self.gameplay_music = "shootinggameBGM.ogg"

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = PlayerShoot(self)
        self.enemy = EnemyShoot(self)
        self.all_sprites.add(self.player, self.enemy)

        self.hits_on_projectiles = 0

    def draw_lives(self):
        heart_image = pygame.image.load("p_heart.png")
        heart_image = pygame.transform.scale(heart_image, (40, 40))
        for i in range(self.player.lives):
            self.screen.blit(heart_image, (10 + i * 35, 10))

    def draw_hits(self):
        hits_text = self.font.render(f"{self.hits_on_projectiles}", True, self.BLACK)
        self.screen.blit(hits_text, (self.WIDTH - hits_text.get_width() - 20, 20))

    def show_scenario(self, images):
        current_image = 0
        running = True
        while running:
            self.clock.tick(self.FPS)
            self.screen.fill(self.WHITE)
            self.screen.blit(images[current_image], (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        current_image += 1
                        if current_image >= len(images):
                            running = False

    def run(self):
        pygame.mixer.music.load(self.intro_music)
        pygame.mixer.music.play(-1)

        intro_images = [pygame.image.load(f"scenario_{i}.png") for i in range(1, 4)]
        self.show_scenario(intro_images)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.gameplay_music)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            self.clock.tick(self.FPS)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

            self.player.update(keys)
            for sprite in self.all_sprites:
                if sprite != self.player:
                    sprite.update()

            if pygame.sprite.spritecollideany(self.player, self.projectiles):
                self.player.lives -= 1
                for projectile in self.projectiles:
                    if projectile.rect.colliderect(self.player.rect):
                        projectile.kill()

                if self.player.lives <= 0:
                    game_over = ShootingGameOver(self)
                    if game_over.run():
                        self.__init__()
                        pygame.mixer.music.load(self.gameplay_music)
                        pygame.mixer.music.play(-1)
                        continue
                    else:
                        pygame.quit()
                        sys.exit()

            hits = pygame.sprite.groupcollide(self.projectiles, self.bullets, True, True)
            self.hits_on_projectiles += len(hits)

            if self.hits_on_projectiles >= 10:
                victory_images = [pygame.image.load(f"victory_{i}.png") for i in range(1, 3)]
                self.show_scenario(victory_images)
                return "SHOOTINGCLEAR" 

            self.screen.blit(pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT)), (0, 0))
            self.all_sprites.draw(self.screen)
            self.draw_lives()
            self.draw_hits()
            pygame.display.flip()

class PlayerShoot(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        player_image = pygame.image.load("lamb_shooting.png")
        self.image = pygame.transform.scale(player_image, (130, 130))
        self.rect = self.image.get_rect()
        self.rect.center = (100, game.HEIGHT // 2)
        self.speed = 5
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.game.HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery, self.game)
        self.game.bullets.add(bullet)
        self.game.all_sprites.add(bullet)

class EnemyShoot(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        enemy_image = pygame.image.load("shooting_enemy.png")
        self.image = pygame.transform.scale(enemy_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (game.WIDTH - 50, game.HEIGHT // 2)
        self.speed = 2
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.top <= 0 or self.rect.bottom >= self.game.HEIGHT:
            self.direction *= -1
        self.throw_projectile()

    def throw_projectile(self):
        if random.random() < 0.02:
            projectile = Projectile(self.rect.centerx, self.rect.centery, self.game)
            self.game.projectiles.add(projectile)
            self.game.all_sprites.add(projectile)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        projectile_image = pygame.image.load("projectile.png")
        self.image = pygame.transform.scale(projectile_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = (game.player.rect.centerx - x) / 50
        self.speed_y = random.uniform(-1, 1) * 3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0 or self.rect.top > self.game.HEIGHT or self.rect.bottom < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        bullet_image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(bullet_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > self.game.WIDTH:
            self.kill()

class ShootingGameOver:
    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load("Gameover.png")
        self.font = pygame.font.Font(game.font_path, 20)
        self.button_text = self.font.render("Try Again!", True, game.WHITE)
        self.button_rect = self.button_text.get_rect(center=(game.WIDTH // 2, 400))

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.game.screen, (100, 100, 100), self.button_rect)
        self.game.screen.blit(self.button_text, self.button_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    return "ShootRestart"
        return None

    def run(self):
        while True:
            result = self.handle_events()
            if result == "quit":
                pygame.quit()
                sys.exit()
            elif result == "ShootRestart":
                return True
            self.draw()
            pygame.display.flip()


#BATTLE GANE

class BattleGameOver:
    def __init__(self, screen):
        self.screen = screen
        pygame.mixer.music.stop()
        self.background = pygame.image.load("Gameover.png").convert()
        self.font = pygame.font.Font("BusanFont_Provisional.ttf", 18)
        self.try_again_button = pygame.Rect(350, 400, 100, 50)
        self.button_text = self.font.render("Try Again!", True, (255, 255, 255))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.try_again_button.collidepoint(event.pos):
                        return "restart"
            
            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, (0, 0, 255), self.try_again_button)
            self.screen.blit(self.button_text, (self.try_again_button.x + 10, self.try_again_button.y + 10))
            pygame.display.flip()

class Victory:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        pygame.mixer.music.stop()
        self.win_bg = pygame.transform.scale(pygame.image.load("win.png").convert(), self.screen_size)
        self.victory_bg = pygame.transform.scale(pygame.image.load("victory.png").convert(), self.screen_size)
        self.lamb_img = pygame.transform.scale(pygame.image.load("cryinglamb.png").convert_alpha(),(300, 300))
        self.font = pygame.font.Font("BusanFont_Provisional.ttf",20)
        self.text_list = [
            "집에 언제가",
            "나 보내줘",
            "제발..."
        ]
        self.text_index = 0
        self.lamb_y = 300
        self.jump_count = 0
        self.max_jumps = 3
        self.jump_direction = -1
        button_x = (self.screen_size[0] - 100)
        button_y = self.screen_size[1] - 50
        self.end_button = pygame.Rect(button_x, button_y, 100, 50)
        self.button_text = self.font.render("집 가기", True, (0, 0, 0))

    def run(self):
        self.show_win()
        pygame.time.wait(3000)

        scenario_set = ScenarioSet()
        scenario_data = scenario_set.get_scenario_set(2)
        scenario = Scenario(scenario_data["images"], scenario_data["bgm"], (800, 600), False)
        scenario.run()

        self.start_victory()

    def show_win(self):
        self.screen.blit(self.win_bg, (0, 0))
        pygame.display.flip()

    def start_victory(self):
        pygame.mixer.music.load('endingBGM.ogg')
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.show_next_text()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.end_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.screen.blit(self.victory_bg, (0, 0))
            self.screen.blit(self.lamb_img, (200, self.lamb_y))
            self.jump_animation()
            text_surface = self.font.render(self.text_list[self.text_index], True, (255, 255, 255))
            self.screen.blit(text_surface, (450, 200))
            pygame.draw.rect(self.screen, (173, 216, 230), self.end_button)
            self.screen.blit(self.button_text, (self.end_button.x + 10, self.end_button.y + 10))
            pygame.display.flip()
            clock.tick(60)

    def jump_animation(self):
        jump_height = 100
        jump_speed = 5
        if self.lamb_y <= 300 - jump_height:
            self.jump_direction = 1
        elif self.lamb_y >= 300:
            self.jump_direction = -1
            self.jump_count += 1
            if self.jump_count >= self.max_jumps:
                return
        self.lamb_y += self.jump_direction * jump_speed

    def show_next_text(self):
        if self.text_index < len(self.text_list) - 1:
            self.text_index += 1

class BattleGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.initialize_sounds()
        self.load_images()
        self.lamb = GameCharBattle("람브", 100, 13, 0.3, 150, 350, self.lamb_img)
        self.villain = GameCharBattle("총장님", 100, 15, 0.2, 520, 320, self.villain_img)
        self.current_turn = "lamb"
        self.battle_msg = ""
        self.crit_msg = ""
        self.speech_bubble = None
        self.bubble_text = ""
        self.font = pygame.font.Font("BusanFont_Provisional.ttf", 20)

    def initialize_sounds(self):
        self.lamb_hit = pygame.mixer.Sound('lamb_attack.ogg')
        self.villain_hit = pygame.mixer.Sound('villain_attack.ogg')
        pygame.mixer.music.load('battleBGM.ogg')
        pygame.mixer.music.play(-1)

    def load_images(self):
        self.bg = pygame.image.load("battlegame.png").convert()
        self.lamb_img = pygame.image.load("battlelamb.png").convert_alpha()
        self.villain_img = pygame.image.load("villain.png").convert_alpha()

    def lamb_attack(self):
        if self.current_turn == "lamb":
            self.reset_messages()
            self.lamb_hit.play()
            self.lamb.do_attack(self.villain, self)
            self.show_message(self.lamb, "lamb")
            self.check_game_over()
            self.switch_to_villain_turn()

    def lamb_heal(self):
        if self.current_turn == "lamb":
            self.reset_messages()
            heal_amount = 15
            self.lamb.hp = min(100, self.lamb.hp + heal_amount)
            self.battle_msg = "람브가 15 hp 만큼 회복 !"
            self.switch_to_villain_turn()

    def villain_turn(self):
        if self.current_turn == "villain":
            self.reset_messages()
            action = random.choice(["attack", "attack", "heal"])
            if action == "attack":
                self.villain_hit.play()
                self.villain.do_attack(self.lamb, self)
                self.show_message(self.villain, "villain")
            else:
                heal_amount = 15
                self.villain.hp = min(100, self.villain.hp + heal_amount)
                self.battle_msg = "총장님이 15 hp 만큼 회복 !"
            self.check_game_over()
            self.switch_to_lamb_turn()

    def reset_messages(self):
        self.battle_msg = ""
        self.crit_msg = ""

    def switch_to_villain_turn(self):
        self.current_turn = "villain"
        pygame.time.set_timer(pygame.USEREVENT, 1200)

    def switch_to_lamb_turn(self):
        self.current_turn = "lamb"

    def show_message(self, char, who):
        if who == "lamb":
            msg_list = [
                "이 날씨에 학교라니",
                "편도로 두시간이 걸렸어",
                "달구지 운행도 못하는데",
                "지하철이 안와",
                "학교가 빙판길이야"
            ]
        else:
            msg_list = [
                "학생이 학교를 나와야지",
                "이 정도는 견뎌내",
                "시험 전에 휴강은 안돼",
                "무단결석은 없길 바란다",
                "나도 출근했단다",
                
            ]
        self.bubble_text = random.choice(msg_list)
        self.speech_bubble = (char.x, char.y - 30)

    def hp_bar(self, x, y, current_hp, max_hp, width=200, height=20):
        pygame.draw.rect(self.screen, (128, 128, 128), (x, y, width, height))
        hp_ratio = current_hp / max_hp
        bar_width = int(width * hp_ratio)
        bar_color = (0, 255, 0) if hp_ratio > 0.5 else (255, 165, 0) if hp_ratio > 0.25 else (255, 0, 0)
        pygame.draw.rect(self.screen, bar_color, (x, y, bar_width, height))
        hp_text = f"{current_hp}/{max_hp}"
        text_surface = self.font.render(hp_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
        self.screen.blit(text_surface, text_rect)

    def check_game_over(self):
        if self.lamb.hp <= 0:
            self.restart_game()
        elif self.villain.hp <= 0:
            self.show_victory()

    def restart_game(self):
        game_over = BattleGameOver(self.screen)
        result = game_over.run()
        if result == "restart":
            self.__init__()

    def show_victory(self):
        victory = Victory(self.screen)
        victory.run()
        pygame.quit()
        sys.exit()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.current_turn == "lamb":
                        self.lamb_attack()
                    elif event.key == pygame.K_UP and self.current_turn == "lamb":
                        self.lamb_heal()
                elif event.type == pygame.USEREVENT:
                    self.villain_turn()

            self.lamb.update_attack_motion()
            self.villain.update_attack_motion()

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.lamb.img, (self.lamb.x, self.lamb.y))
            self.screen.blit(self.villain.img, (self.villain.x, self.villain.y))

            self.hp_bar(10, 570, self.lamb.hp, 100)
            self.hp_bar(590, 570, self.villain.hp, 100)
            
            battle_text_color = (255, 0, 0) if "필살기" in self.battle_msg else (0,100 , 0) if "회복" in self.battle_msg else (0, 0, 0)

            battle_text = self.font.render(self.battle_msg, True, battle_text_color)
            self.screen.blit(battle_text, (400 - battle_text.get_width() // 2, 120))
            
            if self.crit_msg:
                crit_text = self.font.render(self.crit_msg, True, (255, 0, 0))
                self.screen.blit(crit_text, (400 - crit_text.get_width() // 2, 80))

            if self.speech_bubble:
                pygame.draw.rect(self.screen, (255, 255, 255), (self.speech_bubble[0], self.speech_bubble[1] - 60, 230, 50))
                bubble_text = self.font.render(self.bubble_text, True, (0, 0, 0))
                self.screen.blit(bubble_text, (self.speech_bubble[0] + 10, self.speech_bubble[1] - 50))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

class GameCharBattle:
    def __init__(self, name, hp, power, critical, x, y, img):
        self.name = name
        self.hp = hp
        self.power = power
        self.critical = critical
        self.x = x
        self.y = y
        self.img = img
        self.is_attacking = False
        self.attack_frames = 0
        self.original_pos = (x, y)

    def do_attack(self, target, game):
        if random.random() < self.critical:
            damage = self.power * 2
            game.battle_msg = f"{self.name}의 필살기 공격!"
        else:
            damage = self.power
            game.battle_msg = f"{self.name}의 공격!"
        target.hp = max(target.hp - damage, 0)
        self.is_attacking = True
        self.attack_frames = 0

    def update_attack_motion(self):
        if self.is_attacking:
            if self.attack_frames < 5:
                self.x += 2
                self.y += 2
            elif self.attack_frames < 10:
                self.x -= 2
                self.y -= 2
            else:
                self.is_attacking = False
                self.x, self.y = self.original_pos
            self.attack_frames += 1
            

if __name__ == '__main__':
    while True:
        intro = Intro()
        result, screen_size, is_fullscreen = intro.render()

        if result == "START":
            if is_fullscreen:
                pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
            else:
                pygame.display.set_mode(screen_size)
            
            scenario_set = ScenarioSet()
            scenario_data = scenario_set.get_scenario_set(0)
            scenario = Scenario(scenario_data["images"], scenario_data["bgm"], screen_size, is_fullscreen)
            scenario.run()

            waiting = True
            while waiting == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            waiting = False

            while True:
                rungame = RunGame(screen_size, is_fullscreen)
                run_game_result = rungame.run()

                if run_game_result == "GAMEOVER":
                    game_over = GameOverRun(rungame.screen)
                    restart_result = game_over.run()
                    if restart_result == "True":
                        continue
                elif run_game_result == "RUNCLEAR":
                    shalom_screen = True
                    img_lamb_run = pygame.transform.scale(pygame.image.load("lamb_run.png"), (300, 300))
                    while shalom_screen:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                                    shalom_screen = False

                        rungame.screen.fill((0, 0, 0))
                        rungame.screen.blit(rungame.img_shalom_bg, (0, 0))
                        rungame.screen.blit(img_lamb_run, (-40, 250))
                        pygame.display.flip()

                    shooting_game = ShootingGame()
                    shoot_game_result = shooting_game.run()

                    if shoot_game_result == "SHOOTINGCLEAR":
                        scenario_set = ScenarioSet()
                        scenario_data = scenario_set.get_scenario_set(1)
                        scenario = Scenario(scenario_data["images"], scenario_data["bgm"], screen_size, is_fullscreen)
                        scenario.run()
                        battle_game = BattleGame()
                        battle_game.run()

        elif result == "EXIT":
            pygame.quit()
            sys.exit()