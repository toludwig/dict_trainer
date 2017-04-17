import csv
import json
import re
import random
import optparse
import datetime
from notifier import notify

# TODO include this in config
DICT_DELIMITER = "\t"

'''
Each vocable is composed of one head (forein)
and a body (mother tongue part).
Information about the last and total visits is
stored for learning purposes.
'''
FIELDNAMES = ["head", "body", "last", "total"]

'''
Stores filepaths of the files containing the vocabulary.
'''
infiles = []

'''
Holds the list of vocabulary, coming from all infiles.
To save a reference to the source for later writing
the index of the file within infiles is saved.
'''
data = []

'''
Config object, loaded from a json file.
'''
config = {}


def download_infiles():
    # TODO download dict.cc files
    pass


def preprocessing():
    # TODO remove duplicates

    # remove grammatical information of the body
    # i.e. everything that in curly braces
    for voc in data:
        voc["body"] = re.sub(r"\{*\}", "", voc["body"])


def load_files():
    global infiles, data

    for i, infile in enumerate(infiles):
        reader = csv.DictReader(open(infile, 'r'),
                                fieldnames=FIELDNAMES,
                                restval=0, # for empty "last"/"total"
                                delimiter=DICT_DELIMITER)
        vocs = list(reader)
        for voc in vocs:
            voc.update({"source": i})
            data.append(voc)


def shuffle_vocs():
    # TODO different policies?
    # - shuffled over all data vs. files seperately
    global data
    random.shuffle(data)


def rank_vocs(by="total"):
    '''
    if by="last", the most recent seen vocs are ranked lowest
    if by="total", the most often seen vocs are ranked lowest
    '''
    # TODO sort by datetime!!!
    global data
    sorted(data, key=lambda voc: voc[by])


def eval_voc(voc):
    '''
    Writes the current date timestamp in the "last" field and
    increases the value in "total".
    '''
    voc["last"] = datetime.datetime.now()
    voc["total"] += 1


def dump_all_vocs():
    global data

    for i, infile in enumerate(infiles):
        # filter the vocs by source file (encoded by index in "source")
        vocs_from_i = [voc for voc in data if voc["source"] == i]
        with open(infile, 'w') as f:
            writer = csv.DictWriter(f, FIELDNAMES,
                                    delimiter=DICT_DELIMITER,
                                    extrasaction="ignore") # ignore "source"
            writer.writerows(vocs_from_i)


def run_training(dump_frequency=10):
    '''
    Launches the training in a notify-eval-dump loop.
    In every dump_frequency cycle the whole vocabulary is dumped.
    '''
    global data, config
    for i, voc in enumerate(data):
        notify(voc, **config["notifications"])
        eval_voc(voc)
        if i % dump_frequency == 0:
            dump_all_vocs()


if __name__ == '__main__':
    # TODO option parser
    # - config-editor (add/remove files, set interval)
    # - verbose mode (print pairs, ...)
    # - download from dict.cc
    ### optparse

    # read the config file within this directory
    # which stores the file paths for the infiles
    config = json.load(open("config.json"))
    infiles = config["infile_paths"]

    load_files()
    # preprocessing()
    shuffle_vocs()
    rank_vocs()
    run_training()

    # TODO finalization: dump to files in the end
