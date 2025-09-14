import curses


def main(stdscr):
    # this is a spike of using curses for a little ascii cli for playing tic-tac-toe
    # Clear screen
    stdscr.clear()

    # Disable echoing of typed characters
    # curses.noecho()

    # Enable non-blocking input
    stdscr.nodelay(True)

    # Example maze representation (simple 2D list)
    gameboard = [
        "######",
        "######",
        "######",
    ]

    # Draw the maze
    for y, row in enumerate(gameboard):
        for x, char in enumerate(row):
            stdscr.addch(y, x, char)

    # Initial player position
    start_index = 4
    # Main game loop
    while True:
        # stdscr.addch(pa, '@')
        stdscr.refresh()
        key = stdscr.getch()
        x, y = curses.getsyx()
        if key != -1:
            log(curses.LINES, curses.COLS)
            log((x, y))
            # log(key)
        if key == curses.KEY_UP:  # up arrow
            new_y = y - 1
            curses.setsyx(new_y, x)
            stdscr.addch(new_y, x, "-")
        if key == curses.KEY_DOWN:  # up arrow
            new_y = y + 1
            curses.setsyx(new_y, x)
            stdscr.addch(new_y, x, "-")
        if key == curses.KEY_ENTER:
            break
        if key == ord('q'):
            curses.nocbreak()

    # for y, row in enumerate(gameboard):
    #     for x, char in enumerate(row):
    #         stdscr.addch(y, x, char)

        curses.napms(100)  # Small delay


def log(*message):
    with open("log.txt", "w") as f:
        for m in message:
            f.write(str(m))
        f.write(str("\n"))
    # f.close()


if __name__ == '__main__':
    # curses.initscr()
    curses.wrapper(main)
