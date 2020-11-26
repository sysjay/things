import cv2


def timelapse():
    vid_path = "/home/jay/things/webcam/timelapse/"
    vid_file = "uloads-2020-11-26-+07:22:02.mp4"
    vid_lapse = vid_path + "tl.mp4"
    vid = cv2.VideoCapture(vid_path + vid_file)
    frames = []
    success = 1
    count = 0
    speed = 8
    vid.isOpened()
    if vid.isOpened():
        print("vid is opened")
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
        # print(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT) # 3, 4

        # or
        width = vid.get(3)  # float
        height = vid.get(4)  # float

        print('width, height:', width, height)

        while success:
            success, image = vid.read()
            if (count % speed == 0):
                frames.append(image)
            count += 1

        writer = cv2.VideoWriter(vid_lapse, cv2.VideoWriter_fourcc(*"MP4V"), 29.98, (1600, 1200))

        for x in frames:
            writer.write(x)
        writer.release()
