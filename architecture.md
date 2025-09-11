## game

Tracks the evolving state of a single game

## player

has a name
plays a game against another player

## session
- triggered when a player attempts a valid `join_session`
Tracks all the games for a set of players
the score for each player for each game they have won
the number of draws

is started by the server

## server

- starts a web based endpoint
- allows for the command line client to connect to a session

## endpoints

### api

- `/ ` -> serves index.html, the game board for a player to join a game

```
/api/
```

- `POST /connect/{player_id}`
- `GET /player/{player_id}`

### game session streaming endpoint

`wss://api/sessions/{session_id}/stream`


**client -> server**
to join a session

```json
{
"action": "join_session",
"player_id": "playername",
}
```


**server -> client**
```json
{
"event": "player_joined",
"data": {"status": waiting},
}
```



