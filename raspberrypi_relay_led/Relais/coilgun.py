from os import system, get_terminal_size, name as os_name
from sys import stdout, stdin
from time import sleep
from json import load, dump
# from RPi import GPIO

if os_name == "nt":
    from msvcrt import getwch as getwch_msvcrt

    getwch = getwch_msvcrt

else:
    from termios import tcgetattr, tcsetattr, TCSADRAIN
    from tty import setraw

    stdin_fileno = stdin.fileno()
    old_terminal_settings = tcgetattr(stdin_fileno)

    setraw(stdin.fileno())

    def getwch():
        return stdin.read(1)


system("")  # make ANSI escape sequence get processed on windows

# GPIO.setmode(GPIO.BCM)

ESC = "\x1b"

KEY_INDEX = 0 if os_name == "nt" else 1

KEYS_SPECIAL_TO_1 = (("\x00", "\xe0"), (ESC, ))
KEYS_SPECIAL_1 = ((), ("["))
KEYS_SPECIAL_TO_2 = ((), ("1"))
KEYS_SPECIAL_2 = ((), (";", "5"))

KEY_UP = ("H", "A")
KEY_DOWN = ("P", "B")
KEY_LEFT = ("K", "D")
KEY_RIGHT = ("M", "C")
KEY_CTRL_UP = ("\x8d", None)
KEY_CTRL_DOWN = ("\x91", None)
KEY_CTRL_LEFT = ("s", None)
KEY_CTRL_RIGHT = ("t", None)
KEY_POS1 = ("G", "H")
KEY_END = ("O", "F")
KEY_BACKSPACE = ("\x08", "\x7f")
KEY_ENTER = ("\r", "\r")
KEY_CTRL_C = ("\x03", "\x03")

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

PROFILE_POSTFIX = ".cgp"

title = "Coilgun"

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

    padding = (tty_width - len(title)) / 2
    padding_left = int(padding)
    padding_rigth = padding_left if padding_left == padding else padding_left + 1

    p(f"{' ' * padding_left}{title}{' ' * padding_rigth}")

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
    set_cursor_visible(False)
    clear()
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


def bound_time(time):
    if time > MAX_TIME_VALUE:
        return MAX_TIME_VALUE
    elif time < MIN_TIME_VALUE:
        return MIN_TIME_VALUE
    else:
        return time


def run_command():
    global time_values, title, command

    if command in ("q", "quit"):
        return True

    elif command in ("f", "fire"):
        fire()

    elif command.startswith(("lp ", "load-profile ")):

        name = " ".join(command.split(" ")[1:])

        try:
            with open(name + PROFILE_POSTFIX) as f:
                time_values = load(f)
                title = name

            draw_screen()
        except OSError as e:
            return str(e)

    elif command.startswith(("sp", "save-profile")):
        name = " ".join(command.split(" ")[1:])

        if name:
            title = name
            draw_titlebar()
        else:
            name = title

        try:
            with open(name + PROFILE_POSTFIX, "w") as f:
                dump(time_values, f)
        except OSError as e:
            return str(e)

    elif command.replace(".", "", 1).isdecimal():
        time_values[control_arrows_pos_value] = bound_time(float(command))

        draw_value(control_arrows_pos_value)

    elif command.startswith(("sat ", "set-all-times ")):
        val = command.split(" ")[1]

        if val.replace(".", "", 1).isdecimal():
            val = bound_time(float(val))

            for i in range(0, COIL_NUM * 2 - 1, 2):
                time_values[i] = val

                draw_value(i)
        else:
            return "Error - not a number"

    elif command.startswith(("sad ", "set-all-delays ")):
        val = command.split(" ")[1]

        if val.replace(".", "", 1).isdecimal():
            val = bound_time(float(val))

            for i in range(1, COIL_NUM * 2 - 1, 2):
                time_values[i] = val

                draw_value(i)
        else:
            return "Error - not a number"

    elif command.startswith(("sa ", "set-all ")):
        val = command.split(" ")[1]

        if val.replace(".", "", 1).isdecimal():
            val = bound_time(float(val))

            for i in range(COIL_NUM * 2 - 1):
                time_values[i] = val

                draw_value(i)
        else:
            return "Error - not a number"

    elif command in ("r", "redraw"):
        draw_screen()

    else:
        return "Error - unknown command"


def command_bar_cursor_move(step):
    global command_bar_cursor_pos

    command_bar_cursor_pos += step

    if command_bar_cursor_pos > len(command):
        command_bar_cursor_pos = len(command)
    elif command_bar_cursor_pos < 0:
        command_bar_cursor_pos = 0

    draw_command_bar()


def adjust_time(time_index, digit, direction):
    time_values[time_index] += 10**(-digit + 2) * direction
    time_values[time_index] = bound_time(time_values[time_index])

    draw_value(time_index)


def adjust_all_times(time_index, digit, direction):
    val = 10**(-digit + 2) * direction

    for i in range(time_index % 2, COIL_NUM * 2 - 1, 2):
        time_values[i] += val
        time_values[i] = bound_time(time_values[i])

        draw_value(i)


def command_insert_key(key):
    global command

    if command_bar_cursor_pos == 0:
        command += key
    else:
        command = command[:-command_bar_cursor_pos] + key + command[-command_bar_cursor_pos:]

    draw_command_bar()


def key_pressed_up():
    if command_bar_active:
        pass

    else:
        adjust_time(control_arrows_pos_value, control_arrows_pos_digit, 1)


def key_pressed_down():
    if command_bar_active:
        pass

    else:
        adjust_time(control_arrows_pos_value, control_arrows_pos_digit, -1)


def key_pressed_left():
    if command_bar_active:
        command_bar_cursor_move(1)

    else:
        global control_arrows_pos_value, control_arrows_pos_digit

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


def key_pressed_right():
    if command_bar_active:
        command_bar_cursor_move(-1)

    else:
        global control_arrows_pos_value, control_arrows_pos_digit

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


def key_pressed_ctrl_up():
    if command_bar_active:
        pass
    else:
        adjust_all_times(control_arrows_pos_value, control_arrows_pos_digit, 1)


def key_pressed_ctrl_down():
    if command_bar_active:
        pass
    else:
        adjust_all_times(control_arrows_pos_value, control_arrows_pos_digit, -1)


def key_pressed_ctrl_left():
    if command_bar_active:
        pass
    else:
        global control_arrows_pos_value

        draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, False)

        if control_arrows_pos_value == 0:
            control_arrows_pos_value = COIL_NUM * 2 - 2
        else:
            control_arrows_pos_value -= 1

        draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)


def key_pressed_ctrl_right():
    if command_bar_active:
        pass
    else:
        global control_arrows_pos_value

        draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, False)

        if control_arrows_pos_value == COIL_NUM * 2 - 2:
            control_arrows_pos_value = 0
        else:
            control_arrows_pos_value += 1

        draw_control_arrows(control_arrows_pos_value, control_arrows_pos_digit, True)


def key_pressed_pos1():
    if command_bar_active:
        global command_bar_cursor_pos

        command_bar_cursor_pos = len(command)
        draw_command_bar()


def key_pressed_end():
    if command_bar_active:
        global command_bar_cursor_pos

        command_bar_cursor_pos = 0
        draw_command_bar()


def key_pressed_esc():
    global command, command_bar_active

    if command_bar_active:

        command_bar_active = False
        command = ""
        draw_command_bar()


def key_pressed_backspace():
    if command_bar_active:
        global command

        if command_bar_cursor_pos == 0:
            command = command[:-1]

        else:
            command = command[:-(command_bar_cursor_pos + 1)] + command[-command_bar_cursor_pos:]

        draw_command_bar()


def key_pressed_enter():
    global command, command_bar_active

    if command_bar_active:

        exec_return = run_command()

        if exec_return is True:
            return True

        elif exec_return is None:
            command = ""

        else:
            command = " " + exec_return

        command_bar_active = False
        draw_command_bar()
        command = ""


draw_screen()

special_key_comming = 0

while True:
    key = getwch()

    if special_key_comming == 0:
        if key in KEYS_SPECIAL_TO_1[KEY_INDEX]:
            special_key_comming = 1

            continue

        if command_bar_active:
            if key == ESC:
                key_pressed_esc()

            elif key == KEY_BACKSPACE[KEY_INDEX]:
                key_pressed_backspace()

            elif key == KEY_ENTER[KEY_INDEX]:
                exit_now = key_pressed_enter()

                if exit_now:
                    break

            else:
                command_insert_key(key)

        else:
            if key == "q" or key == KEY_CTRL_C[KEY_INDEX]:
                break

            elif key == "f":
                fire()

            elif key == "r":
                draw_screen()

            elif key == ":":
                command_bar_active = True
                draw_command_bar()

            # else:
            #     print("normal: ", bytes(key, "unicode_escape"))

    if special_key_comming == 1:
        if key in KEYS_SPECIAL_1[KEY_INDEX]:
            continue

        elif key in KEYS_SPECIAL_TO_2[KEY_INDEX]:
            special_key_comming = 2

            continue

        if key == KEY_UP[KEY_INDEX]:
            key_pressed_up()

        elif key == KEY_DOWN[KEY_INDEX]:
            key_pressed_down()

        elif key == KEY_LEFT[KEY_INDEX]:
            key_pressed_left()

        elif key == KEY_RIGHT[KEY_INDEX]:
            key_pressed_right()

        elif key == KEY_CTRL_UP[KEY_INDEX]:
            key_pressed_ctrl_up()

        elif key == KEY_CTRL_DOWN[KEY_INDEX]:
            key_pressed_ctrl_down()

        elif key == KEY_CTRL_LEFT[KEY_INDEX]:
            key_pressed_ctrl_left()

        elif key == KEY_CTRL_RIGHT[KEY_INDEX]:
            key_pressed_ctrl_right()

        elif key == KEY_POS1[KEY_INDEX]:
            key_pressed_pos1()

        elif key == KEY_END[KEY_INDEX]:
            key_pressed_end()

        elif key == ESC:
            key_pressed_esc()

        # else:
        #     print("special 1: ", bytes(key, "unicode_escape"))

        special_key_comming = 0

    elif special_key_comming == 2:

        if key in KEYS_SPECIAL_2[KEY_INDEX]:
            continue

        if key == KEY_UP[KEY_INDEX]:
            key_pressed_ctrl_up()

        elif key == KEY_DOWN[KEY_INDEX]:
            key_pressed_ctrl_down()

        elif key == KEY_LEFT[KEY_INDEX]:
            key_pressed_ctrl_left()

        elif key == KEY_RIGHT[KEY_INDEX]:
            key_pressed_ctrl_right()

        # else:
        #     print("special 2: ", bytes(key, "unicode_escape"))

        special_key_comming = 0

set_cursor_pos(tty_height - 1, 0)

set_cursor_visible(True)

if os_name != "nt":
    tcsetattr(stdin_fileno, TCSADRAIN, old_terminal_settings)
