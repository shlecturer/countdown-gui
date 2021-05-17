import logging
import random
import time
from breezypythongui import EasyFrame, EasyCanvas

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CountdownGui(EasyFrame):
    """The CountdownGui class creates a visual representation of the
    Numbers game that is part of Countdown / Letters and Numbers. It
    shows the number to be reached (from 101-999) as a really big
    number (as in size), and the small numbers with which to make it.

    The small numbers available are 1-10 (each 2x), and the big numbers
    are 25, 50, 75, and 100 (each 1x).

    In the game, the player can choose to select 0 - 4 "big numbers",
    while the rest is automatically made up of small numbers. In total,
    six numbers are selected.

    By pressing the yellow button, a new number can be selected.
    """
    SMALL_NUMBERS = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
    BIG_NUMBERS = [25, 50, 75, 100]

    def __init__(self):
        EasyFrame.__init__(self, title="Countdown")

        self.canvas = self.addCanvas(row=0, column=0,
                                     columnspan=6,
                                     width=450,
                                     height=200)
        self.canvas.drawRectangle(2, 2, 451, 201,
                                  outline="white",
                                  fill="black")

        for x in range(3):
            self.canvas.drawText('0', 75 + 150 * x, 100, font=("Courier", 150, 'bold'),
                                 tag=f'bignum-{x}', fill='lightgreen')

        self.__show_bignum('---')
        self.addCanvas(canvas=RedButton(self, on_click=self.create_random_bignum),
                       row=1, column=6)

        nums = []
        for x in range(6):
            canvas = self.addCanvas(row=1, column=x,
                                    width=70,
                                    height=50)
            canvas.drawRectangle(0, 0, 69, 49,
                                 outline="black",
                                 fill="white")
            canvas.drawText(' ', 32, 28, font=("Arial", 36, 'bold'), tag=f'num-{x}')
            nums.append(canvas)

    def __show_bignum(self, num):
        """This method draws a Big Number on the canvas. It splits
        the number into three digits. Each is shown separately on
        the canvas.

        Technically it takes a string of length >= 3. This is not
        checked, so the caller must make sure this is the case.
        """
        fill = 'lightgreen'
        font = ("Courier", 150, 'bold')
        for x in range(3):
            self.canvas.delete(f'bignum-{x}')
            self.canvas.drawText(num[x], 75 + 150 * x, 100, font=font,
                                 tag=f'bignum-{x}', fill=fill)

    def create_random_bignum(self):
        """Create a random number and show it as a Big Number.
        If a guess is provided, it is simply shown. If no guess
        is provided, the program will randomly select one,
        while showing the selection process. It shows numbers
        really quickly while slowing down over 2-3 seconds.
        """
        timeout = 0.0
        for x in range(25):
            time.sleep(timeout)
            if x % 5 == 0:
                timeout += 0.025

            # Get a new random number
            guess = random.randint(101, 999)
            self.__show_bignum(str(guess))

            # Make sure the display updates
            self.update()


class RedButton(EasyCanvas):
    def __init__(self, parent, on_click=None):
        EasyCanvas.__init__(self, parent, width=50, height=50)

        self.drawOval(12, 12, 38, 38, fill='yellow')

        self.__on_click = on_click

    def mouseReleased(self, event):
        if self.__on_click:
            x, y = event.x, event.y
            if 12 <= x <= 38 and 12 <= y <= 38:
                logger.info('Click event. Calling handler.')
                self.__on_click()


def main():
    countdown_gui = CountdownGui()
    countdown_gui.mainloop()


if __name__ == '__main__':
    main()
