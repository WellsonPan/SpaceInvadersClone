class Settings:
    def __init__(self):
        # screen settings
        self.screenWidth = 1200
        self.screenHeight = 800
        self.backgroundColor = (0, 0, 0)

        # ship settings
        self.shipSpeedFactor = 3
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 6
        self.bullet_width = 3
        self.bullet_height = 25
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10

        #Laser settings
        self.laser_speed_factor = 6
        self.laser_width = 3
        self.laser_height = 25
        self.laser_color = (255, 255, 255)
        self.lasers_allowed = 3

        # Alien settings
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 = right, -1 = left
        self.ufo_direction = 1
        self.ufo_speed_factor = self.alien_speed_factor * 1.25

        # stat settings
        self.speedup_scale = 1.25
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.shipSpeedFactor = 3
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 2
        self.alien_points = 50
        self.ufo_points = 200

        self.fleet_direction = 1

    def increase_speed(self):
        self.shipSpeedFactor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ufo_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.ufo_points = int(self.ufo_points * self.score_scale)
        print(self.alien_points)



