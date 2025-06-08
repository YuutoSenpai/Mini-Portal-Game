import pygame
import json
from ..utils.constants import *
from .player import Player
from .portal import Portal
from .game_objects import Box, Switch, Goal
from ..levels.level import Level
from .camera import Camera
from ..ui.ui import UI
from .effects import EffectManager

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Game state
        self.current_level = 0
        self.game_state = "playing"  # playing, paused, won, menu
        self.show_instructions = True
        
        # Timer and scoring system
        self.level_start_time = 0.0
        self.level_time = 0.0
        self.best_times = {}  # Store best times for each level
        self.level_stars = {}  # Store star ratings for each level
        self.hints_shown = set()  # Track which levels have had hints shown
        
        # Core systems
        self.camera = Camera(width, height)
        self.ui = UI(width, height)
        self.effect_manager = EffectManager()
        self.sound_manager = None  # Will be set by MainGame
        
        # Game objects
        self.player = None
        self.blue_portal = None
        self.orange_portal = None
        self.level = None
        
        # Input handling
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)
        
        # Load first level
        self.load_level(0)
        
        # Track current music to avoid unnecessary switches
        self.current_background_music = None
        
    def load_level(self, level_index):
        """Load a specific level"""
        self.current_level = level_index
        self.level = Level(level_index)
        
        # Reset portals
        self.blue_portal = None
        self.orange_portal = None
        
        # Create player at spawn point
        spawn_point = self.level.get_spawn_point()
        self.player = Player(spawn_point[0], spawn_point[1])
        
        # Reset camera
        self.camera.set_target(self.player)
        
        # Reset game state
        self.game_state = "playing"
        
        # Reset hint timer and check if hint was already shown
        self.level.reset_hint_timer()
        if level_index in self.hints_shown:
            self.level.hint_visible = False  # Don't show hint again
        
        # Start level timer
        import time
        self.level_start_time = time.time()
        self.level_time = 0.0
        
        # Switch music based on level
        self.switch_level_music(level_index)
    
    def switch_level_music(self, level_index):
        """Switch background music based on level type"""
        if not self.sound_manager:
            return
        
        # Determine music type based on level
        if level_index <= 2:
            # Early levels - upbeat game music
            music_type = 'game'
        elif level_index <= 5:
            # Mid levels - puzzle music for concentration
            music_type = 'puzzle'
        elif level_index <= 8:
            # Advanced levels - back to game music
            music_type = 'game'
        else:
            # Final levels - puzzle music for concentration
            music_type = 'puzzle'
        
        # Only switch if different from current
        if self.current_background_music != music_type:
            self.sound_manager.play_background_music(music_type)
            self.current_background_music = music_type
        
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.restart_level()
            elif event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            elif event.key == pygame.K_h:
                # Toggle hint and mark as shown
                if self.level:
                    self.level.toggle_hint()
                    self.hints_shown.add(self.current_level)
            elif event.key == pygame.K_n and self.game_state == "won":
                self.next_level()
            elif self.show_instructions:
                self.show_instructions = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_state == "playing" and not self.show_instructions:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_pos = self.camera.screen_to_world(mouse_x, mouse_y)
                
                if event.button == 1:  # Left click - Blue portal
                    self.shoot_portal(world_pos, "blue")
                elif event.button == 3:  # Right click - Orange portal
                    self.shoot_portal(world_pos, "orange")
    
    def shoot_portal(self, target_pos, portal_type):
        """Shoot a portal towards target position"""
        if not self.player:
            return
            
        # Calculate direction from player to target
        dx = target_pos[0] - self.player.x
        dy = target_pos[1] - self.player.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance == 0:
            return
            
        # Normalize direction
        dx /= distance
        dy /= distance
        
        # Raycast to find portal placement
        hit_point, hit_normal, hit_surface = self.level.raycast(
            self.player.x, self.player.y, dx, dy, PORTAL_RANGE
        )
        
        if hit_point and hit_surface == SURFACE_NORMAL:
            # Create portal
            if portal_type == "blue":
                self.blue_portal = Portal(hit_point[0], hit_point[1], "blue", hit_normal)
                if self.orange_portal:
                    self.blue_portal.link_portal(self.orange_portal)
                    self.orange_portal.link_portal(self.blue_portal)
            else:
                self.orange_portal = Portal(hit_point[0], hit_point[1], "orange", hit_normal)
                if self.blue_portal:
                    self.orange_portal.link_portal(self.blue_portal)
                    self.blue_portal.link_portal(self.orange_portal)
            
            # Create portal effect
            self.effect_manager.create_portal_effect(hit_point[0], hit_point[1], portal_type)
            
            # Play sound
            if self.sound_manager:
                self.sound_manager.play_sound('portal_shoot')
    
    def update(self, dt):
        """Update game logic"""
        if self.game_state != "playing" or self.show_instructions:
            return
            
        # Update timer
        import time
        if self.game_state == "playing":
            self.level_time = time.time() - self.level_start_time
        
        # Update input
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        
        # Update player
        if self.player:
            self.player.update(dt, self.keys, self.level)
            
            # Check portal teleportation
            if self.blue_portal and self.blue_portal.check_teleport(self.player):
                if self.orange_portal:
                    self.teleport_object(self.player, self.blue_portal, self.orange_portal)
                    
            if self.orange_portal and self.orange_portal.check_teleport(self.player):
                if self.blue_portal:
                    self.teleport_object(self.player, self.orange_portal, self.blue_portal)
        
        # Update level objects
        was_hint_visible_before = self.level.hint_visible
        self.level.update(dt)
        # If hint became visible due to being stuck, mark it as shown
        if not was_hint_visible_before and self.level.hint_visible:
            self.hints_shown.add(self.current_level)
        
        # Check level objects for portal teleportation
        for obj in self.level.get_movable_objects():
            if self.blue_portal and self.blue_portal.check_teleport(obj):
                if self.orange_portal:
                    self.teleport_object(obj, self.blue_portal, self.orange_portal)
                    
            if self.orange_portal and self.orange_portal.check_teleport(obj):
                if self.blue_portal:
                    self.teleport_object(obj, self.orange_portal, self.blue_portal)
        
        # Update portals
        if self.blue_portal:
            self.blue_portal.update(dt)
        if self.orange_portal:
            self.orange_portal.update(dt)
            
        # Update effects
        self.effect_manager.update(dt)
        
        # Update camera
        self.camera.update(dt)
        
        # Check win condition
        if self.level.check_win_condition(self.player):
            if self.game_state != "won":  # Only play sound once and calculate stars
                # Calculate stars based on completion time
                stars = self.calculate_stars(self.current_level, self.level_time)
                
                # Update best time and stars
                if self.current_level not in self.best_times or self.level_time < self.best_times[self.current_level]:
                    self.best_times[self.current_level] = self.level_time
                
                # Update stars (keep the best)
                if self.current_level not in self.level_stars or stars > self.level_stars[self.current_level]:
                    self.level_stars[self.current_level] = stars
                
                if self.sound_manager:
                    self.sound_manager.play_sound('goal_reached')
                    
                print(f"🎉 Level {self.current_level} splněn za {self.level_time:.1f}s - {stars} hvězd{'y' if stars != 1 else ''}!")
                
            self.game_state = "won"
    
    def teleport_object(self, obj, from_portal, to_portal):
        """Teleport an object through portals"""
        if not from_portal.can_teleport or not to_portal.can_teleport:
            return
            
        # Calculate exit position
        exit_x = to_portal.x + to_portal.normal[0] * (PORTAL_RADIUS + 10)
        exit_y = to_portal.y + to_portal.normal[1] * (PORTAL_RADIUS + 10)
        
        # Move object
        obj.x = exit_x
        obj.y = exit_y
        
        # Transform velocity based on portal orientations with better momentum preservation
        if hasattr(obj, 'vel_x') and hasattr(obj, 'vel_y'):
            # Preserve momentum better for portal physics
            original_speed = (obj.vel_x**2 + obj.vel_y**2)**0.5
            
            # If portals are on different orientations, preserve exit velocity better
            if original_speed > 0:
                # Original momentum multiplier for proper momentum building
                momentum_multiplier = 1.8
                
                # Calculate exit velocity based on portal normal but preserve momentum
                if abs(to_portal.normal[1]) > 0.5:  # Vertical portal (top/bottom)
                    obj.vel_x = to_portal.normal[0] * original_speed * momentum_multiplier
                    obj.vel_y = to_portal.normal[1] * original_speed * momentum_multiplier
                else:  # Horizontal portal (left/right)
                    obj.vel_x = to_portal.normal[0] * original_speed * momentum_multiplier
                    obj.vel_y = to_portal.normal[1] * original_speed * momentum_multiplier
                
                # Original speed limits for proper momentum building
                min_exit_speed = 400
                max_exit_speed = 1000
                current_exit_speed = (obj.vel_x**2 + obj.vel_y**2)**0.5
                
                if current_exit_speed < min_exit_speed:
                    factor = min_exit_speed / max(current_exit_speed, 1)
                    obj.vel_x *= factor
                    obj.vel_y *= factor
                elif current_exit_speed > max_exit_speed:
                    factor = max_exit_speed / current_exit_speed
                    obj.vel_x *= factor
                    obj.vel_y *= factor
        
        # Set cooldown to prevent rapid teleportation
        from_portal.set_cooldown()
        to_portal.set_cooldown()
        
        # Create teleport effect
        self.effect_manager.create_teleport_effect(exit_x, exit_y)
        
        # Play teleport sound
        if self.sound_manager:
            self.sound_manager.play_sound('teleport')
    
    def draw(self, screen):
        """Draw everything"""
        # Clear screen
        screen.fill(BLACK)
        
        # Get camera offset
        cam_x, cam_y = self.camera.get_offset()
        
        # Draw level
        self.level.draw(screen, cam_x, cam_y)
        
        # Draw portals
        if self.blue_portal:
            self.blue_portal.draw(screen, cam_x, cam_y)
        if self.orange_portal:
            self.orange_portal.draw(screen, cam_x, cam_y)
        
        # Draw player
        if self.player:
            self.player.draw(screen, cam_x, cam_y)
        
        # Draw effects
        self.effect_manager.draw(screen, cam_x, cam_y)
        
        # Draw UI
        if self.show_instructions:
            self.ui.draw_instructions(screen)
        elif self.game_state == "won":
            self.ui.draw_win_screen(screen, self.current_level)
        elif self.game_state == "paused":
            self.ui.draw_pause_screen(screen, self.level_time, self.current_level)
        
        # Draw HUD
        current_stars = self.level_stars.get(self.current_level, 0)
        total_stars = sum(self.level_stars.values())
        self.ui.draw_hud(screen, self.current_level + 1, self.level_time, current_stars, total_stars)
    
    def restart_level(self):
        """Restart current level"""
        self.load_level(self.current_level)
    
    def next_level(self):
        """Load next level"""
        self.load_level(self.current_level + 1)
    
    def toggle_pause(self):
        """Toggle pause state"""
        if self.game_state == "playing":
            self.game_state = "paused"
        elif self.game_state == "paused":
            self.game_state = "playing"
    
    def calculate_stars(self, level_index, completion_time):
        """Calculate star rating based on completion time"""
        # Define target times for each level (3 stars, 2 stars, 1 star)
        target_times = {
            0: (15, 30, 60),    # Tutorial: 15s=3★, 30s=2★, 60s=1★
            1: (20, 40, 80),    # Gap level
            2: (25, 45, 90),    # Wall portal
            3: (30, 60, 120),   # Box puzzle
            4: (45, 90, 180),   # Switch puzzle
            5: (60, 120, 240),  # Advanced
            6: (40, 80, 160),   # Momentum
            7: (50, 100, 200),  # Tower
            8: (70, 140, 280),  # Maze
            9: (60, 120, 240),  # Precision
            10: (90, 180, 360), # Final boss
        }
        
        # Default times for procedural levels
        default_times = (60, 120, 240)
        times = target_times.get(level_index, default_times)
        
        if completion_time <= times[0]:
            return 3  # 3 stars
        elif completion_time <= times[1]:
            return 2  # 2 stars
        elif completion_time <= times[2]:
            return 1  # 1 star
        else:
            return 1  # Always give at least 1 star for completion