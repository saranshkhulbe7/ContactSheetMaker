import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from IPython.display import display

file_address = "readonly/DP4.jpeg"
image = Image.open(file_address)
image = image.convert("RGB")

font_type = ImageFont.truetype("readonly/fanwood-webfont.ttf", size = 50)
images = []
image_texts = []

txt_color = 'rgb(255,255,255)'
text_height = 70
text_margin = 10
RGB = [0,1,2]
intensities = [0.1, 0.5, 0.9]


for channel in RGB:
    for intensity in intensities:
        tempImage = PIL.Image.new(image.mode, (image.width, image.height + text_height))
        tempImage.paste(image,(0,0))
        text_part = ImageDraw.Draw(tempImage)
        image_texts.append("channel {} intensity {}".format(channel,intensity))
        text_part.text((0,image.height + text_margin),"channel {} intensity {}".format(channel,intensity), font = font_type, fill = txt_color)
        images.append(tempImage)
image_number = 0
for channel in RGB:
    for intensity in intensities:
        channel_tuple = images[image_number].split()
        color_band = channel_tuple[channel].point(lambda x: x*intensity)
        if channel == 0:
            images[image_number] = Image.merge("RGB", (color_band, channel_tuple[1], channel_tuple[2]))
        elif channel == 1:
            images[image_number] = Image.merge("RGB", (channel_tuple[0], color_band, channel_tuple[2]))
        else:
            images[image_number] = Image.merge("RGB", (channel_tuple[0], channel_tuple[1], color_band))
        image_number+=1

        
contact_sheet = PIL.Image.new(image.mode, (images[0].width*3, images[0].height*3))
x=0
y=0
for img in images:
    contact_sheet.paste(img, (x, y) )
    if x+images[0].width == contact_sheet.width:
        x=0
        y+=images[0].height
    else:
        x+=images[0].width

contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet) 
        
