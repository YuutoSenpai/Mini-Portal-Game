import pygame
from ..utils.constants import *
from ..utils.translations import language_manager

class UI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize fonts
        pygame.font.init()
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI colors
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black
        self.text_color = WHITE
        self.highlight_color = YELLOW
        self.button_color = GRAY
        self.button_hover_color = LIGHT_GRAY
        
    def draw_instructions(self, screen):
        """Draw game instructions"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 50))
        screen.blit(overlay, (0, 0))
        
        # Title
        title = self.large_font.render("MINI PORTAL GAME", True, self.highlight_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "OVLÁDÁNÍ:",
            "WASD / Šipky - Pohyb",
            "Mezerník - Skok", 
            "Levé tlačítko - Modrý portál",
            "Pravé tlačítko - Oranžový portál",
            "R - Restartovat úroveň",
            "ESC - Pozastavit",
            "F11 - Celoobrazovkový režim",
            "",
            "CÍL:",
            "Použijte portály k dosažení cíle!",
            "Na červené plochy nelze umístit portály.",
            "Aktivujte spínače pomocí krabic.",
            "",
            "Stiskněte libovolnou klávesu pro start!"
        ]
        
        y_offset = 250
        for line in instructions:
            if line == "":
                y_offset += 20
                continue
                
            if line.endswith(":"):
                color = self.highlight_color
                font = self.medium_font
            else:
                color = self.text_color
                font = self.small_font
                
            text = font.render(line, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_win_screen(self, screen, level):
        """Draw level completion screen"""
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 50, 0))
        screen.blit(overlay, (0, 0))
        
        # Win message
        win_text = self.large_font.render("LEVEL COMPLETE!", True, self.highlight_color)
        win_rect = win_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(win_text, win_rect)
        
        level_text = self.medium_font.render(f"Level {level + 1} Completed", True, self.text_color)
        level_rect = level_text.get_rect(center=(self.screen_width // 2, 260))
        screen.blit(level_text, level_rect)
        
        # Instructions
        next_text = self.small_font.render("Stiskni N pro načtení dalšího levelu", True, self.text_color)
        next_rect = next_text.get_rect(center=(self.screen_width // 2, 350))
        screen.blit(next_text, next_rect)
        
        restart_text = self.small_font.render("Stiskni R pro restart", True, self.text_color)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, 380))
        screen.blit(restart_text, restart_rect)
    
    def draw_pause_screen(self, screen, level_time=None, current_level=None):
        """Draw enhanced pause screen with level stats"""
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(150)
        overlay.fill((50, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause message
        pause_text = self.large_font.render("PAUSED", True, self.highlight_color)
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(pause_text, pause_rect)
        
        # Level stats if available
        if level_time is not None and current_level is not None:
            stats_y = 220
            
            # Current time
            time_text = f"Čas: {level_time:.1f}s"
            time_surface = self.small_font.render(time_text, True, WHITE)
            time_rect = time_surface.get_rect(center=(self.screen_width // 2, stats_y))
            screen.blit(time_surface, time_rect)
            
            # Star targets
            target_times = {
                0: (15, 30, 60), 1: (20, 40, 80), 2: (25, 45, 90),
                3: (30, 60, 120), 4: (45, 90, 180), 5: (60, 120, 240),
                6: (40, 80, 160), 7: (50, 100, 200), 8: (70, 140, 280),
                9: (60, 120, 240), 10: (90, 180, 360)
            }
            
            times = target_times.get(current_level, (60, 120, 240))
            
            targets_text = f"Star Targets: 3★ ≤{times[0]}s | 2★ ≤{times[1]}s | 1★ ≤{times[2]}s"
            targets_surface = self.small_font.render(targets_text, True, YELLOW)
            targets_rect = targets_surface.get_rect(center=(self.screen_width // 2, stats_y + 30))
            screen.blit(targets_surface, targets_rect)
        
        resume_text = self.small_font.render("Stiskni ESC pro pokračování", True, self.text_color)
        resume_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        screen.blit(resume_text, resume_rect)
    
    def draw_hud(self, screen, level, level_time=None, stars=None, total_stars=None):
        """Draw heads-up display"""
        # Level indicator
        level_text = self.small_font.render(f"Level: {level}", True, self.text_color)
        screen.blit(level_text, (10, 10))
        
        # Timer
        if level_time is not None:
            time_text = self.small_font.render(f"Čas: {level_time:.1f}s", True, self.text_color)
            screen.blit(time_text, (10, 35))
        
        # Stars for current level
        if stars is not None and stars > 0:
            # Draw stars as circles instead of Unicode characters
            star_text = f"Level Stars: {stars}/3"
            stars_surface = self.small_font.render(star_text, True, self.text_color)
            screen.blit(stars_surface, (10, 60))
            
            # Draw visual stars next to text
            star_x = 10 + stars_surface.get_width() + 10
            star_y = 65
            star_size = 8
            
            for i in range(3):
                star_color = YELLOW if i < stars else GRAY
                # Draw star as filled circle
                pygame.draw.circle(screen, star_color, (star_x + i * 20, star_y), star_size)
                # Add shine effect for filled stars
                if i < stars:
                    pygame.draw.circle(screen, WHITE, (star_x + i * 20 - 2, star_y - 2), 3)
        
        # Total stars collected
        if total_stars is not None:
            total_text = f"Hvězd celkem: {total_stars}"
            total_surface = self.small_font.render(total_text, True, YELLOW)
            screen.blit(total_surface, (10, 85))
        
        # Controls reminder
        controls_text = self.small_font.render("LClick: Modrý Portál | RClick: Oranžový Portál | H: Help | F11: Fullscreen", True, self.text_color)
        screen.blit(controls_text, (10, self.screen_height - 30))

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Menu state
        self.current_menu = "main"  # main, settings, credits, load_save, save_select
        self.selected_index = 0
        self.save_slot_count = 3
        self.previous_menu = "main"  # Track previous menu for proper back navigation
        self.game_state_context = "menu"  # Track if we're in menu or paused game context
        
        # Menu items (will be updated with translations)
        self.main_menu_items = []
        
        # In-game pause menu items (will be updated with translations)
        self.pause_menu_items = []
        
        # Settings menu items (will be updated with translations)
        self.settings_items = []
        
        # Initialize menu translations
        self.update_menu_translations()
        
        # Level selection menu items (will be populated with unlocked levels)
        self.level_select_items = []
        self.total_levels = 10  # Levels 0-9 (Level 10 displayed = index 9)
        self.unlocked_levels = 1  # At minimum, level 0 is unlocked
        
        # Scrolling for level selection menu
        self.level_scroll_offset = 0
        self.max_visible_levels = 8  # Maximum levels visible at once
        
        # Initialize with default state (Level 1 unlocked, rest locked)
        self.initialize_default_level_progress()
        
        # Settings values
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.6
        self.sound_effects_enabled = True
        self.background_music_enabled = True
        
        # Colors
        self.bg_color = (20, 30, 50)
        self.text_color = WHITE
        self.selected_color = YELLOW
        self.title_color = CYAN
        
        # Background particles
        self.particles = []
        self.init_particles()
    
    def init_particles(self):
        """Initialize background particles"""
        import random
        for i in range(50):
            particle = {
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'vel_x': random.uniform(-20, 20),
                'vel_y': random.uniform(-20, 20),
                'size': random.uniform(1, 3),
                'alpha': random.randint(50, 150)
            }
            self.particles.append(particle)
    
    def update(self, dt):
        """Update menu animations"""
        # Update particles
        import random
        for particle in self.particles:
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = self.screen_width
            elif particle['x'] > self.screen_width:
                particle['x'] = 0
                
            if particle['y'] < 0:
                particle['y'] = self.screen_height
            elif particle['y'] > self.screen_height:
                particle['y'] = 0
    
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if self.current_menu == "main":
                return self.handle_main_menu_input(event)
            elif self.current_menu == "pause":
                return self.handle_pause_menu_input(event)
            elif self.current_menu == "settings":
                return self.handle_settings_input(event)
            elif self.current_menu == "credits":
                return self.handle_credits_input(event)
            elif self.current_menu == "load_save":
                return self.handle_load_save_input(event)
            elif self.current_menu == "save_select":
                return self.handle_save_select_input(event)
            elif self.current_menu == "level_select":
                return self.handle_level_select_input(event)
            elif self.current_menu == "help":
                return self.handle_help_input(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_click(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_hover(event)
        elif event.type == pygame.MOUSEWHEEL:
            # Handle mouse wheel scrolling in level select menu
            if self.current_menu == "level_select":
                if event.y > 0:  # Scroll up
                    self.level_scroll_offset = max(0, self.level_scroll_offset - 1)
                elif event.y < 0:  # Scroll down
                    max_scroll = max(0, len(self.level_select_items) - self.max_visible_levels)
                    self.level_scroll_offset = min(max_scroll, self.level_scroll_offset + 1)
        return None
    
    def return_from_settings(self):
        """Handle returning from settings menu based on context"""
        if self.game_state_context == "paused":
            # We're in a paused game, return to pause menu
            self.current_menu = "pause"
            self.selected_index = 0
            return "return_to_pause"
        else:
            # We're in main menu context, return to previous menu
            self.current_menu = self.previous_menu
            self.selected_index = 0
            return None
    
    def handle_mouse_click(self, event):
        """Handle mouse clicks on menu items"""
        if event.button == 1:  # Left click
            mouse_x, mouse_y = event.pos
            
            if self.current_menu == "main":
                return self.check_main_menu_click(mouse_x, mouse_y)
            elif self.current_menu == "pause":
                return self.check_pause_menu_click(mouse_x, mouse_y)
            elif self.current_menu == "settings":
                return self.check_settings_click(mouse_x, mouse_y)
            elif self.current_menu == "load_save":
                return self.check_load_save_click(mouse_x, mouse_y)
            elif self.current_menu == "save_select":
                return self.check_save_select_click(mouse_x, mouse_y)
            elif self.current_menu == "level_select":
                return self.check_level_select_click(mouse_x, mouse_y)
        return None
    
    def handle_mouse_hover(self, event):
        """Handle mouse hover to highlight menu items"""
        mouse_x, mouse_y = event.pos
        
        if self.current_menu == "main":
            self.check_main_menu_hover(mouse_x, mouse_y)
        elif self.current_menu == "pause":
            self.check_pause_menu_hover(mouse_x, mouse_y)
        elif self.current_menu == "settings":
            self.check_settings_hover(mouse_x, mouse_y)
        elif self.current_menu == "load_save":
            self.check_load_save_hover(mouse_x, mouse_y)
        elif self.current_menu == "save_select":
            self.check_save_select_hover(mouse_x, mouse_y)
        elif self.current_menu == "level_select":
            self.check_level_select_hover(mouse_x, mouse_y)
    
    def handle_main_menu_input(self, event):
        """Handle main menu input"""
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.main_menu_items)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.main_menu_items)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            selected_item = self.main_menu_items[self.selected_index]
            if selected_item == "Nová hra":
                return "new_game"
            elif selected_item == "Načíst hru":
                self.current_menu = "load_save"
                self.selected_index = 0
            elif selected_item == "Úrovně":
                self.current_menu = "level_select"
                self.selected_index = 0
                self.level_scroll_offset = 0  # Reset scroll to top
                return "update_level_progress"  # Signal to update progress
            elif selected_item == "Nastavení":
                self.previous_menu = self.current_menu
                self.current_menu = "settings"
                self.selected_index = 0
            elif selected_item == "Titulky":
                self.current_menu = "credits"
            elif selected_item == "Konec":
                return "exit"
        
        return None
    
    def handle_pause_menu_input(self, event):
        """Handle pause menu input"""
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.pause_menu_items)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.pause_menu_items)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            selected_item = self.pause_menu_items[self.selected_index]
            if selected_item == "Pokračovat":
                return "resume"
            elif selected_item == "Restartovat úroveň":
                return "restart_level"
            elif selected_item == "Uložit hru":
                self.current_menu = "save_select"
                self.selected_index = 0
            elif selected_item == "Načíst hru":
                self.current_menu = "load_save"
                self.selected_index = 0
            elif selected_item == "Nastavení":
                self.previous_menu = self.current_menu
                self.current_menu = "settings"
                self.selected_index = 0
            elif selected_item == "Nápověda (?)":
                self.current_menu = "help"
                self.selected_index = 0
            elif selected_item == "Zpět do hlavního menu":
                return "exit_to_main"
        elif event.key == pygame.K_ESCAPE:
            return "resume"  # ESC also resumes
        
        return None
    
    def handle_settings_input(self, event):
        """Handle settings menu input"""
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.settings_items)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.settings_items)
        elif event.key == pygame.K_LEFT:
            self.adjust_setting(-0.1)
        elif event.key == pygame.K_RIGHT:
            self.adjust_setting(0.1)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            selected_item = self.settings_items[self.selected_index]
            if selected_item == "Zpět":
                return self.return_from_settings()
            elif selected_item in ["Zvukové efekty", "Hudba na pozadí"]:
                self.adjust_setting(0)  # Toggle the setting
        elif event.key == pygame.K_ESCAPE:
            return self.return_from_settings()
        
        return None
    
    def handle_credits_input(self, event):
        """Handle credits menu input"""
        if event.key == pygame.K_ESCAPE:
            self.current_menu = "main"
            self.selected_index = 0
        return None
    
    def handle_load_save_input(self, event):
        """Handle load save slot menu input"""
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % (self.save_slot_count + 1)  # +1 for Back
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % (self.save_slot_count + 1)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_index < self.save_slot_count:
                return f"load_slot_{self.selected_index}"
            else:  # Back button
                self.current_menu = "main"
                self.selected_index = 0
        elif event.key == pygame.K_DELETE or event.key == pygame.K_d:
            if self.selected_index < self.save_slot_count:
                return f"delete_slot_{self.selected_index}"
        elif event.key == pygame.K_ESCAPE:
            self.current_menu = "main" 
            self.selected_index = 0
        return None
    
    def handle_save_select_input(self, event):
        """Handle save slot selection menu input"""
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % (self.save_slot_count + 1)  # +1 for Back
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % (self.save_slot_count + 1)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_index < self.save_slot_count:
                return f"save_slot_{self.selected_index}"
            else:  # Back button
                self.current_menu = "pause"
                self.selected_index = 0
        elif event.key == pygame.K_ESCAPE:
            self.current_menu = "pause"
            self.selected_index = 0
        return None
    
    def handle_help_input(self, event):
        """Handle help menu input"""
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self.current_menu = "pause"
            self.selected_index = 0
        return None
    
    def adjust_setting(self, delta):
        """Adjust setting values"""
        selected_item = self.settings_items[self.selected_index]
        if selected_item == "Hlavní hlasitost":
            self.master_volume = max(0, min(1, self.master_volume + delta))
        elif selected_item == "Hlasitost efektů":
            self.sfx_volume = max(0, min(1, self.sfx_volume + delta))
        elif selected_item == "Hlasitost hudby":
            self.music_volume = max(0, min(1, self.music_volume + delta))
        elif selected_item == "Zvukové efekty":
            self.sound_effects_enabled = not self.sound_effects_enabled
        elif selected_item == "Hudba na pozadí":
            self.background_music_enabled = not self.background_music_enabled
    
    def draw(self, screen):
        """Draw the menu"""
        # Fill background
        screen.fill(self.bg_color)
        
        # Draw particles
        for particle in self.particles:
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(particle['alpha'])
            particle_surface.fill(CYAN)
            screen.blit(particle_surface, (particle['x'], particle['y']))
        
        if self.current_menu == "main":
            self.draw_main_menu(screen)
        elif self.current_menu == "pause":
            self.draw_pause_menu(screen)
        elif self.current_menu == "settings":
            self.draw_settings_menu(screen)
        elif self.current_menu == "credits":
            self.draw_credits(screen)
        elif self.current_menu == "load_save":
            self.draw_load_save_menu(screen)
        elif self.current_menu == "save_select":
            self.draw_save_select_menu(screen)
        elif self.current_menu == "level_select":
            self.draw_level_select_menu(screen)
        elif self.current_menu == "help":
            self.draw_help_menu(screen)
    
    def draw_main_menu(self, screen):
        """Draw main menu"""
        # Title
        title = self.title_font.render("MINI PORTAL", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("A 2D Portal-Inspired Puzzle Game", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(subtitle, subtitle_rect)
        
        # Menu items
        start_y = 300
        for i, item in enumerate(self.main_menu_items):
            color = self.selected_color if i == self.selected_index else self.text_color
            text = self.button_font.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, start_y + i * 60))
            screen.blit(text, text_rect)
            
            # Selection indicator
            if i == self.selected_index:
                pygame.draw.rect(screen, self.selected_color, 
                               (text_rect.left - 20, text_rect.top - 5, 
                                text_rect.width + 40, text_rect.height + 10), 3)
        
    
    def draw_pause_menu(self, screen):
        """Draw pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((20, 20, 60))
        screen.blit(overlay, (0, 0))
        
        # Title
        title = self.title_font.render("POZASTAVENO", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)
        
        # Menu items
        start_y = 250
        # Debug: print pause menu items if empty
        if not self.pause_menu_items:
            print(f"⚠ Warning: pause_menu_items is empty! Current menu: {self.current_menu}")
            self.update_menu_translations()  # Try to repopulate
        
        for i, item in enumerate(self.pause_menu_items):
            color = self.selected_color if i == self.selected_index else self.text_color
            text = self.button_font.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, start_y + i * 60))
            screen.blit(text, text_rect)
            
            # Selection indicator
            if i == self.selected_index:
                pygame.draw.rect(screen, self.selected_color, 
                               (text_rect.left - 20, text_rect.top - 5, 
                                text_rect.width + 40, text_rect.height + 10), 3)
        
        # Instructions
        instructions = self.small_font.render("ESC nebo vyberte Pokračovat pro pokračování ve hře", True, self.text_color)
        instructions_rect = instructions.get_rect(center=(self.screen_width // 2, start_y + len(self.pause_menu_items) * 60 + 40))
        screen.blit(instructions, instructions_rect)
    
    def draw_settings_menu(self, screen):
        """Draw settings menu"""
        # Title
        title = self.button_font.render(language_manager.get_text("settings").upper(), True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)
        
        # Settings items
        start_y = 250
        for i, item in enumerate(self.settings_items):
            if i == len(self.settings_items) - 1:  # Back is always the last item
                color = self.selected_color if i == self.selected_index else self.text_color
                text = self.button_font.render(item, True, color)
                text_rect = text.get_rect(center=(self.screen_width // 2, start_y + i * 60))
                screen.blit(text, text_rect)
            else:
                # Setting with value
                color = self.selected_color if i == self.selected_index else self.text_color
                
                # Get setting value based on item text
                if item == "Hlavní hlasitost":
                    value = f"{int(self.master_volume * 100)}%"
                elif item == "Hlasitost efektů":
                    value = f"{int(self.sfx_volume * 100)}%"
                elif item == "Hlasitost hudby":
                    value = f"{int(self.music_volume * 100)}%"
                elif item == "Zvukové efekty":
                    value = language_manager.get_text("on") if self.sound_effects_enabled else language_manager.get_text("off")
                elif item == "Hudba na pozadí":
                    value = language_manager.get_text("on") if self.background_music_enabled else language_manager.get_text("off")
                else:
                    value = ""
                
                setting_text = f"{item}: {value}"
                text = self.button_font.render(setting_text, True, color)
                text_rect = text.get_rect(center=(self.screen_width // 2, start_y + i * 60))
                screen.blit(text, text_rect)
            
            # Selection indicator
            if i == self.selected_index:
                pygame.draw.rect(screen, self.selected_color, 
                               (self.screen_width // 2 - 200, start_y + i * 60 - 15, 
                                400, 30), 3)
        
        # Instructions
        instructions = self.small_font.render(language_manager.get_text("settings_instruction"), True, self.text_color)
        instructions_rect = instructions.get_rect(center=(self.screen_width // 2, self.screen_height - 80))
        screen.blit(instructions, instructions_rect)
        
        # Back instruction
        back_instruction = self.small_font.render(language_manager.get_text("esc_back"), True, GRAY)
        back_rect = back_instruction.get_rect(center=(self.screen_width // 2, self.screen_height - 40))
        screen.blit(back_instruction, back_rect)
    
    def draw_credits(self, screen):
        """Draw credits screen"""
        # Title
        title = self.button_font.render("CREDITS", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)
        
        # Credits text
        credits = [
            "Vytvořeno jako školní projekt",
            "",
            "Inspirace - Portal (Valve Corporation)",
            "",
            "Programoval: Jaromír Rýdlo",
            "Grafika: Procedurální",
            "Sound: Free assety",
            "",
            "Děkuji za hraní!",
            "",
            "Stiskni ESC pro pokračování"
        ]
        
        start_y = 250
        for i, line in enumerate(credits):
            if line == "":
                continue
            
            text = self.small_font.render(line, True, self.text_color)
            text_rect = text.get_rect(center=(self.screen_width // 2, start_y + i * 30))
            screen.blit(text, text_rect)
    
    def draw_load_save_menu(self, screen, save_info_callback=None):
        """Draw load save slot selection menu"""
        # Title
        title = self.title_font.render("LOAD GAME", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        start_y = 200
        for i in range(self.save_slot_count):
            slot_text = f"Save Slot {i + 1}"
            detail_text = "Empty"
            
            # Get save info if callback provided
            if save_info_callback:
                save_info = save_info_callback(i)
                if save_info:
                    # Format timestamp
                    try:
                        timestamp = save_info['timestamp'][:19].replace('T', ' ')  # Remove milliseconds and T
                        detail_text = f"Level {save_info['level']} - {save_info['total_stars']} stars - {timestamp}"
                    except:
                        detail_text = f"Level {save_info['level']} - {save_info['total_stars']} stars"
            
            # Highlight selected slot
            color = self.selected_color if i == self.selected_index else self.text_color
            
            slot_surface = self.button_font.render(slot_text, True, color)
            detail_surface = self.small_font.render(detail_text, True, self.text_color)
            
            slot_rect = slot_surface.get_rect(center=(self.screen_width // 2, start_y + i * 80))
            detail_rect = detail_surface.get_rect(center=(self.screen_width // 2, start_y + i * 80 + 30))
            
            # Draw slot background if selected
            if i == self.selected_index:
                bg_rect = pygame.Rect(slot_rect.x - 20, slot_rect.y - 10, 
                                    slot_rect.width + 40, 60)
                pygame.draw.rect(screen, (50, 50, 50), bg_rect)
                pygame.draw.rect(screen, self.selected_color, bg_rect, 2)
            
            screen.blit(slot_surface, slot_rect)
            screen.blit(detail_surface, detail_rect)
        
        # Back button
        back_color = self.selected_color if self.selected_index == self.save_slot_count else self.text_color
        back_text = self.button_font.render("Back", True, back_color)
        back_rect = back_text.get_rect(center=(self.screen_width // 2, start_y + self.save_slot_count * 80))
        screen.blit(back_text, back_rect)
        
        # Instructions
        instructions = self.small_font.render("Stiskni D nebo DELETE pro smazání saves", True, self.text_color)
        instructions_rect = instructions.get_rect(center=(self.screen_width // 2, start_y + self.save_slot_count * 80 + 50))
        screen.blit(instructions, instructions_rect)
    
    def draw_save_select_menu(self, screen):
        """Draw save slot selection menu"""
        # Title
        title = self.title_font.render("SAVE GAME", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        # Similar to load menu but for saving
        start_y = 200
        for i in range(self.save_slot_count):
            slot_text = f"Save Slot {i + 1}"
            detail_text = "Click to save here"
            
            color = self.selected_color if i == self.selected_index else self.text_color
            
            slot_surface = self.button_font.render(slot_text, True, color)
            detail_surface = self.small_font.render(detail_text, True, self.text_color)
            
            slot_rect = slot_surface.get_rect(center=(self.screen_width // 2, start_y + i * 80))
            detail_rect = detail_surface.get_rect(center=(self.screen_width // 2, start_y + i * 80 + 30))
            
            if i == self.selected_index:
                bg_rect = pygame.Rect(slot_rect.x - 20, slot_rect.y - 10, 
                                    slot_rect.width + 40, 60)
                pygame.draw.rect(screen, (50, 50, 50), bg_rect)
                pygame.draw.rect(screen, self.selected_color, bg_rect, 2)
            
            screen.blit(slot_surface, slot_rect)
            screen.blit(detail_surface, detail_rect)
        
        # Back button
        back_color = self.selected_color if self.selected_index == self.save_slot_count else self.text_color
        back_text = self.button_font.render("Back", True, back_color)
        back_rect = back_text.get_rect(center=(self.screen_width // 2, start_y + self.save_slot_count * 80))
        screen.blit(back_text, back_rect)
    def draw_load_save_with_info(self, screen, get_save_info_callback):
        """Draw load save menu with actual save data"""
        # Fill background
        screen.fill(self.bg_color)
        
        # Draw particles
        for particle in self.particles:
            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2))
            particle_surface.set_alpha(particle["alpha"])
            particle_surface.fill(CYAN)
            screen.blit(particle_surface, (particle["x"], particle["y"]))
        
        # Draw load save menu with save info
        self.draw_load_save_menu(screen, get_save_info_callback)
    
    def check_main_menu_click(self, mouse_x, mouse_y):
        """Check if mouse clicked on main menu item"""
        start_y = 300
        for i, item in enumerate(self.main_menu_items):
            item_y = start_y + i * 60
            if item_y - 25 <= mouse_y <= item_y + 25:
                self.selected_index = i
                selected_item = self.main_menu_items[i]
                if selected_item == "Nová hra":
                    return "new_game"
                elif selected_item == "Načíst hru":
                    self.current_menu = "load_save"
                    self.selected_index = 0
                elif selected_item == "Úrovně":
                    self.current_menu = "level_select"
                    self.selected_index = 0
                    self.level_scroll_offset = 0  # Reset scroll to top
                    return "update_level_progress"  # Signal to update progress
                elif selected_item == "Nastavení":
                    self.current_menu = "settings"
                    self.selected_index = 0
                elif selected_item == "Titulky":
                    self.current_menu = "credits"
                elif selected_item == "Konec":
                    return "exit"
        return None
    
    def check_main_menu_hover(self, mouse_x, mouse_y):
        """Check if mouse is hovering over main menu item"""
        start_y = 300
        for i, item in enumerate(self.main_menu_items):
            item_y = start_y + i * 60
            if item_y - 25 <= mouse_y <= item_y + 25:
                self.selected_index = i
                break
    
    def check_pause_menu_click(self, mouse_x, mouse_y):
        """Check if mouse clicked on pause menu item"""
        start_y = 250
        for i, item in enumerate(self.pause_menu_items):
            item_y = start_y + i * 60
            if item_y - 25 <= mouse_y <= item_y + 25:
                self.selected_index = i
                selected_item = self.pause_menu_items[i]
                if selected_item == "Pokračovat":
                    return "resume"
                elif selected_item == "Restartovat úroveň":
                    return "restart_level"
                elif selected_item == "Uložit hru":
                    self.current_menu = "save_select"
                    self.selected_index = 0
                elif selected_item == "Načíst hru":
                    self.current_menu = "load_save"
                    self.selected_index = 0
                elif selected_item == "Nastavení":
                    self.current_menu = "settings"
                    self.selected_index = 0
                elif selected_item == "Nápověda (?)":
                    self.current_menu = "help"
                    self.selected_index = 0
                elif selected_item == "Zpět do hlavního menu":
                    return "exit_to_main"
        return None
    
    def check_pause_menu_hover(self, mouse_x, mouse_y):
        """Check if mouse is hovering over pause menu item"""
        start_y = 250
        for i, item in enumerate(self.pause_menu_items):
            item_y = start_y + i * 60
            if item_y - 25 <= mouse_y <= item_y + 25:
                self.selected_index = i
                break
    
    def check_settings_click(self, mouse_x, mouse_y):
        """Check if mouse clicked on settings item"""
        start_y = 250
        for i, item in enumerate(self.settings_items):
            item_y = start_y + i * 60
            if item_y - 25 <= mouse_y <= item_y + 25:
                self.selected_index = i
                selected_item = self.settings_items[i]
                if selected_item == "Zpět":
                    return self.return_from_settings()
                elif selected_item in ["Zvukové efekty", "Hudba na pozadí"]:
                    self.adjust_setting(0)  # Toggle the setting
                return "setting_changed"
        return None
    
    def check_settings_hover(self, mouse_x, mouse_y):
        """Check if mouse is hovering over settings item"""
        start_y = 250
        for i, item in enumerate(self.settings_items):
            item_y = start_y + i * 60
            if item_y - 25 <= mouse_y <= item_y + 25:
                self.selected_index = i
                break
    
    def check_load_save_click(self, mouse_x, mouse_y):
        """Check if mouse clicked on load save slot"""
        start_y = 200
        for i in range(self.save_slot_count + 1):  # +1 for Back button
            item_y = start_y + i * 80
            if item_y - 30 <= mouse_y <= item_y + 30:
                self.selected_index = i
                if i < self.save_slot_count:
                    return f"load_slot_{i}"
                else:  # Back button
                    self.current_menu = "main"
                    self.selected_index = 0
        return None
    
    def check_load_save_hover(self, mouse_x, mouse_y):
        """Check if mouse is hovering over load save slot"""
        start_y = 200
        for i in range(self.save_slot_count + 1):
            if i < self.save_slot_count:
                # Save slots use 80px spacing
                item_y = start_y + i * 80
                if item_y - 30 <= mouse_y <= item_y + 30:
                    self.selected_index = i
                    break
            else:
                # Back button position matches draw_load_save_menu
                back_y = start_y + self.save_slot_count * 80
                if back_y - 25 <= mouse_y <= back_y + 25:
                    self.selected_index = i
                    break
    
    def check_save_select_click(self, mouse_x, mouse_y):
        """Check if mouse clicked on save slot"""
        start_y = 200
        for i in range(self.save_slot_count + 1):  # +1 for Back button
            item_y = start_y + i * 80
            if item_y - 30 <= mouse_y <= item_y + 30:
                self.selected_index = i
                if i < self.save_slot_count:
                    return f"save_slot_{i}"
                else:  # Back button
                    self.current_menu = "pause"
                    self.selected_index = 0
        return None
    
    def check_save_select_hover(self, mouse_x, mouse_y):
        """Check if mouse is hovering over save slot"""
        start_y = 200
        for i in range(self.save_slot_count + 1):
            item_y = start_y + i * 80
            if item_y - 30 <= mouse_y <= item_y + 30:
                self.selected_index = i
                break

    def draw_help_menu(self, screen, current_level_hint=None):
        """Draw help menu with controls and level hint"""
        # Title
        title = self.title_font.render("NÁPOVĚDA", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        # Controls section
        controls_title = self.button_font.render("OVLÁDÁNÍ:", True, YELLOW)
        controls_rect = controls_title.get_rect(center=(self.screen_width // 2, 180))
        screen.blit(controls_title, controls_rect)
        
        controls = [
            "WASD / Šipky - Pohyb hráče",
            "Mezerník - Skok",
            "Levé tlačítko myši - Modrý portál",
            "Pravé tlačítko myši - Oranžový portál", 
            "H - Přepínání nápověd",
            "R - Restartovat úroveň",
            "ESC - Menu pozastavení",
            "F11 - Celoobrazovkový režim"
        ]
        
        y_offset = 220
        for control in controls:
            text = self.small_font.render(control, True, WHITE)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 25
        
        # Current level hint if provided
        if current_level_hint:
            hint_title = self.button_font.render("NÁPOVĚDA PRO AKTUÁLNÍ ÚROVEŇ:", True, YELLOW)
            hint_rect = hint_title.get_rect(center=(self.screen_width // 2, y_offset + 30))
            screen.blit(hint_title, hint_rect)
            
            hint_text = self.small_font.render(current_level_hint[:80] + "..." if len(current_level_hint) > 80 else current_level_hint, True, CYAN)
            hint_text_rect = hint_text.get_rect(center=(self.screen_width // 2, y_offset + 70))
            screen.blit(hint_text, hint_text_rect)
        
        # Back instruction
        back_text = self.small_font.render("Stiskněte ESC nebo ENTER pro návrat", True, WHITE)
        back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(back_text, back_rect)

    def draw_help_with_info(self, screen, current_level_hint):
        """Draw help menu with actual level hint"""
        # Fill background
        screen.fill(self.bg_color)
        
        # Draw particles
        for particle in self.particles:
            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2))
            particle_surface.set_alpha(particle["alpha"])
            particle_surface.fill(CYAN)
            screen.blit(particle_surface, (particle["x"], particle["y"]))
        
        # Draw help menu with level hint
        self.draw_help_menu(screen, current_level_hint)
    
    def update_level_progress(self, level_stars, current_level):
        """Update level progress data for level selection menu"""
        # Calculate unlocked levels (current level + 1, but at least 1)
        self.unlocked_levels = max(current_level + 1, 1)
        
        # Update level select items based on unlocked levels
        self.level_select_items = []
        for i in range(self.total_levels):
            if i < self.unlocked_levels:
                stars = level_stars.get(i, 0)
                star_text = "*" * stars + "-" * (3 - stars) if stars > 0 else "---"
                self.level_select_items.append(f"Level {i + 1} {star_text}")
            else:
                self.level_select_items.append(f"Level {i + 1} LOCKED")
        
        self.level_select_items.append(language_manager.get_text("back"))
    
    def initialize_default_level_progress(self):
        """Initialize level progress with defaults (Level 1 unlocked, rest locked)"""
        self.level_select_items = []
        # Level 1 is always unlocked
        self.level_select_items.append("Level 1 ---")
        # All other levels start locked
        for i in range(1, self.total_levels):
            self.level_select_items.append(f"Level {i + 1} LOCKED")
        self.level_select_items.append(language_manager.get_text("back"))
    
    def update_menu_translations(self):
        """Update all menu items with current language translations"""
        # Main menu items
        self.main_menu_items = [
            language_manager.get_text("new_game"),
            language_manager.get_text("load_game"),
            language_manager.get_text("levels"),
            language_manager.get_text("settings"), 
            language_manager.get_text("credits"),
            language_manager.get_text("exit")
        ]
        
        # Pause menu items
        self.pause_menu_items = [
            language_manager.get_text("resume"),
            language_manager.get_text("restart_level"),
            language_manager.get_text("save_game"), 
            language_manager.get_text("load_game"),
            language_manager.get_text("settings"),
            language_manager.get_text("help"),
            language_manager.get_text("exit_to_main")
        ]
        
        # Settings menu items
        self.settings_items = [
            language_manager.get_text("master_volume"),
            language_manager.get_text("sfx_volume"), 
            language_manager.get_text("music_volume"),
            language_manager.get_text("sound_effects"),
            language_manager.get_text("background_music"),
            language_manager.get_text("back")
        ]
    
    def handle_level_select_input(self, event):
        """Handle level select menu input"""
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.level_select_items)
            # Scroll up if selected item is above visible area
            if self.selected_index < self.level_scroll_offset:
                self.level_scroll_offset = self.selected_index
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.level_select_items)
            # Scroll down if selected item is below visible area
            if self.selected_index >= self.level_scroll_offset + self.max_visible_levels:
                self.level_scroll_offset = self.selected_index - self.max_visible_levels + 1
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            # Check if "Back" is selected (last item)
            if self.selected_index == len(self.level_select_items) - 1:
                self.current_menu = "main"
                self.selected_index = 2  # Return to "Levels" position
            else:
                # Level selected - check if unlocked
                selected_item = self.level_select_items[self.selected_index]
                if "LOCKED" not in selected_item:  # Level is unlocked
                    # Extract level number (0-based)
                    level_num = self.selected_index
                    return f"load_level_{level_num}"
        elif event.key == pygame.K_ESCAPE:
            self.current_menu = "main"
            self.selected_index = 2  # Return to "Levels" position
        
        return None
    
    def check_level_select_click(self, mouse_x, mouse_y):
        """Check level select menu clicks"""
        start_y = 250
        visible_end = min(self.level_scroll_offset + self.max_visible_levels, len(self.level_select_items))
        
        for i in range(self.level_scroll_offset, visible_end):
            display_index = i - self.level_scroll_offset
            item = self.level_select_items[i]
            item_rect = pygame.Rect(
                self.screen_width // 2 - 200, 
                start_y + display_index * 50 - 20, 
                400, 40
            )
            if item_rect.collidepoint(mouse_x, mouse_y):
                self.selected_index = i
                # Check if "Back" is clicked (last item)
                if i == len(self.level_select_items) - 1:
                    self.current_menu = "main"
                    self.selected_index = 2  # Return to "Levels" position
                elif "LOCKED" not in item:  # Level is unlocked
                    level_num = i
                    return f"load_level_{level_num}"
        return None
    
    def check_level_select_hover(self, mouse_x, mouse_y):
        """Check level select menu hover"""
        start_y = 250
        visible_end = min(self.level_scroll_offset + self.max_visible_levels, len(self.level_select_items))
        
        for i in range(self.level_scroll_offset, visible_end):
            display_index = i - self.level_scroll_offset
            item_rect = pygame.Rect(
                self.screen_width // 2 - 200, 
                start_y + display_index * 50 - 20, 
                400, 40
            )
            if item_rect.collidepoint(mouse_x, mouse_y):
                self.selected_index = i
                # Update scroll offset to keep selected item visible
                if self.selected_index < self.level_scroll_offset:
                    self.level_scroll_offset = self.selected_index
                elif self.selected_index >= self.level_scroll_offset + self.max_visible_levels:
                    self.level_scroll_offset = self.selected_index - self.max_visible_levels + 1
                break
    
    def draw_level_select_menu(self, screen):
        """Draw level selection menu with stars and lock status"""
        # Fill background
        screen.fill(self.bg_color)
        
        # Draw particles
        for particle in self.particles:
            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2))
            particle_surface.set_alpha(particle["alpha"])
            particle_surface.fill(CYAN)
            screen.blit(particle_surface, (particle["x"], particle["y"]))
        
        # Title
        title = self.title_font.render(language_manager.get_text("level_selection"), True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)
        
        # Subtitle with progress info
        completed_levels = len([item for item in self.level_select_items[:-1] if "*" in item])
        progress_text = f"{language_manager.get_text('completed')}: {completed_levels}/{self.total_levels} | {language_manager.get_text('unlocked')}: {self.unlocked_levels}/{self.total_levels}"
        progress_surface = self.small_font.render(progress_text, True, GRAY)
        progress_rect = progress_surface.get_rect(center=(self.screen_width // 2, 190))
        screen.blit(progress_surface, progress_rect)
        
        # Level menu items with scrolling
        start_y = 250
        visible_end = min(self.level_scroll_offset + self.max_visible_levels, len(self.level_select_items))
        
        for i in range(self.level_scroll_offset, visible_end):
            item = self.level_select_items[i]
            display_index = i - self.level_scroll_offset  # Position on screen
            
            # Determine color based on selection and lock status
            if i == self.selected_index:
                color = self.selected_color
                # Draw selection background
                selection_rect = pygame.Rect(
                    self.screen_width // 2 - 220, 
                    start_y + display_index * 50 - 25, 
                    440, 50
                )
                pygame.draw.rect(screen, (50, 50, 100), selection_rect)
                pygame.draw.rect(screen, self.selected_color, selection_rect, 2)
            elif "LOCKED" in item:
                color = GRAY  # Locked levels are grayed out
            elif "*" in item:
                color = YELLOW  # Completed levels in yellow
            else:
                color = self.text_color  # Available but not completed
            
            # Draw the level text
            text_surface = self.button_font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, start_y + display_index * 50))
            screen.blit(text_surface, text_rect)
        
        # Draw scroll indicators
        if self.level_scroll_offset > 0:
            # Up arrow
            up_arrow = self.small_font.render("▲ Více výše", True, WHITE)
            up_rect = up_arrow.get_rect(center=(self.screen_width // 2, start_y - 30))
            screen.blit(up_arrow, up_rect)
        
        if visible_end < len(self.level_select_items):
            # Down arrow
            down_arrow = self.small_font.render("▼ Více níže", True, WHITE)
            down_rect = down_arrow.get_rect(center=(self.screen_width // 2, start_y + self.max_visible_levels * 50 + 10))
            screen.blit(down_arrow, down_rect)
        
        # Instructions
        if any("LOCKED" in item for item in self.level_select_items[:-1]):
            instruction_text = language_manager.get_text("level_instruction")
        else:
            instruction_text = language_manager.get_text("level_instruction_all")
        
        instruction_surface = self.small_font.render(instruction_text, True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        screen.blit(instruction_surface, instruction_rect)
        
        # Back instruction
        back_instruction = self.small_font.render(language_manager.get_text("esc_back"), True, GRAY)
        back_rect = back_instruction.get_rect(center=(self.screen_width // 2, self.screen_height - 40))
        screen.blit(back_instruction, back_rect)
