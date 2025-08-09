import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self, scale_factor):
        super().__init__()
        self.img_list = [
            pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(), scale_factor),
            pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(), scale_factor)
        ]
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(100, 100))

        # Physics
        self.y_velocity = 0
        self.gravity = 1000   # pixels/sec²
        self.flap_power = 350 # jump strength

        # Animation
        self.anim_timer = 0
        self.anim_interval = 0.12  # seconds per frame

        self.update_on = False

    def update(self, dt):
        if self.update_on:
            self.playAnimation(dt)
            self.applyGravity(dt)

            # Clamp top
            if self.rect.y < 0:
                self.rect.y = 0
                self.y_velocity = 0

    def applyGravity(self, dt):
        self.y_velocity += self.gravity * dt
        self.rect.y += self.y_velocity * dt

    def flap(self):
        self.y_velocity = -self.flap_power

    def playAnimation(self, dt):
        self.anim_timer += dt
        if self.anim_timer >= self.anim_interval:
            self.image_index = 1 - self.image_index
            self.image = self.img_list[self.image_index]
            self.anim_timer = 0
