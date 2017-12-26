import subprocess
import time

class Notifier:
    '''
    Currently this is specialised for GNOME. Feel free to extend it.
    '''

    def __init__(self, interval=50, duration=10, verbose=False):
        '''
        interval - the time between fading of a notification and popup of a new
        duration - the time between popup and fading of a single notification
        verbose  - print each notification to std-out
        '''
        self.interval = interval
        self.duration = duration
        self.verbose  = verbose


    def notify(self, pair):
        '''
        pair is a dict containing at least the keys "head"/"body",
        e.g. a pair of vocabulary (e.g. English head, German body).
        The order of head and body affect the order of the notification,
        head will be the title, and body the content of the popup.
        '''
        if self.verbose:
            print(pair)
        subprocess.Popen(['notify-send', pair["head"], pair["body"]])

        time.sleep(self.interval + self.duration)


    def preprocessing(pair):
        # don't show grammatical information of the body
        # i.e. everything between curly braces
        pair["body"] = re.sub(r"\{*\}", "", pair["body"])
        return pair
