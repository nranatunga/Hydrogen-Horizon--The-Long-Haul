import pygame
import os

class SoundManager:
    def __init__(self):
        """Initialize the sound manager with all game sounds"""
        # Ensure mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Set default volumes
        self.sfx_volume = 0.5
        self.music_volume = 0.3
        
        # Dictionary to store sound effects
        self.sounds = {}
        
        # Load sound effects
        try:
            self.sounds['button_click'] = pygame.mixer.Sound(os.path.join('assets', 'button_click1.wav'))
            self.sounds['fuel_collect'] = pygame.mixer.Sound(os.path.join('assets', 'fuel_collect_diesal.wav'))
            self.sounds['fuel_station'] = pygame.mixer.Sound(os.path.join('assets', 'fuel_station_diesal.wav'))
            self.sounds['truck_collision'] = pygame.mixer.Sound(os.path.join('assets', 'truck_collision.wav'))
            self.sounds['health_station'] = pygame.mixer.Sound(os.path.join('assets', 'fuel_station_hydrogen.mp3'))
            # Set volume for all sound effects
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
            
        except Exception as e:
            print(f"Error loading sounds: {e}")
            
    def play_sound(self, sound_name):
        """Play a sound effect once"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def play_music(self, track_name, loop=-1):
        """Play a music track with optional looping"""
        try:
            # Create the full path to the music file
            music_file = os.path.join('assets', f'{track_name}.wav')
            if track_name == 'health_station':  # Special case for mp3
                music_file = os.path.join('assets', f'{track_name}.mp3')
                
            # Load and play the music
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loop)
        except Exception as e:
            print(f"Error playing music track {track_name}: {e}")
                
    def stop_music(self):
        """Stop the currently playing music track"""
        pygame.mixer.music.stop()
        
    def pause_music(self):
        """Pause the currently playing music track"""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Unpause the currently playing music track"""
        pygame.mixer.music.unpause()
        
    def set_sfx_volume(self, volume):
        """Set volume for sound effects (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
            
    def set_music_volume(self, volume):
        """Set volume for music (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)