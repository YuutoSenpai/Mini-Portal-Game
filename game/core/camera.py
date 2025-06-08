import pygame
from ..utils.constants import *

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0
        self.target = None
        self.follow_speed = 5.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Camera bounds (optional)
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        
        # Camera shake
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_timer = 0
    
    def set_target(self, target):
        """Set the camera target to follow"""
        self.target = target
        if target:
            # Immediately center on target
            self.x = target.x - self.screen_width // 2
            self.y = target.y - self.screen_height // 2
    
    def set_bounds(self, min_x, max_x, min_y, max_y):
        """Set camera movement bounds"""
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
    
    def update(self, dt):
        """Update camera position"""
        if self.target:
            # Calculate target position
            target_x = self.target.x - self.screen_width // 2
            target_y = self.target.y - self.screen_height // 2
            
            # Smooth following
            self.x += (target_x - self.x) * self.follow_speed * dt
            self.y += (target_y - self.y) * self.follow_speed * dt
            
            # Apply bounds
            if self.min_x is not None and self.max_x is not None:
                self.x = max(self.min_x, min(self.x, self.max_x - self.screen_width))
            if self.min_y is not None and self.max_y is not None:
                self.y = max(self.min_y, min(self.y, self.max_y - self.screen_height))
        
        # Update camera shake
        if self.shake_timer > 0:
            self.shake_timer -= dt
            if self.shake_timer <= 0:
                self.shake_intensity = 0
                self.offset_x = 0
                self.offset_y = 0
            else:
                import random
                shake_amount = self.shake_intensity * (self.shake_timer / self.shake_duration)
                self.offset_x = random.uniform(-shake_amount, shake_amount)
                self.offset_y = random.uniform(-shake_amount, shake_amount)
    
    def add_shake(self, intensity, duration):
        """Add camera shake effect"""
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration
    
    def get_offset(self):
        """Get camera offset for rendering"""
        return (self.x + self.offset_x, self.y + self.offset_y)
    
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x + self.x + self.offset_x
        world_y = screen_y + self.y + self.offset_y
        return (world_x, world_y)
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x - self.x - self.offset_x
        screen_y = world_y - self.y - self.offset_y
        return (screen_x, screen_y)