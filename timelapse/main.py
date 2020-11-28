import timelapse
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    for x in "banana":
        print(x)

    timelapse.walk_dir("/home/jay/things/webcam/timelapse/tmp/trash/", "upload_20201127_14472965*.jpg")
    timelapse.run_this_test(timelapse.action1, f='harry', l='potter')
    timelapse.run_this_test(timelapse.action2, f='harry', l='potter')
#    timelapse.video_from_images("/home/jay/things/webcam/timelapse/tmp/trash/", "upload_2020112*_*.jpg",
#                                "/home/jay/things/webcam/timelapse/all_tl.avi")
    timelapse.timelapse("/home/jay/things/webcam/timelapse/", "all_tl.avi", "tl2.avi", speed=8)
