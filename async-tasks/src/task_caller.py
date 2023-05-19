
import catalog_app

catalog_app.app.conf.update(broker_url = 'pyamqp://guest:guest@localhost:5672//')

for ix in range(2):
    catalog_app.add.apply_async((ix,ix*3))