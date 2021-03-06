#! /usr/bin/env python3

import csv
import re
import random
import optparse
import ruamel.yaml as yaml
from datetime import datetime

from notifier import Notifier
from downloader import DictDownloader

# all dict.cc-generated txt files are tab-separated,
# in order to not conflict with commas in the
# vocabulary entries
DICT_DELIMITER = "\t"

'''
Each vocable is composed of one head (foreign)
and a body (mother tongue part).
Information about the last and total visits is
stored for learning purposes.
'''
FIELDNAMES = ["head", "body", "last", "total"]

'''
Stores local paths of the files containing the vocabulary.
'''
sources = []

'''
Stores remote paths to exported voc lists of dict.cc in tab-separated format.
'''
remotes = []

'''
Holds the list of vocabulary, coming from all sources.
To have a reference to the source for later writing
the index of the file within sources is saved.
'''
vocs = []

'''
Config object, loaded from a yaml file.
'''
config = {}


def load_files():
    global sources, vocs

    for i, source in enumerate(sources):
        reader = csv.DictReader(open(source, 'r'),
                                restval=None, # if last and total are missing
                                fieldnames=FIELDNAMES,
                                delimiter=DICT_DELIMITER)
        temp = list(reader)
        for voc in temp:
            # ensure right types and fill missing values (as for fresh vocs)
            voc["total"] = int(voc["total"]) if not voc["total"] == None else 0
            if not voc["last"] == None:
                try:
                    voc["last"] = datetime.strptime(voc["last"], "%Y-%m-%d %H:%M:%S.%f")
                except ValueError: # in case microseconds are not given, try:
                    voc["last"] = datetime.strptime(voc["last"], "%Y-%m-%d %H:%M:%S")
            else:
                voc["last"] = datetime.min
            # add source index as a reference for later dumping
            voc["source"] = i
            vocs.append(voc)


def merge_downloaded_sources():
    '''
    NOTE that local and remote paths have to match in order!
    Remotes will be downloaded and new vocs will be included into
    the respective existing sources (they should be loaded before!).
    '''
    downloader = DictDownloader(config["account_data"])

    for i, remote in enumerate(config["remote_paths"]):
        newlist = downloader.download_list(remote)
        # parse lines as entries and split them at the (tab) separator
        entries = newlist.splitlines()
        entries = [tuple(entry.split(DICT_DELIMITER)) for entry in entries]

        # merge entries into the locally loaded vocs
        old_vocs = [(voc["head"], voc["body"]) for voc in vocs]
        for entry in entries:
            if not entry in old_vocs:
                new_voc = {"head": entry[0],
                           "body": entry[1],
                           "last": datetime.min,
                           "total": 0,
                           "source": i}
                vocs.append(new_voc)


def shuffle_vocs():
    global vocs
    random.shuffle(vocs)


def rank_vocs(by="total"):
    '''
    if by="last", the most recent seen vocs are ranked lowest
    if by="total", the most often seen vocs are ranked lowest
    '''
    global vocs
    vocs = sorted(vocs, key=lambda voc: voc[by])


def eval_voc(voc):
    '''
    Writes the current date timestamp in the "last" field and
    increases the value in "total".
    '''
    voc["last"] = datetime.now().replace(microsecond=0) # second precision
    voc["total"] += 1


def dump_all_vocs():
    global vocs

    for i, source in enumerate(sources):
        # filter the vocs by source file (encoded by index in "source")
        vocs_from_i = [voc for voc in vocs if voc["source"] == i]
        with open(source, "w") as f:
            writer = csv.DictWriter(f, FIELDNAMES,
                                    delimiter=DICT_DELIMITER,
                                    extrasaction="ignore") # ignore "source"
            writer.writerows(vocs_from_i)


def run_training(verbose=False, dump_frequency=10):
    '''
    Launches the training in a notify-eval-dump loop.
    In every dump_frequency cycle the whole vocabulary is dumped.
    '''
    global vocs, config
    notifier = Notifier(verbose=verbose, **config["notifications"])

    for i, voc in enumerate(vocs):
        notifier.notify(voc)
        eval_voc(voc)
        if i % dump_frequency == 0:
            dump_all_vocs()


def _parse_options():
    parser = optparse.OptionParser(usage="dict_trainer [options]")
    parser.add_option("-c", "--config",
                      action="store", type="string", dest="config_file",
                      metavar="FILE", default="config.yaml",
                      help="yaml config file including sources and settings")
    parser.add_option("-d", "--download",
                      action="store_true", dest="download", default=False,
                      help="download/sync sources from dict.cc")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="verbosely print pairs and statistics")
    return parser.parse_args()


if __name__ == '__main__':
    (options, _) = _parse_options()

    # read the config file specified in the options (default: in this dir)
    # which stores the file paths for the sources
    # as well as notifier and downloader preferences
    config = yaml.load(open(options.config_file), yaml.RoundTripLoader)
    sources = config["source_paths"]
    remotes = config["remote_paths"]

    load_files()
    if options.download:
        print("Downloading / Syncing sources from dict.cc ...")
        merge_downloaded_sources()
    shuffle_vocs() # shuffling before ranking: vary, but not destroy order
    rank_vocs()
    try:
        run_training(verbose=options.verbose)
    finally:
        dump_all_vocs() # finalization: dump to files in the end
