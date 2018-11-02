from wcwidth import wcswidth


def get_max_title_len(tracklist):
    """Returns the visual length of the visually longest track in a tracklist.
    """
    return max([wcswidth(x['title']) for x in tracklist])


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
        padding = max_len - wcswidth(track['title'])
        lines.append(track_fmt.format(track['number'], track['title'],
                                      ' ' * padding, minutes, seconds))
    return lines
