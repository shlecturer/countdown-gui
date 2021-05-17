import logging
import random
from breezypythongui import EasyFrame, EasyCanvas

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CountdownGui(EasyFrame):
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

        self.create_random_bignum(guess=101)
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

    def create_random_bignum(self, guess=None):
        if not guess:
            guess = random.randint(101, 999)

        n = 100
        for x in range(3):
            self.canvas.delete(f'bignum-{x}')
            m = guess // n
            guess -= m * n
            n //= 10
            self.canvas.drawText(str(m), 75 + 150 * x, 100, font=("Courier", 150, 'bold'),
                                 tag=f'bignum-{x}', fill='lightgreen')


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
