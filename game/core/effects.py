import pygame
import math
import random
from ..utils.constants import *

class Effect:
    """Base effect class"""
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.duration = duration
        self.timer = 0
        self.active = True
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.active = False
    
    def draw(self, screen, cam_x, cam_y):
        pass

class PortalEffect(Effect):
    """Visual effect when portal is created"""
    def __init__(self, x, y, portal_type):
        super().__init__(x, y, 1.5)  # 1.5 seconds
        self.portal_type = portal_type
        self.particles = []
        self.rings = []
        
        # Create initial particles
        for i in range(20):
            self.create_particle()
        
        # Create expanding rings
        for i in range(3):
            self.rings.append({
                'radius': 0,
                'max_radius': 60 + i * 20,
                'alpha': 255,
                'speed': 100 + i * 50
            })
    
    def create_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, 40)
        speed = random.uniform(50, 150)
        
        particle = {
            'x': self.x + math.cos(angle) * distance,
            'y': self.y + math.sin(angle) * distance,
            'vel_x': math.cos(angle) * speed,
            'vel_y': math.sin(angle) * speed,
            'life': random.uniform(0.5, 1.5),
            'max_life': random.uniform(0.5, 1.5),
            'size': random.uniform(2, 6),
            'color': BLUE_PORTAL if self.portal_type == "blue" else ORANGE_PORTAL
        }
        particle['max_life'] = particle['life']
        self.particles.append(particle)
    
    def update(self, dt):
        super().update(dt)
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['life'] -= dt
            
            # Add some gravity
            particle['vel_y'] += 200 * dt
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update rings
        for ring in self.rings:
            ring['radius'] += ring['speed'] * dt
            ring['alpha'] = max(0, 255 * (1 - ring['radius'] / ring['max_radius']))
        
        # Generate new particles
        if len(self.particles) < 15 and self.timer < self.duration * 0.7:
            self.create_particle()
    
    def draw(self, screen, cam_x, cam_y):
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Draw rings
        for ring in self.rings:
            if ring['radius'] < ring['max_radius'] and ring['alpha'] > 0:
                ring_surface = pygame.Surface((ring['radius'] * 2, ring['radius'] * 2))
                ring_surface.set_alpha(int(ring['alpha']))
                
                color = BLUE_PORTAL if self.portal_type == "blue" else ORANGE_PORTAL
                pygame.draw.circle(ring_surface, color, 
                                 (int(ring['radius']), int(ring['radius'])), 
                                 int(ring['radius']), 3)
                
                screen.blit(ring_surface, 
                           (screen_x - ring['radius'], screen_y - ring['radius']))
        
        # Draw particles
        for particle in self.particles:
            p_x = particle['x'] - cam_x
            p_y = particle['y'] - cam_y
            
            # Fade particle based on remaining life
            alpha = int(255 * (particle['life'] / particle['max_life']))
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(particle['color'])
            
            screen.blit(particle_surface, 
                       (p_x - particle['size'], p_y - particle['size']))

class TeleportEffect(Effect):
    """Effect when object teleports through portal"""
    def __init__(self, x, y):
        super().__init__(x, y, 1.0)  # 1 second
        self.particles = []
        self.spiral_particles = []
        
        # Create explosion particles
        for i in range(15):
            self.create_explosion_particle()
        
        # Create spiral particles
        for i in range(8):
            self.create_spiral_particle(i)
    
    def create_explosion_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 200)
        
        particle = {
            'x': self.x,
            'y': self.y,
            'vel_x': math.cos(angle) * speed,
            'vel_y': math.sin(angle) * speed,
            'life': random.uniform(0.3, 0.8),
            'max_life': random.uniform(0.3, 0.8),
            'size': random.uniform(3, 8),
            'color': random.choice([CYAN, WHITE, YELLOW])
        }
        particle['max_life'] = particle['life']
        self.particles.append(particle)
    
    def create_spiral_particle(self, index):
        angle = index * math.pi / 4
        
        particle = {
            'angle': angle,
            'radius': 5,
            'angle_speed': random.uniform(8, 12),
            'radius_speed': random.uniform(30, 50),
            'life': random.uniform(0.8, 1.2),
            'max_life': random.uniform(0.8, 1.2),
            'size': random.uniform(2, 5),
            'color': random.choice([CYAN, BLUE_PORTAL, ORANGE_PORTAL])
        }
        particle['max_life'] = particle['life']
        self.spiral_particles.append(particle)
    
    def update(self, dt):
        super().update(dt)
        
        # Update explosion particles
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['life'] -= dt
            
            # Decelerate
            particle['vel_x'] *= 0.95
            particle['vel_y'] *= 0.95
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update spiral particles
        for particle in self.spiral_particles[:]:
            particle['angle'] += particle['angle_speed'] * dt
            particle['radius'] += particle['radius_speed'] * dt
            particle['life'] -= dt
            
            if particle['life'] <= 0:
                self.spiral_particles.remove(particle)
    
    def draw(self, screen, cam_x, cam_y):
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        # Draw explosion particles
        for particle in self.particles:
            p_x = particle['x'] - cam_x
            p_y = particle['y'] - cam_y
            
            alpha = int(255 * (particle['life'] / particle['max_life']))
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(particle['color'])
            
            screen.blit(particle_surface, 
                       (p_x - particle['size'], p_y - particle['size']))
        
        # Draw spiral particles
        for particle in self.spiral_particles:
            p_x = screen_x + math.cos(particle['angle']) * particle['radius']
            p_y = screen_y + math.sin(particle['angle']) * particle['radius']
            
            alpha = int(255 * (particle['life'] / particle['max_life']))
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(particle['color'])
            
            screen.blit(particle_surface, 
                       (p_x - particle['size'], p_y - particle['size']))

class EffectManager:
    """Manages all visual effects"""
    def __init__(self):
        self.effects = []
    
    def create_portal_effect(self, x, y, portal_type):
        """Create portal creation effect"""
        effect = PortalEffect(x, y, portal_type)
        self.effects.append(effect)
    
    def create_teleport_effect(self, x, y):
        """Create teleportation effect"""
        effect = TeleportEffect(x, y)
        self.effects.append(effect)
    
    def update(self, dt):
        """Update all effects"""
        # Update effects and remove inactive ones
        self.effects = [effect for effect in self.effects if effect.active]
        
        for effect in self.effects:
            effect.update(dt)
    
    def draw(self, screen, cam_x, cam_y):
        """Draw all effects"""
        for effect in self.effects:
            effect.draw(screen, cam_x, cam_y)