colors = {
    "reset": '\x0f',
    "white": '00',
    "black": '01',
    "blue":  '02',
    "green": '03',
    "red": '04',
    "brown": '05',
    "purple": '06',
    "orange": '07',
    "yellow": '08',
    "lightgreen": '09',
    "teal": '10',
    "lightcyan": '11',
    "lightblue": '12',
    "pink": '13',
    "gray": '14',
    "lightgray": '15'
}

def color(msg, c):
    return f"\x03{colors[c]}{msg}"

def bold(msg):
    return f"\x02{msg}"
