#!/usr/bin/env python3

"""
Generates GitHub-flavoured markdown tables from track listings on MusicBrainz
releases.
"""


import argparse
from datetime import timedelta
from unicodedata import east_asian_width
import requests


MB_ENDPOINT_URL = 'musicbrainz.org/ws/2/'


def fetch_mb_release(mbid, user_agent='mb2md/1.0', https=True):
    """Fetches and returns the JSON recordings info for a specific MusicBrainz
    ID from the MusicBrainz API.

    :param mbid: MusicBrainz release ID
    :param user_agent: what user-agent header to send
    :param https: whether to use HTTPS
    :type mbid: string
    :type user_agent: string
    :type https: boolean
    :rtype: dictionary
    """
    schema = "https://" if https else "http://"
    headers = {'user-agent': user_agent}
    response = requests.get('{}{}release/{}?inc=recordings&fmt=json'
                            .format(schema, MB_ENDPOINT_URL, mbid),
                            headers=headers)
    return response.json()


def wrangle_track_list(release_dict):
    """Generates a list of {number, title, length} dictionaries of the tracks
    contained in the MusicBrainz API JSON dict response.

    :param release_dict: dictionary of a response from a MusicBrainz query
    :type release_dict: dictionary
    :rtype: list of {number, title, length} dictionaries
    """
    tracks = []
    for track in release_dict['media'][0]['tracks']:
        length = timedelta(milliseconds=track['recording']['length'])
        track_dict = dict(number=track['number'], title=track['title'],
                          length=length)
        tracks.append(track_dict)
    return tracks


def get_width_aware_len(string):
    """Returns the visual length of a string, i.e. counts double-width
    characters doubly.
    """
    length = 0
    for character in string:
        length += 2 if east_asian_width(character) == 'W' else 1
    return length


def get_max_title_len(tracklist):
    """Returns the visual length of the visually longest track in a tracklist.
    """
    return max([get_width_aware_len(x['title']) for x in tracklist])


def build_table(tracklist):
    """Takes a list of tracks in the form of {number, title, length} dicts,
    formats them into a GitHub-flavoured markdown table, and returns the lines
    of the formatted table as a list of strings, one string for each line.
    """
    lines = []
    max_len = get_max_title_len(tracklist)
    # "this style is fucking gay" -- Hamuko, 2018, not letting me align things
    header_fmt = '| No. | Title{} | Length|'
    sep_fmt = '| ---:|:-----{} | -----:|'
    track_fmt = '|  {:2} | {}{} | {:02}:{:02} |'
    lines.append(header_fmt.format(' ' * (max_len - len('Title'))))
    lines.append(sep_fmt.format('-' * (max_len - len('Title'))))
    for track in tracklist:
        minutes = track['length'].seconds // 60
        seconds = track['length'].seconds % 60
        padding = max_len - get_width_aware_len(track['title'])
        lines.append(track_fmt.format(track['number'], track['title'],
                                      ' ' * padding, minutes, seconds))
    return lines


def main():
    """Command line utility entry point.
    """
    parser = argparse.ArgumentParser(description='Generate markdown table from'
                                                 ' a MusicBrainz release id')
    parser.add_argument('mbid', metavar='MBID', help='MusicBrainz ID')

    args = parser.parse_args()
    mb_release_dict = fetch_mb_release(args.mbid)
    tracks = wrangle_track_list(mb_release_dict)
    print('\n'.join(build_table(tracks)))


if __name__ == '__main__':
    main()
