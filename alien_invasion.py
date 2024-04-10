import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game asset and behaviour."""

    def __init__(self):
        """Initialize the game and create game resources."""
        # Intialize all the pygame modules.
        pygame.init() 

        # Initialize game settings
        self.settings = Settings()

        # Update screen width and height based on the display surface of your computer. 
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Set the caption of the window
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create a ship instance.
        self.ship = Ship(self)

        # Create a group to store bullets.
        self.bullets = pygame.sprite.Group()

        # Create a group to hold the fleet of aliens
        self.aliens = pygame.sprite.Group()

        # Calls the below method
        self._create_fleet()

        # Set the background colour
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Check for events
            self._check_events()

            if self.stats.game_active:  
                # update ship position 
                self.ship.update()
                # Update bullets positions and remove bullets
                self._update_bullets()
                # Update the positoion of each alien
                self._update_aliens()
            # Update the display
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # Exit the game if windows is closed

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    def _check_keydown_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit() # Exit the game if 'q' key is pressed.
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key release."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creates a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of the bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if  bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and that alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:
            # Decrement ship_left.
            self.stats.ship_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and centre the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        Update the positions of all aliens on the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-sheep collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_alien_bottom()

    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this as same as if the ship got hit.
                self._ship_hit()
                break
            
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        # Make the aliens.
        alien = Alien(self)
        # Stores the rectangular width of the alien image
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) 


    def _check_fleet_edges(self):
        """Respond appropriately if ant aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's directions. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen. """
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)

        # Draw the ship on the screen.
        self.ship.blitme()

        # Draw all bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the alien draw on the screen
        self.aliens.draw(self.screen)
            
        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()