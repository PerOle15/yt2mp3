from pytube import YouTube, Playlist
from pydub import AudioSegment
import music_tag
import os
import os.path
from pathlib import Path

musicFolderUrl = 'C:/Users/olepe/Music'


def convertmp3(source: str, artist: str = ''):
    try:
        AudioSegment.from_file(source).export(
            source, format='mp3')
        file = music_tag.load_file(source)
        file['artist'] = artist
        file.save()
    except:
        print('trouble converting file and saving artist')


def youtube2mp3(url: str, filterlive: bool = False):
    # url input from user
    try:
        yt = YouTube(url,
                     use_oauth=True,
                     allow_oauth_cache=True
                     )
    except:
        print('Unable to access Video')
    else:
        # @ Extract audio with 160kbps quality from video
        video = yt.streams.filter(abr='160kbps').last()

        artist = yt.author
        outdir = f'{musicFolderUrl}/{artist}'

        title = video.title
        # filter out titles containing "live"
        if filterlive and ('(Live' in title):
            print(f'"{title}" skipped because it contains "Live"')
            return

        # Check if file already exists

        if (os.path.isfile(f'{outdir}\\{title}.mp3')):
            print(f'The file "{title}.mp3" already exists')
            return

        # @ Download the file
        try:
            out_file = video.download(output_path=outdir)
            base, ext = os.path.splitext(out_file)
            new_file = Path(f'{base}.mp3')
            os.rename(out_file, new_file)
            # @ Check success of download
            if new_file.exists():
                convertmp3(f'{base}.mp3', artist)
                print(
                    f'"{yt.title}" has been successfully downloaded and converted.')
            else:
                print(f'ERROR: "{yt.title}" could not be downloaded!')
        except:
            print(f'Unable to download "{yt.title}"')


def dlPlaylist(url: str, filterlive: bool = True):
    try:
        p = Playlist(url)
    except:
        print('Playlist could not be accessed')
    else:
        print(f'Downloading Playlist: {p.title}')
        for url in p.video_urls:
            youtube2mp3(url, filterlive)
        print(f'Downloaded Playlist: {p.title}')


out = 'C:\\Users\\olepe\\coding\\python\\yt2mp3\\mp3downloads'
yturl = ''

plurl = ''
dlPlaylist(plurl, True)
# youtube2mp3(yturl)
