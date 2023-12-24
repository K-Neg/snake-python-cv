import cv2
import os


class Cell:
    def __init__(self, path: str, width: int, height: int) -> None:
        raw_image = cv2.imread(os.path.join("images", f"{path}.png"))

        self._image = cv2.resize(
            raw_image, (width, height), interpolation=cv2.INTER_NEAREST
        )

    @property
    def image(self):
        return self._image


class Up(Cell):
    def __init__(self, width, height) -> None:
        super().__init__("up", width, height)


class Down(Cell):
    def __init__(self, width, height) -> None:
        super().__init__("down", width, height)


class Left(Cell):
    def __init__(self, width, height) -> None:
        super().__init__("left", width, height)


class Right(Cell):
    def __init__(self, width, height) -> None:
        super().__init__("right", width, height)


class Blank(Cell):
    def __init__(self, width, height) -> None:
        super().__init__("blank", width, height)


class Void(Cell):
    def __init__(self, width, height) -> None:
        super().__init__("void", width, height)

    """
    [[[0 0 0]
    [0 0 0]]
    [[0 0 0]
    [0 0 0]]]"""


TILES = [Up, Down, Left, Right, Blank]
