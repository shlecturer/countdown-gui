import logging
from breezypythongui import EasyCanvas

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Button(EasyCanvas):
    """This class creates a very simple clickable button. The
    button is simply a circle of a certain {colour}. A listener
    can register to its click events by supplying a function
    with the {on_click} parameter.
    """
    MIN = 12
    MAX = 38

    def __init__(self, parent, colour='yellow', on_click=None):
        EasyCanvas.__init__(self, parent, width=50, height=50)

        # Draw the actual "button" (a circle)
        self.oval = self.drawOval(self.MIN, self.MIN, self.MAX, self.MAX, fill=colour)

        # Store the colour
        self.__colour = colour

        # Enable the button
        self.__enabled = True

        # Store the click handler
        self.__on_click = on_click

    def enable(self, enabled=True):
        """Enable or disable the button based on {enabled}.
        The default is True, so the button is enabled.
        """
        self.__enabled = enabled

        # Set colour to grey if disabled, use provided colour if enabled
        self.itemconfigure(self.oval, fill=self.__colour if self.__enabled else 'lightgrey')

    def mousePressed(self, event):
        if not self.__enabled:
            # Ignore if button is disabled
            return

        # Visual indication mouse button press has occurred
        self.itemconfigure(self.oval, outline='lightgrey')

    def mouseReleased(self, event):
        """This method is triggered when the mouse button is released.
        We count that as a click event and call the handler accordingly,
        as there is no "actual" mouse click event.
        """
        if not self.__enabled:
            # Ignore if button is disabled
            return

        # Visual indication that mouse button release has occurred
        self.itemconfigure(self.oval, outline='black')

        # Call click handler if it exists
        if self.__on_click:
            x, y = event.x, event.y
            if self.MIN <= x <= self.MAX and self.MIN <= y <= self.MAX:
                logger.info('Click event. Calling handler.')
                self.__on_click()
