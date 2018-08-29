#!/usr/bin/python

import dbus
import os
import sys


try:
    bus = dbus.SessionBus()
    spotify = bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')

    if os.environ.get('BLOCK_BUTTON'):
        control_iface = dbus.Interface(spotify, 'org.mpris.MediaPlayer2.Player')
        if (os.environ['BLOCK_BUTTON'] == '1'):
            control_iface.Previous()
        elif (os.environ['BLOCK_BUTTON'] == '2'):
            control_iface.PlayPause()
        elif (os.environ['BLOCK_BUTTON'] == '3'):
            control_iface.Next()

    spotify_iface = dbus.Interface(spotify, 'org.freedesktop.DBus.Properties')
    status        = spotify_iface.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
    metadata      = spotify_iface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    artist = metadata['xesam:artist'][0]
    title  = metadata['xesam:title']

    if (sys.version_info > (3, 0)):
        status = str(status)
    else:
        status = status.encode('utf-8')

    if status == 'Playing':
        status_icon = u'\uf04b'
    elif status == 'Paused':
        status_icon = u'\uf04c'
    elif status == 'Stopped':
        status_icon = u'\uf04d'
    else:
        status_icon = u''

    if (sys.version_info > (3, 0)):
        print(status_icon + ' ' + str(artist) + ' - ' + str(title))
    else:
        print (status_icon + ' ' + artist + ' - ' + title).encode('utf-8')

    sys.exit(0)

except dbus.exceptions.DBusException:
    sys.exit(1)
