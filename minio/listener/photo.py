import sys
import piexif
import time
import os
import logging
import re
from PIL import Image,ImageFilter
import shutil
from urllib import parse

IMGPAT= re.compile(".*[.](jpeg|jpg|nef|arw)$",re.IGNORECASE)
JPGPAT= re.compile(".*[.](jpg|jpeg)$",re.IGNORECASE)
MOVPAT= re.compile(".*[.](mp4|mov)$",re.IGNORECASE)
DATEPAT_01 = re.compile(".*?(20[0-2][0-9]).?([0-1][0-9]).?([0-3][0-9]).*",
                        re.IGNORECASE)
DATEPAT_02 = re.compile(".*?(20[0-2][0-9]).?([0-1][0-9]).*", re.IGNORECASE)

logger = logging.getLogger(__file__.split('/')[-1])

def get_image_creation_date(image_source_path):
    image_source_path = parse.unquote(image_source_path)

    def dateFromExifInfo():
        try:
            m = IMGPAT.match(image_source_path)
            if m:
                exif_dict = piexif.load(image_source_path)
                ifd = "Exif"
                readable_dict = {piexif.TAGS[ifd][tag]["name"] : exif_dict[ifd][tag] for tag in exif_dict[ifd]}
                dateTimeTaken = readable_dict['DateTimeOriginal'].decode()
                stamp = dateTimeTaken[:10].replace(':','-')
                logger.debug(f"EXIF Timestamp for {image_source_path} {stamp}")
                return (stamp,'exif')
            return None
        except:
            logger.info("Failed to get Date from exif {0}".format( image_source_path))
            return None
    def dateFromFileName():
        try:
            d,f = os.path.split(image_source_path)
            m = DATEPAT_01. match(f)
            if m:
                stamp =  '-'.join([ t for t in m.groups()])
                logger.info(
                    f"DATE 01 - from FILENAME for {image_source_path} {stamp}")
                return (stamp,'path')

            m = DATEPAT_02.match(image_source_path)
            if m:
                stamp = '-'.join([t for t in m.groups()]+['00'])
                logger.info(
                    f"DATE 02 - from FILENAME for {image_source_path} {stamp}")
                return (stamp, 'path')
            logger.info(
                f"No Date Pattern in  {image_source_path}")

            return None

        except:
            logger.error("Failed to get Date from file name {0}".format( image_source_path))
            return None
    def dateFromFileCTime():
        mtime = os.path.getmtime(image_source_path)
        stamp =  time.strftime('%Y-%m-%d',time.localtime(mtime))
        logger.info(f"DATE from file Timestamp for {image_source_path} {stamp}")
        return (stamp,'mtime')

    time_stamp =  (dateFromExifInfo() or dateFromFileName()) or dateFromFileCTime()
    return time_stamp

def resize_image(source_path, dest_path,size, quality=85,sharpen=False,):
    size = tuple(size)
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
    print(
        f"{dest_path} - Requested thumbnail                       size {size} is {'SAME' if size==image.size else 'LARGER' if size > image.size else 'SMALLER'} than original size\
        {image.size} "                                                                                                                                                                                                      )

    if max(size) > max(image.size):
        print(".. copying original as thumbnail")
        shutil.copy(source_path, dest_path)
        return
    exif_dict = piexif.load(source_path)
    # process im and exif_dict...
    w, h = image.size
    exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    exif_bytes = piexif.dump(exif_dict)
    if 'thumbnail' in exif_dict:
        del exif_dict['thumbnail']
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
    ts = get_image_creation_date(sys.argv[1])
    print(ts)
