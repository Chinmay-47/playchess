# playchess


![License](https://img.shields.io/github/license/Chinmay-47/playchess?label=License&style=plastic)
![Commits](https://img.shields.io/github/commit-activity/y/Chinmay-47/playchess?label=Commits&style=plastic)
![Python](https://img.shields.io/badge/Python-%203.9-green?style=plastic)

<br>

## About
Playchess is a playable AI chess engine that can be used 
to play against AI bots as well as other users.
It is built from scratch using PyGame in Python.

<br>

## Installation
```
git clone https://github.com/Chinmay-47/playchess.git
cd playchess
pip install -e .
```

<br>

## Usage
The PlayChess class is for convenience and is used to aggregate and run all the different game modes. 

```python
from playchess import PlayChess

# To play another user
PlayChess.play_human()

# To play the MinMax bot
PlayChess.play_minmax_bot(pruning=True, depth=2)
```
These functions run the game loop and pop out a window to play the game.

<br>

## Contribute
Contributions to enhance the project are welcome and appreciated.

Some ideas for contribution are:
- Using bit-board representation for the chess board
- Code optimizations (currently uses python lists which are slow)
- Reinforcement learning based bots
- Lastly, documentation for the modules

<br>

## Resources
I would highly recommend checking them out:

- [Pygame Docs](https://www.pygame.org/docs/)
- [Eddie Sharick](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)
- [ArjanCodes](https://www.youtube.com/c/ArjanCodes)
- [mCoding](https://www.youtube.com/c/mCodingWithJamesMurphy)
