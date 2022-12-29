class Rect:
    def __init__(self, right, left, top, bottom):
        self.square = abs((right - left) * (top - bottom))
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom
        self.string = self.coords_to_string()

    def printCoords(self):
        print(
            (self.left, self.bottom),
            (self.left, self.top),
            (self.right, self.top),
            (self.right, self.bottom),
            "square = ",
            self.square / 1000,
            "k",
        )

    def getCenter(self):
        right = (self.right - self.left) / 2
        left = right
        top = (self.top - self.bottom) / 2
        bottom = top
        return Rect(right, left, top, bottom)

    def is_inside(self, rect):
        if (
            (self.left > rect.left)
            and (self.right < rect.right)
            and (self.top < rect.top)
            and (self.bottom > rect.bottom)
        ):
            return True
        else:
            return False

    def coords_to_string(self):
        xs = [
            self.left,
            self.bottom,
            self.left,
            self.top,
            self.right,
            self.top,
            self.right,
            self.bottom,
        ]
        s = " ".join(str(x) for x in xs)
        return s
