import pygame
import json
import math
from ..utils.constants import *
from ..core.game_objects import Box, Switch, Goal
from ..utils.translations import language_manager

class Level:
    """Level class that handles level geometry and objects"""
    def __init__(self, level_index):
        self.level_index = level_index
        self.width = 2000
        self.height = 1200
        
        # Level geometry
        self.walls = []  # List of wall rectangles
        self.non_portalable_walls = []  # Walls that can't have portals
        self.spawn_point = (100, 100)
        
        # Game objects
        self.boxes = []
        self.switches = []
        self.goals = []
        
        # Visual
        self.background_color = (20, 30, 50)  # Dark blue
        self.wall_color = (100, 100, 100)  # Gray
        self.non_portalable_color = (150, 50, 50)  # Red-ish
        
        # Level hints system
        self.hint_text = ""
        self.hint_visible = True  # Start visible
        self.hint_auto_hide_time = 5.0  # Hide after 5 seconds
        self.hint_show_time = 0.0  # Time since hint was shown
        self.time_stuck = 0.0  # Track how long player has been in level
        self.hint_delay = 15.0  # Show hint after 15 seconds if stuck
        
        # Generate level based on index
        self.generate_level(level_index)
        
        # Note: Object validation disabled to prevent modifying level layouts
        # Only call validate_object_positions() manually when debugging
    
    def generate_level(self, level_index):
        """Generate level geometry and objects based on level index"""
        if level_index == 0:
            self.generate_tutorial_level()
        elif level_index == 1:
            self.generate_gap_level()
        elif level_index == 2:
            self.generate_wall_portal_level()
        elif level_index == 3:
            self.generate_box_puzzle_level()
        elif level_index == 4:
            self.generate_switch_puzzle_level()
        elif level_index == 5:
            self.generate_advanced_level()
        elif level_index == 6:
            self.generate_momentum_level()
        elif level_index == 7:
            self.generate_tower_level()
        elif level_index == 8:
            self.generate_maze_level()
        elif level_index == 9:
            self.generate_precision_level()  # This is now the final level (Level 10)
        else:
            # Generate procedural level for indices 10 and higher
            self.generate_procedural_level(level_index)
    
    def generate_tutorial_level(self):
        """Level 0: Basic movement and portal tutorial"""
        # Ground
        self.add_wall(0, self.height - 50, self.width, 50)
        
        # Left wall
        self.add_wall(0, 0, 50, self.height)
        
        # Right wall  
        self.add_wall(self.width - 50, 0, 50, self.height)
        
        # Top wall
        self.add_wall(0, 0, self.width, 50)
        
        # Simple gap to cross (properly spaced - no overlaps)
        self.add_wall(400, self.height - 200, 200, 150)  # Platform 1
        self.add_wall(850, self.height - 200, 200, 150)  # Platform 2 (50px gap from platform 1)
        
        # Spawn point (safe above floor, not in walls)
        self.spawn_point = (150, self.height - 120)  # Away from walls
        
        # Goal positioned safely above platform 2
        goal = Goal(950, self.height - 250)  # Centered on platform 2, 50px above
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = language_manager.get_text("hint_level_0")
    
    def generate_gap_level(self):
        """Level 1: Larger gap requiring portals"""
        # Basic boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Large gap - platforms properly spaced
        self.add_wall(100, self.height - 200, 300, 150)   # Left platform
        self.add_wall(850, self.height - 300, 300, 250)   # Right platform (50px gap)
        
        # Portal walls - properly spaced to avoid overlaps
        self.add_wall(480, self.height - 400, 50, 200)    # Left portal wall (away from platform edge)
        self.add_wall(720, self.height - 500, 50, 200)    # Right portal wall
        
        # Safe spawn point 
        self.spawn_point = (250, self.height - 170)       # Centered on left platform
        
        # Goal positioned safely above right platform
        goal = Goal(1000, self.height - 350)              # Centered on right platform, above it
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = language_manager.get_text("hint_level_1")
    
    def generate_wall_portal_level(self):
        """Level 2: Momentum building and portal through walls"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Left side platform and walls for momentum building (no overlaps)
        self.add_wall(200, self.height - 200, 200, 150)  # Left platform
        self.add_wall(120, self.height - 500, 50, 300)   # Left vertical wall for portals (away from platform)
        
        # Central barrier with proper gap (no overlapping walls)
        center_x = self.width // 2
        self.add_wall(center_x - 25, 50, 50, 250)        # Top part of central wall
        self.add_wall(center_x - 25, 500, 50, self.height - 550)  # Bottom part
        # Gap between Y 300-500 (200px passage)
        self.add_non_portalable_wall(center_x - 25, 350, 50, 100)  # Red blocker in middle
        
        # Right side - properly spaced
        self.add_wall(1400, self.height - 200, 200, 150) # Right platform (far from center)
        self.add_wall(center_x + 150, 250, 50, 400)      # Portal wall with safe distance
        
        # Safe spawn point
        self.spawn_point = (300, self.height - 170)      # Centered on left platform
        
        # Goal positioned safely on right platform
        goal = Goal(1500, self.height - 250)             # Centered on right platform
        self.goals.append(goal)
        
        # Updated hint for momentum strategy
        self.hint_text = language_manager.get_text("hint_level_2")
    
    def generate_box_puzzle_level(self):
        """Level 3: Box pushing puzzle"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Platforms - properly spaced to avoid overlaps
        self.add_wall(100, self.height - 150, 300, 100)   # Start platform
        self.add_wall(650, self.height - 200, 200, 50)    # Mid platform (50px gap)
        self.add_wall(1100, self.height - 300, 300, 50)   # End platform (50px gap)
        
        # Portal walls - positioned to avoid platform overlaps
        self.add_wall(480, self.height - 350, 50, 150)    # Left portal wall (away from platforms)
        self.add_wall(920, self.height - 450, 50, 150)    # Right portal wall (away from platforms)
        
        # Safe spawn point
        self.spawn_point = (250, self.height - 120)       # Centered on start platform
        
        # Box positioned safely on start platform (not overlapping walls)
        box = Box(320, self.height - 200)                 # Away from edges
        self.boxes.append(box)
        
        # Switch positioned on end platform surface
        switch = Switch(1250, self.height - 300)          # Centered on end platform
        self.switches.append(switch)
        
        # Goal positioned above end platform, away from switch
        goal = Goal(1350, self.height - 350, [switch])    # Side of platform, above it
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = language_manager.get_text("hint_level_3")
    
    def generate_switch_puzzle_level(self):
        """Level 4: Multiple switches puzzle"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Complex platform layout - properly spaced (50px minimum gaps)
        self.add_wall(100, self.height - 150, 200, 100)   # Platform 1
        self.add_wall(400, self.height - 250, 150, 50)    # Platform 2 (100px gap)
        self.add_wall(650, self.height - 180, 150, 50)    # Platform 3 (100px gap)
        self.add_wall(900, self.height - 300, 200, 100)   # Platform 4 (100px gap)
        self.add_wall(1200, self.height - 200, 200, 100)  # Platform 5 (100px gap)
        
        # Portal surfaces - positioned away from platforms
        self.add_wall(320, self.height - 400, 50, 150)    # Portal 1 (away from platforms)
        self.add_wall(570, self.height - 350, 50, 170)    # Portal 2 (away from platforms)
        self.add_wall(820, self.height - 500, 50, 200)    # Portal 3 (away from platforms)
        
        # Safe spawn point
        self.spawn_point = (200, self.height - 120)       # Centered on platform 1
        
        # Boxes positioned safely on platforms (away from switches)
        box1 = Box(150, self.height - 200)               # On platform 1
        box2 = Box(420, self.height - 300)               # On platform 2 (moved left, away from switch)
        self.boxes.extend([box1, box2])
        
        # Switches positioned on platform surfaces (away from boxes)
        switch1 = Switch(520, self.height - 250, stay_active=True)  # Platform 2 right side
        switch2 = Switch(1000, self.height - 300, stay_active=True) # Platform 4 center
        self.switches.extend([switch1, switch2])
        
        # Goal positioned safely above platform 5
        goal = Goal(1300, self.height - 250, [switch1, switch2])    # Platform 5 center, above it
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = language_manager.get_text("hint_level_4")
    
    def generate_advanced_level(self):
        """Level 5: Advanced mechanics"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Multi-level platforms - properly spaced (minimum 80px gaps)
        self.add_wall(100, self.height - 150, 200, 100)   # Platform 1
        self.add_wall(380, self.height - 300, 100, 50)    # Platform 2 (80px gap)
        self.add_wall(580, self.height - 200, 100, 50)    # Platform 3 (100px gap)
        self.add_wall(780, self.height - 400, 100, 50)    # Platform 4 (100px gap)
        self.add_wall(980, self.height - 250, 200, 50)    # Platform 5 (100px gap)
        self.add_wall(1280, self.height - 150, 200, 100)  # Platform 6 (100px gap)
        
        # Mixed portal surfaces - positioned safely away from platforms
        self.add_wall(300, self.height - 450, 50, 150)    # Portal 1 (away from platforms)
        self.add_non_portalable_wall(530, self.height - 350, 50, 150)  # Red wall (safe position)
        self.add_wall(730, self.height - 550, 50, 150)    # Portal 2 (away from platforms)
        self.add_wall(930, self.height - 400, 50, 150)    # Portal 3 (away from platforms)
        
        # Safe spawn point
        self.spawn_point = (200, self.height - 120)       # Centered on platform 1
        
        # Boxes positioned safely on platforms (2 boxes for 2 switches)
        box1 = Box(630, self.height - 250)               # Platform 3 center (middle box)
        box2 = Box(830, self.height - 450)               # Platform 4 center (right box)
        self.boxes.extend([box1, box2])
        
        # Switches positioned on platform 5 surface
        switch1 = Switch(1030, self.height - 250)         # Platform 5 left
        switch2 = Switch(1130, self.height - 250)         # Platform 5 right (100px apart)
        self.switches.extend([switch1, switch2])
        
        # Goal positioned safely above platform 6
        goal = Goal(1380, self.height - 200, [switch1, switch2])  # Platform 6 center, above it
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = language_manager.get_text("hint_level_5")
    
    def generate_procedural_level(self, level_index):
        """Generate a procedural level for higher indices with proper spacing"""
        import random
        random.seed(level_index * 42)  # Deterministic randomness
        
        # Basic boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Track occupied areas to prevent overlaps
        occupied_areas = []
        
        # Random platforms with overlap prevention
        platforms = []
        for i in range(random.randint(5, 8)):
            attempts = 0
            while attempts < 20:  # Prevent infinite loops
                x = random.randint(100, self.width - 350)
                y = random.randint(self.height//2, self.height - 200)
                w = random.randint(100, 200)
                h = random.randint(50, 100)
                
                # Check for overlaps with existing platforms
                new_rect = pygame.Rect(x, y, w, h)
                overlaps = False
                for existing in occupied_areas:
                    if new_rect.colliderect(existing.inflate(50, 50)):  # 50px buffer
                        overlaps = True
                        break
                
                if not overlaps:
                    self.add_wall(x, y, w, h)
                    occupied_areas.append(new_rect)
                    platforms.append((x + w//2, y))  # Store center and top for object placement
                    break
                attempts += 1
        
        # Random portal walls with spacing
        for i in range(random.randint(3, 5)):
            attempts = 0
            while attempts < 15:
                x = random.randint(150, self.width - 250)
                y = random.randint(200, self.height - 400)
                w, h = 50, random.randint(100, 200)
                
                # Check for overlaps
                new_rect = pygame.Rect(x, y, w, h)
                overlaps = False
                for existing in occupied_areas:
                    if new_rect.colliderect(existing.inflate(30, 30)):  # 30px buffer
                        overlaps = True
                        break
                
                if not overlaps:
                    self.add_wall(x, y, w, h)
                    occupied_areas.append(new_rect)
                    break
                attempts += 1
        
        # Safe spawn point
        self.spawn_point = (150, self.height - 120)
        
        # Objects positioned on platforms to prevent floating
        num_boxes = min(level_index // 2, 3)
        placed_boxes = 0
        for platform_x, platform_y in platforms:
            if placed_boxes >= num_boxes:
                break
            box = Box(platform_x, platform_y - 50)  # 50px above platform surface
            self.boxes.append(box)
            placed_boxes += 1
        
        num_switches = min(level_index // 3, 2)
        switches = []
        placed_switches = 0
        for platform_x, platform_y in platforms:
            if placed_switches >= num_switches:
                break
            if placed_switches * 2 < len(platforms):  # Space switches out
                switch = Switch(platform_x + 50, platform_y, stay_active=True)  # Offset from boxes
                switches.append(switch)
                self.switches.append(switch)
                placed_switches += 1
        
        # Goal positioned safely
        goal = Goal(self.width - 150, self.height - 150, switches)
        self.goals.append(goal)
    
    def generate_momentum_level(self):
        """Level 7: Anti-skip momentum puzzle with barriers"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Starting platform
        self.add_wall(100, self.height - 150, 200, 100)
        
        # First puzzle section - requires box
        self.add_wall(400, self.height - 200, 150, 50)   # Box platform
        self.add_wall(600, self.height - 300, 100, 50)   # Switch platform
        
        # Portal walls for first section  
        self.add_wall(350, self.height - 350, 50, 150)   # Portal wall
        
        # Anti-skip barriers - prevent direct momentum to goal (properly spaced)
        self.add_non_portalable_wall(770, 50, 50, 400)   # Ceiling barrier
        self.add_non_portalable_wall(920, 50, 50, 500)   # Tall barrier  
        self.add_non_portalable_wall(1070, 50, 50, 600)  # Very tall barrier
        
        # Momentum section - but contained (avoid overlaps)
        self.add_wall(820, self.height - 200, 130, 50)   # Launch platform (smaller, non-overlapping)
        self.add_wall(1120, self.height - 500, 130, 50)  # High platform (behind barriers)
        
        # Contained momentum portal walls (properly spaced)
        self.add_wall(720, self.height - 350, 50, 150)   # Bottom portal
        self.add_wall(1020, self.height - 650, 50, 150)  # Top portal (safe area)
        
        # Final section - requires completing first puzzle
        self.add_wall(1300, self.height - 400, 150, 50)  # Intermediate platform
        self.add_wall(1500, self.height - 250, 200, 50)  # Goal platform
        
        # Additional anti-skip barriers around goal
        self.add_non_portalable_wall(1450, 50, 50, 200)  # Goal area barrier
        self.add_non_portalable_wall(1750, 50, 50, 300)  # Side barrier
        
        # Portal wall for final navigation
        self.add_wall(1250, self.height - 550, 50, 150)  # Final portal wall
        self.add_wall(1650, self.height - 400, 50, 150)  # Goal portal wall
        
        self.spawn_point = (200, self.height - 120)
        
        # Box needed to activate switch
        box = Box(450, self.height - 250)
        self.boxes.append(box)
        
        # Switch that unlocks goal
        switch = Switch(650, self.height - 300, stay_active=True)
        self.switches.append(switch)
        
        # Goal requires switch activation
        goal = Goal(1600, self.height - 300, [switch])
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = "Použij momentum, ale nejdříve splň puzzle!"
    
    def generate_tower_level(self):
        """Level 8: Properly spaced multi-platform puzzle with no overlaps"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Starting area - large platform
        self.add_wall(100, self.height - 150, 250, 100)  # Reduced width to prevent overlaps
        
        # First challenge - elevated platforms requiring portals (properly spaced)
        self.add_wall(450, self.height - 250, 150, 50)   # Platform 1 (100px gap from start)
        self.add_wall(700, self.height - 350, 150, 50)   # Platform 2 (100px gap, higher)
        
        # Portal walls for navigation (positioned to avoid overlaps)
        self.add_wall(380, self.height - 400, 50, 150)   # Portal wall 1 (away from platforms)
        self.add_wall(630, self.height - 500, 50, 150)   # Portal wall 2 (away from platforms)
        
        # Middle section - momentum challenge (properly spaced)
        self.add_wall(950, self.height - 200, 150, 50)   # Launch platform (100px gap)
        self.add_wall(1200, self.height - 450, 150, 50)  # High platform (100px gap)
        
        # Momentum portal walls (positioned to avoid overlaps)
        self.add_wall(880, self.height - 350, 50, 150)   # Bottom portal (away from platform)
        self.add_wall(1130, 100, 50, 150)               # Top portal (away from platform)
        
        # Final section - goal area (INSIDE map boundaries with spacing)
        self.add_wall(1450, self.height - 300, 200, 50)  # Goal platform (100px gap, INSIDE 2000px width)
        
        # Portal wall for final section (positioned to avoid overlaps)
        self.add_wall(1380, self.height - 450, 50, 150)  # Final portal wall (away from platform)
        
        # Spawn point - safe on starting platform
        self.spawn_point = (225, self.height - 120)      # Centered on starting platform
        
        # Single box for simple puzzle (positioned safely on platform)
        box1 = Box(525, self.height - 300)              # Centered on platform 1
        self.boxes.append(box1)
        
        # Single switch for simple puzzle (positioned safely on platform)
        switch1 = Switch(775, self.height - 350, stay_active=True)  # Centered on platform 2
        self.switches.append(switch1)
        
        # Goal positioned SAFELY INSIDE map boundaries
        goal = Goal(1550, self.height - 350, [switch1])  # Centered on goal platform, WELL INSIDE map
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = "Použij portály a momentum abys dosáhl cíle!"
    
    def generate_maze_level(self):
        """Level 9: Advanced multi-box puzzle with proper spacing"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # Starting platform
        self.add_wall(100, self.height - 150, 200, 100)
        
        # First puzzle area - elevated platforms (fixed positioning to avoid overlaps)
        self.add_wall(400, self.height - 250, 120, 50)   # Box platform 1 (reduced width)
        self.add_wall(620, self.height - 350, 120, 50)   # Switch platform 1 (100px gap)
        self.add_wall(320, self.height - 400, 80, 50)    # Side platform (moved left)
        
        # Portal walls for first area (repositioned to avoid overlaps)
        self.add_wall(250, self.height - 500, 50, 150)   # Left portal wall (moved left)
        self.add_wall(540, self.height - 450, 50, 100)   # Middle portal wall (adjusted)
        self.add_wall(760, self.height - 500, 50, 150)   # Right portal wall (moved up)
        
        # Second puzzle area - momentum section (better spacing)
        self.add_wall(900, self.height - 200, 120, 50)   # Lower platform (reduced width)
        self.add_wall(1120, self.height - 450, 120, 50)  # High platform (100px gap)
        self.add_wall(1340, self.height - 300, 100, 50)  # Medium platform (100px gap)
        
        # Momentum portal walls (repositioned)
        self.add_wall(850, self.height - 350, 50, 150)   # Left momentum wall (moved left)
        self.add_wall(1070, 100, 50, 150)               # Top portal wall (moved left)
        self.add_wall(1270, self.height - 500, 50, 150)  # High portal wall (moved left)
        
        # Final area - complex multi-switch puzzle (proper spacing)
        self.add_wall(1480, self.height - 250, 120, 50)  # Switch platform 2 (moved left)
        self.add_wall(1700, self.height - 400, 120, 50)  # Switch platform 3 (100px gap)
        self.add_wall(1590, self.height - 550, 90, 50)   # Box platform 2 (repositioned)
        self.add_wall(1750, self.height - 150, 150, 100) # Goal platform (moved left)
        
        # Final area portal walls (adjusted positions)
        self.add_wall(1430, self.height - 600, 50, 150)  # Portal wall 1 (moved left and up)
        self.add_wall(1650, self.height - 280, 50, 80)   # Portal wall 2 (repositioned)
        self.add_wall(1850, self.height - 350, 50, 200)  # Portal wall 3 (moved left)
        
        # Strategic smaller platforms for box movement (repositioned)
        self.add_wall(500, self.height - 180, 80, 50)    # Bridge platform 1 (moved down)
        self.add_wall(700, self.height - 180, 80, 50)    # Bridge platform 2 (moved left)
        self.add_wall(1020, self.height - 320, 80, 50)   # Bridge platform 3 (adjusted)
        
        # Spawn point
        self.spawn_point = (200, self.height - 120)
        
        # Multiple boxes for complex puzzle
        box1 = Box(450, self.height - 300)  # First box
        box2 = Box(950, self.height - 250)  # Second box (moved left)
        box3 = Box(1630, self.height - 600) # Third box (adjusted position)
        self.boxes.extend([box1, box2, box3])
        
        # Multiple switches requiring different boxes
        switch1 = Switch(680, self.height - 350, stay_active=True)   # On platform
        switch2 = Switch(1540, self.height - 250, stay_active=True)  # On platform 2
        switch3 = Switch(1760, self.height - 400, stay_active=True)  # On platform 3
        self.switches.extend([switch1, switch2, switch3])
        
        # Goal requires all three switches
        goal = Goal(1825, self.height - 200, [switch1, switch2, switch3])
        self.goals.append(goal)
        
        # Level hint
        self.hint_text = language_manager.get_text("hint_level_8")
    
    def generate_precision_level(self):
        """Level 10: Ultimate challenge - The Gauntlet"""
        # Boundaries
        self.add_wall(0, self.height - 50, self.width, 50)
        self.add_wall(0, 0, 50, self.height)
        self.add_wall(self.width - 50, 0, 50, self.height)
        self.add_wall(0, 0, self.width, 50)
        
        # === STAGE 1: Precision Portal Maze ===
        # Starting platform
        self.add_wall(100, self.height - 150, 150, 100)
        
        # Narrow corridor with precise portal placement required
        self.add_wall(300, self.height - 100, 30, 50)    # Floor piece 1
        self.add_wall(380, self.height - 100, 30, 50)    # Floor piece 2
        self.add_wall(460, self.height - 100, 30, 50)    # Floor piece 3
        
        # Vertical maze walls requiring careful navigation
        self.add_wall(280, self.height - 300, 20, 150)   # Thin wall 1
        self.add_wall(360, self.height - 350, 20, 200)   # Thin wall 2
        self.add_wall(440, self.height - 400, 20, 250)   # Thin wall 3
        
        # First box platform (elevated)
        self.add_wall(520, self.height - 200, 80, 30)
        
        # === STAGE 2: Momentum Amplifier ===
        # Launch ramp
        self.add_wall(650, self.height - 150, 100, 30)
        
        # Momentum portal surfaces (very specific angles needed)
        self.add_wall(620, self.height - 300, 30, 100)   # Left momentum wall
        self.add_wall(750, self.height - 500, 30, 100)   # Right momentum wall
        
        # High platform requiring perfect momentum
        self.add_wall(850, self.height - 600, 80, 30)
        
        # Anti-cheese barriers
        self.add_non_portalable_wall(700, 50, 200, 20)   # Ceiling barrier
        self.add_non_portalable_wall(800, self.height - 450, 100, 20)  # Mid barrier
        
        # === STAGE 3: Multi-Box Puzzle Tower ===
        # Base of tower
        self.add_wall(1000, self.height - 150, 120, 100)
        
        # Tower levels (each requires box stacking)
        self.add_wall(1000, self.height - 280, 120, 30)  # Level 1
        self.add_wall(1000, self.height - 410, 120, 30)  # Level 2
        self.add_wall(1000, self.height - 540, 120, 30)  # Level 3
        
        # Side platforms for box manipulation
        self.add_wall(1150, self.height - 350, 60, 30)   # Helper platform 1
        self.add_wall(850, self.height - 350, 60, 30)    # Helper platform 2
        
        # Portal surfaces for tower
        self.add_wall(950, self.height - 650, 30, 300)   # Left tower wall
        self.add_wall(1140, self.height - 650, 30, 300)  # Right tower wall
        
        # === STAGE 4: The Final Ascent ===
        # Disappearing platforms (represented by thin platforms)
        self.add_wall(1250, self.height - 400, 40, 20)   # Platform 1
        self.add_wall(1350, self.height - 500, 40, 20)   # Platform 2
        self.add_wall(1450, self.height - 600, 40, 20)   # Platform 3
        
        # Final challenge platform
        self.add_wall(1550, self.height - 700, 150, 30)
        
        # Goal platform (very high up)
        self.add_wall(1700, self.height - 850, 200, 30)
        
        # Final portal surfaces (limited options)
        self.add_wall(1500, self.height - 800, 30, 100)  # Final portal 1
        self.add_wall(1650, self.height - 900, 30, 100)  # Final portal 2
        
        # === OBJECTS AND MECHANICS ===
        # Multiple boxes for tower puzzle (positioned safely)
        box1 = Box(175, self.height - 200)               # Starting platform (100-250, Y=height-150)
        box2 = Box(880, self.height - 100)               # Ground floor below helper platform (safe spawn)
        box3 = Box(700, self.height - 180)               # Launch ramp center: 650+50=700, Y=height-150-30=height-180  
        box4 = Box(1180, self.height - 100)              # Ground floor below helper platform (safe spawn)
        self.boxes.extend([box1, box2, box3, box4])
        
        # Switches in challenging positions (positioned away from boxes)
        switch1 = Switch(580, self.height - 200, stay_active=True)      # After maze platform - moved right
        switch2 = Switch(880, self.height - 600, stay_active=True)      # High momentum platform
        switch3 = Switch(1080, self.height - 540, stay_active=True)     # Tower top - moved right
        switch4 = Switch(1625, self.height - 700, stay_active=True)     # Final challenge
        self.switches.extend([switch1, switch2, switch3, switch4])
        
        # Spawn point
        self.spawn_point = (175, self.height - 120)
        
        # Final goal requires ALL switches (ultimate test)
        goal = Goal(1800, self.height - 900, [switch1, switch2, switch3, switch4])
        self.goals.append(goal)
        
        # Epic final hint
        self.hint_text = "Ovládni všechny dovedonosti: preciznost, momentum a stackování!"
    
    
    def add_wall(self, x, y, width, height):
        """Add a normal wall"""
        self.walls.append(pygame.Rect(x, y, width, height))
    
    def add_non_portalable_wall(self, x, y, width, height):
        """Add a non-portalable wall"""
        self.non_portalable_walls.append(pygame.Rect(x, y, width, height))
    
    def is_solid(self, x, y):
        """Check if a point is inside solid geometry"""
        point = (x, y)
        
        # Check normal walls
        for wall in self.walls:
            if wall.collidepoint(point):
                return True
        
        # Check non-portalable walls
        for wall in self.non_portalable_walls:
            if wall.collidepoint(point):
                return True
        
        return False
    
    def raycast(self, start_x, start_y, dir_x, dir_y, max_distance):
        """Raycast to find wall intersection"""
        step_size = 2  # Good balance of accuracy and performance
        current_x = start_x
        current_y = start_y
        distance = 0
        
        while distance < max_distance:
            current_x += dir_x * step_size
            current_y += dir_y * step_size
            distance += step_size
            
            # Check non-portalable walls first (they block portals completely)
            for wall in self.non_portalable_walls:
                if wall.collidepoint(current_x, current_y):
                    normal = self.get_surface_normal(wall, current_x, current_y)
                    return (current_x, current_y), normal, SURFACE_NON_PORTALABLE
            
            # Check normal walls (can hold portals)
            for wall in self.walls:
                if wall.collidepoint(current_x, current_y):
                    normal = self.get_surface_normal(wall, current_x, current_y)
                    return (current_x, current_y), normal, SURFACE_NORMAL
        
        return None, None, None
    
    def get_surface_normal(self, wall, hit_x, hit_y):
        """Get surface normal for a wall at hit point"""
        # Simple normal calculation
        center_x = wall.centerx
        center_y = wall.centery
        
        # Determine which face was hit
        left_dist = abs(hit_x - wall.left)
        right_dist = abs(hit_x - wall.right)
        top_dist = abs(hit_y - wall.top)
        bottom_dist = abs(hit_y - wall.bottom)
        
        min_dist = min(left_dist, right_dist, top_dist, bottom_dist)
        
        if min_dist == left_dist:
            return (-1, 0)  # Left face
        elif min_dist == right_dist:
            return (1, 0)   # Right face
        elif min_dist == top_dist:
            return (0, -1)  # Top face
        else:
            return (0, 1)   # Bottom face
    
    def get_spawn_point(self):
        """Get safe player spawn point"""
        # Check if spawn point is safe (not inside any objects)
        spawn_x, spawn_y = self.spawn_point
        player_width, player_height = 30, 40  # Player dimensions
        
        # Create player rect at spawn point
        player_rect = pygame.Rect(spawn_x - player_width//2, spawn_y - player_height, player_width, player_height)
        
        # Check collision with walls
        for wall in self.walls + self.non_portalable_walls:
            if player_rect.colliderect(wall):
                # Find safe spawn point nearby
                return self.find_safe_spawn_point(spawn_x, spawn_y)
        
        # Check collision with boxes
        for box in self.boxes:
            box_rect = pygame.Rect(box.x - box.width//2, box.y - box.height, box.width, box.height)
            if player_rect.colliderect(box_rect):
                return self.find_safe_spawn_point(spawn_x, spawn_y)
        
        return self.spawn_point
    
    def find_safe_spawn_point(self, original_x, original_y):
        """Find a safe spawn point near the original location"""
        player_width, player_height = 30, 40
        
        # First try spawning above the collision (most common case)
        for height_offset in [60, 100, 150, 200, 250]:
            test_x = original_x
            test_y = original_y - height_offset
            
            # Make sure it's within level bounds
            if test_y < 50:
                continue
                
            # Create test rect
            test_rect = pygame.Rect(test_x - player_width//2, test_y - player_height, player_width, player_height)
            
            # Check if this position is safe
            is_safe = True
            
            # Check walls
            for wall in self.walls + self.non_portalable_walls:
                if test_rect.colliderect(wall):
                    is_safe = False
                    break
            
            if not is_safe:
                continue
            
            # Check boxes
            for box in self.boxes:
                box_rect = pygame.Rect(box.x - box.width//2, box.y - box.height, box.width, box.height)
                if test_rect.colliderect(box_rect):
                    is_safe = False
                    break
            
            if is_safe:
                print(f"⚠ Moved spawn point UP from ({original_x}, {original_y}) to ({test_x}, {test_y}) to avoid collision")
                return (test_x, test_y)
        
        # If spawning above doesn't work, try horizontal positions
        for x_offset in [-80, 80, -120, 120, -160, 160]:
            test_x = original_x + x_offset
            test_y = original_y
            
            # Make sure it's within level bounds
            if test_x < 50 or test_x > self.width - 50:
                continue
                
            # Create test rect
            test_rect = pygame.Rect(test_x - player_width//2, test_y - player_height, player_width, player_height)
            
            # Check if this position is safe
            is_safe = True
            
            # Check walls
            for wall in self.walls + self.non_portalable_walls:
                if test_rect.colliderect(wall):
                    is_safe = False
                    break
            
            if not is_safe:
                continue
            
            # Check boxes
            for box in self.boxes:
                box_rect = pygame.Rect(box.x - box.width//2, box.y - box.height, box.width, box.height)
                if test_rect.colliderect(box_rect):
                    is_safe = False
                    break
            
            if is_safe:
                print(f"⚠ Moved spawn point HORIZONTALLY from ({original_x}, {original_y}) to ({test_x}, {test_y}) to avoid collision")
                return (test_x, test_y)
        
        # Last resort: try spiral pattern
        for radius in range(50, 300, 50):
            for angle in range(0, 360, 45):
                angle_rad = math.radians(angle)
                test_x = original_x + radius * math.cos(angle_rad)
                test_y = original_y + radius * math.sin(angle_rad)
                
                # Make sure it's within level bounds
                if test_x < 50 or test_x > self.width - 50:
                    continue
                if test_y < 50 or test_y > self.height - 50:
                    continue
                
                # Create test rect
                test_rect = pygame.Rect(test_x - player_width//2, test_y - player_height, player_width, player_height)
                
                # Check if this position is safe
                is_safe = True
                
                # Check walls
                for wall in self.walls + self.non_portalable_walls:
                    if test_rect.colliderect(wall):
                        is_safe = False
                        break
                
                if not is_safe:
                    continue
                
                # Check boxes
                for box in self.boxes:
                    box_rect = pygame.Rect(box.x - box.width//2, box.y - box.height, box.width, box.height)
                    if test_rect.colliderect(box_rect):
                        is_safe = False
                        break
                
                if is_safe:
                    print(f"⚠ Moved spawn point from ({original_x}, {original_y}) to ({test_x}, {test_y}) to avoid collision")
                    return (test_x, test_y)
        
        # If no safe position found, return original (with warning)
        print(f"⚠ Warning: Could not find safe spawn point, using original position")
        return (original_x, original_y)
    
    def validate_object_positions(self):
        """Validate that all objects are positioned correctly (not overlapping)"""
        # Check player spawn point
        spawn_x, spawn_y = self.spawn_point
        player_rect = pygame.Rect(spawn_x - 15, spawn_y - 20, 30, 40)
        
        # Validate and fix object positions (but NOT boundary walls)
        print(f"📊 Validating Level {self.level_index} with {len(self.walls)} walls, {len(self.boxes)} boxes")
        
        # Note: Boundary walls (ground, ceiling, left/right walls) are supposed to touch corners
        # Only check for problematic overlaps between gameplay platforms
        
        # Check boxes don't overlap with walls or each other
        for i, box in enumerate(self.boxes):
            box_rect = pygame.Rect(box.x - box.width//2, box.y - box.height//2, box.width, box.height)
            
            # Check wall collisions
            for wall in self.walls + self.non_portalable_walls:
                if box_rect.colliderect(wall):
                    print(f"⚠ Warning: Box {i} overlaps with wall at ({box.x}, {box.y})")
                    # Move box up to safe position
                    box.y = wall.top - box.height//2 - 20  # More clearance
                    print(f"✓ Box {i} moved up to Y={box.y}")
            
            # Check box-box collisions  
            for j, other_box in enumerate(self.boxes):
                if i != j:
                    other_rect = pygame.Rect(other_box.x - other_box.width//2, other_box.y - other_box.height//2, 
                                           other_box.width, other_box.height)
                    if box_rect.colliderect(other_rect):
                        print(f"⚠ Warning: Box {i} overlaps with Box {j}")
                        # Move box with more separation
                        box.x += 80  # Larger separation
                        print(f"✓ Box {i} moved right to X={box.x}")
        
        # Check switches are on valid surfaces
        for i, switch in enumerate(self.switches):
            switch_rect = pygame.Rect(switch.x - switch.width//2, switch.y - switch.height//2, 
                                    switch.width, switch.height)
            
            # Check if switch is on a platform (should be on top of a wall)
            on_platform = False
            for wall in self.walls:
                if (switch.y >= wall.top - 10 and switch.y <= wall.top + 10 and
                    switch.x >= wall.left and switch.x <= wall.right):
                    on_platform = True
                    switch.y = wall.top  # Snap to platform surface
                    break
            
            if not on_platform:
                print(f"⚠ Warning: Switch {i} not on platform at ({switch.x}, {switch.y})")
        
        # Check goals are positioned inside map boundaries and above platforms
        for i, goal in enumerate(self.goals):
            goal_rect = pygame.Rect(goal.x - goal.width//2, goal.y - goal.height//2, 
                                  goal.width, goal.height)
            
            # Check if goal is outside map boundaries (stricter boundaries for safety)
            if goal.x < 150 or goal.x > self.width - 200:  # More conservative boundaries
                print(f"⚠ Warning: Goal {i} outside horizontal boundaries at ({goal.x}, {goal.y})")
                goal.x = max(200, min(self.width - 200, goal.x))
                print(f"✓ Goal {i} repositioned to X={goal.x}")
            
            if goal.y < 150 or goal.y > self.height - 150:
                print(f"⚠ Warning: Goal {i} outside vertical boundaries at ({goal.x}, {goal.y})")
                goal.y = max(200, min(self.height - 200, goal.y))
                print(f"✓ Goal {i} repositioned to Y={goal.y}")
            
            # Check wall collisions
            for wall in self.walls + self.non_portalable_walls:
                if goal_rect.colliderect(wall):
                    print(f"⚠ Warning: Goal {i} overlaps with wall at ({goal.x}, {goal.y})")
                    # Move goal above wall
                    goal.y = wall.top - goal.height//2 - 20
                    
            # Ensure goal is on or above a platform
            on_platform = False
            for wall in self.walls:
                if (goal.x >= wall.left - 50 and goal.x <= wall.right + 50 and
                    goal.y >= wall.top - 100 and goal.y <= wall.top + 20):
                    on_platform = True
                    goal.y = wall.top - 50  # Position above platform
                    break
            
            if not on_platform:
                print(f"⚠ Warning: Goal {i} not near any platform at ({goal.x}, {goal.y})")
                # Find nearest platform
                nearest_wall = None
                min_dist = float('inf')
                for wall in self.walls:
                    dist = abs(goal.x - wall.centerx) + abs(goal.y - wall.centery)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_wall = wall
                
                if nearest_wall:
                    goal.x = nearest_wall.centerx
                    goal.y = nearest_wall.top - 50
    
    def get_movable_objects(self):
        """Get all movable objects (boxes)"""
        return self.boxes
    
    def update(self, dt):
        """Update level objects"""
        # Update hint system
        self.time_stuck += dt
        self.hint_show_time += dt
        
        # Auto-hide hint after showing at start
        if self.hint_visible and self.hint_show_time >= self.hint_auto_hide_time:
            self.hint_visible = False
        
        # Show hint again if player is stuck
        if self.time_stuck >= self.hint_delay and not self.hint_visible:
            self.hint_visible = True
            # This will be handled by the game class to mark as shown
        
        # Update boxes
        for box in self.boxes:
            box.update(dt, self)
        
        # Update switches
        for switch in self.switches:
            switch.update(dt, self)
            
            # Check if any boxes are on the switch
            for box in self.boxes:
                if switch.is_object_on_switch(box):
                    switch.add_object(box)
        
        # Update goals
        for goal in self.goals:
            goal.update(dt, self)
    
    def reset_hint_timer(self):
        """Reset hint timer when level reloads"""
        self.time_stuck = 0.0
        self.hint_show_time = 0.0
        self.hint_visible = True  # Show at start of level
    
    def toggle_hint(self):
        """Manually toggle hint visibility"""
        self.hint_visible = not self.hint_visible
    
    def check_win_condition(self, player):
        """Check if player has reached an active goal"""
        for goal in self.goals:
            if goal.check_player_collision(player):
                return True
        return False
    
    def draw(self, screen, cam_x, cam_y):
        """Draw the level"""
        # Fill background
        screen.fill(self.background_color)
        
        # Draw normal walls
        for wall in self.walls:
            screen_rect = (wall.x - cam_x, wall.y - cam_y, wall.width, wall.height)
            pygame.draw.rect(screen, self.wall_color, screen_rect)
            pygame.draw.rect(screen, WHITE, screen_rect, 2)
        
        # Draw non-portalable walls
        for wall in self.non_portalable_walls:
            screen_rect = (wall.x - cam_x, wall.y - cam_y, wall.width, wall.height)
            pygame.draw.rect(screen, self.non_portalable_color, screen_rect)
            pygame.draw.rect(screen, RED, screen_rect, 3)
            
            # Add warning pattern
            for i in range(0, wall.width, 20):
                for j in range(0, wall.height, 20):
                    if (i + j) // 20 % 2 == 0:
                        stripe_rect = (wall.x - cam_x + i, wall.y - cam_y + j, 10, 10)
                        pygame.draw.rect(screen, YELLOW, stripe_rect)
        
        # Draw boxes
        for box in self.boxes:
            box.draw(screen, cam_x, cam_y)
        
        # Draw switches
        for switch in self.switches:
            switch.draw(screen, cam_x, cam_y)
        
        # Draw goals
        for goal in self.goals:
            goal.draw(screen, cam_x, cam_y)
        
        # Draw hint if visible
        self.draw_hint(screen)
    
    def draw_hint(self, screen):
        """Draw level hint"""
        if self.hint_visible and self.hint_text:
            # Create hint box
            font = pygame.font.Font(None, 28)
            hint_surface = font.render(self.hint_text, True, WHITE)
            
            # Calculate position (bottom center of screen)
            screen_width = screen.get_width()
            hint_width = hint_surface.get_width()
            hint_height = hint_surface.get_height()
            
            x = (screen_width - hint_width) // 2
            y = screen.get_height() - hint_height - 80
            
            # Draw semi-transparent background
            bg_padding = 20
            bg_rect = pygame.Rect(x - bg_padding, y - bg_padding//2, 
                                hint_width + bg_padding*2, hint_height + bg_padding)
            
            # Create semi-transparent surface
            hint_bg = pygame.Surface((bg_rect.width, bg_rect.height))
            hint_bg.set_alpha(180)
            hint_bg.fill((0, 0, 0))
            screen.blit(hint_bg, (bg_rect.x, bg_rect.y))
            
            # Draw border
            pygame.draw.rect(screen, YELLOW, bg_rect, 2)
            
            # Draw hint text
            screen.blit(hint_surface, (x, y))
            
            # Draw hint controls
            control_font = pygame.font.Font(None, 20)
            control_text = control_font.render("Stiskni H pro zobrazení nápovědy", True, GRAY)
            control_x = (screen_width - control_text.get_width()) // 2
            control_y = y + hint_height + 5
            screen.blit(control_text, (control_x, control_y))