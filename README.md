Offline Dict Trainer
====================

For people like me who have collected a lot of vocabulary on [dict.cc](www.dict.cc)
and want to actually learn it. This, I suppose, is best done offline with
regular reminders popping up every 5 minutes, or so.

So, I wrote a script showing vocables in adjustable frequencies. Looks like:
![popup preview](./demo.png)

How to run
----------
1. Go to dict.cc, login and export your vocabulary lists as tab-separated txt.
   Download these manually (automatic downloader does not work yet).
2. Open `config.json`, enter the paths to your source files (for now pointing
   to `./samples/*`) and edit the self explaining settings.
3. Run `python dict_trainer.py`. You'll need Python 3 or higher.

Features
--------
* load vocabulary data from multiple files
* shuffled but ranked by "last seen" date or "totally seen" counter
* adjustable duration of/between popups

Disclaimer
----------
* notifications currently only support GNOME
* the downloader does not yet work
