''' Wrapper arrounf pyatuogui to add a time delay to all actions '''
import pyautogui as autogui
from time import sleep


def moveTo(*args, d=0.1, ** kwargs):

    autogui.moveTo(*args, **kwargs)

    if d > 0:
        sleep(d)


def typewrite(*args, d=0.1, ** kwargs):

    autogui.typewrite(*args, **kwargs)

    if d > 0:
        sleep(d)


def click(*args, d=0.1, ** kwargs):

    autogui.click(*args, **kwargs)

    if d > 0:
        sleep(d)


def press(*args, d=0.1, ** kwargs):

    autogui.press(*args, **kwargs)

    if d > 0:
        sleep(d)


def hotkey(*args, d=0.1, ** kwargs):

    autogui.hotkey(*args, **kwargs)

    if d > 0:
        sleep(d)


def keyDown(*args, d=0.1, ** kwargs):

    autogui.keyDown(*args, **kwargs)

    if d > 0:
        sleep(d)


def keyUp(*args, d=0.1, ** kwargs):

    autogui.keyUp(*args, **kwargs)

    if d > 0:
        sleep(d)


def position(*args, ** kwargs):
    return autogui.position(*args, **kwargs)
