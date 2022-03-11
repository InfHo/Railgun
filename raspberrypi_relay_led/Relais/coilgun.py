from os import system, get_terminal_size, name as os_name
from sys import stdout
from msvcrt import getwch  # , kbhit
from time import sleep
# from RPi import GPIO

system("")  # make ANSI escape sequence get processed on windows

# GPIO.setmode(GPIO.BCM)

ESC = "\x1b"

KEY_SPECIAL = "\x00"

KEY_CTRL_C = "\x03"
KEY_BACKSPACE = "\x08"
KEY_ENTER = "\r"

KEY_UP = "H"
KEY_DOWN = "P"
KEY_LEFT = "K"
KEY_RIGHT = "M"
KEY_CTRL_UP = "\x8d"
KEY_CTRL_DOWN = "\x91"
KEY_CTRL_LEFT = "s"
KEY_CTRL_RIGHT = "t"
KEY_POS1 = "G"
KEY_END = "O"

LINE_H = "─"
LINE_V = "│"
CORNER_UL = "┌"
CORNER_UR = "┐"
CORNER_LL = "└"
CORNER_LR = "┘"
EXTRUSION_R = "├"
EXTRUSION_L = "┤"
EXTRUSION_U = "┴"
EXTRUSION_D = "┬"
ARROW_UP = "▲"
ARROW_DOWN = "▼"

coil_pins = [1, 2, 3, 4]
COIL_NUM = len(coil_pins)

CONTENT_MIN_WIDTH = 9 * COIL_NUM - 1
CONTENT_MIN_HEIGHT = 10

CONTENT_DELAY_OFFSET = 4

MAX_TIME_VALUE = 999.99
MIN_TIME_VALUE = 0
TIME_VALUE_DIGITS = 4

TITLE = "Coilgun"

content_x_start = 0
content_y_start = 0

cursor_x_pos = 0
cursor_y_pos = 0

control_arrows_pos_value = 0
control_arrows_pos_digit = 0

command = ""
command_bar_active = False
command_bar_cursor_pos = 0

time_values = [0 for _ in range(COIL_NUM * 2 - 1)]


def p(string):
    stdout.write(string)
    stdout.flush()


def clear():
    if os_name == "nt":
        system("cls")
    else:
        system("clear")


def update_tty_size():
    global tty_width, tty_height
    tty_width, tty_height = get_terminal_size()


tty_width = tty_height = 0
update_tty_size()


def set_cursor_pos(y, x):
    global cursor_x_pos, cursor_y_pos
    p(f"{ESC}[{y + 1};{x}H")
    cursor_x_pos, cursor_y_pos = x, y


def set_cursor_x_pos(x):
    global cursor_x_pos

    cursor_x_pos = x
    p(f"{ESC}[{x}G")


def set_cursor_y_pos(y):
    global cursor_y_pos

    cursor_y_pos = y
    p(f"{ESC}[{y + 1}d")


def move_cursor(y, x):
    set_cursor_pos(cursor_y_pos + y, cursor_x_pos + x)


def move_cursor_x(x):
    set_cursor_x_pos(cursor_x_pos + x)


def move_cursor_y(y):
    set_cursor_y_pos(cursor_y_pos + y)


def set_cursor_visible(visible):
    if visible:
        p(f"{ESC}[?25h")
    else:
        p(f"{ESC}[?25l")


def set_mode(mode):
    if isinstance(mode, int):
        p(f"{ESC}[{mode}m")
        return

    if mode == "normal":
        set_mode(0)
    elif mode == "negative":
        set_mode(7)
    elif mode == "positive":
        set_mode(27)

    return Exception("unsupported mode")


def draw_titlebar():
    set_cursor_pos(0, 0)
    set_mode("negative")

    padding = (tty_width - len(TITLE)) / 2
    padding_left = int(padding)
    padding_rigth = padding_left if padding_left == padding else padding_left + 1

    p(f"{' ' * padding_left}{TITLE}{' ' * padding_rigth}")

    set_mode("normal")


def draw_content():
    global content_x_start, content_y_start

    content_x_start = int((tty_width - CONTENT_MIN_WIDTH) / 2)
    content_y_start = int((tty_height - CONTENT_MIN_HEIGHT) / 2)

    set_cursor_pos(content_y_start, content_x_start)

    line = ""
    for i in range(COIL_NUM):
        line += f"    {i * 2}    "
    p(line)

    set_cursor_pos(content_y_start + 1, content_x_start)

    line = ""
    for i in range(COIL_NUM):
        line += f"{CORNER_UL}{LINE_H * 6}{CORNER_UR} "
    p(line)

    set_cursor_pos(content_y_start + 2, content_x_start)

    line = ""
    for i in range(COIL_NUM):
        line += f"{LINE_V}{' ' * 6}{LINE_V} "
    p(line)

    set_cursor_pos(content_y_start + 3, content_x_start)

    line = ""
    line += f"{LINE_V}{' ' * 6}{EXTRUSION_R}{EXTRUSION_D}"
    for i in range(COIL_NUM - 2):
        line += f"{EXTRUSION_L}{' ' * 6}{EXTRUSION_R}{EXTRUSION_D}"
    line += f"{EXTRUSION_L}{' ' * 6}{LINE_V}"
    p(line)

    set_cursor_pos(content_y_start + 4, content_x_start)

    line = ""
    for i in range(COIL_NUM):
        line += f"{LINE_V}{' ' * 6}{LINE_V * 2}"
    line = line[:-1]
    p(line)

    set_cursor_pos(content_y_start + 5, content_x_start)

    line = ""
    for i in range(COIL_NUM - 1):
        line += f"{CORNER_LL}{LINE_H * 6}{CORNER_LR}{i * 2 + 1}"
    line += f"{CORNER_LL}{LINE_H * 6}{CORNER_LR}"
    p(line)

    set_cursor_pos(content_y_start + 6, content_x_start + CONTENT_DELAY_OFFSET)

    line = ""
    for i in range(COIL_NUM - 1):
        line += f"{CORNER_UL}{LINE_H * 3}{EXTRUSION_U}{LINE_H * 2}{CORNER_UR} "
    p(line)

    set_cursor_pos(content_y_start + 7, content_x_start + CONTENT_DELAY_OFFSET)

    line = ""
    for i in range(COIL_NUM - 1):
        line += f"{LINE_V}{' ' * 6}{LINE_V} "
    p(line)

    set_cursor_pos(content_y_start + 8, content_x_start + CONTENT_DELAY_OFFSET)

    line = ""
    for i in range(COIL_NUM - 1):
        line += f"{LINE_V}{' ' * 6}{LINE_V} "
    p(line)

    set_cursor_pos(content_y_start + 9, content_x_start + CONTENT_DELAY_OFFSET)
    line = ""
    for i in range(COIL_NUM - 1):
        line += f"{LINE_V}{' ' * 6}{LINE_V} "
    p(line)

    set_cursor_pos(content_y_start + 10, content_x_start + CONTENT_DELAY_OFFSET)

    line = ""
    for i in range(COIL_NUM - 1):
        line += f"{CORNER_LL}{LINE_H * 6}{CORNER_LR} "
    p(line)


def draw_value(i):
    str_value = f"{time_values[i]:.2f}".zfill(6)

    if i % 2 == 0:  # coil
        set_cursor_pos(content_y_start + 3, content_x_start + 1 + int(i * 4.5))
        p(str_value)
    else:  # delay
        set_cursor_pos(content_y_start + 8, content_x_start + 1 + int(i * 4.5))
        p(str_value)


def draw_control_arrows(i, j, visible):
    if i % 2 == 0:  # coil
        set_cursor_pos(content_y_start + 2, content_x_start + 1 + int(i * 4.5) + j + (1 if j > 2 else 0))
        p(ARROW_UP if visible else " ")
        set_cursor_y_pos(content_y_start + 4)
        move_cursor_x(0)
        p(ARROW_DOWN if visible else " ")
    else:  # delay
        set_cursor_pos(content_y_start + 7, content_x_start + 1 + int(i * 4.5) + j + (1 if j > 2 else 0))
        p(ARROW_UP if visible else " ")
        set_cursor_y_pos(content_y_start + 9)
        move_cursor_x(0)
        p(ARROW_DOWN if visible else " ")


def draw_command_bar():
    set_cursor_visible(False)

    set_cursor_pos(tty_height - 1, 0)

    padding = (tty_width - 1 - len(command))

    p(f":{command}{' ' * padding}")

    set_cursor_x_pos(2 + len(command) - command_bar_cursor_pos)

    if command_bar_active:
        set_cursor_visible(True)


def draw_screen():
    update_tty_size()
    draw_titlebar()
    draw_content()

    for i in range(COIL_NUM * 2 - 1):
        draw_value(i)

    draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)

    draw_command_bar()


def fire():
    for i in range(COIL_NUM):
        # GPIO.output(coil_pins[i], GPIO.HIGH)
        sleep(time_values[i] / 1000)
        # GPIO.output(coil_pins[i], GPIO.LOW)
        if i < COIL_NUM - 1:
            sleep(time_values[i + 1] / 1000)


def run_command():
    if command == "q" or command == "quit":
        exit()


set_cursor_visible(False)

clear()

draw_screen()

special_key_comming = False

while True:
    key = getwch()

    if key == KEY_SPECIAL:
        special_key_comming = True
        continue

    if special_key_comming:
        special_key_comming = False

        if command_bar_active:
            if key == KEY_LEFT:
                command_bar_cursor_pos += 1

                if command_bar_cursor_pos > len(command):
                    command_bar_cursor_pos = len(command)

                draw_command_bar()
            elif key == KEY_RIGHT:
                command_bar_cursor_pos -= 1

                if command_bar_cursor_pos < 0:
                    command_bar_cursor_pos = 0

                draw_command_bar()
            elif key == KEY_POS1:
                command_bar_cursor_pos = len(command)
                draw_command_bar()
            elif key == KEY_END:
                command_bar_cursor_pos = 0
                draw_command_bar()
        else:
            if key == KEY_UP:
                time_values[control_arrows_pos_value] += 10**(-control_arrows_pos_digit + 2)

                if time_values[control_arrows_pos_value] > MAX_TIME_VALUE:
                    time_values[control_arrows_pos_value] = MAX_TIME_VALUE
                draw_value(control_arrows_pos_value)
            elif key == KEY_DOWN:
                time_values[control_arrows_pos_value] -= 10**(-control_arrows_pos_digit + 2)

                if time_values[control_arrows_pos_value] < MIN_TIME_VALUE:
                    time_values[control_arrows_pos_value] = MIN_TIME_VALUE
                draw_value(control_arrows_pos_value)
            elif key == KEY_LEFT:
                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, False)

                if control_arrows_pos_digit == 0:
                    if control_arrows_pos_value == 0:
                        control_arrows_pos_value = COIL_NUM * 2 - 2
                    else:
                        control_arrows_pos_value -= 1
                    control_arrows_pos_digit = TIME_VALUE_DIGITS
                else:
                    control_arrows_pos_digit -= 1

                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)
            elif key == KEY_RIGHT:
                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, False)

                if control_arrows_pos_digit == TIME_VALUE_DIGITS:
                    if control_arrows_pos_value == COIL_NUM * 2 - 2:
                        control_arrows_pos_value = 0
                    else:
                        control_arrows_pos_value += 1
                    control_arrows_pos_digit = 0
                else:
                    control_arrows_pos_digit += 1

                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)
            elif key == KEY_CTRL_UP:
                val = 10**(-control_arrows_pos_digit + 2)

                for i in range(control_arrows_pos_value % 2, COIL_NUM * 2 - 1, 2):
                    time_values[i] += val

                    if time_values[i] > MAX_TIME_VALUE:
                        time_values[i] = MAX_TIME_VALUE
                    draw_value(i)
            elif key == KEY_CTRL_DOWN:
                val = 10**(-control_arrows_pos_digit + 2)

                for i in range(control_arrows_pos_value % 2, COIL_NUM * 2 - 1, 2):
                    time_values[i] -= val

                    if time_values[i] < MIN_TIME_VALUE:
                        time_values[i] = MIN_TIME_VALUE
                    draw_value(i)
            elif key == KEY_CTRL_LEFT:
                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, False)

                if control_arrows_pos_value == 0:
                    control_arrows_pos_value = COIL_NUM * 2 - 2
                else:
                    control_arrows_pos_value -= 1

                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)
            elif key == KEY_CTRL_RIGHT:
                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, False)

                if control_arrows_pos_value == COIL_NUM * 2 - 2:
                    control_arrows_pos_value = 0
                else:
                    control_arrows_pos_value += 1

                draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)
            # else:
            #     print("special: ", bytes(key, "unicode_escape"))

    else:
        if command_bar_active:
            if key == ESC:
                command_bar_active = False
                command = ""
                draw_command_bar()
            elif key == KEY_BACKSPACE:
                if command_bar_cursor_pos == 0:
                    command = command[:-1]
                else:
                    command = command[:-(command_bar_cursor_pos + 1)] + command[-command_bar_cursor_pos:]
                draw_command_bar()
            elif key == KEY_ENTER:
                run_command()

                command = ""
                command_bar_active = False
                draw_command_bar()
            else:
                if command_bar_cursor_pos == 0:
                    command += key
                else:
                    command = command[:-command_bar_cursor_pos] + key + command[-command_bar_cursor_pos:]
                draw_command_bar()
        else:
            if key == "q" or key == KEY_CTRL_C:
                break
            elif key == "f":
                fire()
            elif key == ":":
                command_bar_active = True
                draw_command_bar()
            # else:
            #     print("normal: ", bytes(key, "unicode_escape"))

set_cursor_pos(tty_height - 1, 0)
