# soundmanager.py
import pygame
from pathlib import Path

def find_assets_dir() -> Path:
    """Walk up from this file until an 'assets' directory is found."""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent / "assets"
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Could not find 'assets' folder starting from: {here}")

class SoundManager:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except Exception as e:
                print(f"Audio init failed: {e}")
                self.sounds = {}
                self.assets_dir = None
                return

        self.sfx_volume = 0.5
        self.music_volume = 0.3
        self.sounds = {}

        self.assets_dir = find_assets_dir()
        print("Sound assets_dir:", self.assets_dir)  # keep until confirmed

        try:
            self.sounds["button_click"]    = pygame.mixer.Sound(str(self.assets_dir / "button_click1.wav"))
            self.sounds["fuel_collect"]    = pygame.mixer.Sound(str(self.assets_dir / "fuel_collect_diesal.wav"))
            self.sounds["fuel_station"]    = pygame.mixer.Sound(str(self.assets_dir / "fuel_station_diesal.wav"))
            self.sounds["truck_collision"] = pygame.mixer.Sound(str(self.assets_dir / "truck_collision.wav"))

            for s in self.sounds.values():
                s.set_volume(self.sfx_volume)

            print("Loaded sounds:", list(self.sounds.keys()))
        except Exception as e:
            print(f"Error loading sounds: {e}")

    def play_sound(self, sound_name: str):
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()

    # OPTION 1: restore play_music for your existing main3.py call
    def play_music(self, track_name: str, loop: int = -1):
        """
        Play background music by track name without extension.
        Example: play_music('main_menu') will try main_menu.ogg/.wav/.mp3 in assets.
        """
        if not self.assets_dir:
            print("Cannot play music: assets_dir not set (mixer init may have failed).")
            return

        candidates = [".ogg", ".wav", ".mp3"]
        for ext in candidates:
            path = self.assets_dir / f"{track_name}{ext}"
            if path.exists():
                try:
                    pygame.mixer.music.load(str(path))
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(loop)
                    return
                except Exception as e:
                    print(f"Error playing music file {path.name}: {e}")
                    return

        print(f"Music track not found: {track_name} (tried {', '.join(track_name+e for e in candidates)})")

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for s in self.sounds.values():
            s.set_volume(self.sfx_volume)

    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
