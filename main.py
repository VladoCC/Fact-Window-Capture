import cv2 as cv
from time import time

import win32gui

from windowcapture import WindowCapture
import hwnd

if __name__ == '__main__':
    print("Select window search method:")
    print("  1 - Manual search for new windows")
    print("  2 - Search for any window by name")
    print("""  Other - Search for 'Preview' window by name""")
    print("Selection: ")

    way = input()

    if way == "1":
        while True:
            variants = hwnd.find_new_window()
            print("Select window:")
            for i in range(len(variants)):
                print("  ", str(i+1), " - ", variants[i])
            print("   0 - Repeat search")
            print("Selection: ")
            pos = int(input())
            if pos != 0 and pos <= len(variants):
                hwnd = variants[pos - 1][0]
                break
    else:
        window_name = "Preview"
        if way == "2":
            print("Input window name: ")
            window_name = input()
        hwnd = win32gui.FindWindow(None, window_name)
        if not hwnd:
            raise Exception('Window not found: {}'.format(window_name))

    # initialize the WindowCapture class
    wincap = WindowCapture(hwnd)

    loop_time = time()
    cont = True
    win_name = 'Captured window stream'

    while cont:

        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        cv.imshow(win_name, screenshot)

        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # waits 1 ms every loop to process key presses
        cv.waitKey(1)
        try:
            # this line will throw exception if you press exit on OpenCV window
            cont = cv.getWindowProperty(win_name, 0) >= 0
        except:
            # ends the loop after exit button is pressed
            break

    cv.destroyAllWindows()