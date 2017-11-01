# Text in Image
Text in image is a tool that allows you to embed a hidden message into an image.

* Kenny Nham
* CPSC 353, Tuesday 7:00PM
* October 31, 2017

## Requirements
* Python version: 3.6.3
* PIL module: 4.1.2

## System Architecture
The program consists of several functions including:  
* extractTextLength(image)
* extractText(image)
* textFits(image, message)
* storeMsgLen(image, message)
* embedText(image, newimage, message)

## Instructions
#### To embed a message in an image use:
    $ python steg.py ['-m' or '--embed'] [/path/to/picture.jpg] ['new_picture_name'] ['message']

#### To extract a message from an image use:
    $ python steg.py ['-x' or '--extract'] [/path/to/picture.jpg]

