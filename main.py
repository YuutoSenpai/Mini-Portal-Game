import pygame
import sys
from game.main_game import MainGame

def main():
    pygame.init()
    
    # Game constants
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # Initialize display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mini Portal Game")
    clock = pygame.time.Clock()
    
    # Create main game instance
    main_game = MainGame(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Main game loop
    while main_game.running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game.quit()
                break
            else:
                main_game.handle_event(event)
        
        # Update and draw (use current screen in case of fullscreen toggle)
        current_screen = main_game.screen
        main_game.update(dt)
        main_game.draw(current_screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()