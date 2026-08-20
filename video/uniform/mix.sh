#!/bin/sh
# $1 — уровень музыки в дБ
ffmpeg -hide_banner -loglevel error -y -i voice_cut.wav -i music.wav -filter_complex "\
[1:a]highpass=f=60,equalizer=f=280:width_type=o:width=1.7:g=-3.5,equalizer=f=3200:width_type=o:width=1.2:g=2.0,volume=$1dB[m];\
[m][0:a]sidechaincompress=threshold=0.030:ratio=8:attack=12:release=380:makeup=1:level_sc=1.0[md]" \
-map "[md]" -ar 48000 -ac 2 music_ducked.wav
