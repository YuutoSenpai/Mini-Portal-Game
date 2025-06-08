import pygame
import math
from ..utils.constants import *

class GameObject:
    """Base class for all game objects"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)
    
    def can_teleport(self):
        return True

class Box(GameObject):
    """Movable box that can be pushed and teleported"""
    def __init__(self, x, y):
        super().__init__(x, y, BOX_SIZE, BOX_SIZE)
        self.color = (139, 69, 19)  # Brown
        self.outline_color = (101, 67, 33)  # Dark brown
        self.mass = 1.0
        self.friction = 0.7
        self.teleport_cooldown = 0
        
    def update(self, dt, level):
        """Update box physics"""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY * dt
            
        # Limit fall speed
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        
        # Apply friction
        if self.on_ground:
            self.vel_x *= self.friction
        
        # Update position
        new_x = self.x + self.vel_x * dt
        new_y = self.y + self.vel_y * dt
        
        # Collision detection
        self.handle_collisions(new_x, new_y, level)
        
        # Update teleport cooldown
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= dt
    
    def handle_collisions(self, new_x, new_y, level):
        """Handle collisions with level geometry"""
        # Check horizontal collision with push-out
        if self.check_collision(new_x, self.y, level):
            # Try to push box out of collision
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
            # Try to push box out of collision
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
            if self.vel_y >= 0:
                self.on_ground = False
    
    def check_collision(self, x, y, level):
        """Check collision with level geometry"""
        corners = [
            (x - self.width//2, y - self.height//2),
            (x + self.width//2, y - self.height//2),
            (x - self.width//2, y + self.height//2),
            (x + self.width//2, y + self.height//2)
        ]
        
        for corner_x, corner_y in corners:
            if level.is_solid(corner_x, corner_y):
                return True
        return False
    
    def push(self, force_x, force_y):
        """Apply push force to the box"""
        self.vel_x += force_x / self.mass
        self.vel_y += force_y / self.mass
    
    def can_teleport(self):
        return self.teleport_cooldown <= 0
    
    def set_teleport_cooldown(self):
        self.teleport_cooldown = TELEPORT_COOLDOWN
    
    def draw(self, screen, cam_x, cam_y):
        """Draw the box with 3D effect"""
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Main box body
        box_rect = (screen_x - self.width//2, screen_y - self.height//2, 
                   self.width, self.height)
        pygame.draw.rect(screen, self.color, box_rect)
        
        # 3D effect - top face
        top_points = [
            (screen_x - self.width//2, screen_y - self.height//2),
            (screen_x + self.width//2, screen_y - self.height//2),
            (screen_x + self.width//2 - 5, screen_y - self.height//2 - 5),
            (screen_x - self.width//2 - 5, screen_y - self.height//2 - 5)
        ]
        lighter_color = tuple(min(255, c + 30) for c in self.color)
        pygame.draw.polygon(screen, lighter_color, top_points)
        
        # 3D effect - right face
        right_points = [
            (screen_x + self.width//2, screen_y - self.height//2),
            (screen_x + self.width//2, screen_y + self.height//2),
            (screen_x + self.width//2 - 5, screen_y + self.height//2 - 5),
            (screen_x + self.width//2 - 5, screen_y - self.height//2 - 5)
        ]
        darker_color = tuple(max(0, c - 30) for c in self.color)
        pygame.draw.polygon(screen, darker_color, right_points)
        
        # Outline
        pygame.draw.rect(screen, self.outline_color, box_rect, 2)
        
        # Wood grain lines
        for i in range(3):
            y_offset = -self.height//2 + (i + 1) * self.height//4
            pygame.draw.line(screen, self.outline_color,
                           (screen_x - self.width//2 + 5, screen_y + y_offset),
                           (screen_x + self.width//2 - 5, screen_y + y_offset), 1)

class Switch(GameObject):
    """Pressure switch that activates when stepped on"""
    def __init__(self, x, y, stay_active=False):
        super().__init__(x, y, SWITCH_SIZE, SWITCH_SIZE//2)
        self.active = False
        self.stay_active = stay_active
        self.objects_on_switch = []
        self.activation_timer = 0
        self.deactivation_delay = 1.0  # Seconds before deactivating
        
        # Visual
        self.active_color = GREEN
        self.inactive_color = RED
        self.base_color = GRAY
        
    def update(self, dt, level):
        """Update switch state"""
        # Remove objects no longer on switch
        self.objects_on_switch = [obj for obj in self.objects_on_switch 
                                 if self.is_object_on_switch(obj)]
        
        # Check activation
        if self.objects_on_switch and not self.active:
            self.active = True
            self.activation_timer = 0
        elif not self.objects_on_switch and self.active and not self.stay_active:
            self.activation_timer += dt
            if self.activation_timer >= self.deactivation_delay:
                self.active = False
                self.activation_timer = 0
    
    def add_object(self, obj):
        """Add an object to the switch"""
        if obj not in self.objects_on_switch:
            self.objects_on_switch.append(obj)
    
    def is_object_on_switch(self, obj):
        """Check if an object is still on the switch"""
        obj_rect = obj.get_rect()
        switch_rect = pygame.Rect(self.x - self.width//2, 
                                 self.y - self.height//2,
                                 self.width, self.height)
        return obj_rect.colliderect(switch_rect)
    
    def can_teleport(self):
        return False  # Switches cannot be teleported
    
    def draw(self, screen, cam_x, cam_y):
        """Draw the switch"""
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Base platform
        base_rect = (screen_x - self.width//2, screen_y - self.height//2 + 5,
                    self.width, self.height + 10)
        pygame.draw.rect(screen, self.base_color, base_rect)
        pygame.draw.rect(screen, DARK_GRAY, base_rect, 2)
        
        # Switch plate
        plate_height = self.height if not self.active else self.height//2
        plate_rect = (screen_x - self.width//2 + 5, 
                     screen_y - plate_height//2,
                     self.width - 10, plate_height)
        
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, color, plate_rect)
        pygame.draw.rect(screen, WHITE, plate_rect, 2)
        
        # Status indicator
        indicator_radius = 5
        indicator_color = GREEN if self.active else RED
        pygame.draw.circle(screen, indicator_color,
                          (int(screen_x), int(screen_y - self.height//2 - 10)),
                          indicator_radius)
        pygame.draw.circle(screen, WHITE,
                          (int(screen_x), int(screen_y - self.height//2 - 10)),
                          indicator_radius, 2)

class Goal(GameObject):
    """Goal object that player must reach to complete level"""
    def __init__(self, x, y, required_switches=None):
        super().__init__(x, y, GOAL_SIZE, GOAL_SIZE)
        self.required_switches = required_switches or []
        self.animation_timer = 0
        self.particles = []
        
        # Visual
        self.color = YELLOW
        self.inactive_color = GRAY
        
    def update(self, dt, level):
        """Update goal animation and particles"""
        self.animation_timer += dt
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['life'] -= dt
            particle['alpha'] -= 100 * dt
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Create new particles if goal is active
        if self.is_active() and len(self.particles) < 15:
            self.create_particle()
    
    def is_active(self):
        """Check if goal is active (all required switches activated)"""
        if not self.required_switches:
            return True
        
        return all(switch.active for switch in self.required_switches)
    
    def create_particle(self):
        """Create sparkle particle"""
        import random
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, self.width//2)
        
        particle = {
            'x': self.x + math.cos(angle) * distance,
            'y': self.y + math.sin(angle) * distance,
            'vel_x': random.uniform(-30, 30),
            'vel_y': random.uniform(-50, -20),
            'life': random.uniform(1, 2),
            'alpha': 255,
            'size': random.uniform(2, 4)
        }
        self.particles.append(particle)
    
    def check_player_collision(self, player):
        """Check if player reaches the goal"""
        if not self.is_active():
            return False
        
        player_rect = player.get_rect()
        goal_rect = self.get_rect()
        return player_rect.colliderect(goal_rect)
    
    def can_teleport(self):
        return False
    
    def draw(self, screen, cam_x, cam_y):
        """Draw the goal with effects"""
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Draw particles
        for particle in self.particles:
            p_x = particle['x'] - cam_x
            p_y = particle['y'] - cam_y
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(int(particle['alpha']))
            particle_surface.fill(YELLOW)
            screen.blit(particle_surface, (p_x - particle['size'], p_y - particle['size']))
        
        # Main goal body
        if self.is_active():
            # Pulsing effect
            pulse = math.sin(self.animation_timer * 6) * 0.1 + 1
            current_size = int(self.width * pulse)
            color = self.color
        else:
            current_size = self.width
            color = self.inactive_color
        
        # Star shape
        star_points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = current_size // 2
            else:
                radius = current_size // 4
            
            x = screen_x + math.cos(angle) * radius
            y = screen_y + math.sin(angle) * radius
            star_points.append((x, y))
        
        pygame.draw.polygon(screen, color, star_points)
        pygame.draw.polygon(screen, WHITE, star_points, 3)
        
        # Center circle
        center_radius = current_size // 6
        pygame.draw.circle(screen, WHITE, (int(screen_x), int(screen_y)), center_radius)
        
        # Rotating ring effect if active
        if self.is_active():
            for i in range(8):
                angle = self.animation_timer * 2 + i * math.pi / 4
                ring_x = screen_x + math.cos(angle) * (current_size // 2 + 10)
                ring_y = screen_y + math.sin(angle) * (current_size // 2 + 10)
                pygame.draw.circle(screen, YELLOW, (int(ring_x), int(ring_y)), 3)