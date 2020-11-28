import cv2
import os
from os.path import isfile, join
import fnmatch
import glob
import numpy as np


def action1(**args):
    print('action1'),
    print(args)


def action2(**args):
    print('action2')
    print(args)
    f = args['f']
    l = args['l']
    print("F=", f)
    print("L=", l)


def run_this_test(function_name, **args):
    print("run_this_test")
    print(args)
    for i in args:
        print("args" + i)
    function_name(f=args['l'], l=args['f'])


def walk_dir(path, file):
    files = [f for f in os.listdir(path)]
    files.sort()
    for f in files:
        match = fnmatch.fnmatch(f, file)
        if match:
            print("Filename: " + f)


def list_dir(path, file):
    with os.scandir(path) as it:
        for entry in it:
            if fnmatch.fnmatch(entry.name, file):
                print(entry.name)


def video_from_images(vid_path, vid_file, outfile, fourcc='DIVX'):
    frames_per_second = 29.98
    frame_size = (1600, 1200)

    out = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*fourcc), frames_per_second, frame_size)

    files = glob.glob(vid_path+vid_file)
    percent_done = 0
    print("files:" + str(len(files)))
    for filename in files:
#        print("filename = " + filename)
        percent_done += 1
        print(percent_done, len(files), percent_done/len(files))
        img = cv2.imread(filename)
        out.write(img)

    out.release()


def timelapse(vid_path, vid_file, outfile, speed=8):
    vid_lapse = vid_path + outfile
    vid = cv2.VideoCapture(vid_path + vid_file)
    frames = []
    success = 1
    count = 0
    vid.isOpened()
    if vid.isOpened():
        print("vid is opened")
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
        # print(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT) # 3, 4

        # or
        width = vid.get(3)  # float
        height = vid.get(4)  # float
        codec = int(vid.get(cv2.CAP_PROP_FOURCC))
        fourcc_codec = chr(codec & 0xff) + chr((codec >> 8) & 0xff) + chr((codec >> 16) & 0xff) + chr(
            (codec >> 24) & 0xff)
        print('width, height:', width, height, "code =  ", fourcc_codec)

        while success:
            success, image = vid.read()
            if count % speed == 0:
                frames.append(image)
            count += 1

        writer = cv2.VideoWriter(vid_lapse, cv2.VideoWriter_fourcc(*"DIVX"), 29.98, (1600, 1200))

        for x in frames:
            writer.write(x)
        writer.release()
