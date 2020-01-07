#!/usr/bin/env python3.5

import sys


def gro_print(date, track, pitch, dur, loud):
    print ('T'+str(date), 'V'+str(track), 'K'+str(pitch), 'P'+str(pitch), 'U'+str(dur), 'L'+str(loud))

filein = 'ann_quant.txt'
fileout = 'ann_quant.gro'

def parse_file(filein, fileout):
    with open(filein) as file:
        line = file.readline()
        while line:
            field = line.split('\t')
            date = field[0]
            track = 1
            label = field[2]
            if label == 'b\n':
                gro_print(field[0], 1, 101, 0.12, 100)
            elif label == 'db\n':
                gro_print(field[0], 1, 106, 0.15, 120)
            elif label == 'bW\n':
                gro_print(field[0], 1, 89, 0.12, 100)
            elif label == 'dbW\n':
                gro_print(field[0], 1, 95, 0.15, 120)
            line = file.readline()