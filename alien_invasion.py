import sys
from time import sleep
import pygame
from settings import Settings
from background import GameBackground
from game_stats import GameStats
from scoreboard import Scoreboard
from start_button import PlayButton
from pause_button import PauseButton
from quit_button import QuitButton
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.bg = GameBackground()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.NOFRAME)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Make the Play and pause button.
        self.play_button = PlayButton(self, "START")
        self.pause_button = PauseButton(self, "RESUME")
        self.quit_button = QuitButton(self, "QUIT")

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Update high score and quit game.
                high_score = open("High_Score.txt", "w")
                high_score.write(str(self.stats.high_score))
                high_score.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # Update high score and quit game.
            with open("High_Score.txt", "w") as high_score:
                high_score.write(str(self.stats.high_score))
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            pygame.mixer.music.pause()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        elif event.key == pygame.K_r:
            if self.stats.ships_left > 0:
                self.stats.game_active = True
                pygame.mixer.music.unpause()
                pygame.mouse.set_visible(False)
            else:
                pass

    def _check_keyup_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Respond to mouse clicks."""
        play_button = self.play_button.rect.collidepoint(mouse_pos)
        resume = self.pause_button.rect.collidepoint(mouse_pos)
        quit = self.quit_button.rect.collidepoint(mouse_pos)
        if quit and not self.stats.game_active:
            # Update high score.
            with open("High_Score.txt", "w") as high_score:
                high_score.write(str(self.stats.high_score))
            # Quit game.
            pygame.quit()
            sys.exit()
        if resume and not self.stats.game_active:
            # Resume game if there are still ships remaining.
            if self.stats.ships_left > 0:
                self.stats.game_active = True
                pygame.mixer.music.unpause()
                pygame.mouse.set_visible(False)
            else:
                pass
        if play_button and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialise_dynamic_settings()
            self._start_game()

    def _start_game(self):
        """Starts the game."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        # Create a new fleet, center the ship, start game music.
        self._create_fleet()
        self.ship.center_ship()
        self._game_music()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
        self._start_new_level()

    def _start_new_level(self):
        """Start a new level if all aliens have been destroyed."""
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            self._game_music()
            # Pause
            sleep(0.5)

    def _end_game(self):
        """End game and render GAME OVER image.."""
        game_over_str = "GAME OVER"
        self.text_color = (255, 76, 0)
        self.font = pygame.font.SysFont(None, 80, True, True)
        self.game_over_image = self.font.render(game_over_str, True, self.text_color)
        # Position the image in the center
        self.screen_rect = self.screen.get_rect()
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen_rect.center
        self.screen.blit(self.game_over_image, self.game_over_rect)
        sleep(1)
        self.stats.game_active = False
        pygame.mixer.music.stop()
        pygame.mouse.set_visible(True)

    def _crash_sound(self):
        """Play sound when ship is hit."""
        sound = pygame.mixer.Sound("sounds/crash_sound_trimmed.wav")
        pygame.mixer.Sound.play(sound)

    def _bullet_sound(self):
        """"Play sound when bullet is shot."""
        shot = pygame.mixer.Sound("sounds/gunfire_sound.mp3")
        pygame.mixer.Sound.play(shot)

    def _game_music(self):
        """"Play music when the game starts."""
        pygame.mixer.music.load("sounds/bg_music_trimmed.wav")
        pygame.mixer.music.play(-1)

    def _update_aliens(self):
        """Check if the fleet is at an edge,
        then update the position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            pygame.mixer.music.stop()
            self._crash_sound()
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self._bullet_sound()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.bg.image, self.bg.rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Draw the score information.
        self.sb.show_score()
        # Draw the buttons if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.pause_button.draw_button()
            self.quit_button.draw_button()
        if self.stats.ships_left <= 0:
            self._end_game()
        #Make the most recently drawn screen visible.
        pygame.display.flip()
 
    def _create_fleet(self):
        """Create a fleet of aliens."""
        #Make an alien and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2* alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2*alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    
if __name__ == "__main__":
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()