from minio import Minio

import time
import os
import shutil
import sys
import os
import shutil
import urllib.parse
import hashlib
import thumbs_service

import logging
from mutil import get_cfg_val
LOGGER = logging.getLogger(__file__.split('/')[-1])


VAULT_BASE_MOUNT=os.environ.get('VAULT_BASE_MOUNT','/data-out')

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096*4), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class FileService:
    def __init__(self,**kwargs) -> None:
        MINIO_HOST_PORT = get_cfg_val(kwargs, os.environ, 'MINIO_HOST_PORT', "libra:9000")
        MINIO_USERNAME = get_cfg_val(kwargs, os.environ, 'MINIO_USERNAME', "kalpa")
        MINIO_PASSWORD = get_cfg_val(kwargs, os.environ, 'MINIO_PASSWORD', "rekongpeo")
        self.minio_client = Minio(MINIO_HOST_PORT,
                    access_key=MINIO_USERNAME,
                    secret_key=MINIO_PASSWORD,
                    secure=False)
    def download_file(self,bucket_name,object_name):
        key = urllib.parse.unquote_plus( f"{object_name}").replace('/','-')
        tmp_file = f"/tmp/{key}"
        info = self.minio_client.stat_object(bucket_name,object_name)
        LOGGER.info(f"downloading: {bucket_name=} {object_name=} {tmp_file=} ,{info.last_modified=}")
        self.minio_client.fget_object(bucket_name,object_name, tmp_file)
        LOGGER.info(f"done downloading: {bucket_name=} {object_name=} {tmp_file=}")
        v_path = self.move_file_to_catalog(tmp_file,VAULT_BASE_MOUNT)
        
        self.minio_client.remove_object(bucket_name,object_name)
        LOGGER.info(f"Removed key {bucket_name=} {object_name=}")
        os.remove(tmp_file)        
        LOGGER.info(f"Removed path {tmp_file=}")
        return v_path
        
    def move_file_to_catalog(self,tmp_file, dst_base_dir):
        dst_dir = f"{dst_base_dir}/ORIGN"
        _date_stamp,method = thumbs_service.get_image_creation_date(tmp_file)
        date_stamp = _date_stamp.split('-')
        
        if method == "mtime":
            file_name = f"{md5(tmp_file)[:8]}-{tmp_file.split('/')[-1]}"
            date_stamp = ('2099','07','04',)
        else:
            file_name = tmp_file.split('/')[-1]
        origin_time = time.mktime(time.strptime("-".join(date_stamp),"%Y-%m-%d"))
        cataloged_file_path = os.path.join(dst_dir, *date_stamp, file_name)
        print(f"{cataloged_file_path=} ,{dst_dir=},{date_stamp=} {file_name=}",)
        try:
            if os.path.exists(tmp_file):
                if os.path.exists(cataloged_file_path):
                    sz_src,sz_cataloged_file_path = os.path.getsize(tmp_file),os.path.getsize(cataloged_file_path)
                    if sz_cataloged_file_path >= sz_src:
                        LOGGER.info(f"Original File exists and is NOT smaller - {cataloged_file_path=}")
                        return cataloged_file_path
                cataloged_file_pathdir ,f= os.path.split(cataloged_file_path)
                os.makedirs(cataloged_file_pathdir, mode=511, exist_ok=True)
                shutil.copyfile(tmp_file,cataloged_file_path)
                os.utime(cataloged_file_path,(origin_time,origin_time,))
                LOGGER.info(f"Copy ok {tmp_file} -> {cataloged_file_path} , {time.gmtime(origin_time)=}")
                return cataloged_file_path
            else:
                LOGGER.warning(f":+ move_file_to_catalog Does not exist {tmp_file=}")
            return None
        except:
            LOGGER.exception(f"Copy fail {tmp_file} -> {cataloged_file_path}")
            return None


if __name__ == '__main__':
    logging.basicConfig(    format = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                        level=logging.INFO)
    _FileService = FileService()
    _FileService.download_file(sys.argv[1],sys.argv[2])
    # task_enqueue_key('images', 'PICT_20220101_104102.JPG')
    # time.sleep(300)

    # move_to_catalog_folder('images/PICT_20220101_104102.JPG',
    #                        src_dir='/opt/data',
    #                        dst_dir='/mnt/ssd/avashist/PhotoVault/vault/ORIGN')

    # task_remove_s3_object('images', 'birdman.jpeg')
    # _tn_300('/data-out')
