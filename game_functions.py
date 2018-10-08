import sys
import pygame
import pygame.font
from bullet import Bullet
from bullet import Laser
from alien import Alien
from time import sleep
import time
from random import randint
from Bunkers import Bunkers
from alien import UFO


def readHighScore():
    file = open("files/highScores.txt", "r")
    high = int(file.read())
    file.close()
    return high

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score(readHighScore())

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)
            break

def playExplosion(screen, entity):
    explosion = ["images/Exp1.png", "images/Exp1.png", "images/Exp1.png", "images/Exp1.png", "images/Exp1.png",
                 "images/Exp2.png", "images/Exp2.png","images/Exp2.png","images/Exp2.png","images/Exp2.png",
                 "images/Exp3.png", "images/Exp3.png","images/Exp3.png","images/Exp3.png","images/Exp3.png",
                 "images/Exp4.png", "images/Exp4.png","images/Exp4.png","images/Exp4.png","images/Exp4.png",
                 "images/Exp5.png", "images/Exp5.png","images/Exp5.png","images/Exp5.png","images/Exp5.png",
                 "images/Exp4.png", "images/Exp4.png","images/Exp4.png","images/Exp4.png","images/Exp4.png"]
    for img in explosion:
        image = pygame.image.load(img)
        rect = image.get_rect()
        rect.centerx = entity.rect.centerx
        rect.centery = entity.rect.centery
        screen.blit(image, rect)
        pygame.display.flip()

def playUfoScore(ai_settings, screen, entity):
    now = time.time()
    sec = now % 60

    width, height = 200, 50
    button_color = (0, 0, 0)
    text_color = (0, 255, 0)
    font = pygame.font.SysFont(None, 48)

    rect = pygame.Rect(0, 0, width, height)
    rect.centery = entity.rect.centery
    rect.centerx = entity.rect.centerx

    msg_image = font.render(str(ai_settings.ufo_points), True, text_color, button_color)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.center = rect.center
    for i in range(120):
        screen.blit(msg_image, msg_image_rect)
        pygame.display.flip()

def shipShoot():
    pygame.mixer.init()
    pygame.mixer.music.load("files/Laser.wav")
    pygame.mixer.music.play()

def alienShoot():
    pygame.mixer.init()
    pygame.mixer.music.load("files/AlienLaser.wav")
    pygame.mixer.music.play()

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        lasers.empty()
        bunkers.empty()
        ufo.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        createBunkers(ai_settings, screen, bunkers)
        ship.center_ship()

        sleep(0.5)
    else:
        file = open("files/highScores.txt", "r")
        current = int(file.read())
        file.close()
        if stats.high_score > current:
            file = open("files/highScores.txt", "w")
            file.write(str(stats.high_score))
            file.close()
        stats.game_active = False
        pygame.mouse.set_visible(True)

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)
    # print("Ship hit!!!")

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screenHeight - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screenWidth - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen, row_number)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen, 0)
    number_aliens_x1 = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x1):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        shipShoot()
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def printHighScores(screen):
    font = pygame.font.SysFont(None, 48)
    high_score = int(round(readHighScore(), -1))
    high_score_str = "{:,} Pts".format(high_score)
    high_score_image = font.render(high_score_str, True, (255, 255, 255), (0, 0, 0))
    screen_rect = screen.get_rect()

    high_score_rect = high_score_image.get_rect()
    high_score_rect.centerx = screen_rect.centerx
    high_score_rect.centery = screen_rect.centery

    exitHighString = "Exit"
    exitImage = font.render(exitHighString, True, (255, 255, 255), (0, 0, 0))
    exitRect = exitImage.get_rect()
    exitRect.centerx = screen_rect.centerx
    exitRect.centery = screen_rect.centery + 350

    font = pygame.font.SysFont(None, 72)
    highScore = "High Score"
    scoreImage = font.render(highScore, True, (255, 255, 255), (0, 0, 0))
    scoreRect = scoreImage.get_rect()
    scoreRect.centerx = screen_rect.centerx
    scoreRect.top = screen_rect.top + 50

    screen.fill((0, 0, 0))
    screen.blit(scoreImage, scoreRect)
    screen.blit(high_score_image, high_score_rect)
    screen.blit(exitImage, exitRect)
    pygame.display.flip()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bunkers, high, ufo):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    displayHigh = high.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        stats.menu = False
        sb.prep_score()
        sb.prep_high_score(readHighScore())
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        ufo.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        createBunkers(ai_settings, screen, bunkers)
        ship.center_ship()
    elif displayHigh and not stats.game_active and not stats.menu:
        stats.menu = True
    elif displayHigh and not stats.game_active and stats.menu:
        stats.menu = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bunkers, high, ufo):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bunkers, high, ufo)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def updateScreen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, lasers, bunkers, ufo):
    screen.fill(ai_settings.backgroundColor)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for laser in lasers.sprites():
        laser.draw_laser()
    ship.blitMe()
    aliens.draw(screen)
    bunkers.draw(screen)
    ufo.draw(screen)
    sb.show_score()
    pygame.display.flip()

def check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets, ufo, True, True)

    if collisions:
        for aliensz in collisions.values():
            for alien in aliensz:
                playExplosion(screen, alien)
            stats.score += ai_settings.alien_points * len(aliensz)
            sb.prep_score()
        check_high_score(stats, sb)

    if collisions2:
        for ufos in collisions2.values():
            for u in ufos:
                playUfoScore(ai_settings, screen, u)
            stats.score += ai_settings.ufo_points * len(ufos)
            sb.prep_score()
        check_high_score(stats, sb)
        ai_settings.ufo_direction *= -1

    if len(aliens) == 0:
        bullets.empty()
        lasers.empty()
        bunkers.empty()
        ufo.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
        createBunkers(ai_settings, screen, bunkers)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)

def check_laser_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    collisions = pygame.sprite.groupcollide(bullets, lasers, True, True)
    collisionsShip = pygame.sprite.spritecollideany(ship, lasers)

    if collisionsShip:
        playExplosion(screen, ship)
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)

def update_lasers(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo):
    lasers.update()
    for laser in lasers.copy():
        if laser.rect.top >= ai_settings.screenHeight:
            lasers.remove(laser)
    check_laser_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, bunkers, ufo)

def fire_laser(ai_settings, screen, aliens, lasers):
    now = time.time()
    sec = now % 60
    if int(sec) % randint(30, 60) == 0 and len(lasers) < ai_settings.lasers_allowed and len(aliens) > 0:
        alienShooter = randint(0, len(aliens) - 1)
        new_laser = Laser(ai_settings, screen, list(aliens)[alienShooter])
        lasers.add(new_laser)
        alienShoot()

def get_number_bunker_x(ai_settings, alien_width):
    available_space_x = ai_settings.screenWidth - alien_width
    number_aliens_x = int(available_space_x / (alien_width))
    return number_aliens_x

def create_bunker (ai_settings, screen, bunkers, bunker_number):
    bunker = Bunkers(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 2 * bunker_width * bunker_number + 1.5 * bunker_width
    bunker.rect.x = bunker.x
    bunker.rect.y = bunker.rect.height + 8 * bunker.rect.height
    bunkers.add(bunker)

def createBunkers(ai_settings, screen, bunkers):
    bunker = Bunkers(ai_settings, screen)
    number_aliens_x1 = get_number_bunker_x(ai_settings, bunker.rect.width)

    for bunker_number in range(5):
        create_bunker(ai_settings, screen, bunkers, bunker_number)

def checkBunkerHit(bullets, lasers, bunkers, aliens):
    collisions = pygame.sprite.groupcollide(aliens, bunkers, True, True)

    for bunker in bunkers.copy():
        if pygame.sprite.spritecollide(bunker, bullets, True):
            bunker.updateHitCount()
        elif pygame.sprite.spritecollide(bunker, lasers, True):
            bunker.updateHitCount()

def updateBunkers(bullets, lasers, bunkers, aliens):
    bunkers.update()
    for bunker in bunkers.sprites():
        if bunker.hitCount >= 5:
            bunkers.remove(bunker)
    checkBunkerHit(bullets, lasers, bunkers, aliens)

def spawnUFO(ai_settings, screen, ufo):
    now = time.time()
    sec = now % 60
    sweep = UFO(ai_settings, screen)
    if int(sec) % 10 == 0 and int(sec) != 0 and int(sec) % 20 != 0:
        ufo.add(sweep)

def updateUFO(ai_settings, ufo):
    ufo.update()
    for sweep in ufo.sprites():
        if sweep.check_edges():
            ufo.remove(sweep)
            ai_settings.ufo_direction *= -1
            break

def startGame(play_button, high, startScreen):
    startScreen.printStart()
    play_button.draw_button()
    high.draw_button()
    pygame.display.flip()
