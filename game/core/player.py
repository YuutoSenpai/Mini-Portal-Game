import pygame
import math
from ..utils.constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        
        # State
        self.on_ground = False
        self.teleport_cooldown = 0
        
        # Visual
        self.color = BLUE
        self.trail = []  # For visual trail effect
        
    def update(self, dt, keys, level):
        """Update player physics and movement"""
        # Handle input
        self.handle_input(keys, dt)
        
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY * dt
            
        # Limit fall speed
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        
        # Apply friction when on ground
        if self.on_ground:
            self.vel_x *= FRICTION
        
        # Update position
        new_x = self.x + self.vel_x * dt
        new_y = self.y + self.vel_y * dt
        
        # Collision detection
        self.handle_collisions(new_x, new_y, level)
        
        # Velocity validation to prevent flying bug
        max_velocity = 1000
        if abs(self.vel_x) > max_velocity:
            self.vel_x = max_velocity if self.vel_x > 0 else -max_velocity
        if abs(self.vel_y) > max_velocity:
            self.vel_y = max_velocity if self.vel_y > 0 else -max_velocity
            
        # Check for NaN/infinite values
        if math.isnan(self.vel_x) or math.isinf(self.vel_x):
            self.vel_x = 0
        if math.isnan(self.vel_y) or math.isinf(self.vel_y):
            self.vel_y = 0
        
        # Update teleport cooldown
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= dt
            
        # Update trail
        self.update_trail()
    
    def handle_input(self, keys, dt):
        """Handle player input"""
        # Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
        else:
            if self.on_ground:
                self.vel_x *= 0.8  # Decelerate when no input
        
        # Jumping
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -JUMP_FORCE
            self.on_ground = False
    
    def handle_collisions(self, new_x, new_y, level):
        """Handle collisions with level geometry"""
        # Check horizontal collision with push-out
        if self.check_collision(new_x, self.y, level):
            # Try to push player out of collision
            if new_x > self.x:  # Moving right
                while self.check_collision(new_x, self.y, level) and new_x > self.x:
                    new_x -= 1
            else:  # Moving left
                while self.check_collision(new_x, self.y, level) and new_x < self.x:
                    new_x += 1
            
            self.vel_x = 0
            if not self.check_collision(new_x, self.y, level):
                self.x = new_x
        else:
            self.x = new_x
        
        # Check vertical collision with push-out
        if self.check_collision(self.x, new_y, level):
            # Try to push player out of collision
            if new_y > self.y:  # Moving down
                while self.check_collision(self.x, new_y, level) and new_y > self.y:
                    new_y -= 1
                self.on_ground = True
            else:  # Moving up
                while self.check_collision(self.x, new_y, level) and new_y < self.y:
                    new_y += 1
            
            self.vel_y = 0
            if not self.check_collision(self.x, new_y, level):
                self.y = new_y
        else:
            self.y = new_y
            if self.vel_y >= 0:  # Was falling or stationary
                self.on_ground = False
    
    def check_collision(self, x, y, level):
        """Check if player collides with level geometry at given position"""
        # Player corners
        corners = [
            (x - self.width//2, y - self.height//2),  # Top-left
            (x + self.width//2, y - self.height//2),  # Top-right
            (x - self.width//2, y + self.height//2),  # Bottom-left
            (x + self.width//2, y + self.height//2)   # Bottom-right
        ]
        
        for corner_x, corner_y in corners:
            if level.is_solid(corner_x, corner_y):
                return True
        
        return False
    
    def update_trail(self):
        """Update visual trail behind player"""
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
    
    def draw(self, screen, cam_x, cam_y):
        """Draw the player"""
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail) * 0.3
            trail_color = (*self.color, int(255 * alpha))
            trail_screen_x = trail_x - cam_x
            trail_screen_y = trail_y - cam_y
            
            # Create surface for alpha blending
            trail_surface = pygame.Surface((self.width//2, self.height//2))
            trail_surface.set_alpha(int(255 * alpha))
            trail_surface.fill(self.color)
            screen.blit(trail_surface, (trail_screen_x - self.width//4, trail_screen_y - self.height//4))
        
        # Draw main player body
        pygame.draw.rect(screen, self.color, 
                        (screen_x - self.width//2, screen_y - self.height//2, 
                         self.width, self.height))
        
        # Draw player outline
        pygame.draw.rect(screen, WHITE, 
                        (screen_x - self.width//2, screen_y - self.height//2, 
                         self.width, self.height), 2)
        
        # Draw direction indicator (simple arrow)
        if abs(self.vel_x) > 10:
            direction = 1 if self.vel_x > 0 else -1
            arrow_points = [
                (screen_x + direction * self.width//2, screen_y),
                (screen_x + direction * (self.width//2 + 10), screen_y - 5),
                (screen_x + direction * (self.width//2 + 10), screen_y + 5)
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)
    
    def get_rect(self):
        """Get player's collision rectangle"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)
    
    def set_position(self, x, y):
        """Set player position (used for teleportation)"""
        self.x = x
        self.y = y
        self.teleport_cooldown = TELEPORT_COOLDOWN
    
    def can_teleport(self):
        """Check if player can be teleported"""
        return self.teleport_cooldown <= 0