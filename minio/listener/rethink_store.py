from rethinkdb import RethinkDB
from typing import NamedTuple
import hashlib
import os
import sys
import re
import logging

logger = logging.getLogger(__file__.split('/')[-1])

RETHINK_HOST = os.environ.get('RETHINK_HOST', 'localhost')


class Photo(NamedTuple):
    image_yyyymmdd_xxx: str
    year: int
    month:int
    day: int

PAT = re.compile('((1999)|20\d{2})\/\d{2}/\d{2}/.*$')
class RethinkClient:
    db_name = 'photovault'
    table_name = 'photos'
    def __init__(self) -> None:
        self.r = RethinkDB()
        self.conn = self.r.connect(RETHINK_HOST, 28015).repl()
    def ensure_db(self):
        r = self.r
        if not(r.db_list().contains(self.db_name).run()):
            r.db_create(self.db_name).run()
        r_db = r.db(self.db_name)
        if not self.table_name in r_db.table_list().run():
            r_db.table_create(self.table_name).run()
    def add_photo(self,photo_path_list) -> tuple:
        doc_list = []
        for photo_path in photo_path_list:
            m = PAT.search(photo_path)
            if not m:
                logger.info(f"Coult not add {photo_path} as it does not match pattern")
                continue
            _path = m.group(0)
            year,month,day = [int(i) for i in _path.split('/')[:3]]
            photo = Photo(m.group(0),year,month,day)
            _id = hashlib.sha256(photo.image_yyyymmdd_xxx.encode()).hexdigest()[-16:]
            d = photo._asdict()
            d['id'] = _id
            doc_list.append(d)

        r = self.r
        result = r\
            .db(self.db_name)\
            .table(self.table_name)\
            .insert(doc_list,conflict= 'update').run(self.conn)
        logger.info('Inserted document(s) - %s',result)
        if result['inserted'] == 0:
            return False,result
        return True,None


if __name__ == "__main__":
    _RethinkClient = RethinkClient()
    rval = _RethinkClient.add_photo(sys.argv[1])
    print(rval)