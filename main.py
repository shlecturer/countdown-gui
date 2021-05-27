import logging
import time
from breezypythongui import EasyFrame, HORIZONTAL
from button import Button
from numbers import Numbers

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
    By pressing the button, a new number can be selected.
    """
    def __init__(self):
        EasyFrame.__init__(self, title="Let's play Countdown!")

        self.__big_num = self.addCanvas(row=0, column=0,
                                        columnspan=6,
                                        width=450,
                                        height=200,
                                        background='black')

        # Number of big numbers (from radio button group)
        self.__n_big = 2

        # Target number
        self.__show_target_number('---')

        # Create a button that starts the process of getting a target
        self.__button = Button(self, on_click=self.__create_random_bignum)
        self.__button.enable(False)
        self.addCanvas(canvas=self.__button, row=1, column=6)

        # Draw the "cards" that hold the numbers (big and small)
        self.__nums = []
        for x in range(6):
            canvas = self.addCanvas(row=1, column=x,
                                    width=70,
                                    height=50, background='white')
            canvas.drawRectangle(1, 1, 69, 49,
                                 outline="black",
                                 fill="white")
            canvas.drawText('-', 32, 28, font=("Arial", 32, 'bold'), tag=f'num-{x}')
            self.__nums.append(canvas)

        # Create the button group to select the number of BIG ones
        self.__group = self.addRadiobuttonGroup(row=2, column=0,
                                                columnspan=6, rowspan=1,
                                                orient=HORIZONTAL)
        self.__group.addRadiobutton(text='4 Big', command=lambda: self.__set_big_num(4))
        self.__group.addRadiobutton(text='3 Big', command=lambda: self.__set_big_num(3))
        # default button
        default = self.__group.addRadiobutton(text='2 Big', command=lambda: self.__set_big_num(2))
        self.__group.addRadiobutton(text='1 Big', command=lambda: self.__set_big_num(1))
        self.__group.addRadiobutton(text='All small', command=lambda: self.__set_big_num(0))
        self.__group.setSelectedButton(default)

        # Start a round of Countdown!
        self.addButton("Let's play Countdown!", row=3, column=0,
                       columnspan=6, rowspan=3,
                       # fgcolour='white',
                       # bgcolour='blue',
                       command=self.__play)

    def __set_big_num(self, num):
        """Set the number of big numbers from the radio group..
        """
        self.__n_big = num

    def __show_target_number(self, num):
        """This method draws a Big Number on the canvas. It splits
        the number into three digits. Each is shown separately on
        the canvas.
        Technically it takes a string of length >= 3. This is not
        checked, so the caller must make sure this is the case.
        """
        fill = 'lightgreen'
        font = ("Courier", 150, 'bold')
        for x in range(3):
            self.__big_num.delete(f'bignum-{x}')
            self.__big_num.drawText(num[x], 75 + 150 * x, 100, font=font,
                                    tag=f'bignum-{x}', fill=fill)

    def __create_random_bignum(self):
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
            guess = Numbers.get_target_number(low=100, high=999)
            self.__show_target_number(str(guess))

            # Make sure the display updates
            self.update()

    def __play(self):
        """This method starts a round. It sets the "big number" in the display
        to --- to indicate a new round has started. It selects a number of
        random numbers based on the selected RadioButton. The player can
        choose between 0 and 4 big numbers. The rest will be small numbers.
        """
        self.__show_target_number('---')

        # Get the randoms selection and update the display
        sample = Numbers.get_random_selection(self.__n_big)
        for x in range(6):
            canvas = self.__nums[x]
            canvas.delete(f'num-{x}')
            canvas.drawText(str(sample[x]), 32, 28, font=("Arial", 32, 'bold'), tag=f'num-{x}')

        self.__button.enable(True)


def main():
    countdown_gui = CountdownGui()
    countdown_gui.mainloop()


if __name__ == '__main__':
    main()
