import sys
import pygame

from settings import Settings
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
            # update ship position 
            self.ship.update()
            # Update bullets positions and remove bullets
            self._update_bullets()
            # Update the display
            self._update_screen()

    def _update_bullets(self):
        """Update position of the bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if  bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Print number of active bullets
        print(len(self.bullets))

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

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make the aliens.
        alien = Alien(self)
        self.aliens.add(alien) 

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