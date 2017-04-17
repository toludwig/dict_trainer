import subprocess
import time


# TODO make threaded??

def notify(pair, interval=50, duration=10):
    '''
    Currently this is specialised for GNOME.

    pair is a dict containing at least the keys "head"/"body",
    e.g. a pair of vocabulary (e.g. English head, German body).
    The order of head and body affect the order of the notification,
    head will be the title, and body the content of the popup.

    Keywords:
    interval - the time between fading of the old and popup of the new notification
    duration - the time between popup and fading of a single notification
    '''
    print(pair) # TODO do this only in verbose mode
    subprocess.Popen(['notify-send', pair["head"], pair["body"]])

    time.sleep(interval + duration)

