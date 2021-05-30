#!/usr/bin/python
# encoding: utf-8

import io
import json
import constants as const
from Classes.touch import Touch
import matplotlib.pyplot as plt
import numpy as np

ALL_TOUCHES = []


def init_font():
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf8')

    import matplotlib
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['font.family'] = "AppleGothic"


def init_data():
    global ALL_TOUCHES

    with io.open('../data/logs.json', encoding='utf-8') as file:
        json_data = json.load(file)

        log_list = json_data['logs']

        for log_item in log_list:
            width = log_item['screenSize']['width']
            touch_list = log_item['touches']

            user_touches = []
            for touch_item in touch_list:
                page = touch_item['path']
                target = touch_item['content']
                pos_x = touch_item['pageX']
                pos_y = touch_item['pageY']
                time_str = touch_item['createdAt'].split('.')[0].replace('T', " ").replace("Z", "")
                touch_model = Touch(width, pos_x, pos_y, page, target, time_str)
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
    return_me = [touch.get_position() for touch in logs if touch.is_in_target(target_to_find)]
    return return_me
    # for touch in logs:
    #     if touch.is_in_target(target_to_find):
    #         position = touch.get_position()
    #         return_me.append(position)

    # return return_me


def get_touch_pos_in_page(logs):
    return_me = [touch.get_position() for touch in logs]

    page = logs[0].get_page()
    page_goal = [target_in_page[1] for target_in_page in const.TARGET_IN_PAGE if target_in_page[0] == page][0]
    colors = []
    for touch in logs:
        target = touch.get_target()
        if target in page_goal:
            colors.append(const.GREEN)
        else:
            colors.append(const.RED)

    return return_me, colors


def show_pos_graph(data, colors, title):
    X = [i for i in range(const.MAX_WIDTH)] * 2
    Y = [const.KEYBOARD_BOTTOM for i in range(const.MAX_WIDTH)] + [const.KEYBOARD_TOP for i in range(const.MAX_WIDTH)]

    for (x, y) in data:
        X.append(x)
        Y.append(y)

    C = [const.BLACK for i in range(2 * const.MAX_WIDTH)]
    C.extend(colors)

    plt.figure(figsize=(const.MAX_WIDTH/const.DPI, const.MAX_HEIGHT/const.DPI))
    plt.scatter(X, Y, c=C, s=3/const.DPI)
    plt.xlim(0, const.MAX_WIDTH)
    plt.ylim(const.MAX_HEIGHT, 0)
    plt.title(title)

    file = plt.gcf()
    file.savefig(f'{const.RESULT_PATH}/{title}.png', dpi=const.DPI)
    plt.show()
    print(f"Successfully saved {title}.png!")


def draw_correct_touches():
    for (path, target, _) in const.TARGET_IN_PAGE:
        for char in target:
            logs_in_path = get_logs_by_path(path)
            touch_pos_list, colors = get_touch_pos_list_by_target(logs_in_path, char)
            show_pos_graph(touch_pos_list, colors, f"{path}/{char}")


def draw_all_touches():
    for (path, _, word) in const.TARGET_IN_PAGE:
        logs_in_path = get_logs_by_path(path)
        touch_pos_list, colors = get_touch_pos_in_page(logs_in_path)
        show_pos_graph(touch_pos_list, colors, word)


if __name__ == "__main__":
    init_font()
    init_data()

    # draw_correct_touches()
    draw_all_touches()
