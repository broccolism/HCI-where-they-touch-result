# encoding=utf8
class Touch:
    def __init__(self, width, x, y, page, target, created_at):
        self.x = x - (width - 350) / 2
        self.y = y
        self.page = page
        self.target = target
        self.created_at = created_at

    def __str__(self):
        return 'To touch {page}/{target}: ({x}, {y})'.format(page=self.page, target=self.target, x=self.x, y=self.y)

    def get_position(self):
        return (self.x, self.y)

    def get_page(self):
        return self.page

    def get_target(self):
        return self.target

    def is_in_page(self, page):
        return self.page == page

    def is_in_target(self, target):
        return self.target == target
