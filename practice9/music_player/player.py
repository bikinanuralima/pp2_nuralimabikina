import pygame
import os


class MusicPlayer:
    def __init__(self, folder):
        pygame.mixer.init()

        self.folder = folder
        self.tracks = []
        self.current_track = 0
        self.playing = False

        # Load music files from folder
        for file in os.listdir(folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                self.tracks.append(file)

        self.tracks.sort()

    def play(self):
        if len(self.tracks) == 0:
            print("Playlist is empty!")
            return

        path = os.path.join(
            self.folder,
            self.tracks[self.current_track]
        )

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        if len(self.tracks) == 0:
            return

        self.current_track += 1

        if self.current_track >= len(self.tracks):
            self.current_track = 0

        self.play()

    def previous_track(self):
        if len(self.tracks) == 0:
            return

        self.current_track -= 1

        if self.current_track < 0:
            self.current_track = len(self.tracks) - 1

        self.play()

    def get_current_track(self):
        if len(self.tracks) == 0:
            return "No tracks available"

        return self.tracks[self.current_track]

    def get_position(self):
        # Playback position in milliseconds
        return pygame.mixer.music.get_pos()