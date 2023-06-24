from difflib import SequenceMatcher

from yt_dlp import YoutubeDL

_ytdl: YoutubeDL = YoutubeDL({
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch'
})


def is_music(title: str, artist: str, album: str | None = None) -> bool:
    """
    Return True if the given title, artist and album are music.

    :param title: The title of the media.
    :param artist: The artist of the media.
    :param album: The album of the media.

    :return: True if the given title, artist and album are music.
    """

    data = _ytdl.extract_info(f"{title} {artist} {album or ''}", download=False, process=True)

    try:
        info = data['entries'][0]
    except (KeyError, IndexError):
        return False
    del data

    if 'Music' in info['categories'] or any('music' == tag.lower() for tag in info['tags']):
        return True
    return SequenceMatcher(None, f"{title} {artist}", f"{info['title']} {info['uploader']}").ratio() > 0.75
