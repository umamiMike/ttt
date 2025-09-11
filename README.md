## Tic Tac Toe

## installation and setup

1. clone from `{TODO: }` and cd into the directory
2. `python -m pip install -r requirements.txt`
3. run `python main.py`
4. from the terminal 
## Design Choices:
This is a demo game of tic-tac-toe.  
It will have core game logic management, 
- a web server for hosting an api 
- A web client for a player interface
- A `curses` based ui for a terminal interface.  
- it will communicate via websocket connections

## Reasoning
I wanted to demo the architecture using multiple types of interfaces but without large dependencies.

I use big frameworks a ton.  With this, I want to build things from the ground up, with as few libraries, but using, and illustrating, the concepts of an `event driven` system
I thought it would be fun to make something that 2 players could play, from two very different types of interfaces, but have a similar experience.

