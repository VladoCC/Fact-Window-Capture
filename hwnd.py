import win32gui


def enum(hwnd, results):
    # collecting hwnd and name of every window into a set
    results.add((hwnd, win32gui.GetWindowText(hwnd)))


def get_windows():
    # clearing set before filling it with new data
    winset = set()
    # calling api which calls back to our enum func for each window on the screen
    win32gui.EnumWindows(enum, winset)
    return winset


def find_new_window():
    # collecting a set of windows available before the search
    last = get_windows()
    while True:
        windows = get_windows()
        # checking if any windows appeared/disappared
        diff = last.difference(windows)
        if len(diff) > 0:
            break
    # collecting difference between two sets to a list
    result = list(windows - last)
    return result
