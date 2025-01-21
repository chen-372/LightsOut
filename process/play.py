import PySimpleGUI as pg
from matplotlib.ft2font import HORIZONTAL

window = pg.Window(
    title="test",
    layout=[
        [
            pg.Titlebar("Hello"),
        ],
        [
            pg.Slider((0, 1), orientation="h", disable_number_display=True),
        ],

    ],
)

while True:
    main_event, main_value = window.read()

    if main_event == pg.WIN_CLOSED:
        break


window.close()
