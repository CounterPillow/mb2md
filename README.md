mkmdtl
======

mkmdtl is a collection of utilities for generating GitHub-flavoured markdown
tables from track listing data.


Dependencies
------------

* Python 3
* requests
* wcwidth


Tools
-----

### mb2md

mb2md generates a markdown table from a MusicBrainz track listing.

#### Usage


```
mb2md MBID
```

### mi2md

mi2md generates a markdown table with track metadata obtained through the
`mediainfo` utility.

#### Usage

```
mi2md FILE [FILE...]
```

**Example:**
```
mi2md somealbum/*.flac
```


License
-------

This project is licensed under the zlib license. See the "LICENSE" file for the
full license text.
