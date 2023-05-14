from minio import Minio

import time
import os
import logging
import shutil
import photo
import sys
import os
import shutil
import queue
import threading
import datetime
import urllib.parse
import hashlib
# import photo_listings
from tags_service import TagServiceClient

_TagServiceClient = TagServiceClient()

logger = logging.getLogger(__file__.split('/')[-1])

MINIO_HOST_PORT = os.environ.get('MINIO_HOST_PORT', "minio:9000")
client = Minio(MINIO_HOST_PORT,
               access_key='kalpa',
               secret_key='rekongpeo',
               secure=False)
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
            time.sleep(delay+1)
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


def task_enqueue_key(bucket_name,object_name,delay=10):
    task_queue.put((
        bucket_name,
        object_name,
        time.time() + delay,
    ))
    logger.info(f"Queued up key {bucket_name}/{object_name}")


def task_enqueue_bucket(bucket):
    ix = 0
    for item in client.list_objects(bucket, recursive=True):
        if not item.is_dir:
            ix += 1
            task_enqueue_key(item.bucket_name, item.object_name,delay=0.05*ix)

def do_tasks(bucket_name, object_name):
    try:
        logger.info(f'Working on {bucket_name}/{object_name}')
        key = urllib.parse.unquote_plus( f"{bucket_name}/{object_name}")
        cataloged_file = move_to_catalog_folder(key)
        if cataloged_file:
            if photo.JPGPAT.match(cataloged_file):
                task_make_tn(cataloged_file,tn_file_path=cataloged_file.replace('ORIGN','S2000'),size=2000)
                task_make_tn(cataloged_file,tn_file_path=cataloged_file.replace('ORIGN','S0300'),size=300)
                logger.info(f"Created Thumbnails {key}")
                _TagServiceClient.add_photo(
                    [cataloged_file], [f"ns0:upload-date:{datetime.date.today().isoformat()}"])
            task_remove_s3_object(bucket_name, object_name)
        logger.info(f'Done {bucket_name}/{object_name}')
        #run_listings()
    except:
        logger.exception(f'Failed {bucket_name}/{object_name}')
        pass

# last_run =[0]
# def run_listings():
#     now = time.time()
#     if (now - last_run[0]) > 60*5: #more than 5 min
#         last_run[0] = now
#         logger.info("Creating File listings")
#         photo_listings.folder_listing_json('/data-out/S2000')
#     pass


def _tn_300(vault_dir):
    source = f"{vault_dir}/S2000"
    for root, dirs, files in os.walk(source):
        logger.info(f"Working on {root}")
        files =[file for file in files if photo.JPGPAT.match(file)]
        file_paths = [os.path.join(root, name) for name in files]
        for file_path in file_paths:
            tn_file_path = file_path.replace('S2000','S0300')
            task_make_tn(file_path,tn_file_path=tn_file_path,size=300)
            logger.info(f"Created tn {tn_file_path}")


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096*4), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def move_file_to_catalog(src, dst_dir='/data-out/ORIGN'):
    _date_stamp,method = photo.get_image_creation_date(src)
    date_stamp = _date_stamp.split('-')
    if method == "mtime":
        file_name = f"{md5(src)}-{src.split('/')[-1]}"
        tgt = os.path.join(dst_dir,'9999','00','00',file_name)
    else:
        file_name = src.split('/')[-1]
        tgt = os.path.join(dst_dir, *date_stamp, file_name)

    try:
        if os.path.exists(src):
            if os.path.exists(tgt):
                sz_src,sz_tgt = os.path.getsize(src),os.path.getsize(tgt)
                if sz_tgt >= sz_src:
                    logger.info(f"Original File exists and is NOT smaller - {tgt}")
                    return tgt
            tgtdir ,f= os.path.split(tgt)
            os.makedirs(tgtdir, mode=511, exist_ok=True)
            shutil.copyfile(src,tgt)
            logger.info(f"Copy ok {src} -> {tgt}")
            return tgt
        else:
            logger.warning(f":+ move_file_to_catalog Does not exist {src=}")
        return None
    except:
        logger.exception(f"Copy fail {src} -> {tgt}")
        return None


def move_to_catalog_folder(key,src_dir='/data', dst_dir='/data-out/ORIGN'):
    src = os.path.join(src_dir, key)
    return move_file_to_catalog(src,dst_dir=dst_dir)

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

    # task_remove_s3_object('images', 'birdman.jpeg')
    _tn_300('/data-out')
