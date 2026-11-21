# Mickey's Clock

A pygame clock that shows **minutes and seconds only**, using the hands from the
Mickey Mouse clock photo (`images/mickeyclock.jpeg`):

* **Right hand** (long, pointing arm) = minutes hand
* **Left hand** (short arm at the cheek) = seconds hand
  (set `SWAP_HANDS = True` in `clock.py` to swap them)

## Run
```bash
pip3 install pygame
python3 main.py
```
Esc or closing the window quits.

## Images
* `mickeyclock.jpeg` - the original photo.
* `clock_face.png` - the photo with both arms removed (dial only).
* `hand_left.png`, `hand_right.png` - the two hands cut out of the photo (with transparency).
* `hub.png` - the centre knob, drawn on top of the hands.
* `hands.json` - pivot points and the angle each arm has in the photo.

They are produced from the photo by `build_assets.py` (only needed if you want to
regenerate them: `pip3 install opencv-python numpy pillow`, then
`python3 build_assets.py images/mickeyclock.jpeg`).

## How it works
* `get_time()` reads the system time; `tm_sec % 60` guards against leap seconds (60/61).
* Seconds angle = `sec * 6`; minutes angle = `min * 6 + sec * 0.1`.
* Each hand is rotated with `pygame.transform.rotate()` around its pivot
  ([blit_rotate](https://stackoverflow.com/a/54714144)). Pygame turns counter-clockwise,
  so the angle is negated and the arm's resting angle in the photo is subtracted.
* The loop redraws at 30 FPS but always reads the system clock, so it stays in sync
  and the hands step once per second.
