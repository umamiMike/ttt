## Tic Tac Toe

This is a demo game of tic-tac-toe.

## Why I built it

I have wanted to explore connecting  distributed clients using an event-driven system.  

I use big frameworks a ton. For a change I wanted to go back to buildng things
from the ground up, with as few 3rd party libraries as possible.
This is meant to demo  concepts of an `event-driven` system
there are two topics :
- "game/move" which the clients use to communicate with the backend and
- "game/state" for the backend to respond to all connected clients.

all the state of the game is managed on the backend side, and is **published** to the clients who, in turn, update their own state accordingly.

This is far from what I would consider complete, but it functions as a happy path demo.

## Design Choices:

- A web client for a player interface
- a web server for hosting the web client
- communication will be done via mqtt broker, with the web server, web client, communicating via event messages

## dependencies

- `paho mqtt client` (Python)
- `mqttjs` JS client
- `mosquitto` mqtt service

## installation and setup

### installing mqtt broker

**On windows**

- [ get the latest mosquitto installer](https://mosquitto.org/files/binary/win64/mosquitto-2.0.22-install-windows-x64.exe)

On mac

`brew install mosquitto`

On linux

using apt
```
sudo apt install mosquitto

```

or snap 
```
snap install mosquitto
```


for more info visit their [downloads page](https://mosquitto.org/download/)

1. clone from `git@github.com:umamiMike/ttt.git`
1. cd into the directory
2. `python -m pip install -r requirements.txt`

**start the mosquitto server** 

```
mosquitto -c "$(pwd)/broker/mosquitto.conf" -v
```

if successful you should see something like 

```sh
1757813654: mosquitto version 2.0.22 starting
1757813654: Config loaded from ./broker/mosquitto.conf.
1757813654: Opening ipv6 listen socket on port 1883.
1757813654: Opening ipv4 listen socket on port 1883.
1757813654: Opening websockets listen socket on port 9001.
1757813654: mosquitto version 2.0.22 running
```


**start the static web server**

for web client

```
python -m web.server
```


**start the mqtt backend client**
python -m web.mqtt_client

**open the web client**

- [open your browser running on port 8005](http://localhost:8005)
- [open another browser running on port 8005](http://localhost:8005)

Now you will be able to play tictactoe with 2 seperate browser clients

## next steps

-  [ ] add server config to make it available on the network.  It is probably more fun if you can play somebody on a different computer
- [ ] make session matchmaking.  Currently there is only a single session, as this was a toy demo. Then many people can pair up and play.
- [ ] create a cli client so you can play it from your terminal OR a web client.
- [ ] DRY up a bunch of the backend handling
- [ ] convert the js to being more modular

> I had originally intended to create a game you could connect to via a cli OR web client. I have only built the web interface. I have a spike of a curses based interface
