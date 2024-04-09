from django.test import TestCase
from pathlib import Path

# Create your tests here.
import os
from django.core.files import File
from .models import Artist, Album, Song, Playlist

parent_directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

folder_path = os.path.join(parent_directory_path, "test_data")


def remove_extra(list):
    if ".DS_Store" in list:
        list.remove(".DS_Store")
    return list


contents = remove_extra(os.listdir(folder_path))


def create_favorite_playlist():
    return Playlist.objects.create(name="my favorite")


def create_artist(name):
    return Artist.objects.create(name=name)


def create_album(name, artist):
    album = Album.objects.create(name=name)
    album.artist.add(artist)
    album.save()
    return album


def create_song(
    audio,
    album,
    artist,
):
    path = Path(audio)
    [_index, _name] = path.stem.split("_")
    song = Song.objects.create(name=_name, audio=None, track=_index, album=album)
    with path.open(mode="rb") as f:
        song.audio = File(f, name=path.name)
        song.save()
    song.artist.add(artist)
    song.save()
    return song


create_favorite_playlist()

for artist in contents:
    print(artist)
    artist_path = os.path.join(folder_path, artist)
    artist_obj = create_artist(artist)
    if os.path.isdir(artist_path):
        albums = remove_extra(os.listdir(artist_path))
        for album in albums:
            print(album)
            album_obj = create_album(name=album, artist=artist_obj)
            album_path = os.path.join(artist_path, album)
            songs = remove_extra(os.listdir(album_path))
            for song in songs:
                print(song)
                song_path = os.path.join(album_path, song)
                create_song(
                    audio=song_path,
                    album=album_obj,
                    artist=artist_obj,
                )
