import os
import photo
import my_tasks
import logging
import shutil
import sys

logger = logging.getLogger(__file__)

def move_file_to_catalog(src, dst_dir='/data-out/ORIGN'):
    _date_stamp,method = photo.get_image_creation_date(src)
    date_stamp = _date_stamp.split('-')
    if method == "mtime":
        file_name = f"{my_tasks.md5(src)}-{src.split('/')[-1]}"
        tgt = os.path.join(dst_dir,'9999','00','00',file_name)
    else:
        file_name = src.split('/')[-1]
        tgt = os.path.join(dst_dir, *date_stamp, file_name)

    if src == tgt:
        logger.debug(f"source and target are same {src}")
        return 
    try:
        if os.path.exists(src):
            if os.path.exists(tgt):
                sz_src,sz_tgt = os.path.getsize(src),os.path.getsize(tgt)
                if sz_tgt >= sz_src:
                    # os.remove(src)
                    logger.info(f"Removed {src}, Target file exists and is {'larger' if sz_tgt > sz_src else 'same'} - {tgt}")
                    return tgt
            tgtdir ,f= os.path.split(tgt)
            logger.info(f"os.makedirs({tgtdir}, mode=511, exist_ok=True)")
            os.makedirs(tgtdir, mode=511, exist_ok=True)
            logger.info(f"shutil.move({src},{tgt})")
            shutil.move(src,tgt)
            logger.info(f"Move ok {src} -> {tgt}")
            return tgt
        return None
    except:
        logger.exception(f"Move fail {src} -> {tgt}")
        return None


def organize_paths(base_dir):    
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            src = os.path.join(root, name)
        # for name in dirs:
        #     print(os.path.join(root, name)) 
            move_file_to_catalog(src,dst_dir=base_dir)
    pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)    
    organize_paths(sys.argv[1])