import pygame
import os
from ..utils.constants import *

class SoundManager:
    """Manages all game audio"""
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Sound volumes
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.6
        
        # Sound effects
        self.sounds = {}
        
        # Background music
        self.current_music = None
        self.music_channel = None
        self.background_tracks = {}
        
        # Load sounds (create simple procedural sounds if files don't exist)
        self.load_sounds()
        
        # Music settings
        self.enable_procedural_music = True  # Set to False to disable procedural music
        
        # Create background music tracks
        if self.enable_procedural_music:
            self.create_background_music()
        else:
            self.create_silent_music()
        
    def load_sounds(self):
        """Load or create sound effects"""
        # Try to load sound files, create procedural ones if they don't exist
        sound_files = {
            'portal_shoot': 'portal_shoot.wav',
            'portal_open': 'portal_open.wav', 
            'teleport': 'teleport.wav',
            'jump': 'jump.wav',
            'switch_on': 'switch_on.wav',
            'switch_off': 'switch_off.wav',
            'goal_reached': 'goal_reached.wav',
            'box_push': 'box_push.wav',
            'level_complete': 'level_complete.wav'
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join('sounds', filename)
            
            try:
                # Try to load actual sound file
                if os.path.exists(sound_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                else:
                    # Create procedural sound
                    self.sounds[sound_name] = self.create_sound(sound_name)
            except:
                # Fallback to procedural sound
                self.sounds[sound_name] = self.create_sound(sound_name)
    
    def create_sound(self, sound_type):
        """Create procedural sound effects"""
        import numpy as np
        
        sample_rate = 22050
        
        if sound_type == 'portal_shoot':
            # Whoosh sound
            duration = 0.3
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 200 + 300 * np.exp(-t * 3)
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 2)
            
        elif sound_type == 'portal_open':
            # Sci-fi portal opening
            duration = 0.5
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 100 + 400 * (1 - np.exp(-t * 5))
            wave = np.sin(2 * np.pi * frequency * t) * (1 - t/duration)
            
        elif sound_type == 'teleport':
            # Teleport zap
            duration = 0.4
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 300 + 500 * np.sin(t * 20)
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 3)
            
        elif sound_type == 'jump':
            # Simple jump sound
            duration = 0.2
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 220 + 110 * np.exp(-t * 5)
            wave = np.sin(2 * np.pi * frequency * t) * (1 - t/duration)
            
        elif sound_type == 'switch_on':
            # Click sound
            duration = 0.1
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 800
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 10)
            
        elif sound_type == 'switch_off':
            # Lower click
            duration = 0.1
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 400
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 10)
            
        elif sound_type == 'goal_reached':
            # Success chime
            duration = 0.8
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequencies = [523, 659, 784]  # C, E, G
            wave = np.zeros_like(t)
            for i, freq in enumerate(frequencies):
                start = i * duration / 3
                mask = t >= start
                wave[mask] += np.sin(2 * np.pi * freq * (t[mask] - start)) * np.exp(-(t[mask] - start) * 2)
            
        elif sound_type == 'box_push':
            # Scraping sound
            duration = 0.3
            t = np.linspace(0, duration, int(sample_rate * duration))
            noise = np.random.normal(0, 0.1, len(t))
            frequency = 150
            wave = (np.sin(2 * np.pi * frequency * t) + noise) * (1 - t/duration)
            
        elif sound_type == 'level_complete':
            # Victory fanfare
            duration = 1.5
            t = np.linspace(0, duration, int(sample_rate * duration))
            melody = [523, 659, 784, 1047]  # C, E, G, C
            wave = np.zeros_like(t)
            for i, freq in enumerate(melody):
                start = i * duration / 4
                end = (i + 1) * duration / 4
                mask = (t >= start) & (t < end)
                wave[mask] = np.sin(2 * np.pi * freq * (t[mask] - start)) * (1 - (t[mask] - start)/(end - start))
        
        else:
            # Default beep
            duration = 0.2
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * 440 * t) * (1 - t/duration)
        
        # Normalize and convert to pygame sound
        wave = np.clip(wave * 32767, -32767, 32767).astype(np.int16)
        
        # Create stereo array with proper contiguous memory layout
        stereo_wave = np.zeros((len(wave), 2), dtype=np.int16)
        stereo_wave[:, 0] = wave  # Left channel
        stereo_wave[:, 1] = wave  # Right channel
        
        # Ensure contiguous array
        stereo_wave = np.ascontiguousarray(stereo_wave)
        
        try:
            return pygame.sndarray.make_sound(stereo_wave)
        except:
            # Fallback to simple beep if numpy isn't available
            return self.create_simple_beep()
    
    def create_simple_beep(self):
        """Create a simple beep sound without numpy"""
        import array
        import math
        
        sample_rate = 22050
        duration = 0.2
        frequency = 440
        
        frames = int(duration * sample_rate)
        
        # Create a proper 2D array for stereo
        sound_array = []
        
        for i in range(frames):
            t = i / sample_rate
            # Simple sine wave with fade out
            amplitude = 16383 * (1 - t / duration)
            wave_value = int(amplitude * math.sin(2 * math.pi * frequency * t))
            
            # Add left and right channel
            sound_array.append([wave_value, wave_value])
        
        try:
            import numpy as np
            sound_array = np.array(sound_array, dtype=np.int16)
            return pygame.sndarray.make_sound(sound_array)
        except:
            # If that fails, create empty sound
            return pygame.mixer.Sound(buffer=array.array('h', [0, 0] * 100))
    
    def create_background_music(self):
        """Create procedural background music tracks"""
        try:
            import numpy as np
            
            # Menu music - ambient and mysterious
            self.background_tracks['menu'] = self.create_menu_music()
            
            # Game music - upbeat and energetic
            self.background_tracks['game'] = self.create_game_music()
            
            # Puzzle music - thoughtful and calm
            self.background_tracks['puzzle'] = self.create_puzzle_music()
            
            print("✓ Background music tracks created")
            
        except Exception as e:
            print(f"⚠ Could not create background music: {e}")
            # Create silent tracks as fallback
            self.background_tracks = {
                'menu': self.create_simple_beep(),
                'game': self.create_simple_beep(),
                'puzzle': self.create_simple_beep()
            }
    
    def create_menu_music(self):
        """Create ambient menu music"""
        import numpy as np
        import math
        
        sample_rate = 22050
        duration = 30  # 30 seconds loop
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Base ambient pad with slow chord progression
        # Em - G - D - Am progression
        chords = [
            [164.81, 196.00, 246.94],  # Em (E, G, B)
            [196.00, 246.94, 293.66],  # G (G, B, D)
            [146.83, 184.99, 220.00],  # D (D, F#, A)
            [220.00, 261.63, 329.63]   # Am (A, C, E)
        ]
        
        wave = np.zeros_like(t)
        chord_duration = duration / len(chords)
        
        for i, chord in enumerate(chords):
            start_time = i * chord_duration
            end_time = (i + 1) * chord_duration
            mask = (t >= start_time) & (t < end_time)
            
            # Create chord with soft attack and decay
            chord_wave = np.zeros_like(t[mask])
            for freq in chord:
                # Add harmonics for richer sound
                chord_wave += 0.3 * np.sin(2 * np.pi * freq * (t[mask] - start_time))
                chord_wave += 0.1 * np.sin(2 * np.pi * freq * 2 * (t[mask] - start_time))
            
            # Soft envelope
            envelope = np.exp(-(t[mask] - start_time) * 0.3) * (1 - np.exp(-(t[mask] - start_time) * 5))
            wave[mask] = chord_wave * envelope
        
        # Add some ethereal high notes
        for i in range(8):
            freq = 523.25 * (2 ** (i / 12))  # C major scale in higher octave
            phase = np.random.random() * 2 * np.pi
            note_wave = 0.05 * np.sin(2 * np.pi * freq * t + phase) * np.sin(0.1 * np.pi * t)
            wave += note_wave
        
        return self.numpy_to_sound(wave)
    
    def create_game_music(self):
        """Create upbeat game music"""
        import numpy as np
        import math
        
        sample_rate = 22050
        duration = 20  # 20 seconds loop
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Upbeat electronic melody
        # Key of C major, 120 BPM
        beat_duration = 60.0 / 120  # 0.5 seconds per beat
        
        # Melody notes (C major scale)
        melody_notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C D E F G A B C
        
        # Create melody pattern
        melody_pattern = [0, 2, 4, 2, 0, 4, 6, 4, 2, 0, 4, 2, 0, 2, 4, 7]  # Note indices
        
        wave = np.zeros_like(t)
        
        # Add melody
        for i, note_idx in enumerate(melody_pattern):
            start_time = i * beat_duration
            end_time = min((i + 1) * beat_duration, duration)
            
            if start_time >= duration:
                break
                
            mask = (t >= start_time) & (t < end_time)
            if np.any(mask):
                freq = melody_notes[note_idx]
                
                # Electronic sound with envelope
                note_t = t[mask] - start_time
                envelope = np.exp(-note_t * 3) * (1 - np.exp(-note_t * 20))
                
                # Square wave for electronic feel
                note_wave = 0.2 * np.sign(np.sin(2 * np.pi * freq * note_t))
                note_wave += 0.1 * np.sin(2 * np.pi * freq * 2 * note_t)  # Octave harmonic
                
                wave[mask] += note_wave * envelope
        
        # Add bass line
        bass_pattern = [0, 0, 2, 2, 4, 4, 2, 2] * 4  # Repeating bass
        bass_notes = [130.81, 146.83, 164.81]  # C D E (lower octave)
        
        for i, note_idx in enumerate(bass_pattern):
            if note_idx >= len(bass_notes):
                continue
                
            start_time = i * beat_duration
            end_time = min((i + 1) * beat_duration, duration)
            
            if start_time >= duration:
                break
                
            mask = (t >= start_time) & (t < end_time)
            if np.any(mask):
                freq = bass_notes[note_idx]
                note_t = t[mask] - start_time
                
                # Simple sine wave for bass
                bass_wave = 0.15 * np.sin(2 * np.pi * freq * note_t)
                wave[mask] += bass_wave
        
        return self.numpy_to_sound(wave)
    
    def create_puzzle_music(self):
        """Create calm puzzle-solving music"""
        import numpy as np
        import math
        
        sample_rate = 22050
        duration = 25  # 25 seconds loop
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Gentle, contemplative melody
        # Pentatonic scale for a calm feel
        pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00]  # C D E G A
        
        wave = np.zeros_like(t)
        
        # Slow, flowing melody
        note_duration = 2.0  # 2 seconds per note
        melody_pattern = [0, 2, 4, 3, 1, 4, 2, 0, 3, 1, 4, 2, 0]
        
        for i, note_idx in enumerate(melody_pattern):
            if note_idx >= len(pentatonic):
                continue
                
            start_time = i * note_duration
            end_time = min((i + 1) * note_duration, duration)
            
            if start_time >= duration:
                break
                
            mask = (t >= start_time) & (t < end_time)
            if np.any(mask):
                freq = pentatonic[note_idx]
                note_t = t[mask] - start_time
                
                # Soft sine wave with gentle envelope
                envelope = np.exp(-note_t * 0.5) * (1 - np.exp(-note_t * 2))
                note_wave = 0.15 * np.sin(2 * np.pi * freq * note_t)
                
                # Add some soft harmonics
                note_wave += 0.05 * np.sin(2 * np.pi * freq * 1.5 * note_t)  # Perfect fifth
                
                wave[mask] += note_wave * envelope
        
        # Add gentle arpeggiated accompaniment
        arp_notes = [130.81, 164.81, 196.00, 164.81]  # C E G E (lower octave)
        arp_duration = 1.0
        
        for i in range(int(duration / arp_duration)):
            note_idx = i % len(arp_notes)
            start_time = i * arp_duration
            end_time = min((i + 1) * arp_duration, duration)
            
            mask = (t >= start_time) & (t < end_time)
            if np.any(mask):
                freq = arp_notes[note_idx]
                note_t = t[mask] - start_time
                
                arp_wave = 0.08 * np.sin(2 * np.pi * freq * note_t) * np.exp(-note_t * 1.5)
                wave[mask] += arp_wave
        
        return self.numpy_to_sound(wave)
    
    def create_silent_music(self):
        """Create silent music tracks for users who prefer no background music"""
        import numpy as np
        
        # Create very quiet ambient tracks instead of complete silence
        sample_rate = 22050
        duration = 5.0  # Short silent loops
        frames = int(sample_rate * duration)
        
        # Very quiet white noise for ambience
        quiet_noise = np.random.normal(0, 0.001, frames).astype(np.float32)
        
        # Create stereo array
        stereo_wave = np.zeros((frames, 2), dtype=np.int16)
        stereo_wave[:, 0] = (quiet_noise * 100).astype(np.int16)  # Very quiet
        stereo_wave[:, 1] = (quiet_noise * 100).astype(np.int16)
        
        try:
            silent_sound = pygame.sndarray.make_sound(stereo_wave)
            self.background_tracks = {
                'menu': silent_sound,
                'game': silent_sound,
                'puzzle': silent_sound
            }
            print("✓ Silent music mode enabled")
        except:
            # Fallback to beeps if needed
            beep = self.create_simple_beep()
            self.background_tracks = {'menu': beep, 'game': beep, 'puzzle': beep}
    
    def numpy_to_sound(self, wave):
        """Convert numpy array to pygame sound"""
        import numpy as np
        
        # Normalize and convert to pygame sound
        wave = np.clip(wave * 16383, -16383, 16383).astype(np.int16)
        
        # Create stereo array
        stereo_wave = np.zeros((len(wave), 2), dtype=np.int16)
        stereo_wave[:, 0] = wave  # Left channel
        stereo_wave[:, 1] = wave  # Right channel
        
        # Ensure contiguous array
        stereo_wave = np.ascontiguousarray(stereo_wave)
        
        try:
            return pygame.sndarray.make_sound(stereo_wave)
        except:
            return self.create_simple_beep()
    
    def play_sound(self, sound_name, volume_override=None):
        """Play a sound effect"""
        # Check if sound effects are enabled (will be set by main game)
        if hasattr(self, 'sound_effects_enabled') and not self.sound_effects_enabled:
            return
            
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            volume = volume_override if volume_override else (self.sfx_volume * self.master_volume)
            sound.set_volume(volume)
            sound.play()
    
    def play_background_music(self, track_name, loop=-1):
        """Play procedural background music"""
        if track_name in self.background_tracks:
            # Don't restart if already playing the same track
            if self.current_music == track_name and self.music_channel and self.music_channel.get_busy():
                return
                
            # Stop current music
            self.stop_music()
            
            # Get a dedicated channel for music
            if self.music_channel is None:
                self.music_channel = pygame.mixer.Channel(0)
            
            # Play the track
            sound = self.background_tracks[track_name]
            sound.set_volume(self.music_volume * self.master_volume * 0.6)  # Keep music quieter than SFX
            
            if loop == -1:
                # Infinite loop
                self.music_channel.play(sound, loops=-1)
            else:
                self.music_channel.play(sound, loops=loop)
            
            self.current_music = track_name
            print(f"♪ Playing background music: {track_name}")
    
    def play_music(self, music_file, loop=-1):
        """Play background music from file (legacy method)"""
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            pygame.mixer.music.play(loop)
            self.current_music = music_file
        except:
            # Fallback to procedural music
            if 'menu' in self.background_tracks:
                self.play_background_music('menu', loop)
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        if self.music_channel:
            self.music_channel.stop()
        self.current_music = None
    
    def set_master_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0, min(1, volume))
        
        # Update music volume
        if self.current_music:
            if self.music_channel and self.current_music in self.background_tracks:
                sound = self.background_tracks[self.current_music]
                sound.set_volume(self.music_volume * self.master_volume * 0.6)
            else:
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0, min(1, volume))
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0, min(1, volume))
        
        # Update current music volume
        if self.current_music:
            if self.music_channel and self.current_music in self.background_tracks:
                sound = self.background_tracks[self.current_music]
                sound.set_volume(self.music_volume * self.master_volume * 0.6)
            else:
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def get_volumes(self):
        """Get current volume settings"""
        return {
            'master': self.master_volume,
            'sfx': self.sfx_volume,
            'music': self.music_volume
        }