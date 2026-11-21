import pygame
import os
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 22)

# Music folder
music_folder = os.path.join(
    os.path.dirname(__file__),
    "music",
    "sample_tracks"
)

player = MusicPlayer(music_folder)

running = True

while running:

    screen.fill((30, 30, 30))

    # Keyboard events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.previous_track()

            elif event.key == pygame.K_q:
                running = False

    # Display current track
    track_name = player.get_current_track()

    title = font.render(
        "Music Player",
        True,
        (255, 255, 255)
    )

    track_text = small_font.render(
        "Track: " + track_name,
        True,
        (255, 255, 255)
    )

    screen.blit(title, (250, 50))
    screen.blit(track_text, (50, 130))

    # Display controls
    controls = [
        "P - Play",
        "S - Stop",
        "N - Next",
        "B - Previous",
        "Q - Quit"
    ]

    y = 200

    for control in controls:
        text = small_font.render(
            control,
            True,
            (200, 200, 200)
        )

        screen.blit(text, (50, y))
        y += 35

    # Playback position
    position = player.get_position()

    position_text = small_font.render(
        "Position: " + str(max(position, 0) // 1000) + " sec",
        True,
        (255, 255, 0)
    )

    screen.blit(position_text, (400, 200))

    pygame.display.flip()

pygame.quit()