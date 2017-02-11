# -*- coding: utf-8 -*-

import curses
import curses.panel
from time import sleep


def make_panel(l, h, x, y, string):
    win = curses.newwin(h, l, y, x)
    win.erase()
    win.box()
    win.addstr(1, 1, string)

    panel = curses.panel.new_panel(win)
    return win, panel


def test(stdscr):
    try:
        curses.curs_set(0)
    except:
        pass

    stdscr.box()
    stdscr.addstr(1, 1, "crypt0n1t3")
    win1, panel1 = make_panel(16, 20, 2, 2, "M3NU")
    win2, panel2 = make_panel(56, 20, 18, 2, "3D1T0R")
    curses.panel.update_panels()
    stdscr.refresh()
    sleep(0.314)

    panel1.top()
    curses.panel.update_panels()
    stdscr.refresh()

    # sleep(0.314)
    # for i in range(20):
    #     panel2.move(8, 8 + i)

    curses.panel.update_panels()
    stdscr.refresh()
    sleep(0.1)

    sleep(5)


if __name__ == '__main__':
    curses.wrapper(test)
