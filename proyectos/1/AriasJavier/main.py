import curses
from curses import wrapper
import time

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("foo")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
