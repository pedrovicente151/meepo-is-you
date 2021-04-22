"""
Assignment 1: Meepo is You

=== CSC148 Winter 2021 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains the Actor class and all its subclasses that represent
different types of elements in the game.
"""

import pygame
from typing import Tuple, Optional
from settings import *


class Actor:
    """
    A class that represents all the actors in the game. This class includes any
    attributes/methods that are common between the actors

    === Public Attributes ===
    x:
        x coordinate of this actor's location on the stage
    y:
        y coordinate of this actor's location on the stage
    image:
        the image of the actor

    === Private Attributes ===
    _is_stop:
        Flag to keep track of whether this object cannot be moved through
    _is_push:
        Flag to keep track of whether this object is pushable

    Representation Invariant: x,y must be greater or equal to 0
    """
    x: int
    y: int
    _is_stop: bool
    _is_push: bool
    image: pygame.Surface

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self._is_stop = False
        self._is_push = False
        self.image = pygame.Surface((TILESIZE, TILESIZE))

    def is_stop(self) -> bool:
        """
        Getter for _is_stop
        """
        return self._is_stop

    def is_push(self) -> bool:
        """
        Getter for _is_push
        """
        return self._is_push

    def copy(self) -> 'Actor':
        """
        Creates an identical copy of self and returns the new copy
        To be implemented in the subclasses
        """
        raise NotImplementedError

    def move(self, game_: 'Game', dx: int, dy: int) -> bool:
        """
        Function to move an Actor on the screen, to the direction
        indicated by dx and dy

        game_: the Game object
        dx: the offset in the x coordinate
        dx: the offset in the y coordinate

        Returns whether <self> actually moves.

        Note: this method is different from the "player_move" method in the
        Character class. A "player_move" is trigger by key pressed directly.
        This more general "move" can be a move caused by a push. In fact, this
        "move" method is used in the implementation of "player_move".

        Things to think about in this method:
        - The object cannot go off the screen boundaries
        - The move may push other objects to move as well.
        - The move might not happen because it's blocked by an unmovable object,
          in which case this method should return False
        - Recall how push works: you may push and move a line of multiple
          objects as long as the move is not blocked by something.
        """

        #  Doesn't Leave Map
        if self.x + dx == -1:
            return False

        lst_of_coordinates = []
        coordinates = [self.x, self.y]
        types = [Bush, Wall, Rock, Flag, Is, Subject, Attribute]

        #  Check all coordinates and append to List of Coordinates
        for item in game_.get_actors():
            if type(item) in types:
                new_item = game_.get_actor(item.x, item.y)
                item_coordinates = (new_item.x, new_item.y)
                lst_of_coordinates.append(item_coordinates)

        #  Keep track of Item ahead
        front_of_meepo = (coordinates[0] + dx, coordinates[1] + dy)

        #  Check Object in front of Meepo
        if front_of_meepo in lst_of_coordinates:
            block = game_.get_actor(front_of_meepo[0], front_of_meepo[1])
            #  Doesn't Pass Bushes
            if isinstance(block, Bush):
                return False
            #  Doesn't Move Non-Pushable Objects
            if type(block) in types:
                if not block._is_push:
                    return False
            block.move(game_, dx, dy)

        #  Move Meepo
        self.x += dx
        self.y += dy

        return True


class Character(Actor):
    """
    A class that represents non-Blocks/Bushes on the screen
    i.e., Meepo, Wall, Rock, Flag

    A Character could potentially be the player that is controlled by the
    key presses

    === Additional Private Attributes ===
    _is_player:
        Whether the character is the player, i.e., "<Character> isYou"
    _is_lose:
        Whether the rules contains "<Character> isLose"
    _is_win:
        Whether the rules contains "<Character> isWin"
    """
    _is_player: bool
    _is_lose: bool
    _is_win: bool

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes the Character
        """
        super().__init__(x, y)
        self._is_player = False
        self._is_lose = False
        self._is_win = False

    def is_win(self) -> bool:
        """
        Getter for _is_win
        """
        return self._is_win

    def is_lose(self) -> bool:
        """
        Getter for _is_lose
        """
        return self._is_lose

    def is_player(self) -> bool:
        """
        Getter for _is_player
        """
        return self._is_player

    def set_player(self) -> None:
        """
        Sets flag to make this actor the player.
        """
        self._is_player = True
        self._is_stop = False
        self._is_push = False

    def unset_player(self) -> None:
        """
        Unsets the flag to make the actor not the player.
        """
        self._is_player = False

    def set_stop(self) -> None:
        """
        Sets flag to make actor incapable of being moved through or pushed.
        """
        self._is_stop = True
        # self._is_push = False
        self._is_player = False

    def unset_stop(self) -> None:
        """
        Unsets the flag that prevents actor from being moved through or pushed.
        """
        self._is_stop = False

    def set_push(self) -> None:
        """
        Sets the flag that allows the actor to be pushable
        """
        self._is_push = True
        self._is_stop = False
        self._is_player = False

    def unset_push(self) -> None:
        """
        Unsets the flag that allows the actor to be pushable
        """
        self._is_push = False

    def set_win(self) -> None:
        """
        Sets this actor to be the win Condition.
        """
        self._is_win = True
        self._is_lose = False

    def unset_win(self) -> None:
        """
        Unsets this actor from being the win Condition.
        """
        self._is_win = False

    def set_lose(self) -> None:
        """
        Sets this flag to be the lose condition.
        """
        self._is_lose = True
        self._is_win = False

    def unset_lose(self) -> None:
        """
        Unsets this flag from being the lose condition.
        """
        self._is_lose = False

    def copy_flags(self, other: "Character") -> None:
        """
        Copy the boolean flags to the <other> object
        This is a helper method that should be used by the copy methods
        implemented in the subclasses.
        """
        other._is_player = self._is_player
        other._is_push = self._is_push
        other._is_stop = self._is_stop
        other._is_lose = self._is_lose
        other._is_win = self._is_win

    def copy(self) -> 'Character':
        """
        Returns a copy of this object itself.
        Need to be implemented in the subclasses
        """
        raise NotImplementedError

    def handle_key_press(self, game_: 'Game') -> Tuple[int, int]:
        """
        Process the key press input and
        return (dx, dy), the offsets on the x and y directions.
        """
        key_pressed = game_.keys_pressed
        dx, dy = 0, 0
        if key_pressed[pygame.K_LEFT]:
            dx -= 1
        elif key_pressed[pygame.K_RIGHT]:
            dx += 1
        elif key_pressed[pygame.K_UP]:
            dy -= 1
        elif key_pressed[pygame.K_DOWN]:
            dy += 1
        return dx, dy

    def player_move(self, game_: 'Game') -> bool:
        """
        Detects input from the keyboard and moves the Player on the game stage
        based on directional key presses.

        Also, after the move, check if we have won or lost the game,
        and call the win() and lose() methods in Game accordingly
        """
        dx, dy = self.handle_key_press(game_)
        if dx == 0 and dy == 0:
            return False
        return self.move(game_, dx, dy)


class Meepo(Character):
    """
    Class representing Ms. Meepo in the game.

    Meepo is a special Character because we want to change her image as
    she moves in different directions. We also want to see the movement of
    her "arms" as she moves.

    === Additional Public Attributes ===
    walk_right:
        Image for walking right
    walk_left:
        Image for walking left
    walk_up:
        Image for walking up
    walk_down:
        Image for walking down
    """
    walk_left: list
    walk_right: list
    walk_down: list
    walk_up: list

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes the Meepo Class
        Load the images for displaying Ms. Meepo's movement.
        """
        super().__init__(x, y)

        # Add motion images
        self.walk_right = [load_image(PLAYER_SPRITE_R1),
                           load_image(PLAYER_SPRITE_R2)]
        self.walk_left = [
            pygame.transform.flip(load_image(PLAYER_SPRITE_R1), True, False),
            pygame.transform.flip(load_image(PLAYER_SPRITE_R2), True, False)
        ]
        self.walk_up = [load_image(PLAYER_SPRITE_U1),
                        load_image(PLAYER_SPRITE_U2)]
        self.walk_down = [load_image(PLAYER_SPRITE_B1),
                          load_image(PLAYER_SPRITE_B2)]
        self.image = self.walk_down[1]

    def copy(self) -> 'Actor':
        """
        Creates an identical copy of self and returns the new copy
        To be implemented in the subclasses
        """
        return Meepo(self.x, self.y)

    def handle_key_press(self, game_: 'Game') -> Tuple[int, int]:
        """
        Overriding the same method in the base class, adding the modification
        of the image depending on the direction of the move.
        """
        key_pressed = game_.keys_pressed
        dx, dy = 0, 0

        #  Left
        if key_pressed[pygame.K_LEFT]:
            dx -= 1
            if self.image == self.walk_left[0]:
                self.image = self.walk_left[1]
            else:
                self.image = self.walk_left[0]
        #  Right
        elif key_pressed[pygame.K_RIGHT]:
            dx += 1
            if self.image == self.walk_right[0]:
                self.image = self.walk_right[1]
            else:
                self.image = self.walk_right[0]
        #  Up
        elif key_pressed[pygame.K_UP]:
            dy -= 1
            if self.image == self.walk_up[0]:
                self.image = self.walk_up[1]
            else:
                self.image = self.walk_up[0]
        #  Down
        elif key_pressed[pygame.K_DOWN]:
            dy += 1
            if self.image == self.walk_down[0]:
                self.image = self.walk_down[1]
            else:
                self.image = self.walk_down[0]

        return dx, dy


class Wall(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = load_image(WALL_SPRITE)


class Rock(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = load_image(ROCK_SPRITE)


class Flag(Character):
    """
    Class representing movable objects in the game.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = load_image(FLAG_SPRITE)


class Bush(Actor):
    """
    Class representing the edges and unmovable objects in the game.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.image = load_image(BUSH_SPRITE)

        # Bush is always unmovable and cannot be moved through
        self._is_stop = True
        self._is_push = False

    def copy(self) -> 'Bush':
        """
        Returns a copy of the Bush object
        """
        return Bush(self.x, self.y)


class Block(Actor):
    """
    Class for words in the game such as
    "Meepo", "you", "is", "rock", "lose", "victor", "flag", "push", and "stop".

    Blocks are used for indicating rules in the game.

    ================
    Additional public attribute:
    word: the word on this block
    """
    word: str

    def __init__(self, x: int, y: int, word_: str) -> None:
        super().__init__(x, y)
        self.word = word_
        # Blocks are always pushable and cannot be moved through.
        self._is_push = True
        self._is_stop = True

    def copy(self) -> 'Block':
        """
        Creates an identical copy of self and returns the new copy.
        To be implemented in the subclasses
        """
        raise NotImplementedError


class Subject(Block):
    """
    Class representing the Subject blocks in the game, e.g.,
    "Meepo", "Wall", "Flag", "Rock" (see SUBJECTS in settings.py)
    """

    def __init__(self, x: int, y: int, word_: str) -> None:
        super().__init__(x, y, word_)
        self.word = word_
        key = self.word.lower()
        if key in WORDS_SPRITES:
            self.image = load_image(WORDS_SPRITES[key])

    def copy(self) -> 'Block':
        """
        Creates an identical copy of self and returns the new copy.
        """
        return Subject(self.x, self.y, self.word)


class Attribute(Block):
    """
    Class representing the Attribute blocks in the game, e.g.,
    "Push", "Stop", "Victory", "Lose", "You"
    """

    def __init__(self, x: int, y: int, word_: str) -> None:
        super().__init__(x, y, word_)
        self.word = word_
        key = self.word.lower()
        if key in WORDS_SPRITES:
            self.image = load_image(WORDS_SPRITES[key])

    def copy(self) -> 'Block':
        """
        Creates an identical copy of self and returns the new copy.
        """
        return Attribute(self.x, self.y, self.word)


class Is(Block):
    """
    Class representing the Is blocks in the game.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, " is")  # Note the space in " is"
        self.image = load_image(IS_PURPLE)

    def copy(self) -> 'Block':
        """
        Creates an identical copy of self and returns the new copy.
        """
        return Is(self.x, self.y)

    def update(self, up: Optional[Actor],
               down: Optional[Actor],
               left: Optional[Actor],
               right: Optional[Actor]) -> Tuple[str, str]:
        """
        Detect horizontally and vertically if a new rule has been created in
        the format of a string "Subject isAttribute".

        up, down, left, right: the Actors that are adjacent (in the four
        directions) to this IS block

        Return a tuple of (horizontal, vertical) rules if a rule is detected
        in either direction, otherwise put an empty string at the tuple index.

        Some example return values:
        - ("Wall isPush", "Flag isWin)"
        - ("", "Rock isYou")
        - ("", "")

        Also, use IS images with different colours:
        - if no rule is detected on this IS block, use IS_PURPLE
        - if one rule is detected on this IS block, use IS_LIGHT_BLUE
        - if two rules are detected on this IS block, use IS_DARK_BLUE

        Note: We always read the rule left-to-right or up-to-down, e.g.,
        if it reads "Push is Wall" from left to right, or from bottom to top,
        it is NOT a valid rule.

        Hint: you may use the built-in method isinstance() to check the class
        type of an object.
        """
        lst_of_possibilities = []
        horizontal_condition = ""
        vertical_condition = ""

        # for object in SUBJECTS:
        #     for word in ATTRIBUTES:
        #         new_str = SUBJECTS[object] + " is" + ATTRIBUTES[word]
        #         lst_of_possibilities.append(new_str)

        if isinstance(left, Subject):
            noun = left.word
            if isinstance(right, Attribute):
                action = right.word

                horizontal_condition = noun + " is" + action


        if isinstance(up, Subject):
            noun = up.word
            if isinstance(down, Attribute):
                action = right.word

                vertical_condition = noun + " is" + action

        #  Set Colors for Is blocks
        if up is None or left is None:
            self.image = load_image(IS_PURPLE)

        if isinstance(up, Subject) or isinstance(down, Attribute):
            self.image = load_image(IS_LIGHT_BLUE)

        if isinstance(left, Subject) and isinstance(right, Attribute):
            self.image = load_image(IS_DARK_BLUE)

        if isinstance(left, Subject) or isinstance(right, Attribute):
            self.image = load_image(IS_LIGHT_BLUE)

        if isinstance(left, Subject) and isinstance(right, Attribute):
            self.image = load_image(IS_DARK_BLUE)

        return horizontal_condition, vertical_condition


def load_image(img_name: str, width: int = TILESIZE,
               height: int = TILESIZE) -> pygame.image:
    """
    Return a pygame img of the PNG img_name that has been scaled according
    to the given width and size
    """
    img = pygame.image.load(img_name).convert_alpha()
    return pygame.transform.scale(img, (width, height))


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['settings', 'stack', 'actor', 'pygame']
    })
