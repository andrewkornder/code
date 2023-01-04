from PIL import Image
import cv2
import os


ascii = '$@B%8&WM#*o-_+~<>;:,"^`. '
scale = 255 / (len(ascii) - 1)


def get_image(path):
    return Image.open(path)


def image_to_ascii(image, compression=10):
    # TODO: font coloring for the image?

    w, h = image.size
    result = []
    for y in range(0, h, compression):
        result.append(' ' * 15)
        for x in range(0, w, compression):  # y then x so that the program scans in rows
            pixel_values = [sum(image.getpixel((x + a, y + b))) for a in range(compression) for b in range(compression)]
            # getting an average brightness for the square of pixels
            brightness = sum(pixel_values) / (compression ** 2 * 3)

            result[-1] += ascii[int(brightness / scale)]  # 25 is the amount of characters used in the ascii

    return '\n'.join(result)
    # return '\n'.join(' ' * 15 + ''.join(sum([sum(image.getpixel((x + a, y + b))) for a in range(compression) for b in range(compression)]) / (compression ** 2 * 3) for x in range(0, image.size[0], compression)) for y in range(0, image.size[1], compression))


def parse_video(path, folder='frames'):
    video = cv2.VideoCapture(path)
    success, frame = video.read()

    if not success:
        return False

    f = 0

    while success:
        cv2.imwrite(f'./{folder}/frame{f}.jpg', frame)
        success, frame = video.read()

        f += 1
        if not success:
            return f  # reached the end of the video, return total frames


def convert_all_frames(path, folder='frames', speed=1):
    frames = parse_video(path, folder)

    for frame in range(0, frames, speed):
        image = get_image(f'{folder}/frame{frame}.jpg')
        frame_ascii = image_to_ascii(image)

        # open('display.txt', 'w').write(frame_ascii)
        # os.system('start display.txt')
        print(f'\n\n{frame_ascii}\n\n')


if __name__ == '__main__':
    convert_all_frames('bad_apple.mkv', speed=int(input('speed?\n')))
