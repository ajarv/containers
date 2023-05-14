import os
import re
import json
import sys
from rethink_store import RethinkClient

_RethinkClient = RethinkClient()
JPGPAT = re.compile(".*[.](jpg)$", re.IGNORECASE)

YYYYMMDDPAT = re.compile('((1999)|20[0-2]\d{1})\/\d{2}/\d{2}/.*$')


def folder_listing_json(folder):
    '''
    Generates a json listing for JPEG files
    '''
    _ofiles = []
    _folder = os.path.abspath(folder)
    _fl = len(_folder)
    for root, dirs, files in os.walk(folder):
        files = [file for file in files if JPGPAT.match(file)]
        file_paths = [
            os.path.abspath(os.path.join(root, name))[_fl:].replace('\\', '/')
            for name in files
        ]
        _ofiles += file_paths

    _ofiles = [_ofile for _ofile in _ofiles if YYYYMMDDPAT.search(_ofile)]


    _d, _fn = os.path.split(folder)
    _json_file = os.path.join(_d, "{}__list.json".format(_fn))
    _ofiles.sort()
    _o = dict(total=len(_ofiles), files=_ofiles)
    with open(_json_file, 'w') as f:
        json.dump(_o, f, indent=2)

    print(f"Begin adding to Rethink DB")
    for ix in range(0, len(_ofiles), 256):
        result = _RethinkClient.add_photo(_ofiles[ix:ix + 256])
    print(f"Completed indexing - {folder}")


if __name__ == '__main__':
    folder_listing_json(sys.argv[1])
