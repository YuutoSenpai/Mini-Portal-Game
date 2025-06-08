import pygame
import json
import os
from .utils.constants import *
from .core.game import Game
from .ui.ui import Menu
from .ui.sound_manager import SoundManager
from .utils.translations import language_manager

class MainGame:
    """Main game controller that handles menus and game states"""
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Game state
        self.state = "menu"  # menu, game, settings
        self.running = True
        self.fullscreen = False
        self.windowed_size = (width, height)
        
        # Systems
        self.menu = Menu(width, height)
        self.game = None
        self.sound_manager = SoundManager()
        
        # Save/Load
        self.save_dir = "data/saves"
        self.save_slots = 3  # Number of save slots
        self.current_save_slot = 0
        self.settings_file = "data/settings/settings.json"
        self.level_completion_saved = False  # Track if we've saved after level completion
        self.previous_level = None  # Track level changes
        
        # Ensure save and settings directories exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        if not os.path.exists(os.path.dirname(self.settings_file)):
            os.makedirs(os.path.dirname(self.settings_file))
        
        # Load settings
        self.load_settings()
        
        # Apply loaded settings
        self.apply_audio_settings()
        
        # Start menu music
        self.sound_manager.play_background_music('menu')
    
    def load_settings(self):
        """Load game settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    
                    self.menu.master_volume = settings.get('master_volume', 0.7)
                    self.menu.sfx_volume = settings.get('sfx_volume', 0.8)
                    self.menu.music_volume = settings.get('music_volume', 0.6)
        except:
            # Use default settings if loading fails
            pass
    
    def save_settings(self):
        """Save game settings"""
        try:
            settings = {
                'master_volume': self.menu.master_volume,
                'sfx_volume': self.menu.sfx_volume,
                'music_volume': self.menu.music_volume
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except:
            pass
    
    def apply_audio_settings(self):
        """Apply audio settings to sound manager"""
        # Apply volume settings
        self.sound_manager.set_master_volume(self.menu.master_volume)
        self.sound_manager.set_sfx_volume(self.menu.sfx_volume)
        self.sound_manager.set_music_volume(self.menu.music_volume)
        
        # Apply audio enable/disable settings
        if hasattr(self.sound_manager, 'enable_procedural_music'):
            self.sound_manager.enable_procedural_music = self.menu.background_music_enabled
        
        # Set sound effects enabled flag
        self.sound_manager.sound_effects_enabled = self.menu.sound_effects_enabled
            
        # If music was disabled, stop current music
        if not self.menu.background_music_enabled:
            self.sound_manager.stop_music()
        elif self.menu.background_music_enabled and self.state == "menu":
            # Restart menu music if it was enabled
            self.sound_manager.play_background_music('menu')
    
    def get_save_file_path(self, slot_index):
        """Get save file path for specific slot"""
        return os.path.join(self.save_dir, f"save_slot_{slot_index}.json")
    
    def load_game(self, slot_index=None):
        """Load saved game from specific slot"""
        if slot_index is None:
            slot_index = self.current_save_slot
            
        save_file = self.get_save_file_path(slot_index)
        
        try:
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                    current_level = save_data.get('current_level', 0)
                    
                    # Create game instance with loaded level
                    self.game = Game(self.screen, self.width, self.height)
                    self.game.sound_manager = self.sound_manager
                    
                    # Load saved progress data
                    self.game.best_times = save_data.get('best_times', {})
                    self.game.level_stars = save_data.get('level_stars', {})
                    self.game.hints_shown = set(save_data.get('hints_shown', []))
                    
                    # Convert string keys back to integers
                    self.game.best_times = {int(k): v for k, v in self.game.best_times.items()}
                    self.game.level_stars = {int(k): v for k, v in self.game.level_stars.items()}
                    
                    self.game.load_level(current_level)
                    
                    # Restore player position if available
                    player_x = save_data.get('player_x')
                    player_y = save_data.get('player_y')
                    if player_x is not None and player_y is not None and self.game.player:
                        self.game.player.x = player_x
                        self.game.player.y = player_y
                        print(f"🔄 Restored player position to ({player_x}, {player_y})")
                    self.current_save_slot = slot_index
                    
                    return True
        except Exception as e:
            print(f"Error loading save slot {slot_index}: {e}")
        
        return False
    
    def get_save_info(self, slot_index):
        """Get information about a save slot"""
        save_file = self.get_save_file_path(slot_index)
        
        if not os.path.exists(save_file):
            return None
            
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                return {
                    'slot': slot_index,
                    'level': save_data.get('current_level', 0),
                    'timestamp': save_data.get('save_timestamp', ''),
                    'total_stars': save_data.get('total_stars', 0),
                    'levels_completed': save_data.get('levels_completed', 0)
                }
        except:
            return None
    
    def save_game(self, slot_index=None):
        """Save current game state to specific slot"""
        if not self.game:
            return False
            
        if slot_index is None:
            slot_index = self.current_save_slot
            
        save_file = self.get_save_file_path(slot_index)
        
        try:
            import datetime
            save_data = {
                'current_level': self.game.current_level,
                'player_x': self.game.player.x if self.game.player else 0,
                'player_y': self.game.player.y if self.game.player else 0,
                'game_state': self.game.game_state,
                'save_timestamp': datetime.datetime.now().isoformat(),
                'levels_completed': self.game.current_level,
                'best_times': self.game.best_times,
                'level_stars': self.game.level_stars,
                'hints_shown': list(self.game.hints_shown),
                'total_stars': sum(self.game.level_stars.values()),
                'levels_unlocked': max(self.game.current_level + 1, len(self.game.level_stars))
            }
            
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
                
            self.current_save_slot = slot_index
            print(f"Game saved to slot {slot_index}")
            return True
        except Exception as e:
            print(f"Failed to save game to slot {slot_index}: {e}")
            return False
    
    def load_specific_level(self, level_index):
        """Load a specific level from level select menu"""
        # Create or get existing game instance
        if not self.game:
            self.game = Game(self.screen, self.width, self.height)
            self.game.sound_manager = self.sound_manager
        
        # Update level progress in menu before entering game
        self.update_menu_level_progress()
        
        # Check if level is unlocked (based on current save or progress)
        max_unlocked = 0
        
        # Check all save slots to find highest unlocked level
        for slot in range(self.save_slots):
            save_info = self.get_save_info(slot)
            if save_info:
                max_unlocked = max(max_unlocked, save_info['levels_completed'])
        
        # Always allow level 0, and allow up to max completed + 1
        if level_index > max_unlocked and level_index > 0:
            self.sound_manager.play_sound('switch_off')
            print(f"Level {level_index + 1} is locked! Complete previous levels first.")
            return
        
        # Load the requested level
        self.game.load_level(level_index)
        self.state = "game"
        self.level_completion_saved = False
        self.previous_level = level_index
        
        # Switch to game music and play sound
        self.sound_manager.play_background_music('game')
        self.sound_manager.play_sound('portal_open')
        print(f"Loaded Level {level_index + 1}")
    
    def update_menu_level_progress(self):
        """Update menu with current level progress from all save slots"""
        # Find the highest level progress across all save slots
        max_level = 0
        combined_stars = {}
        
        print(f"🔍 Checking {self.save_slots} save slots for level progress...")
        
        for slot in range(self.save_slots):
            save_info = self.get_save_info(slot)
            if save_info:
                print(f"  📁 Slot {slot}: Level {save_info['level']}, Stars: {save_info.get('total_stars', 0)}")
                max_level = max(max_level, save_info['level'])
                # Get detailed save data for stars
                save_file = self.get_save_file_path(slot)
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                        level_stars = save_data.get('level_stars', {})
                        # Convert string keys to int and merge with best stars found
                        for level_str, stars in level_stars.items():
                            level_num = int(level_str)
                            combined_stars[level_num] = max(combined_stars.get(level_num, 0), stars)
                            print(f"    ⭐ Level {level_num}: {stars} stars")
                except Exception as e:
                    print(f"    ❌ Error reading slot {slot}: {e}")
            else:
                print(f"  📁 Slot {slot}: Empty")
        
        print(f"📊 Final progress: Max level {max_level}, Combined stars: {combined_stars}")
        
        # Update menu with progress data
        self.menu.update_level_progress(combined_stars, max_level)
    
    
    def delete_save(self, slot_index):
        """Delete a save file"""
        save_file = self.get_save_file_path(slot_index)
        try:
            if os.path.exists(save_file):
                os.remove(save_file)
                return True
            else:
                return False
        except Exception as e:
            print(f"Failed to delete save slot {slot_index}: {e}")
            return False
    
    def new_game(self):
        """Start a new game"""
        self.game = Game(self.screen, self.width, self.height)
        self.game.sound_manager = self.sound_manager
        self.game.load_level(0)
        self.state = "game"
        self.level_completion_saved = False  # Reset save flag for new game
        self.previous_level = 0  # Initialize level tracking
        
        # Switch to game music
        self.sound_manager.play_background_music('game')
        
        # Play game start sound
        self.sound_manager.play_sound('level_complete', 0.5)
    
    def load_saved_game(self):
        """Load saved game"""
        if self.load_game():
            self.state = "game"
            self.level_completion_saved = False  # Reset save flag for loaded game
            self.previous_level = self.game.current_level if self.game else 0  # Initialize level tracking
            self.sound_manager.play_background_music('game')
            self.sound_manager.play_sound('portal_open')
        else:
            # No save file exists
            self.sound_manager.play_sound('switch_off')
            print("No save file found!")
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            # Switch to fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()
        else:
            # Switch back to windowed
            self.screen = pygame.display.set_mode(self.windowed_size)
            self.width, self.height = self.windowed_size
        
        # Update menu size
        self.menu.screen_width = self.width
        self.menu.screen_height = self.height
        
        # Update game camera if game is running
        if self.game:
            self.game.camera.screen_width = self.width
            self.game.camera.screen_height = self.height
            self.game.ui.screen_width = self.width
            self.game.ui.screen_height = self.height
            
            # Validate player position after screen change to prevent clipping
            if self.game.player:
                # Check if player is outside level boundaries OR inside walls
                player_rect = pygame.Rect(self.game.player.x - 15, self.game.player.y - 20, 30, 40)
                needs_reset = False
                
                # Check boundary violations
                if (self.game.player.x < 50 or self.game.player.x > self.game.level.width - 50 or
                    self.game.player.y < 50 or self.game.player.y > self.game.level.height - 50):
                    needs_reset = True
                    print("⚠ Player outside level boundaries after screen change")
                
                # Check wall collisions (prevent clipping through walls)
                for wall in self.game.level.walls + self.game.level.non_portalable_walls:
                    if player_rect.colliderect(wall):
                        needs_reset = True
                        print("⚠ Player inside wall after screen change")
                        break
                
                # Check box collisions
                for box in self.game.level.boxes:
                    box_rect = pygame.Rect(box.x - box.width//2, box.y - box.height, box.width, box.height)
                    if player_rect.colliderect(box_rect):
                        needs_reset = True
                        print("⚠ Player inside box after screen change")
                        break
                
                if needs_reset:
                    # Reset player to safe spawn point
                    spawn_point = self.game.level.get_spawn_point()
                    self.game.player.x = spawn_point[0]
                    self.game.player.y = spawn_point[1]
                    self.game.player.vel_x = 0
                    self.game.player.vel_y = 0
                    print(f"⚠ Player position reset to ({spawn_point[0]}, {spawn_point[1]}) due to screen change")
    
    def handle_event(self, event):
        """Handle pygame events"""
        # Global fullscreen toggle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()
                return
        
        if self.state == "menu":
            action = self.menu.handle_input(event)
            
            if action == "new_game":
                self.new_game()
            elif action and action.startswith("load_slot_"):
                slot_index = int(action.split("_")[2])
                if self.load_game(slot_index):
                    self.state = "game"
                    self.level_completion_saved = False  # Reset save flag when loading
                    self.previous_level = self.game.current_level if self.game else 0  # Initialize level tracking
                    self.sound_manager.play_background_music('game')
                    self.sound_manager.play_sound('portal_open')
                else:
                    self.sound_manager.play_sound('switch_off')
                    print(f"No save found in slot {slot_index}")
            elif action and action.startswith("delete_slot_"):
                slot_index = int(action.split("_")[2])
                if self.delete_save(slot_index):
                    self.sound_manager.play_sound('switch_off')
                    print(f"Deleted save slot {slot_index}")
                else:
                    print(f"No save to delete in slot {slot_index}")
            elif action and action.startswith("load_level_"):
                level_index = int(action.split("_")[2])
                self.load_specific_level(level_index)
            elif action == "update_level_progress":
                self.update_menu_level_progress()
            elif action == "exit":
                self.running = False
                
        elif self.state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Pause the game
                    self.state = "paused"
                    self.menu.current_menu = "pause"
                    self.menu.selected_index = 0
                    self.menu.game_state_context = "paused"  # Set context to paused game
                    # Ensure menu translations are up to date
                    self.menu.update_menu_translations()
                    return
            
            # Pass event to game
            if self.game:
                result = self.game.handle_event(event)
                
                # Level completion tracking (removed auto-save)
                if self.game.game_state == "won" and not self.level_completion_saved:
                    self.level_completion_saved = True
                    
        elif self.state == "paused":
            action = self.menu.handle_input(event)
            
            if action == "return_to_pause":
                # Already handled by menu, just ensure we stay in paused state
                pass
            elif action == "resume":
                self.state = "game"
            elif action == "restart_level":
                if self.game:
                    self.game.restart_level()
                    self.level_completion_saved = False  # Reset save flag when restarting
                    self.state = "game"
            elif action and action.startswith("save_slot_"):
                slot_index = int(action.split("_")[2])
                if self.save_game(slot_index):
                    self.sound_manager.play_sound('portal_open')
                    # Return to pause menu
                    self.menu.current_menu = "pause"
                    self.menu.selected_index = 0
                else:
                    self.sound_manager.play_sound('switch_off')
            elif action and action.startswith("load_slot_"):
                slot_index = int(action.split("_")[2])
                if self.load_game(slot_index):
                    self.state = "game"
                    self.level_completion_saved = False  # Reset save flag when loading in pause menu
                    self.previous_level = self.game.current_level if self.game else 0  # Initialize level tracking
                    self.sound_manager.play_background_music('game')
                    self.sound_manager.play_sound('portal_open')
                else:
                    self.sound_manager.play_sound('switch_off')
            elif action and action.startswith("delete_slot_"):
                slot_index = int(action.split("_")[2])
                if self.delete_save(slot_index):
                    self.sound_manager.play_sound('switch_off')
                    print(f"Deleted save slot {slot_index}")
                    # Return to pause menu
                    self.menu.current_menu = "pause"
                    self.menu.selected_index = 0
                else:
                    print(f"No save to delete in slot {slot_index}")
            elif action == "exit_to_main":
                self.state = "menu"
                self.menu.current_menu = "main"
                self.menu.selected_index = 0
                self.menu.game_state_context = "menu"  # Reset context to main menu
                self.update_menu_level_progress()  # Update level progress when returning to menu
                self.sound_manager.play_background_music('menu')
    
    def update(self, dt):
        """Update game logic"""
        if self.state == "menu":
            self.menu.update(dt)
            
            # Update level progress when in menu (but not too frequently)
            if not hasattr(self, '_last_level_update'):
                self._last_level_update = 0
            self._last_level_update += dt
            if self._last_level_update > 1.0:  # Update every second
                self.update_menu_level_progress()
                self._last_level_update = 0
            
            # Apply audio settings changes
            self.apply_audio_settings()
            
        elif self.state == "paused":
            self.menu.update(dt)
            
            # Apply audio settings changes
            self.apply_audio_settings()
            
        elif self.state == "game" and self.game:
            self.game.update(dt)
            
            # Check if level changed (for next level progression)
            if self.previous_level is not None and self.game.current_level != self.previous_level:
                self.level_completion_saved = False  # Reset save flag on level change
            self.previous_level = self.game.current_level
            
            # Removed auto-save to prevent unwanted overwrites
    
    def draw(self, screen):
        """Draw everything"""
        if self.state == "menu":
            # Pass save info callback to menu for load save display
            if self.menu.current_menu == "load_save":
                # Create a custom draw for load save menu with save info
                self.menu.draw_load_save_with_info(screen, self.get_save_info)
            else:
                self.menu.draw(screen)
            
        elif self.state == "paused":
            # Draw game in background (dimmed)
            if self.game:
                self.game.draw(screen)
            
            # Draw pause menu on top with save info if needed
            if self.menu.current_menu == "load_save":
                self.menu.draw_load_save_with_info(screen, self.get_save_info)
            elif self.menu.current_menu == "help":
                # Get current level hint if game is running
                level_hint = self.game.level.hint_text if self.game and self.game.level else None
                self.menu.draw_help_with_info(screen, level_hint)
            else:
                self.menu.draw(screen)
            
        elif self.state == "game" and self.game:
            self.game.draw(screen)
            
            # Draw additional UI elements for menu access
            font = pygame.font.Font(None, 24)
            menu_text = font.render("ESC - Menu", True, WHITE)
            screen.blit(menu_text, (self.width - 120, 10))
    
    def quit(self):
        """Clean up and quit"""
        # Save settings only (removed auto-save of game state)
        self.save_settings()
        
        # Stop audio
        self.sound_manager.stop_music()
        
        self.running = False