from PIL import Image
import sys
import os.path

# Number of pixels to store the length of the hidden message
TEXT_LENGTH = 11

def extractTextLength(image):
    """
    Extract the text length from the last 11 pixels from the picture.

    Args:
        image:      The image to extract the text length from.
    """
    picwidth, picheight = image.size
    picwidth -= 1
    picheight -= 1
    binstring = ""
    
    # Create a binary bit string of the text length
    for x in range(picwidth, picwidth - TEXT_LENGTH, -1):
        rgb = image.getpixel((x, picheight))

        # append the binary conversion of the pixel to length_list
        for j in rgb:
            # Append 1 to bin list if (R, G, or B) is odd, 0 if even
            if j % 2 == 1:
                binstring += '1'
            else:
                binstring += '0'

    # Get rid of the last bit value and proceed to
    # turn the binstring into an int stored in actual_length
    binstring = binstring[:-1]
    msglen = int(binstring, 2)
    return int(msglen / 8)

# Convert binary to text and concatenate it to a string
def extractText(img):
    """
    Prints the hidden message.

    Args:
        img:    The image to extract the message from.
    """


    image = Image.open(img)
    msglen = extractTextLength(image)
    bitlen = msglen * 8
    
    # Set the starting position
    picwidth, picheight = image.size
    picwidth -= 1
    picheight -= 1

    # Set number of pixels to iterate through
    if (bitlen % 3 != 0):
        numpixels = int(bitlen / 3 + 1)
    else:
        numpixels = int(bitlen / 3)

    binstring = ""
    eightbitlist = []

    x = picwidth - TEXT_LENGTH
    y = picheight
    y_end = picheight - (int(numpixels / picwidth) + 1)
    pixel_it = numpixels

    # Create the binary bit string
    while (y >= y_end):
        while (x >= 0 and pixel_it > 0):
            rgb = image.getpixel((x, y))
            for j in rgb:
                if j % 2 == 1:
                    binstring += '1'
                else:
                    binstring += '0'
            pixel_it -= 1
            x -= 1
        if (x == -1):
            x = picwidth
        y -= 1

    # From the binary string, slice 8-bit strings and store them into a list
    frontbound = 0
    while (frontbound + 8 <= len(binstring)):
        eightbitlist.append(binstring[frontbound:frontbound + 8])
        frontbound += 8

    # Convert the 8-bit strings into chars
    message = ""
    for eightbitstr in eightbitlist:
        message += chr(int(eightbitstr, 2))
    print(message)

def textFits(image, message):
    """
    Checks if the message will fit into the picture.

    Args:
        image:      The image that you want to embed the message in.
        message:    The message to embed.
    """
    picwidth, picheight = image.size
    # Maximum length of the message that the picture can hold is 
    # ((width * height - 11) * 3 bits per rgb / 8bits per letter)
    max_msg_len = (picwidth * picheight - TEXT_LENGTH) * 3 / 8
    if (len(message) * 8 > max_msg_len):
        return False
    return True

# Hide text length into the first 11 pixels
def storeMsgLen(image, message):
    """
    Stores the binary representation of the message length into the 
    last 11 pixels of the picture.

    Args:
        image:      The image that you are storing the binary representation of message length in.
        message:    The message to embed.
    """
    msglen = len(message) * 8
    picwidth, picheight = image.size
    picwidth -= 1
    picheight -= 1
    rgb_list = []

    # convert msglen to binary string
    bin_msglen = str(bin(msglen))
    
    # get rid of the '0b' in front of the binary string
    bin_msglen = bin_msglen[2:len(bin_msglen)]

    # Store all of the R, G, and B values into a list
    for x in range(picwidth, picwidth - TEXT_LENGTH, -1):
        rgb = image.getpixel((x, picheight))
        r, g, b = rgb
        rgb_list.append(r)
        rgb_list.append(g)
        rgb_list.append(b)

    # Change all values to even in rgb_list up til the length of 
    # the length of the binary string of the message length
    it = 0
    endpoint = len(rgb_list) - len(bin_msglen) - 1
    while (it < endpoint):
        if (rgb_list[it] % 2 == 1): rgb_list[it] -= 1
        it += 1

    # Change the remaining values of rgb_list to even/odd when comparing to the binary string corrolating to message length
    it_bin_msglen = 0
    it_rgb_list = endpoint
    while (it_rgb_list < len(rgb_list) - 1):
        # If the bit is 1, but the color is even, change it to odd
        if (bin_msglen[it_bin_msglen] == '1'):
            if (rgb_list[it_rgb_list] % 2 == 0):
                rgb_list[it_rgb_list] += 1
        # If the bit is 0, but the color is odd, change it to even
        else:
            if (rgb_list[it_rgb_list] % 2 == 1):
                rgb_list[it_rgb_list] -= 1
        it_rgb_list += 1
        it_bin_msglen += 1

    # Create a new rgb tuple with the changed color values and
    # put the pixel back into the picture with the new rgb values
    frontbound = 0
    x = picwidth
    y = picheight
    while (frontbound + 3 <= len(rgb_list)):
        r, g, b = rgb_list[frontbound: frontbound + 3]
        image.putpixel((x, y), (r, g, b))
        frontbound += 3
        x -= 1

def embedText(img, newimg, message):
    """
    Embeds a message into a picture starting from the 12th from the last pixel, going left and up.

    Args:
        img:        The image that you want to embed the message in.
        newimg:     The name of the new image to save the embedded picture.
        message:    The message to embed.
    """
    image = Image.open(img)


    msglen = len(message) * 8
    storeMsgLen(image, message)
    picwidth, picheight = image.size
    picwidth -= 1
    picheight -= 1

    if (msglen % 3 != 0):
        numpixels = int(msglen / 3 + 1)
    else:
        numpixels = int(msglen / 3)
    bin_str_list = []
    bit_list = []
    
    # Convert the message to 8-bit binary strings and store them into bin_list[]
    for ch in message: 
        binstr = ch.encode('ascii')
        bin_str_list.append(format(ord(binstr), '08b'))

    # Append single bits from the 8-bit binary strings to bit_list[]
    for binstr in bin_str_list:
        for bit in binstr:
            bit_list.append(bit)

    
    rgb_list = []
    x = startx = picwidth - TEXT_LENGTH
    y = picheight
    y_end = picheight - (int(numpixels / picwidth) + 1)
    pixel_it = numpixels

    # Iterate through the pixels and store the rgb values into rgb_list[]
    while (y >= y_end):
        while (x >= 0 and pixel_it > 0):
            r, g, b = image.getpixel((x, y))
            rgb_list.append(r)
            rgb_list.append(g)
            rgb_list.append(b)
            x -= 1
            pixel_it -= 1
            if (x == -1):
                x = picwidth
        y -= 1

    # Compare bin_list[] and rgb_list[] and change the color values to even if 
    # the bit in bin_list is 0 and change the color values to odd if the bit in bin_list is 1
    i = 0
    while (i < len(bit_list)):
        # If the bit is '1' but the color is even, change it to odd
        if (bit_list[i] == '1'):
            if (rgb_list[i] % 2 == 0):
                rgb_list[i] += 1
        # If the bit is '0', but the color is odd, change it to even
        else:
            if (rgb_list[i] % 2 == 1):
                rgb_list[i] -= 1
        i += 1

    # Convert back to rgb tuple and change the pixels to their values    
    frontbound = 0
    x = startx
    y = picheight
    while (frontbound + 3 <= len(rgb_list)):
        r, g, b = rgb_list[frontbound: frontbound + 3]
        image.putpixel((x, y), (r, g, b))
        frontbound += 3
        x -= 1
        if (x == -1):
            x = picwidth 
            y -= 1

    image.save(newimg, "PNG")
    print("Message embedding complete")


"""
Main:
Take arguments from the command line and execute the code.
"""
if (sys.argv[1] == '-m' or sys.argv[1] == '--embed'):
    embedText(sys.argv[2], sys.argv[3], sys.argv[4])
elif (sys.argv[1] == '-x' or sys.argv[1] == '--extract'):
    extractText(sys.argv[2])
else:
    print("Invalid arguments.\n")
    print("To embed a message in an image use:")
    print("$ python steg.py ['-m' or '--embed'] [/path/to/picture.jpg] ['new_picture_name'] ['message']\n")
    print("To embed a message from a file in an image use:")
    print("$ python steg.py ['-m' or '--embed'] ['-f' or '--file'] [/path/to/picture.jpg] ['new_picture_name'] ['message']\n")
    print("To extract the hidden message from an image use:")
    print("$ python steg.py ['-x' or '--extract'] [/path/to/picture.jpg]")
    sys.exit()