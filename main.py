from asyncio import run, get_event_loop, sleep
from os import getpid
from sqlite3 import connect

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager, \
    GlobalSystemMediaTransportControlsSessionPlaybackInfo as MediaPlaybackInfo, \
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as MediaPlaybackStatus

from lib.check_media import is_music


"""
This script is used to check if the current media is music.
It uses the Windows Media Control API to get the current media.
It then uses the Youtube API to check if the media is music.

If the media is music, the script will send the title, artist and album to the server.

The script will run in a loop and will check the media every 10 seconds.
"""


async def main() -> None:
    """
    The main function of the program.
    :returns: None
    """

    with connect("./db/database.sqlite") as con:
        with open("./db/build.sql", "r") as f:
            con.executescript(f.read())
        con.commit()

        cur = con.cursor()
        cur.execute("INSERT INTO pids (pid) VALUES (?)", (getpid(),))
        con.commit()

    while True:
        sessions = await MediaManager.request_async()

        for session in sessions.get_sessions():
            info: MediaPlaybackInfo = await session.try_get_media_properties_async()
            status: MediaPlaybackStatus = session.get_playback_info().playback_status

            if status == MediaPlaybackStatus.PAUSED:
                continue

            title: str = info.title
            artist: str = info.artist
            album: str = info.album_artist

            # Run is_music in a separate thread.
            loop = get_event_loop()
            _is_music: bool = await loop.run_in_executor(None, is_music, title, artist, album)

            if _is_music:
                print(f"Title: {title}\nArtist: {artist}\nAlbum: {album}\n")
        await sleep(10)


if __name__ == "__main__":
    run(main())
