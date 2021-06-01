class Key:
    def __init__(self, is_large, name, center_x, center_y):
        self.is_large = is_large
        self.name = name
        self.center_x = float(center_x)
        self.center_y = float(center_y)

    def __str__(self):
        type_str = "Large" if self.is_large else "Small"
        return f"{type_str} {self.name}: ({self.center_x}, {self.center_y})"

    def get_diff(self, pos, width):
        real_x = float(self.center_x) - (float(width) - 350) / 2
        real_y = self.center_y
        diff_x = pos[0] - real_x
        diff_y = pos[1] - real_y
        return (diff_x, diff_y)

    def is_large(self):
        return self.is_large

    def get_name(self):
        return self.name
