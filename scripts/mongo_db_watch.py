# This script serves as an example of how we can watch events on Mongo DB.

# pylint: disable=missing-docstring
# pylint: enable=missing-docstring
import os
import ssl
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

from flask import Flask
from flask_pymongo import PyMongo


mongo = PyMongo()  # pylint:disable=C0103


def main():
    app = Flask(__name__)
    uri = 'mongodb://{user}:{pwd}@{host}/{db}{suffix}'
    app.config["MONGO_URI"] = uri.format(
        user=os.environ.get('PYXIS_MONGO_USERNAME'),
        pwd=os.environ.get('PYXIS_MONGO_PASSWORD'),
        host=os.environ.get('PYXIS_MONGO_HOST'),
        db=os.environ.get('PYXIS_MONGO_DB', 'data'),
        suffix=os.environ.get('PYXIS_MONGO_URI_SUFFIX', '?authSource=admin'),
    )

    mongo.init_app(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE, ssl_match_hostname=False)

    collections = [
        mongo.db.containerImage,
        mongo.db.containerRepository,
        mongo.db.containerVendor,
    ]
    futures = []
    with ThreadPoolExecutor(max_workers=len(collections)) as executor:
        for colection in collections:
            futures.append(executor.submit(watch, colection))
        for future in futures:
            print(future.result())


def watch(collection):
    print('Watching: {}'.format(collection))
    cursor = collection.watch()
    while True:
        pprint(next(cursor))
        print('-' * 100)


if __name__ == "__main__":
    main()
