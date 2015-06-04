#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import time
from core.mydb import Mydb

detail_page_url = "http://api.vod.jamdeocloud.com/medias/api/media/{0}"
# medias database
medias_db = Mydb()
medias_db.connect('repository')
medias_db_session = medias_db.open("all_medias")

class VodMedia():
    def __init__(self, mediaid):
        self.id = mediaid
        self.data =None
        self.title = 'anonymous'
        self.category_id = None
        self.country = 'None'
        self._fill()

    def _fill_with_local(self):
        media = medias_db_session.select({"mediaid": self.id})
        if media is None:
            return False
        self.title = media[1][1]
        self.category_id = media[1][2]
        self.country = media[1][3]
        return True
        
    def _fill_with_remote(self):
        time.sleep(0.1)
        url = detail_page_url.format(self.id)
        #print "fetch_media_data::VodMedia::_fill() url", url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            rsp_data = response.read()
            self.data = json.loads(rsp_data)
            self.title = self.data['title'].encode('utf-8')
            self.category_id = self.data['category_id']
            self.country = self.data['country'].encode('utf-8')
        except:
            pass
        
    def _fill(self):
        if self._fill_with_local():
            return
        else:
            self._fill_with_remote()
            if self.category_id is None:
                return
            try:
                medias_db_session.insert({"mediaid": self.id,
                                          "title": self.title,
                                          "categoryid": self.category_id,
                                          'country': self.country})
                medias_db_session.commit()
            except:
                print "fail to insert mediaid", self.id

    def get_title(self):
        return self.title

    def get_category_id(self):
        return self.category_id

    def get_country(self):
        return self.country
