import pygame

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
CYAN = (0, 255, 255)

# Portal colors
BLUE_PORTAL = (100, 150, 255)
ORANGE_PORTAL = (255, 150, 100)

# Physics constants
GRAVITY = 800
FRICTION = 0.95  # Even less friction for faster momentum building
MAX_FALL_SPEED = 700  # Reduced to prevent flying bug while keeping good momentum

# Player constants
PLAYER_SPEED = 300
JUMP_FORCE = 400
PLAYER_SIZE = 30

# Portal constants
PORTAL_RADIUS = 25
PORTAL_RANGE = 600
TELEPORT_COOLDOWN = 0.1  # Very fast cooldown for rapid momentum building

# Game object sizes
BOX_SIZE = 40
SWITCH_SIZE = 50
GOAL_SIZE = 60

# Surface types
SURFACE_NORMAL = 0
SURFACE_NON_PORTALABLE = 1
SURFACE_WATER = 2
SURFACE_GLASS = 3

# Layers
LAYER_BACKGROUND = 0
LAYER_OBJECTS = 1
LAYER_PLAYER = 2
LAYER_PORTALS = 3
LAYER_EFFECTS = 4
LAYER_UI = 5