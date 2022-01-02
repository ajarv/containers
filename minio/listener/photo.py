
import sys
import piexif
import time
import os
import logging
import re
from PIL import Image,ImageFilter
import shutil


IMGPAT= re.compile(".*[.](jpg|nef|arw)$",re.IGNORECASE)
JPGPAT= re.compile(".*[.](jpg|jpeg)$",re.IGNORECASE)
MOVPAT= re.compile(".*[.](mp4|mov)$",re.IGNORECASE)
DATEPAT_01 = re.compile(".*?([1-2][0-9]{3}).*?([0-1][0-9]).*?([0-3][0-9]).*",re.IGNORECASE)
logger = logging.getLogger(__file__)

def get_image_creation_date(image_source_path):
    def dateFromExifInfo():
        try:
            m = IMGPAT.match(f)
            if m:
                exif_dict = piexif.load(image_source_path)
                ifd = "Exif"
                readable_dict = {piexif.TAGS[ifd][tag]["name"] : exif_dict[ifd][tag] for tag in exif_dict[ifd]}
                dateTimeTaken = readable_dict['DateTimeOriginal'].decode()
                stamp = dateTimeTaken[:10].replace(':','-')
                logger.info(f"EXIF Timestamp for {image_source_path} {stamp}")
                return stamp
            return None
        except:
            logger.info("Failed to get Date from exif {0}".format( image_source_path))
            return None
    def dateFromFileName():
        try:
            d,f = os.path.split(image_source_path)
            m = DATEPAT_01.match(f)
            if m:
                stamp =  '-'.join([ t for t in m.groups()])
                logger.info(f"DATE from FILENAME for {image_source_path} {stamp}")
                return stamp
            return None
        except:
            logger.info("Failed to get Date from file name {0}".format( image_source_path))
            return None
    def dateFromFileCTime():
        mtime = os.path.getmtime(image_source_path)
        stamp =  time.strftime('%Y-%m-%d',time.localtime(mtime))
        logger.info(f"DATE from file Timestamp for {image_source_path} {stamp}")
        return stamp

    time_stamp =  dateFromExifInfo() or dateFromFileName() or dateFromFileCTime()
    
    return time_stamp

def resize_image(source_path, dest_path,size, quality=85, sharpen=True,):
    _dir = os.path.split(dest_path)[0]
    if not os.path.exists(_dir) : os.makedirs(_dir)

    if os.path.exists(dest_path):
        print ("Resized image exists -",dest_path)
        return

    _dest_path = dest_path+".tmp"
    if os.path.exists(_dest_path):
        os.remove(_dest_path)
    # resize image
    image = Image.open(source_path)
    exif_dict = piexif.load(source_path)
    # process im and exif_dict...
    w, h = image.size
    exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    exif_bytes = piexif.dump(exif_dict)
    try:
        image.thumbnail(size, Image.ANTIALIAS )
    except:
        logger.exception(f"Failed to resize image {source_path}")
        return False
    image = image.filter(ImageFilter.SHARPEN)
    image.save(_dest_path, "JPEG", quality=quality,exif_bytes=exif_bytes)
    os.rename(_dest_path,dest_path)
    return True





if __name__ == '__main__':
    ts = get_image_creation_date_time(sys.argv[1])
    print(ts)
