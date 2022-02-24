#!/usr/bin/python3
from PIL import Image
import sys
import os

def interpolate( val, y0, x0, y1, x1 ):
  return (val-x0)*(y1-y0)/(x1-x0) + y0

def blue( grayscale ):
  if ( grayscale < -0.33 ): return 1.0
  elif ( grayscale < 0.33 ): return interpolate( grayscale, 1.0, -0.33, 0.0, 0.33 );
  else: return 0.0

def green( grayscale ): 
  if ( grayscale < -1.0 ): return 0.0
  if  ( grayscale < -0.33 ): return interpolate( grayscale, 0.0, -1.0, 1.0, -0.33 );
  elif ( grayscale < 0.33 ): return 1.0
  elif ( grayscale <= 1.0 ): return interpolate( grayscale, 1.0, 0.33, 0.0, 1.0 );
  else: return 1.0

def red( grayscale ):
  if ( grayscale < -0.33 ):
    return 0.0
  elif ( grayscale < 0.33 ):
    return interpolate( grayscale, 0.0, -0.33, 1.0, 0.33 )
  else:
      return 1.0


def rain_fall(visible,thermal_image):
    apply  = visible.copy()
    for x in range(0,thermal_image.width):
        for y in range(0,thermal_image.height):
            min_thermal = 200
            value = thermal_image.getpixel((x,y))
            if type(value)==int:
                grey_scale  = value
            else:
                grey_scale = int((float(value[0])+float(value[1])+float(value[2]))/3.0)
            if(grey_scale > min_thermal):
                v  = (grey_scale-min_thermal)/(255-min_thermal)
                apply.putpixel((x,y),(int(red((v-0.5)*2)*255),int(green((v-0.5)*2)*255),int(blue((v-0.5)*2)*255)))
    return apply

def vegetation_detect(rgb221:Image.Image):
    apply  = rgb221.copy()
    for x in range(0,rgb221.width):
        for y in range(0,rgb221.height):
            msuMR1 = rgb221.getpixel((x,y))[2]
            msuMR2 = rgb221.getpixel((x,y))[0]
            is_veg = msuMR2 - msuMR1 > 25
            visible_average = int((msuMR1+msuMR2)/2)
            apply.putpixel((x,y),(msuMR2,msuMR2 if is_veg else visible_average,msuMR1))
    return apply
def no_veg(rgb221:Image.Image):
    apply  = rgb221.copy()
    for x in range(0,rgb221.width):
        for y in range(0,rgb221.height):
            msuMR1 = rgb221.getpixel((x,y))[2]
            msuMR2 = rgb221.getpixel((x,y))[0]
            visible_average = int((msuMR1+msuMR2)/2)
            apply.putpixel((x,y),(msuMR2,visible_average,msuMR1))
    return apply

def meteor_lrpt_proc(rgb221:Image.Image, thermal: Image.Image):
    veg = vegetation_detect(rgb221)
    print("Created vegetation RGB")


    noveg = no_veg(rgb221)
    print("Created non-vegetation RGB")


    return (veg,noveg, thermal, rain_fall(veg,thermal))
def main():
    if(len(sys.argv) < 4):
        print("Usage: ./meteor_lrpt_proc <input rgb221> <input thermal> <output directory>")
        exit(-1)
    input_rgb221 = sys.argv[1]
    input_thermal = sys.argv[2]
    output_directory = sys.argv[3]
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    
    veg, noveg, thermal, rainfall = meteor_lrpt_proc(Image.open(input_rgb221), Image.open(input_thermal))

    thermal.save(output_directory+"/thermal.png")
    veg.save(output_directory+"/veg.png")
    noveg.save(output_directory+"/noveg.png")
    rainfall.save(output_directory+"/rainfall.png")
if __name__ == "__main__":
    main()
