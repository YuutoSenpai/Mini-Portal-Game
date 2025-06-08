"""
Language and translation system for the Portal Game
Supports English and Czech languages
"""

class LanguageManager:
    def __init__(self):
        self.current_language = "cz"  # Default to Czech only
        self.translations = {
            "en": {
                # Main Menu
                "new_game": "New Game",
                "load_game": "Load Game", 
                "levels": "Levels",
                "settings": "Settings",
                "credits": "Credits",
                "exit": "Exit",
                "language": "Language: EN",
                
                # Pause Menu
                "resume": "Resume",
                "restart_level": "Restart Level",
                "save_game": "Save Game",
                "help": "Help (?)",
                "exit_to_main": "Exit to Main Menu",
                
                # Settings Menu
                "master_volume": "Master Volume",
                "sfx_volume": "SFX Volume",
                "music_volume": "Music Volume",
                "sound_effects": "Sound Effects",
                "background_music": "Background Music",
                "back": "Back",
                "on": "ON",
                "off": "OFF",
                "settings_instruction": "Use LEFT/RIGHT arrows to adjust values",
                "esc_back": "ESC - Back to Main Menu",
                
                # Level Selection
                "level_selection": "LEVEL SELECTION",
                "completed": "Completed",
                "unlocked": "Unlocked",
                "locked": "LOCKED",
                "level_instruction": "Complete levels to unlock more! Use ARROW KEYS to navigate, ENTER to select",
                "level_instruction_all": "All levels unlocked! Use ARROW KEYS to navigate, ENTER to select",
                
                # Game UI
                "level": "Level",
                "time": "Time",
                "stars": "Stars",
                "paused": "PAUSED",
                "level_complete": "LEVEL COMPLETE!",
                "level_completed": "Level {0} Completed",
                "next_level": "Press N for next level",
                "restart": "Press R to restart",
                "esc_menu": "ESC - Menu",
                
                # Instructions
                "controls": "CONTROLS:",
                "move": "WASD / Arrow Keys - Move",
                "jump": "Space - Jump",
                "blue_portal": "Left Click - Blue Portal",
                "orange_portal": "Right Click - Orange Portal",
                "restart_key": "R - Restart Level",
                "pause_key": "ESC - Pause",
                "fullscreen": "F11 - Fullscreen Toggle",
                "objective": "OBJECTIVE:",
                "objective_text": "Use portals to reach the goal!",
                "red_surfaces": "Red surfaces cannot have portals.",
                "activate_switches": "Activate switches with boxes.",
                "press_start": "Press any key to start!",
                
                # Help Menu
                "help_title": "HELP & CONTROLS",
                "current_level_hint": "CURRENT LEVEL HINT:",
                "return_instruction": "Press ESC or ENTER to return",
                
                # Credits
                "credits_title": "CREDITS",
                "game_by": "Mini Portal Game",
                "created_by": "Created with Python & Pygame",
                "inspired_by": "Inspired by Portal series",
                "music_by": "Sound Effects: Procedural",
                
                # Save/Load
                "save_slot": "Save Slot",
                "load_slot": "Load Slot", 
                "delete_slot": "Delete Slot",
                "empty_slot": "Empty Slot",
                "no_save": "No save found in slot {0}",
                "save_deleted": "Deleted save slot {0}",
                "game_saved": "Game saved to slot {0}",
                
                # Level Hints
                "hint_level_0": "Nápověda: Vybuduj momentum tím, že oba portály dáš pod sebe a jdi se proletět!",
                "hint_level_1": "Nápověda: Potřebuješ oba portály pro teleportaci! Zkus umístit portály na vertikální zdi abys dosáhl vyšších platform.",
                "hint_level_2": "Nápověda: Vybuduj momentum tím, že oba portály dáš pod sebe a jdi se proletět!",
                "hint_level_3": "Nápověda: teleportuj boxy pomocí portálů a dostaň se do cíle!",
                "hint_level_4": "Nápověda: Aktivuj všechny switche pomocí boxů.",
                "hint_level_5": "Nápověda: Použij vše, co umíš. Momentum, boxy, switche.",
                "hint_level_6": "Nápověda: Vybuduj momentum tím, že oba portály dáš pod sebe a jdi se proletět!",
                "hint_level_7": "Nápověda: Zdi blokují budování momenta. Správně naviguj a dostaneš se do cíle!",
                "hint_level_8": "Nápověda: Aktivuj všechny switche pomocí boxů.",
                "hint_level_9": "Nápověda: Precizní umístění portálu je klíčem! Dej si na čase.",
                "hint_level_10": "Nápověda: Poslední výzva kombinuje vše, co si se naučil. Momentum, boxy, switche a preciznost!",
                
                # System Messages
                "loading": "Loading...",
                "error": "Error",
                "locked_level": "Level {0} is locked! Complete previous levels first.",
                "level_loaded": "Loaded Level {0}",
            },
            
            "cz": {
                # Main Menu
                "new_game": "Nová hra",
                "load_game": "Načíst hru",
                "levels": "Úrovně", 
                "settings": "Nastavení",
                "credits": "Titulky",
                "exit": "Konec",
                "language": "Jazyk: CZ",
                
                # Pause Menu
                "resume": "Pokračovat",
                "restart_level": "Restartovat úroveň",
                "save_game": "Uložit hru",
                "help": "Nápověda (?)",
                "exit_to_main": "Zpět do hlavního menu",
                
                # Settings Menu
                "master_volume": "Hlavní hlasitost",
                "sfx_volume": "Hlasitost efektů",
                "music_volume": "Hlasitost hudby",
                "sound_effects": "Zvukové efekty",
                "background_music": "Hudba na pozadí",
                "back": "Zpět",
                "on": "ZAP",
                "off": "VYP",
                "settings_instruction": "Použijte šipky VLEVO/VPRAVO pro nastavení hodnot",
                "esc_back": "ESC - Zpět do hlavního menu",
                
                # Level Selection
                "level_selection": "VÝBĚR ÚROVNĚ",
                "completed": "Dokončeno",
                "unlocked": "Odemčeno",
                "locked": "ZAMČENO",
                "level_instruction": "Dokončete úrovně pro odemčení dalších! Použijte ŠIPKY pro navigaci, ENTER pro výběr",
                "level_instruction_all": "Všechny úrovně odemčeny! Použijte ŠIPKY pro navigaci, ENTER pro výběr",
                
                # Game UI
                "level": "Úroveň",
                "time": "Čas",
                "stars": "Hvězdy",
                "paused": "POZASTAVENO",
                "level_complete": "ÚROVEŇ DOKONČENA!",
                "level_completed": "Úroveň {0} dokončena",
                "next_level": "Stiskněte N pro další úroveň",
                "restart": "Stiskněte R pro restart",
                "esc_menu": "ESC - Menu",
                
                # Instructions
                "controls": "OVLÁDÁNÍ:",
                "move": "WASD / Šipky - Pohyb",
                "jump": "Mezerník - Skok",
                "blue_portal": "Levé tlačítko - Modrý portál",
                "orange_portal": "Pravé tlačítko - Oranžový portál",
                "restart_key": "R - Restartovat úroveň",
                "pause_key": "ESC - Pozastavit",
                "fullscreen": "F11 - Celoobrazovkový režim",
                "objective": "CÍL:",
                "objective_text": "Použijte portály k dosažení cíle!",
                "red_surfaces": "Na červené plochy nelze umístit portály.",
                "activate_switches": "Aktivujte spínače pomocí krabic.",
                "press_start": "Stiskněte libovolnou klávesu pro start!",
                
                # Help Menu
                "help_title": "NÁPOVĚDA & OVLÁDÁNÍ",
                "current_level_hint": "NÁPOVĚDA AKTUÁLNÍ ÚROVNĚ:",
                "return_instruction": "Stiskněte ESC nebo ENTER pro návrat",
                
                # Credits
                "credits_title": "TITULKY",
                "game_by": "Mini Portal Game",
                "created_by": "Vytvořeno pomocí Python & Pygame",
                "inspired_by": "Inspirováno sérií Portal",
                "music_by": "Zvukové efekty: Procedurální",
                
                # Save/Load
                "save_slot": "Pozice uložení",
                "load_slot": "Načíst pozici",
                "delete_slot": "Smazat pozici",
                "empty_slot": "Prázdná pozice",
                "no_save": "V pozici {0} nebyla nalezena uložená hra",
                "save_deleted": "Smazána pozice {0}",
                "game_saved": "Hra uložena do pozice {0}",
                
                # Level Hints
                "hint_level_0": "Nápověda: Levým klikem vystřelíte modrý portál, pravým oranžový. Projděte jedním a teleportujete se k druhému!",
                "hint_level_1": "Nápověda: Pro teleportaci potřebujete oba portály! Zkuste umístit portály na svislé stěny a dosáhněte vyšší platformy.",
                "hint_level_2": "Nápověda: Získejte momentum! Umístěte portály pod sebe. Opakovaně jimi procházejte pro získání výšky, pak se portálujte přes mezeru v červené stěně.",
                "hint_level_3": "Nápověda: Teleportujte krabici na vyšší platformy pomocí portálů a dostaňte je na spínače",
                "hint_level_4": "Nápověda: Aktivujte všechny spínače pro odemčení cíle! Použijte krabice k podržení spínačů.",
                "hint_level_5": "Nápověda: Pokročilá mechanika kombinuje všechny vaše dovednosti! Použijte krabice, spínače a momentum společně.",
                "hint_level_6": "Nápověda: Použijte momentum k dosažení vysokých míst! Získejte rychlost opakovaným procházením portály.",
                "hint_level_7": "Nápověda: Strop blokuje budování momenta! Použijte krabici k podržení spínače, pak opatrně navigujte věží.",
                "hint_level_8": "Nápověda: Každá komora má unikátní hádanku. Přesouvejte krabice mezi komorami pomocí portálů a aktivujte všechny spínače v pořadí.",
                "hint_level_9": "Nápověda: Přesné umístění portálů je klíčové! Věnujte čas pečlivému míření na malé plochy.",
                "hint_level_10": "Nápověda: Finální výzva kombinuje všechny mechaniky! Použijte krabice, spínače, momentum a přesnost společně.",
                
                # System Messages
                "loading": "Načítání...",
                "error": "Chyba",
                "locked_level": "Úroveň {0} je zamčená! Nejprve dokončete předchozí úrovně.",
                "level_loaded": "Načtena úroveň {0}",
            }
        }
    
    def set_language(self, language_code):
        """Set the current language"""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_language(self):
        """Get current language code"""
        return self.current_language
    
    def get_text(self, key, *args):
        """Get translated text for a key, with optional formatting arguments"""
        try:
            text = self.translations[self.current_language].get(key, key)
            if args:
                return text.format(*args)
            return text
        except:
            # Return the key if translation fails
            return key
    
    def toggle_language(self):
        """Language toggle disabled - Czech only"""
        return self.current_language

# Global language manager instance
language_manager = LanguageManager()