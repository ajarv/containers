


TAG_SERVICE_HOST=libra TAG_SERVICE_AUTH_TOKEN=efdc792bcdaadc420d2c0ea680173b73d682c6d4 python tags_service.py 2021/09/25/PICT_20210925_083146.JPG  'ns0:location:11339 Florindo Rd' ns0:event:fun 'ns0:person:Ajar Vashisth'


curl 'http://libra:8000/api/obj/' -X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: Token efdc792bcdaadc420d2c0ea680173b73d682c6d4' \
--data-raw '{"key": "2021/09/25/PICT_20210925_083146.JPG", "tags": ["ns0:c_day:25", "ns0:c_month:9", "ns0:c_year:2021", "ns0:location:backyard", "ns0:event:fun", "ns0:person:Ajar Vashisth"]}'
