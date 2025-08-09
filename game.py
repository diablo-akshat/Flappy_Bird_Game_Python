import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()

class Game:
    def __init__(self):
        self.width, self.height = 600, 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Flappy Bird - Smooth DT Version")

        self.clock = pg.time.Clock()
        self.move_speed = 250

        self.bird = Bird(self.scale_factor)

        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_timer = 0
        self.pipe_spawn_interval = 1.5  # seconds

        self.score = 0
        self.font = pg.font.Font(None, 60)  # default font
        self.game_over = False


        self.setUpBgAndGround()
        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            # Calculate delta time (seconds)
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                   if event.key == pg.K_RETURN:
                   
                      if self.game_over:
                         self.resetGame()
                      else:
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                        self.bird.y_velocity = 0

                   if event.key == pg.K_SPACE and self.is_enter_pressed:
                      self.bird.flap()



                

            self.updateEverything(dt)
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
       if self.bird.rect.bottom > 568:
        self.bird.rect.bottom = 568
        self.triggerGameOver()

       if self.pipes:
           if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
              self.bird.rect.colliderect(self.pipes[0].rect_up)):
              self.triggerGameOver()

    def triggerGameOver(self):
        self.is_enter_pressed = False
        self.bird.update_on = False
        self.game_over = True


    def updateEverything(self, dt):
        if self.is_enter_pressed and not self.game_over:
            # Move ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # Pipe spawning with dt
            self.pipe_timer += dt
            if self.pipe_timer >= self.pipe_spawn_interval:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_timer = 0

            # Move pipes
            for pipe in self.pipes:
                pipe.update(dt)

            # Remove old pipes
            if self.pipes and self.pipes[0].rect_up.right < 0:
                self.pipes.pop(0)
            for pipe in self.pipes:
                if pipe.rect_up.right < self.bird.rect.left and not hasattr(pipe, "scored"):
                 self.score += 1
                 pipe.scored = True

        # Always update bird (gravity stops if update_on=False)
        self.bird.update(dt)

    def drawEverything(self):
    # Draw background
        self.win.blit(self.bg_img, (0, -300))
    
    # Draw pipes
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
    
    # Draw ground
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
    
    # Draw birds
        self.win.blit(self.bird.image, self.bird.rect)

    # Draw score at the top center
        score_surf = self.font.render(str(self.score), True, (255, 255, 255))
        self.win.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 50))

    # If game over, draw overlay text
        if self.game_over:
           go_surf = self.font.render("GAME OVER", True, (255, 0, 0))
           restart_surf = pg.font.Font(None, 40).render("Press Enter to Restart", True, (255, 255, 255))
           self.win.blit(go_surf, (self.width // 2 - go_surf.get_width() // 2, self.height // 2 - 50))
           self.win.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10))


    def setUpBgAndGround(self):
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

    def resetGame(self):
    # Reset variables
       self.score = 0
       self.game_over = False
       self.is_enter_pressed = False

    # Reset bird position and state
       self.bird.rect.center = (self.width // 4, self.height // 2)
       self.bird.y_velocity = 0
       self.bird.update_on = False

    # Reset pipes
       self.pipes.clear()
       self.spawn_pipe_timer = 0
 
    # Reset ground position
       self.ground1_rect.x = 0
       self.ground2_rect.x = self.ground1_rect.width

game = Game()
