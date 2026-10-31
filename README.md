# GrassHunter

A small top-down action RPG in the style of the classic Zelda games, written in Python with pygame.
The world is designed in [Tiled](https://www.mapeditor.org/) and loaded with pytmx.

## Features so far
- Window, game loop and settings
- Player movement with collisions (smaller hitbox for realistic contacts)
- Camera that follows the player, with Y-sorting (sprites further down are drawn on top)
- World map made in Tiled: floor, details, grass, objects and invisible walls (coast, cliffs)
- Player animations: walk, idle and attack in 4 directions

## Controls
| Key | Action |
|---|---|
| Arrow keys | Move |
| Space | Attack |
| Left Ctrl | Magic |

## Run it
```bash
pip install -r requirements.txt
python code/main.py
```
`pygame-ce` also works instead of `pygame`.

## Project structure
```
assets/   graphics (tilesets, Hunter character, player animation frames)
code/     game source (main.py is the entry point)
maps/     world_map.tmx (Tiled map read by the game) and old CSV exports
```

## Credits
- **Graphics**: [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack)
  by **Pixel-boy** and **AAA**, released under the
  [CC0 1.0 license](https://creativecommons.org/publicdomain/zero/1.0/).
  The tilesets, the map elements and the *Hunter* character come from this pack.
  The player frames in `assets/graphics/player/` were cut from the Hunter sprite sheets
  (`Walk.png`, `Idle.png`, `Attack.png`) and scaled from 16 px to 64 px.
- **Code structure** inspired by the Zelda-style pygame tutorial by
  [Clear Code](https://www.youtube.com/@ClearCode).
- **Map editor**: [Tiled](https://www.mapeditor.org/), map loading with [pytmx](https://github.com/bitcraft/pytmx).
