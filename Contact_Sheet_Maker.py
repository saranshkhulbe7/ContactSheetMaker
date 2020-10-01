import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageEnhance
from IPython.display import display
import time
import math

def getDimensions(n):
    sq = math.sqrt(n)
    width_factor = math.ceil(sq)
    height_factor = math.floor(sq)
    return (width_factor,height_factor)


def variator(n):
    lst = []
    for i in range(1,n+1):
        lst.append((1/n)*i)
    return lst


def colorVariantContactSheet(file_address):
    number_of_variation_per_color = int(input("Number of images in a single color variation : "))
    image = Image.open(file_address)
    image = image.convert("RGB")

    font_type = ImageFont.truetype("readonly/fanwood-webfont.ttf", size = 50)
    images = []
    image_texts = []

    white_color_code = 'rgb(255,255,255)'
    text_height = 70
    text_margin = 10
    RGB = [0,1,2]
    color_intensities = variator(number_of_variation_per_color)


    for channel in RGB:
        for intensity in color_intensities:
            tempImage = PIL.Image.new(image.mode, (image.width, image.height + text_height))
            tempImage.paste(image,(0,0))
            text_part = ImageDraw.Draw(tempImage)
            image_texts.append("channel {} intensity {}".format(channel,intensity))
            text_part.text((0,image.height + text_margin),"channel {} intensity {}".format(channel,intensity), font = font_type, fill = white_color_code)
            images.append(tempImage)
            
            
    image_number = 0
    for channel in RGB:
        for intensity in color_intensities:
            channel_tuple = images[image_number].split()
            color_band = channel_tuple[channel].point(lambda x: x*intensity)
            if channel == 0:
                images[image_number] = Image.merge("RGB", (color_band, channel_tuple[1], channel_tuple[2]))
            elif channel == 1:
                images[image_number] = Image.merge("RGB", (channel_tuple[0], color_band, channel_tuple[2]))
            else:
                images[image_number] = Image.merge("RGB", (channel_tuple[0], channel_tuple[1], color_band))
            image_number+=1

        
    contact_sheet = PIL.Image.new(image.mode, (images[0].width*len(color_intensities), images[0].height*len(RGB)), color = white_color_code)
    x=0
    y=0
    for img in images:
        contact_sheet.paste(img, (x, y) )
        if x+images[0].width == contact_sheet.width:
            x=0
            y+=images[0].height
        else:
            x+=images[0].width
    return contact_sheet


def brightnessVariantContactSheet(file_address):
    number_of_brightness_variation = int(input("Number of brightness variation needed : "))
    image = Image.open(file_address)
    image = image.convert('RGB')
    images = []
    image_texts = []
    
    font_type = ImageFont.truetype("readonly/fanwood-webfont.ttf", size = 50)
    white_color_code = 'rgb(255,255,255)'
    text_height = 70
    text_margin = 10
    brightness_intensities = variator(number_of_brightness_variation)
    
    
    for i in range(number_of_brightness_variation):
        enhancer = ImageEnhance.Brightness(image)
        images.append(enhancer.enhance(brightness_intensities[i]))
    image_number = 0
    
    
    for intensity in brightness_intensities:
        tempImage = PIL.Image.new(image.mode, (image.width, image.height + text_height))
        tempImage.paste(images[image_number],(0,0))
        text_part = ImageDraw.Draw(tempImage)
        image_texts.append("intensity {}".format(intensity))
        text_part.text((0,image.height + text_margin),"intensity {}".format(intensity), font = font_type, fill = white_color_code)
        images[image_number] = tempImage
        image_number+=1
    
    width_factor,height_factor = getDimensions(number_of_brightness_variation)
    
    contact_sheet=PIL.Image.new(image.mode, (images[0].width*width_factor,images[0].height*height_factor), color = white_color_code)
    x=0
    y=0
    for img in images:
        contact_sheet.paste(img, (x, y) )
        if x+images[0].width == contact_sheet.width:
            x=0
            y+=images[0].height
        else:
            x+=images[0].width
    contact_sheet = contact_sheet.resize((int(contact_sheet.width/width_factor),int(contact_sheet.height/height_factor) ))
    return contact_sheet

def displayContactSheet(file_address):
    print("Contact Sheet Menu")
    print("1. Color Variant Contact Sheet")
    print("2. Brightness Variant Contact Sheet")
    time.sleep(1)
    choice = int(input("Enter the serial no. of your variant : "))
    if choice == 1 :
        developed_contact_sheet = colorVariantContactSheet(file_address)
        display(developed_contact_sheet)
    elif choice == 2:
        developed_contact_sheet = brightnessVariantContactSheet(file_address)
        display(developed_contact_sheet)
    else:
        displayContactSheet(file_address)

file_address = "readonly/Mountains.jpeg"
displayContactSheet(file_address)

        
