class user:
    def __init__(self, id, size, touches, answers,  tries):
        self.id = id
        self.size = size
        self.touches = touches
        self.answers = answers
        self.tries = tries

    def get_all_touches(self):
        return self.touches

    # def get_touch_position(self, page, content):
    #     touches = self.touches
    #     return

    def get_age(self):
        return self.answers.age

    def get_typping_type(self):
        return self.answers.type

    def get_gender(self):
        return self.answers.age

    def get_screen_width(self):
        return self.size.width

    def get_screen_height(self):
        return self.size.height

    def get_trial_count(self, target):
        return self.tries[target]
