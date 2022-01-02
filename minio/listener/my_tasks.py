import sys
import time
import os
import logging
import re
import shutil
import photo
from minio import Minio

logger = logging.getLogger(__file__)

client = Minio('minio:9000', access_key='kalpa', secret_key='rekongpeo', secure=False)

def task_make_tn(orign_file_path,size=2048):
    try:
        m = photo.JPGPAT.match(orign_file_path)
        if not m:
            logger.debug(f"Not an image file {orign_file_path}")
            return None
        tgt = orign_file_path.replace('ORIGN','S2000')
        if os.path.exists(orign_file_path):
            photo.resize_image(orign_file_path, tgt, [size,size], quality=85, sharpen=True,)
            return tgt
    except:
        logger.exception(f"TN Create fail {orign_file_path} -> {tgt}")
        return None

def task_remove_s3_object(bucket,key):
    client.remove_object(bucket,key)


def task_enqueue_bucket(bucket,q):
    for item in client.list_objects(bucket):
        if not item.is_dir:
            key = f"{item.bucket_name}/{item.object_name}"
            q.put((item.bucket_name,key,time.time()+10,))
            logger.info(f"Queued up key {key}")



def move_to_catalog_folder(key):
    src = os.path.join('/data',key)
    date_stamp = photo.get_image_creation_date(src).split('-')
    tgt = os.path.join('/data-out/ORIGN',*date_stamp,key)
    try:
        if os.path.exists(src):
            tgtdir ,f= os.path.split(tgt)
            os.makedirs(tgtdir, mode=511, exist_ok=True)
            shutil.copyfile(src,tgt)
            logger.info(f"Copy ok {src} -> {tgt}")
            return tgt
        return None
    except:
        logger.exception(f"Copy fail {src} -> {tgt}")
        return None