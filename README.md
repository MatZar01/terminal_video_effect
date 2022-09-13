![Project usage](https://i.ibb.co/Fx1J85M/Zrzut-ekranu-2022-09-13-o-19-59-56.png "Use example")

# Terminal Video Effect

>**This small program will allow you to give binary, terminal and other effects to your video or webcam stream.**

## Table of contents
* [General info](#general-info)
* [Dependencies](#dependencies)
* [Using TVE](#using-tve)
* [Use examples](#use-examples)

## General info

This small project was created purely for entertainment purposes, to see how well a primitive display (such as a binary or terminal) can accurately reproduce an image recorded with an RGB camera. At the same time, it is not a method of video compression, although with this method the recording can be transmitted using much less data, and displayed directly on the terminal.

This project was tested on MacOS and Linux, but if you'll carefully mind your backslash, you should run it also on Windows.

Also check out [my site](https://www.iitis.pl/pl/person/mzarski) at the institute of the Polish Academy of Sciences, where I work ;-)

## Dependencies

I developed TVE  using Python 3.8. It should run on older versions too. Packages needed: 


* Numpy
* OpenCV
* Pillow


So not that much.

## Using TVE

TVE runs from command line. Simply run `python3 ./main_script.py -h` for help. I'll walk you through the options available.

* `-h --help` - We've got this covered already.
* `--video` - you can pass path to the video you want to convert. Leaving this empty will result in trying to open your webcam, so you can see output live.
* `--output` - if you want to save output file with effect you've chosen, pass path to it's new location. You'll want to use `.mp4` file format.
* `--size` - passing an `int` number will allow you to change how output video looks like -- meaning the size of each dot or area covered by single character. The default size is 10 (looks fine in most videos, depends on resolution).
* `--invert` - if set to `True`, will invert colors in your video. Works best with binary output (setting `--color` to `False`).
* `--chars` - if set to `True`, your output will be enturely made of characters. You will see both new window with wideo, as well as output in your terminal (don't panic, you may want to stretch it a bit).
* `--font` - you can pass path to your desired font .ttf file, if you want to use specific font. Leaving this empty will result in default font.
* `--color` - passing `False` will result in binary (black/white) output.

That's all, simple, right?

## Use examples

You will find them in `/use_examples` directory. The input was `in_vid.mp4`. Then using commands:

* `python3 ./main_script --video ./in_vid.mp4 --output ./font.mp4 --chars True`, characterized video `./font.mp4` was created. Note that it is a bit vertically stretched, as fonts tend to be higher than wider. You can use square-shaped font however, if you'll find one.
* `python3 ./main_script --video ./in_vid.mp4 --output ./binary.mp4 --color False`, video called `./binary.mp4` was created. 
* `python3 ./main_script --video ./in_vid.mp4 --output ./binary.mp4 --color True`, video `./colored.mp4` was created.

Note, that you can always change size of dots using `--size` argument.

Have fun with it ;-)
