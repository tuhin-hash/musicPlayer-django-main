#!/usr/bin/env python
"""
Bulk import audio files into the Song model.
Usage:
  python import_songs.py path/to/folder

It will walk the folder, find audio files (.mp3,.wav,.ogg,.m4a,.flac),
optionally find an image with the same base name, and create Song objects.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicPlayer.settings')
django.setup()

from django.core.files import File
from App.models import Song

AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif'}


def import_songs(directory):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print('Not a directory:', directory)
        return

    created = 0
    for root, _, files in os.walk(directory):
        for fname in files:
            base, ext = os.path.splitext(fname)
            if ext.lower() not in AUDIO_EXTS:
                continue

            audio_path = os.path.join(root, fname)
            # try to find an image with the same base name
            img_path = None
            for ie in IMAGE_EXTS:
                candidate = os.path.join(root, base + ie)
                if os.path.exists(candidate):
                    img_path = candidate
                    break

            title = base.replace('_', ' ').replace('-', ' ')
            artist = 'Unknown'
            duration = '0:00'

            song = Song(title=title, artist=artist, duration=duration)

            # Save audio file into the FileField
            with open(audio_path, 'rb') as af:
                django_file = File(af)
                song.audio_file.save(fname, django_file, save=False)

                if img_path:
                    with open(img_path, 'rb') as imf:
                        song.image.save(os.path.basename(img_path), File(imf), save=False)

            song.save()
            created += 1
            print('Created:', song.title, '-', song.audio_file.name)

    print('Import complete. Created {} songs.'.format(created))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python import_songs.py path/to/folder')
        sys.exit(1)
    import_songs(sys.argv[1])
