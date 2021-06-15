import pygame


##
# Text class
#  sets up a textbox with given text, position, and additional information
class Text:
    def __init__(self, display, text, position=(0, 0), location="topleft", fontSize=20,
                 font="comicsansms", color=(0, 0, 0), backColor=None):
        """
        Initialize the textbox with given info

        :param display: pygame window
        :param text: textbox text
        :param position: x and y position on the pygame window
        :param location: position to topleft, bottomright, center, etc
        :param fontSize: size of the text
        :param font: font of the text
        :param color: Color of the font
        :param backColor: Background color of the textbox
        """

        # Set up text
        self._color = color
        self._backColor = backColor
        self._display = display
        self._font = pygame.font.SysFont(font, fontSize)
        self._text = self._font.render(text, True, color, backColor)
        self._rect = self._text.get_rect()

        # Set up position
        self._location = location.lower()
        self._pos = position
        self.setPos()

    def text(self):
        """
        Gets the text

        :return: text of the textbox
        """

        return self._text

    def rect(self):
        """
        Gets the rectangle enclosing the textbox

        :return: rect of the textbox
        """
        return self._rect

    def setPos(self):
        """
        update position of the text
        """

        if self._location == "topLeft":
            self._rect.topleft = self._pos
        elif self._location == "topright":
            self._rect.topright = self._pos
        elif self._location == "bottomleft":
            self._rect.bottomleft = self._pos
        elif self._location == "bottomright":
            self._rect.bottomright = self._pos
        else:
            self._rect.center = self._pos

    def changePos(self, position):
        """
        Move and update position of the textbox

        :param position: x and y coordinates on the pygame window
        """

        self._pos = position
        self.setPos()

    def changeLocation(self, location):
        """
        change and update the coordinate locations of the textbox

        :param location: topleft, topright, bottomleft, bottomright, or center
        """

        if location in ("topleft", "topright", "bottomleft", "bottomright", "center"):
            self._location = location
        self.setPos()

    def setText(self, text):
        """
        set text in the textbox

        :param text: text for the textbox
        """

        self._text = self._font.render(text, True, self._color, self._backColor)
        self._rect = self._text.get_rect()
        self.setPos()

    def draw(self):
        """
        displays the text on the pygame window
        """

        # Draw Text
        self._display.blit(self._text, self._rect)


##
# Button class (inherits Text)
#  a textbox but with  button-like display
class Button(Text):
    def __init__(self, display, text, position=(0, 0), location="center", fontSize=20, font="comicsansms"):
        """
        Initializes the button

        :param display: pygame window
        :param text: textbox text
        :param position: x and y position on the pygame window
        :param location: position to topleft, bottomright, center, etc
        :param fontSize: size of the text
        :param font: font of the text
        """

        GRAY = (100, 100, 100)
        BLACK = (0, 0, 0)
        super().__init__(display, text, position, location, fontSize, font, BLACK, GRAY)

    def draw(self):
        """
        draw the textbox on pygame window
        """

        LIGHT_GRAY = (150, 150, 150)
        DARK_GRAY = (50, 50, 50)
        size = 5
        x, y, w, h = self._rect

        # Draw Borders
        pygame.draw.line(self._display, LIGHT_GRAY, (x, y), (x + w, y), size)
        pygame.draw.line(self._display, LIGHT_GRAY, (x, y), (x, y + h), size)
        pygame.draw.line(self._display, DARK_GRAY, (x, y + h), (x + w, y + h), size)
        pygame.draw.line(self._display, DARK_GRAY, (x + w, y), (x + w, y + h), size)

        # Draw Button
        self._display.blit(self._text, self._rect)


##
# InputBox class
#  creates an interactive input box that can take keyboard inputs
class InputBox:
    def __init__(self, display, x, y, w, h, text=""):
        """
        Initialize the input box

        :param display: pygame window
        :param x: x position on the pygame
        :param y: y position on the pygame
        :param w: width of the textbox
        :param h: height of the textbox
        :param text: text in the textbox
        """
        BLACK = (0, 0, 0)

        self._display = display
        self._text = text
        self._rect = pygame.Rect(x, y, w, h)
        self._font = pygame.font.SysFont("comicsansms", 20)
        self._surface = self._font.render(self._text, True, BLACK)

        self.INACTIVE_COLOR = (106, 202, 154)
        self.ACTIVE_COLOR = (255, 255, 255)
        self._active = False

    def event(self, event):
        """
        Check and update if the input box is selected and inputs are given

        :param event: pygame event
        """

        # set active/inactive
        if event.type == pygame.MOUSEBUTTONDOWN:
            # clicked on input box
            if self._rect.collidepoint(event.pos):
                self._active = True
            else:
                self._active = False
        # Input entered
        elif event.type == pygame.KEYUP and self._active:
            # Backspace
            if event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            # Add input
            else:
                if len(self._text) < 5:
                    self._text += event.unicode

            self._surface = self._font.render(self._text, True, (0, 0, 0))

    def text(self):
        """
        Gets input text
        :return:
        """

        return self._text

    def draw(self):
        """
        Draws the enclosing rectangle on pygame window along with the text
        """

        if self._active:
            color = self.ACTIVE_COLOR
        else:
            color = self.INACTIVE_COLOR

        # Draw Border
        pygame.draw.rect(self._display, color, self._rect, 2)
        # Show text
        self._display.blit(self._surface, self._rect)

    def setCenter(self, position):
        """
        Set the enclosing rectangle center position

        :param position: x and y coordinates on the pygame
        """
        self._rect.center = position
