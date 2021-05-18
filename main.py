import logging
import random
import time
from tkinter import HORIZONTAL
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
    NUMBERS = {
        'small': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
        'big': [25, 50, 75, 100],
    }

    def __init__(self):
        EasyFrame.__init__(self, title="Countdown")

        self.canvas = self.addCanvas(row=0, column=0,
                                     columnspan=6,
                                     width=450,
                                     height=200)
        self.canvas.drawRectangle(2, 2, 451, 201,
                                  outline="white",
                                  fill="black")

        self.__show_bignum('---')
        self.addCanvas(canvas=RedButton(self, on_click=self.create_random_bignum),
                       row=1, column=6)

        self.__nums = []
        for x in range(6):
            canvas = self.addCanvas(row=1, column=x,
                                    width=70,
                                    height=50)
            canvas.drawRectangle(0, 0, 69, 49,
                                 outline="black",
                                 fill="white")
            canvas.drawText('-', 32, 28, font=("Arial", 36, 'bold'), tag=f'num-{x}')
            self.__nums.append(canvas)

        self.group = self.addRadiobuttonGroup(row=2, column=0, columnspan=6, rowspan=1,
                                              orient=HORIZONTAL)
        self.group.addRadiobutton('4 Big')
        self.group.addRadiobutton('3 Big')
        default = self.group.addRadiobutton('2 Big')
        self.group.addRadiobutton('1 Big')
        self.group.addRadiobutton('All small')

        self.group.setSelectedButton(default)

        self.addButton("Play", row=3, column=0, columnspan=6, rowspan=2, command=self.play)

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
            guess = random.randint(100, 999)
            self.__show_bignum(str(guess))

            # Make sure the display updates
            self.update()

    def get_random_selection(self, big, total=6):
        """This method gets a random selection of numbers from the
        available numbers. The number of "big numbers" must be
        provided as the argument {big}. The parameter {total} is
        optional and set 6 by default (the actual number for the
        official Countdown game.
        """
        assert total - big >= 0

        big_numbers = random.sample(self.NUMBERS['big'], big)
        small_numbers = random.sample(self.NUMBERS['small'], total - big)
        return big_numbers + small_numbers

    def play(self):
        """This method starts a round. It sets the "big number" in the display
        to --- to indicate a new round has started. It selects a number of
        random numbers based on the selected RadioButton. The player can
        choose between 0 and 4 big numbers. The rest will be small numbers.
        """
        self.__show_bignum('---')

        # Get the selected value from the Button Group
        value = self.group.getSelectedButton()['value'][0]
        if value == 'A':
            big = 0  # All small
        else:
            big = int(value)  # The number of "big numbers"

        # Get the random selection and update the display
        sample = self.get_random_selection(big)
        for x in range(6):
            canvas = self.__nums[x]
            canvas.delete(f'num-{x}')
            canvas.drawText(str(sample[x]), 32, 28, font=("Arial", 36, 'bold'), tag=f'num-{x}')


class RedButton(EasyCanvas):
    def __init__(self, parent, on_click=None):
        EasyCanvas.__init__(self, parent, width=50, height=50)

        self.drawOval(12, 12, 38, 38, fill='yellow')  # circle

        self.__on_click = on_click

    def mouseReleased(self, event):
        """This method is triggered when the mouse button is released.
        We count that as a click event and call the handler accordingly..
        """
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
