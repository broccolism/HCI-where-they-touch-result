#!/usr/bin/python
# encoding: utf-8

import io
import json
import constants as const
from Classes.touch import Touch
from Classes.key import Key
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np
from collections import Counter

ALL_TOUCHES = []
ALL_TRIALS = {
    "카네이션": [],
    "호두마루": [],
    "당근": [],
    "스파게티": [],
    "후라이드치킨": [],
    "뱃지": []
}
LARGE_KEYS = []
SMALL_KEYS = []


def init_font():
    import matplotlib
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['font.family'] = "AppleGothic"


def init_data():
    global ALL_TOUCHES, ALL_TRIALS, LARGE_KEYS, SMALL_KEYS

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

            trials = log_item['tries']
            for trial in trials:
                count = trial['tries']
                word = trial['target']

                ALL_TRIALS[word].append(count)

    with io.open('../data/large_keyboard_pos.json', encoding='utf-8') as file:
        json_data = json.load(file)

        key_list = json_data['keys']

        for key in key_list:
            is_large = True
            name = key['name']
            center = key['center']
            center_x = center['x']
            center_y = center['y']
            key_model = Key(is_large, name, center_x, center_y)
            LARGE_KEYS.append(key_model)

    with io.open('../data/small_keyboard_pos.json', encoding='utf-8') as file:
        json_data = json.load(file)

        key_list = json_data['keys']

        for key in key_list:
            is_large = False
            name = key['name']
            center = key['center']
            center_x = center['x']
            center_y = center['y']
            key_model = Key(is_large, name, center_x, center_y)
            SMALL_KEYS.append(key_model)

    return


def get_logs_by_path(path):
    return_me = []
    for touch in ALL_TOUCHES:
        if touch.is_in_page(path):
            return_me.append(touch)

    return return_me


def get_touch_pos_list_by_target(logs, target_to_find):
    return_me = [touch.get_position() for touch in logs if touch.is_in_target(target_to_find)]
    return return_me, [const.GREEN for i in range(len(return_me))]
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
            show_pos_graph(touch_pos_list, colors, f"{path[1:]}-{char}")


def draw_all_touches():
    for (path, _, word) in const.TARGET_IN_PAGE:
        logs_in_path = get_logs_by_path(path)
        touch_pos_list, colors = get_touch_pos_in_page(logs_in_path)
        show_pos_graph(touch_pos_list, colors, word)


def get_average_diff():
    key_touches = [touch for touch in ALL_TOUCHES if len(touch.get_target()) == 1]
    x_diff_list_large = []
    y_diff_list_large = []
    x_diff_list_small = []
    y_diff_list_small = []
    for touch in key_touches:
        position = touch.get_position()
        target = touch.get_target()

        if touch.get_page() in const.LARGE_PAGES:
            target_key = [key for key in LARGE_KEYS if key.get_name() == target][0]
            x_diff_list_large.append(target_key.get_diff(position)[0])
            y_diff_list_large.append(target_key.get_diff(position)[1])
        else:
            target_key = [key for key in SMALL_KEYS if key.get_name() == target][0]
            x_diff_list_small.append(target_key.get_diff(position)[0])
            y_diff_list_small.append(target_key.get_diff(position)[1])

    x_diff_list_large = np.array(x_diff_list_large)
    y_diff_list_large = np.array(y_diff_list_large)
    x_diff_list_small = np.array(x_diff_list_small)
    y_diff_list_small = np.array(y_diff_list_small)
    return (x_diff_list_large, y_diff_list_large, x_diff_list_small, y_diff_list_small)


def show_boxplot(x, y):
    # the figure and axes
    fig, (ax1, ax2) = plt.subplots(ncols=2)

    # plotting the original data
    ax1.scatter(x, y, c='r', s=1)

    # doing the box plot
    boxplot_2d(x, y, ax=ax2, whis=1)

    plt.show()

# This code is from
# https://stackoverflow.com/questions/53849636/draw-a-double-box-plot-chart-2-axes-box-plot-box-plot-correlation-diagram-in


def boxplot_2d(x, y, ax, whis=1.5):
    xlimits = [np.percentile(x, q) for q in (25, 50, 75)]
    ylimits = [np.percentile(y, q) for q in (25, 50, 75)]
    plt.title(f"{([round(x, 2) for x in xlimits],[round(y, 2) for y in ylimits] )}")
    # the box
    box = Rectangle(
        (xlimits[0], ylimits[0]),
        (xlimits[2]-xlimits[0]),
        (ylimits[2]-ylimits[0]),
        ec='k',
        zorder=0
    )
    ax.add_patch(box)

    # the x median
    vline = Line2D(
        [xlimits[1], xlimits[1]], [ylimits[0], ylimits[2]],
        color='k',
        zorder=1
    )
    ax.add_line(vline)

    # the y median
    hline = Line2D(
        [xlimits[0], xlimits[2]], [ylimits[1], ylimits[1]],
        color='k',
        zorder=1
    )
    ax.add_line(hline)

    # the central point
    ax.plot([xlimits[1]], [ylimits[1]], color='k', marker='o')

    # the x-whisker
    # defined as in matplotlib boxplot:
    # As a float, determines the reach of the whiskers to the beyond the
    # first and third quartiles. In other words, where IQR is the
    # interquartile range (Q3-Q1), the upper whisker will extend to
    # last datum less than Q3 + whis*IQR). Similarly, the lower whisker
    # will extend to the first datum greater than Q1 - whis*IQR. Beyond
    # the whiskers, data are considered outliers and are plotted as
    # individual points. Set this to an unreasonably high value to force
    # the whiskers to show the min and max values. Alternatively, set this
    # to an ascending sequence of percentile (e.g., [5, 95]) to set the
    # whiskers at specific percentiles of the data. Finally, whis can
    # be the string 'range' to force the whiskers to the min and max of
    # the data.
    iqr = xlimits[2]-xlimits[0]

    # left
    left = np.min(x[x > xlimits[0]-whis*iqr])
    whisker_line = Line2D(
        [left, xlimits[0]], [ylimits[1], ylimits[1]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [left, left], [ylimits[0], ylimits[2]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_bar)

    # right
    right = np.max(x[x < xlimits[2]+whis*iqr])
    whisker_line = Line2D(
        [right, xlimits[2]], [ylimits[1], ylimits[1]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [right, right], [ylimits[0], ylimits[2]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_bar)

    # the y-whisker
    iqr = ylimits[2]-ylimits[0]

    # bottom
    bottom = np.min(y[y > ylimits[0]-whis*iqr])
    whisker_line = Line2D(
        [xlimits[1], xlimits[1]], [bottom, ylimits[0]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [xlimits[0], xlimits[2]], [bottom, bottom],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_bar)

    # top
    top = np.max(y[y < ylimits[2]+whis*iqr])
    whisker_line = Line2D(
        [xlimits[1], xlimits[1]], [top, ylimits[2]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [xlimits[0], xlimits[2]], [top, top],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_bar)

    # outliers
    mask = (x < left) | (x > right) | (y < bottom) | (y > top)
    ax.scatter(
        x[mask], y[mask],
        facecolors='none', edgecolors='k'
    )


def get_avg_trials():
    for key in ALL_TRIALS:
        trials = ALL_TRIALS[key]
        counter = Counter(trials)
        x = sorted([name for name in counter])
        y = [counter[name] for name in x]
        print(x, y)
        plt.plot(x, y)
        plt.title(key)

        file = plt.gcf()
        file.savefig(f'{const.RESULT_PATH}/{key}-graph.png', dpi=const.DPI)
        plt.show()
        print(f"Successfully saved {const.RESULT_PATH}/{key}-graph.png!")


if __name__ == "__main__":
    init_font()
    init_data()

    draw_all_touches()

    large_x, large_y, small_x, small_y = get_average_diff()
    show_boxplot(large_x, large_y)
    show_boxplot(small_x, small_y)

    get_avg_trials()
