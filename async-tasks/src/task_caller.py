
import catalog_app
import os
import json 
import sys
# catalog_app.app.conf.update(broker_url = 'pyamqp://guest:guest@localhost:5672//')

# for ix in range(2):
#     catalog_app.add.apply_async((ix,ix*3))


VAULT_BASE_MOUNT=os.environ.get('VAULT_BASE_MOUNT','/data-out')

def list_files():
    with open('/tmp/photos.json','r') as f:
        mlist = json.load(f)
    ix = 0
    for f in mlist:
        ix+=1
        file_path = f"{VAULT_BASE_MOUNT}/ORIGN/{f}"    
        catalog_app.add_file_tags.apply_async((file_path,),countdown=(ix*1e-2))
        # print(file_path)
    pass

list_files()

def tag_file():
    file_path = sys.argv[1]
    catalog_app.add_file_tags.apply_async((file_path,),countdown=3.1)

# tag_file()