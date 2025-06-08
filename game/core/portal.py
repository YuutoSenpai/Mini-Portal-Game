import pygame
import math
import random
from ..utils.constants import *

class Portal:
    def __init__(self, x, y, portal_type, normal):
        self.x = x
        self.y = y
        self.portal_type = portal_type  # "blue" or "orange"
        self.normal = normal  # Surface normal (dx, dy)
        self.radius = PORTAL_RADIUS
        
        # Portal state
        self.active = True
        self.can_teleport = True
        self.cooldown_timer = 0
        self.linked_portal = None
        
        # Visual effects
        self.animation_timer = 0
        self.particles = []
        
        # Colors
        self.color = BLUE_PORTAL if portal_type == "blue" else ORANGE_PORTAL
        self.inner_color = (255, 255, 255, 128)
        
    def update(self, dt):
        """Update portal animation and effects"""
        self.animation_timer += dt
        
        # Update cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0:
                self.can_teleport = True
        
        # Update particles
        self.update_particles(dt)
        
        # Generate new particles
        if len(self.particles) < 20:
            self.create_particle()
    
    def update_particles(self, dt):
        """Update portal particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['life'] -= dt
            particle['alpha'] -= 200 * dt
            
            if particle['life'] <= 0 or particle['alpha'] <= 0:
                self.particles.remove(particle)
    
    def create_particle(self):
        """Create a new particle around the portal"""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, self.radius)
        
        particle = {
            'x': self.x + math.cos(angle) * distance,
            'y': self.y + math.sin(angle) * distance,
            'vel_x': random.uniform(-50, 50),
            'vel_y': random.uniform(-50, 50),
            'life': random.uniform(1, 3),
            'alpha': 255,
            'size': random.uniform(2, 6)
        }
        self.particles.append(particle)
    
    def link_portal(self, other_portal):
        """Link this portal to another portal"""
        self.linked_portal = other_portal
    
    def check_teleport(self, obj):
        """Check if an object should be teleported through this portal"""
        if not self.can_teleport or not self.linked_portal:
            return False
        
        if not hasattr(obj, 'can_teleport') or not obj.can_teleport():
            return False
        
        # Check distance to portal center
        dx = obj.x - self.x
        dy = obj.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        return distance < self.radius
    
    def set_cooldown(self):
        """Set teleportation cooldown"""
        self.can_teleport = False
        self.cooldown_timer = TELEPORT_COOLDOWN
    
    def draw(self, screen, cam_x, cam_y):
        """Draw the portal with effects"""
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Draw portal particles
        for particle in self.particles:
            p_screen_x = particle['x'] - cam_x
            p_screen_y = particle['y'] - cam_y
            
            # Create particle surface with alpha
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(int(particle['alpha']))
            particle_surface.fill(self.color)
            
            screen.blit(particle_surface, 
                       (p_screen_x - particle['size'], p_screen_y - particle['size']))
        
        # Draw portal main body
        # Outer ring
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)
        
        # Inner portal (swirling effect)
        inner_radius = int(self.radius * 0.7)
        swirl_offset = int(math.sin(self.animation_timer * 5) * 3)
        
        pygame.draw.circle(screen, (0, 0, 0), 
                          (int(screen_x + swirl_offset), int(screen_y)), inner_radius)
        
        # Portal rim with animation
        rim_thickness = 3 + int(math.sin(self.animation_timer * 8) * 2)
        pygame.draw.circle(screen, WHITE, (int(screen_x), int(screen_y)), 
                          self.radius, rim_thickness)
        
        # Draw portal normal (direction indicator)
        if self.normal:
            end_x = screen_x + self.normal[0] * (self.radius + 15)
            end_y = screen_y + self.normal[1] * (self.radius + 15)
            pygame.draw.line(screen, WHITE, (screen_x, screen_y), (end_x, end_y), 3)
            
            # Arrowhead
            arrow_size = 8
            perpendicular = (-self.normal[1], self.normal[0])
            arrow_point1 = (end_x - self.normal[0] * arrow_size + perpendicular[0] * arrow_size//2,
                           end_y - self.normal[1] * arrow_size + perpendicular[1] * arrow_size//2)
            arrow_point2 = (end_x - self.normal[0] * arrow_size - perpendicular[0] * arrow_size//2,
                           end_y - self.normal[1] * arrow_size - perpendicular[1] * arrow_size//2)
            
            pygame.draw.polygon(screen, WHITE, [(end_x, end_y), arrow_point1, arrow_point2])
        
        # Cooldown indicator
        if not self.can_teleport:
            cooldown_alpha = int(128 * (self.cooldown_timer / TELEPORT_COOLDOWN))
            cooldown_surface = pygame.Surface((self.radius * 2, self.radius * 2))
            cooldown_surface.set_alpha(cooldown_alpha)
            cooldown_surface.fill(RED)
            screen.blit(cooldown_surface, 
                       (screen_x - self.radius, screen_y - self.radius))

