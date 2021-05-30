#!/usr/bin/env python
import json
import datetime
import constants as const
from Classes.touch import Touch


ALL_TOUCHES = []


def init_data():
    global ALL_TOUCHES
    frame = {'x', 'y'}

    with open('../data/logs.json') as file:
        json_data = json.load(file)

        log_list = json_data['logs']
        for log_item in log_list:
            touch_list = log_item['touches']

            user_touches = []
            for touch_item in touch_list:
                page = touch_item['path']
                target = touch_item['content']
                pos_x = touch_item['pageX']
                pos_y = touch_item['pageY']
                time_str = touch_item['createdAt'].split('.')[0].replace('T', " ").replace("Z", "")
                created_at = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                touch_model = Touch(pos_x, pos_y, page, target, created_at)
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


if __name__ == "__main__":
    init_data()

    for path in const.PAGES:
        logs_in_path = get_logs_by_path(path)
        touch_pos_list = get_touch_pos_list_by_target(logs_in_path, 'ㅅ')
