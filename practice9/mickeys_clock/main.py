"""Mickey's Clock - minutes and seconds only, shown with Mickey's hands."""
import pygame

from clock import MickeyClock

SIZE = 700   # window is SIZE x SIZE pixels
FPS = 30     # redraw often so the window stays responsive; the hands step once per second


def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    mickey = MickeyClock(SIZE)
    font = pygame.font.SysFont(None, 28)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.fill((255, 255, 255))
        minutes, seconds = mickey.draw(screen)
        label = font.render("{:02d}:{:02d}".format(minutes, seconds), True, (70, 70, 70))
        screen.blit(label, label.get_rect(midbottom=(SIZE // 2, SIZE - 6)))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
