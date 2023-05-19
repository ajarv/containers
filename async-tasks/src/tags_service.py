from typing import NamedTuple
import os
import sys
import re
import requests
import logging
from mutil import get_cfg_val
LOGGER = logging.getLogger(__file__.split('/')[-1])

class Photo(NamedTuple):
    image_yyyymmdd_xxx: str
    year: int
    month: int
    day: int

PAT = re.compile('((1999)|20\d{2})\/\d{2}/\d{2}/.*$')

class TagServiceClient:
    def __init__(self,**kwargs) -> None:
        TAG_SERVICE_HOST = get_cfg_val(kwargs, os.environ, 'TAG_SERVICE_HOST', 'libra')
        TAG_SERVICE_PORT = get_cfg_val(kwargs, os.environ, 'TAG_SERVICE_PORT', '8000')
        self.TAG_SERVICE_AUTH_TOKEN = get_cfg_val(kwargs, os.environ, 'TAG_SERVICE_AUTH_TOKEN', '')
        self.api_url_base = f"http://{TAG_SERVICE_HOST}:{TAG_SERVICE_PORT}/api"

    def add_photo(self, photo_path_list, tag_list=None) -> tuple:
        results = []
        for photo_path in photo_path_list:
            LOGGER.info(f"+: add_photo - {photo_path=}")
            m = PAT.search(photo_path)
            if not m:
                LOGGER.info(
                    f"Coult not add {photo_path} as it does not match pattern")
                continue
            _path = m.group(0)
            year, month, day = [int(i) for i in _path.split('/')[:3]]
            photo = Photo(m.group(0), year, month, day)

            # _id = hashlib.sha256(
            #     photo.image_yyyymmdd_xxx.encode()).hexdigest()[-16:]
            implicit_tags = [
                f'ns0:c_year:{photo.year:04}',
                f'ns0:c_month:{photo.year:04}:{photo.month:02}',
                f'ns0:c_date:{photo.year:04}:{photo.month:02}:{photo.day:02}'
            ]
            if tag_list is not None:
                implicit_tags.extend(tag_list)
            res01 = requests.post(
                f"{self.api_url_base}/obj/",
                json={
                    "key": photo.image_yyyymmdd_xxx,
                    "tags": implicit_tags
                },
                headers={
                    'Authorization':
                    f'Token {self.TAG_SERVICE_AUTH_TOKEN}'
                })
            LOGGER.info(res01)
            results.append(res01)
        return results


if __name__ == "__main__":
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    _TagServiceClient = TagServiceClient()
    photo_path = sys.argv[1]
    tag_list = sys.argv[2:]
    rval = _TagServiceClient.add_photo([photo_path],tag_list)
    print(rval)