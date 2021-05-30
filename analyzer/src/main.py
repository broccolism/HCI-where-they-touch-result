#!/usr/bin/env python
import json
import datetime
import constants as const
from Classes.touch import Touch
import matplotlib.pyplot as plt


ALL_TOUCHES = []
MAX_WIDTH = 350
MAX_HEIGHT = 660


def init_data():
    global ALL_TOUCHES

    with open('../data/logs.json') as file:
        json_data = json.load(file)

        log_list = json_data['logs']
        for log_item in log_list:
            width = float(log_item['screenSize']['width'])
            touch_list = log_item['touches']

            user_touches = []
            for touch_item in touch_list:
                page = touch_item['path']
                target = touch_item['content']
                pos_x = float(touch_item['pageX'])
                pos_y = float(touch_item['pageY'])
                time_str = touch_item['createdAt'].split('.')[0].replace('T', " ").replace("Z", "")
                created_at = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                touch_model = Touch(width, pos_x, pos_y, page, target, created_at)
                user_touches.append(touch_model)

            ALL_TOUCHES.extend(user_touches)
    return


def get_logs_by_path(path):
    return_me = []
    for touch in ALL_TOUCHES:
        if touch.is_in_page(path):
            return_me.append(touch)

    return return_me


def get_touch_pos_list_by_target(logs, target_to_find):
    return_me = []

    for touch in logs:
        if touch.is_in_target(target_to_find):
            position = touch.get_position()
            return_me.append(position)

    return return_me


def show_pos_graph(data, title):
    X = []
    Y = []
    for (x, y) in data:
        X.append(x)
        Y.append(y)

    plt.scatter(X, Y)
    plt.xlim(0, MAX_WIDTH)
    plt.ylim(0, MAX_HEIGHT)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    init_data()

    # for path in const.PAGES:
    logs_in_path = get_logs_by_path('/keyboard#0')
    touch_pos_list = get_touch_pos_list_by_target(logs_in_path, 'ㅅ')
    show_pos_graph(touch_pos_list, 'ㅅ')
