from IT8951.display import AutoEPDDisplay
from IT8951 import constants
from PIL import  Image, ImageDraw,ImageFont
from cs_global import mensajes,icon,rectangulos
import time



def drawScreen():
    print('Drawing screen ...')
    display = AutoEPDDisplay(vcom=-2.06)
    display.clear()
    fontsize = 50
    fontT = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', fontsize)
    draw = ImageDraw.Draw(display.frame_buf)
    draw.text((260, 540), "CuramSenes", font=fontT)
    fontsize = 35
    font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', fontsize)
    fontsize = 20
    fontSmall = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', fontsize)
    for idx in range(5):
        draw.rectangle(rectangulos[idx],fill=None,width=3)
    for idx, mensaje in enumerate(mensajes):
        if(icon[mensaje[0] ]!= ""):
            img = Image.open("iconos/"+icon[mensaje[0]])
            display.frame_buf.paste(img, (rectangulos[idx][0][0]+4, rectangulos[idx][0][1]+30) )
        draw.rectangle(rectangulos[idx],fill=None,width=4)
        draw.multiline_text((rectangulos[idx][0][0]+109, rectangulos[idx][0][1]+70), mensaje[1], font=font)    
        if (mensaje[0] == "b"):
            draw.multiline_text((rectangulos[idx][0][0]+109, rectangulos[idx][0][1]+120), mensaje[2], font=fontSmall)
    display.draw_full(constants.DisplayModes.GC16)

