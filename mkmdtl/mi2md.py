#!/usr/bin/env python3

import argparse
import json
import os.path
import subprocess
import sys
from datetime import timedelta
from mkmdtl import md


def get_mediainfo_dict(f):
    p = subprocess.run(['mediainfo', '--Output=JSON', f],
                       stdout=subprocess.PIPE)
    p.check_returncode()
    j = json.loads(p.stdout.decode('utf-8'))
    return j


def wrangle_mediainfo_dicts(mi_dicts):
    tracks = []
    for f in mi_dicts:
        for subt in mi_dicts[f]['media']['track']:
            if subt['@type'] != 'General':
                continue
            td = dict(number=int(subt['Track_Position']), title=subt['Title'],
                      length=timedelta(seconds=float(subt['Duration'])))
            tracks.append(td)
    return sorted(tracks, key=lambda t: t['number'])


def main():
    parser = argparse.ArgumentParser(description='Generate markdown table from'
                                                 ' file metadata')
    parser.add_argument('files', metavar='FILE', nargs='+')
    args = parser.parse_args()
    mi_dicts = dict()
    for f in args.files:
        if not os.path.isfile(f):
            if os.path.isdir(f):
                print("'{}' is a directory, skipping".format(f),
                      file=sys.stderr)
                continue
            else:
                print("No such file '{}'".format(f), file=sys.stderr)
                sys.exit(1)
        mi_dicts[f] = get_mediainfo_dict(f)
    if len(mi_dicts) == 0:
        print("No files to process", file=sys.stderr)
        sys.exit(1)
    tracks = wrangle_mediainfo_dicts(mi_dicts)
    print('\n'.join(md.build_table(tracks)))


if __name__ == '__main__':
    main()
