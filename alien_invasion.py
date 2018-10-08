import vlc
import pygame
import pygame.time
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from pygame.sprite import GroupSingle
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from Start import Start
from button import highScore

def runGame():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screenWidth, ai_settings.screenHeight))
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()

    # Play button
    play_button = Button(ai_settings, screen, "Play Game")
    high = highScore(ai_settings, screen, "High Score")

    # game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # ship and bullets
    ship = Ship(ai_settings, screen)
    bullets = Group()

    # aliens and lasers
    aliens = Group()
    lasers = Group()
    ufo = GroupSingle()

    #Bunker
    bunkers = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    startScreen = Start(ai_settings, screen)
    soundFile = vlc.MediaPlayer("files/SpaceInvaders.mp3")

    while True:
        clock.tick(62)
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bunkers, high, ufo)
        if stats.game_active:
            soundFile.play()
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)
            gf.fire_laser(ai_settings, screen, aliens, lasers)
            gf.update_lasers(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)
            gf.updateBunkers(bullets, lasers, bunkers, aliens)
            gf.spawnUFO(ai_settings, screen, ufo)
            gf.updateUFO(ai_settings, ufo)
            gf.updateScreen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, lasers, bunkers, ufo)
        elif not stats.game_active and not stats.menu:
            gf.startGame(play_button, high, startScreen)
            soundFile.stop()
        elif stats.menu:
            gf.printHighScores(screen)
            soundFile.stop()

runGame()