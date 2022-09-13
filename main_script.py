import cv2
import numpy as np
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont

class CircleCanvas:
    def __init__(self, frame, circle_size, inv=False, char=False, font_path=''):
        np.set_printoptions(threshold=sys.maxsize, linewidth=250)

        self.frame = frame
        self.in_shape = frame.shape
        self.circle_size = circle_size
        self.canvas = np.zeros_like(frame).astype('uint8')
        self.canvas = cv2.resize(self.canvas, None, fx=circle_size, fy=circle_size)
        self.inv = inv
        self.char = char
        self.out_letters = ''

        if font_path == '':
            self.font = ImageFont.load_default()
        else:
            self.font = ImageFont.truetype(font_path, 16)

        self.x, self.y = self.get_canvas_letters_shape()

        self.col2char = {0: ' ', 1: '.', 2: ':',
                         3: '-', 4: '=', 5: '+',
                         6: '*', 7: '#', 8: '%',
                         9: '&', 10: '@'}

    def return_canvas(self):
        if self.char:
            self.pick_char()
            return self.letters_to_canvas()
        else:
            if self.inv:
                return 255 - self.canvas
            return self.canvas

    def pos_converter(self, pos):
        return (pos[0] * self.circle_size, pos[1] * self.circle_size)

    def draw_circle(self):
        for x in range(self.in_shape[0]):
            for y in range(self.in_shape[1]):
                cv2.circle(self.canvas, self.pos_converter((y, x)), self.get_rad((x, y)), self.get_color((x, y)), -1)

    def get_rad(self, pos):
        return int(np.average((self.frame[pos[0]][pos[1]] / 255) * 10))

    def get_color(self, pos):
        if self.frame.shape[-1] == 3:
            color = self.frame[pos[0]][pos[1]]
            return color.tolist()
        else:
            return 255

    def pick_char(self):
        out = ''
        for x in range(self.in_shape[0]):
            for y in range(self.in_shape[1]):
                out += self.col2char[self.get_rad((x, y))]
            out += '\n'

        self.out_letters = out
        print(out)

    def letters_to_canvas(self):
        image = np.zeros((1920, 1080))
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)
        draw.multiline_text((10, -50), self.out_letters, font=self.font)
        image = np.array(image)[0:self.x, 0:self.y]
        return image.astype('uint8')*255

    def get_canvas_letters_shape(self):
        image = np.zeros((1920, 1080))
        out = ''
        for x in range(self.in_shape[0]):
            for y in range(self.in_shape[1]):
                out += '@'
            out += '\n'

        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)
        draw.multiline_text((10, 10), out, font=self.font)
        image = np.array(image)
        non_zero = np.argwhere(image)
        y, x = non_zero[-1]
        return  y + 10, x + 10

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', help='Pass path to the video',
                        type=str, nargs='?', const='', default='')
    parser.add_argument('--output', help="Choose file save destination",
                        type=str, nargs='?', const='', default='')
    parser.add_argument('--invert', help="Set True to invert the output colors",
                        type=str, nargs='?', const='False', default='False')
    parser.add_argument('--chars', help='Set True to output characterized image',
                        type=str, nargs='?', const='False', default='False')
    parser.add_argument('--font', help='Set desired output font',
                        type=str, nargs='?', const='', default='')
    parser.add_argument('--color', help='Set True if output should be 3-channel',
                        type=str, nargs='?', const='False', default='False')
    args = parser.parse_args()
    args.color = eval(args.color)
    args.invert = eval(args.invert)
    args.chars = eval(args.chars)
    args.font = args.font

    return args

def open_stream(path):
    if args.video != '':
        vid = cv2.VideoCapture(path)
    else:
        vid = cv2.VideoCapture(0)

    try:
        fps = int(vid.get(cv2.CAP_PROP_FPS))
    except: fps = 15

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return vid, fps, [width, height]

def create_output(path, fps, shape):
    return cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"MJPG"), fps, shape)

def multiply_channels(frame):
    return np.dstack([frame, frame, frame])


if __name__ == '__main__':

    args = parse_arguments()
    first_frame = True
    print("Press q in video window to stop")

    save_vid = False
    if args.output != '': save_vid = True

    SIZE = 10

    vid, fps, shape = open_stream(args.video)

    if save_vid:
        out_vid = create_output(args.output, fps, shape)

    while True:
        ret, frame = vid.read()

        # break at the end of file
        if not ret:
            print('Video ended')
            break

        frame = cv2.resize(frame, None, fx=1/SIZE, fy=1/SIZE)

        if not args.color:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        canvas = CircleCanvas(frame, SIZE, inv=args.invert, char=args.chars, font_path=args.font)

        if args.chars and first_frame:
            out_vid = create_output(args.output, fps, (canvas.y, canvas.x))
            first_frame = False

        canvas.draw_circle()
        out_frame = canvas.return_canvas()

        # save output video
        if save_vid:
            if out_frame.shape[-1] != 3:
                out_frame = multiply_channels(out_frame)

            out_vid.write(out_frame)

        cv2.imshow('frame', out_frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    if save_vid: out_vid.release()
    cv2.destroyAllWindows()
