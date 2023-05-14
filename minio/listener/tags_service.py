from typing import NamedTuple
import hashlib
import os
import sys
import re
import logging
import requests

logger = logging.getLogger(__file__.split('/')[-1])

TAG_SERVICE_HOST = os.environ.get('TAG_SERVICE_HOST', 'localhost')
TAG_SERVICE_PORT = os.environ.get('TAG_SERVICE_PORT', '8000')
TAG_SERVICE_AUTH_TOKEN = os.environ.get('TAG_SERVICE_AUTH_TOKEN')


class Photo(NamedTuple):
    image_yyyymmdd_xxx: str
    year: int
    month: int
    day: int


PAT = re.compile('((1999)|20\d{2})\/\d{2}/\d{2}/.*$')


class TagServiceClient:
    def __init__(self) -> None:
        self.api_url_base = f"http://{TAG_SERVICE_HOST}:{TAG_SERVICE_PORT}/api"

    def add_photo(self, photo_path_list, tag_list=None) -> tuple:
        results = []
        for photo_path in photo_path_list:
            logger.info(f"+: add_photo - {photo_path=}")
            m = PAT.search(photo_path)
            if not m:
                logger.info(
                    f"Coult not add {photo_path} as it does not match pattern")
                continue
            _path = m.group(0)
            year, month, day = [int(i) for i in _path.split('/')[:3]]
            photo = Photo(m.group(0), year, month, day)

            # _id = hashlib.sha256(
            #     photo.image_yyyymmdd_xxx.encode()).hexdigest()[-16:]
            implicit_tags = [
                f'ns0:c_day:{photo.day}', f'ns0:c_month:{photo.month}',
                f'ns0:c_year:{photo.year}'
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
                    f'Token {TAG_SERVICE_AUTH_TOKEN}'
                })
            logger.info(res01)
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