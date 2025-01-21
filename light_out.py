# light_out.py

import io
from turtle import back
import PySimpleGUI as pg
from PIL import Image


debug = False


map = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

unlock_level = [0]

clicks_num = 0

map_lib = [
    [0, 4, 14, 4, 0],
    [4, 10, 14, 10, 4],
    [2, 14, 21, 21, 8],
    [0, 23, 13, 26, 10],
    [25, 28, 19, 19, 27],
]

"""

map_lib = [
    [0, 4, 14, 4, 0],
    [0, 4, 14, 4, 0],
    [0, 4, 14, 4, 0],
    [0, 4, 14, 4, 0],
    [0, 4, 14, 4, 0],
]

"""

current_level = 1


def make_img(path: str, size: tuple):
    image = Image.open(path)
    image.thumbnail(size)
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    return bio.getvalue()


img_light_on = make_img("img\light_on.png", (40, 40))
img_light_off = make_img("img\light_off.png", (40, 40))


def update_map() -> bool:
    """update the whole map (size: 5x5); also test if the game is win"""
    win = True
    for x in range(5):
        for y in range(5):
            if map[y][x] == 0:
                main[f"-BUTTON{x}{y}-"].update(button_color="black")
                main[f"-BUTTON{x}{y}-"].update(image_data=img_light_off)
            else:
                main[f"-BUTTON{x}{y}-"].update(button_color="white")
                main[f"-BUTTON{x}{y}-"].update(image_data=img_light_on)
                win = False
    return win


def load_map(level: int) -> list:
    """load the map data from the library"""
    level -= 1
    load = list()
    for y in range(5):
        bin_y = str(bin(map_lib.copy()[level][y]))[2:]
        bin_y = "0" * (5 - len(bin_y)) + bin_y
        load.append([])
        for x in range(5):
            load[y].append(int(bin_y[x]))

    # print(load)
    return load


def click(position: list):
    position

    if map[position[1]][position[0]] == 1:
        map[position[1]][position[0]] = 0

    else:
        map[position[1]][position[0]] = 1

    for x_dis, y_dis in [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    ]:  # x displacement and y displacement (4 diractions: left down right up)
        x_fin = position[0] + x_dis  # x final
        y_fin = position[1] + y_dis  # y final
        if 0 <= x_fin <= 4 and 0 <= y_fin <= 4:
            if map[y_fin][x_fin] == 1:
                map[y_fin][x_fin] = 0
            else:
                map[y_fin][x_fin] = 1


map = load_map(level=1)
# adding 25buttons in to the style

layout = [
    [
        pg.Button(
            key=f"-BUTTON{x}{y}-",
            button_text="    ",
            button_color="black" if map[y][x] == 0 else "white",
            image_data=img_light_off if map[y][x] == 0 else img_light_on,
        )
        for x in range(5)
    ]
    for y in range(5)
]
layout.append(
    [pg.Text(text=f"Clicks: {clicks_num}", key="-CLICKS_NUM-", background_color="gray")]
)

frame_map = pg.Frame(title="map", layout=layout, background_color="gray")

del layout

# add 5 radio buttons
layout = [
    [
        pg.Radio(
            text=f"House {x+1}",
            key=f"-LEVEL{x+1}-",
            group_id="Level",
            enable_events=True,
            default=True if x == 0 else False,
            visible=True if x in unlock_level else False,
            background_color="gray",
        )
    ]
    for x in range(5)
]

layout.append(
    [pg.Button(button_text="Reset Level", key="-RESET-", button_color="gray")]
)
layout.append(
    [
        pg.Text(
            text="""Get stuck?\nTry to reset the level...""",
            visible=False,
            key="-STUCK-",
            background_color="gray",
        )
    ]
)

frame_setting = pg.Frame(
    title="setting",
    layout=layout,
    background_color="gray",
)
del layout
"""
layout = [
    [
        pg.
    ]
]
frame_tools = pg.Frame(title="Developmenter Tools", layout=layout)

"""


main = pg.Window(
    title="Light Out",
    layout=[
        [
            pg.Titlebar(
                title="Light Out",
                icon=make_img("img\home.png", (20, 20)),
                background_color="black",
            )
        ],
        [frame_map, frame_setting],
    ],
    background_color="gray",
)


while True:
    main_event, main_value = main.read()

    if main_event == pg.WIN_CLOSED:
        break

    if main_event == "-RESET-":
        map = load_map(current_level)
        update_map()
        clicks_num = 0
        main["-CLICKS_NUM-"].update(f"Clicks: {clicks_num}")
        main["-STUCK-"].update(visible=False)

    if debug:
        pg.Print("Events:")
        pg.Print(main_event)
        pg.Print("Values:")
        pg.Print(main_value)

    if main_event[:6] == "-LEVEL":
        if int(main_event[6]) != current_level:
            current_level = int(main_event[6])
            map = load_map(current_level)
            update_map()
            clicks_num = 0
            main["-CLICKS_NUM-"].update(f"Clicks: {clicks_num}")
            main["-STUCK-"].update(visible=False)

    if main_event[:7] == "-BUTTON":
        click([int(main_event[7]), int(main_event[8])])
        clicks_num += 1
        main["-CLICKS_NUM-"].update(f"Clicks: {clicks_num}")

        if update_map():
            # print("win")
            text = ""
            if len(unlock_level) < 5 and current_level == len(unlock_level):
                unlock_level.append(len(unlock_level))
                main[f"-LEVEL{len(unlock_level)}-"].update(visible=True)
                text = "You get it!"
                next_text = "Move To Next House"
            elif len(unlock_level) == 5 and current_level == len(unlock_level):
                text = "You finished all the challenge!"
                next_text = "Yah!"
            if text != "":
                hint_window = pg.Window(
                    title="Congratulation",
                    layout=[
                        [
                            pg.Titlebar(
                                title="Light Out",
                                icon=make_img("img\home.png", (20, 20)),
                                background_color="black",
                            )
                        ],
                        [
                            pg.Text(
                                text=f"{text}", size=(30, 2), background_color="gray"
                            )
                        ],
                        [
                            pg.Button(
                                button_text=next_text,
                                key="-NEXT-",
                                button_color="gray",
                            )
                        ],
                    ],
                    background_color="gray",
                )

                # disable old windows
                while True:
                    if (
                        hint_window.read()[0] == "-NEXT-"
                        or hint_window.read()[0] == pg.WIN_CLOSED
                    ):
                        hint_window.close()
                        break

    if clicks_num >= current_level * 3:
        main["-STUCK-"].update(visible=True)

main.close()
