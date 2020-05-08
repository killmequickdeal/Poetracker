import requests
import time
import sys
import re
import psycopg2
import os

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'poetracker',
            'USER': 'postgres',
            'PASSWORD': 'crinkle',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


class Sniper:
    def __init__(self):
        self.DEBUG = True
        self.League = "Delirium"

    def run(self):
        url_api = "http://www.pathofexile.com/api/public-stash-tabs?id="
        r = requests.get("http://poe.ninja/api/Data/GetStats")
        next_change_id = r.json().get('next_change_id')
        print(next_change_id)

        conn = psycopg2.connect(host=DATABASES['default']['HOST'], database=DATABASES['default']['NAME'],
                                user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'],
                                port=DATABASES['default']['PORT'])
        cur = conn.cursor()
        item_sql = """INSERT INTO itemviewer_item(icon, league, name, typeline, ilvl, note)
                        VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;"""
        category_sql = """INSERT INTO itemviewer_categories(name, item_id)
                        VALUES(%s, %s);"""
        property_sql = """INSERT INTO itemviewer_property(mod, type, item_id)
                        VALUES(%s, %s, %s);"""

        timeout = 60
        start_time = time.time()
        while time.time() < start_time + timeout:
            try:
                params = {'id': next_change_id}
                r = requests.get(url_api, params=params)

                data = r.json()

                next_change_id = data['next_change_id']

                for stash in data['stashes']:
                    lastCharacterName = stash['lastCharacterName']
                    items = stash['items']
                    stashName = stash.get('stash')

                    # scan items
                    for item in items:
                        note = item.get('note', None)
                        if note:
                            icon = item.get('icon', None)
                            league = item.get('league', None)
                            name = item.get('name', None)
                            typeline = item.get('typeLine', None)
                            ilvl = str(item.get('ilvl', None))
                            implicits = item.get('implicitMods', None)
                            explicits = item.get('explicitMods', None)
                            crafted = item.get('craftedMods', None)
                            extended = item.get('extended')
                            category = extended['category']

                            try:

                                cur.execute(item_sql, (icon, league, name, typeline, ilvl, note,))
                                item_id = cur.fetchone()[0]
                                if implicits:
                                    for implicit in implicits:
                                        cur.execute(property_sql, (implicit, "I", item_id))
                                if explicits:
                                    for explicit in explicits:
                                        cur.execute(property_sql, (explicit, "E", item_id))
                                if crafted:
                                    for craft in crafted:
                                        cur.execute(property_sql, (craft, "C", item_id))

                                cur.execute(category_sql, (category, item_id,))
                                if 'subcategories' in extended:
                                    for subcategory in extended['subcategories']:
                                        cur.execute(category_sql, (subcategory, item_id,))

                                conn.commit()
                            except Exception as e:
                                print(e)
                                conn.rollback()




                # wait 5 seconds until parsing next structure
                # time.sleep(0)
            except KeyboardInterrupt:
                sys.exit(1)

        conn.close()

LegionSniper = Sniper()
LegionSniper.run()