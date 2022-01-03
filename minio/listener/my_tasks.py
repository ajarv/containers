import sys
import time
import os
import logging
import shutil
import photo
from minio import Minio
import sys
import os
import shutil
import queue
import threading
import urllib.parse

logger = logging.getLogger(__file__)

client = Minio('minio:9000', access_key='kalpa', secret_key='rekongpeo', secure=False)
task_queue = queue.Queue()


def worker():
    while True:
        (   bucket_name,
            object_name,
            valid_after,
        ) = task_queue.get()
        delay = valid_after - time.time()
        if delay > 0:
            logger.info(f'Will work on {bucket_name}/{object_name} in {delay} sec')
            time.sleep(delay)
        do_tasks(bucket_name,object_name)
        task_queue.task_done()


# turn-on the worker thread
threading.Thread(target=worker, daemon=True).start()


def task_make_tn(orign_file_path,tn_file_path=None,size=2000):
    try:
        m = photo.JPGPAT.match(orign_file_path)
        if not m:
            logger.debug(f"Not an image file {orign_file_path}")
            return None
        tn_file_path = tn_file_path or orign_file_path.replace('ORIGN','S2000')
        if os.path.exists(orign_file_path):
            photo.resize_image(orign_file_path, tn_file_path, [size,size], quality=85, sharpen=True,)
            return tn_file_path
    except:
        logger.exception(f"TN Create fail {orign_file_path} -> {tn_file_path}")
        return None

def task_remove_s3_object(bucket,key):
    client.remove_object(bucket,key)
    logger.info(f"Removed key {bucket} {key}")


def task_enqueue_key(bucket_name,object_name):
    task_queue.put((
        bucket_name,
        object_name,
        time.time() + 10,
    ))
    logger.info(f"Queued up key {object_name}")


def task_enqueue_bucket(bucket):
    for item in client.list_objects(bucket, recursive=True):
        if not item.is_dir:
            task_enqueue_key(item.bucket_name, item.object_name)


def do_tasks(bucket_name, object_name):
    try:
        logger.info(f'Working on {bucket_name}/{object_name}')
        key = urllib.parse.unquote( f"{bucket_name}/{object_name}")
        cataloged_file = move_to_catalog_folder(key)
        if cataloged_file:
            if photo.JPGPAT.match(cataloged_file):
                task_make_tn(cataloged_file,tn_file_path=cataloged_file.replace('ORIGN','S2000'),size=2000):
                task_make_tn(cataloged_file,tn_file_path=cataloged_file.replace('ORIGN','S0300'),size=300):
                logger.info(f"Created Thumbnails {key}")
            task_remove_s3_object(bucket_name, object_name)
        logger.info(f'Done {bucket_name}/{object_name}')
    except:
        logger.exception(f'Failed {bucket_name}/{object_name}')
        pass


def move_to_catalog_folder(key,src_dir='/data', dst_dir='/data-out/ORIGN'):
    src = os.path.join(src_dir,key)
    date_stamp = photo.get_image_creation_date(src).split('-')
    tgt = os.path.join(dst_dir,*date_stamp,key.split('/')[-1])
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

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    client = Minio('localhost:9000',
                    access_key='kalpa',
                    secret_key='rekongpeo',
                    secure=False)
    # task_enqueue_key('images', 'PICT_20220101_104102.JPG')
    # time.sleep(300)

    # move_to_catalog_folder('images/PICT_20220101_104102.JPG',
    #                        src_dir='/opt/data',
    #                        dst_dir='/mnt/ssd/avashist/PhotoVault/vault/ORIGN')

    task_remove_s3_object('images', 'birdman.jpeg')
