#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# Copyright (c)  2015 Denny Wang (wangliang8@hisense.com)
# License: Hisense Cloud
'''
this file will be used to generate the vod poster for masterview, all data
will be parsed from the json format data.

Note, only the first Facet will be postered when there is more than one
Facet in one Tile
'''

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import re
import os
import json
import jinja2
import urlparse
import pycurl
import launcher_monitor
from datetime import datetime, timedelta

from utils import info, debug, err, errtrace, export_poster_list_js
from launcher_monitor3 import data_initialize, handle_argv
import api_module
import settings

iqiyi_re = re.compile(r'qiyipic')



class TileHtmlElement(object):
    #html_tag = ('''<div class="divcss5" style="top:{top};left:{left};width:{width};height:{height};'''
    #            '''position:absolute;z-index:1;visibility:show; '''
    #            '''background:url({pic}) no-repeat; background-size:100% 100%">'''
    #            '''<span>{text}</span></div>''')
    html_tag = ('''<div style="top:{top};left:{left};width:{width};height:{height};'''
                '''position:absolute;z-index:1;visibility:show;">'''
                '''<a href="{url}"><img src="{pic}" title="{title}" style="width:100%;height:100%"></img></a></div>''')
    def __init__(self):
        self.pos = []
        self.size = []
        self.facets = []

    def export(self):
        # if the picture is from iqiyi, save it to local disk
        picture = self.facets[0].pic
        m = iqiyi_re.search(picture)
        if m:
            picture = settings.dump_pic(picture)
            
        return TileHtmlElement.html_tag.format(top=self.pos[1],
                                               left=self.pos[0],
                                               width=self.size[1],
                                               height=self.size[0],
                                               pic=picture,
                                               title=self.facets[0].title,
                                               url=self.facets[0].url)
        

class FacetHtmlElement(object):
    def __init__(self, pic, title):
        self.pic = pic
        self.title = title
        self.url = ""

class ViewExport(object):
    def __init__(self, view_obj):
        self.view = view_obj

    def get_pos(self):
        ''' actually just get the pos of the first element '''
        if len(self.view.tiles) == 0:
            err("ViewExport::get_pos() view %s has no tiles"%view.name)
            exit(0)
        return (self.view.tiles[0].pos[0], self.view.tiles[0].pos[1])

    def gen_pos_delta(self, new_pos):
        ''' generate the position delta for position you want to actually
        have and the position in the master_view data, the delta will apply
        to all the posters '''
        pos1 = self.get_pos()
        delta_pos = list(map(lambda x: x[0]-x[1], zip(new_pos, pos1))) 
        return delta_pos

    def get_whole_height(self):
        ''' a tricky way to only return a fixed height, because i
        just know it '''
        return 320

    def export(self, pos):
        if len(self.view.tiles) == 0:
            return ""
        cell = 3
        elements = []
        i = 0
        x = pos[0]
        for tile in self.view.tiles:
            tile_html = TileHtmlElement()
            tile_html.pos = [x, pos[1]]
            x += view.tiles[i].size[1] + cell
            i += 1
            tile_html.size = tile.size
            for facet in tile.facets:
                f = FacetHtmlElement(facet.pic, facet.title)
                if facet.typecode not in api_module.api_mapping:
                    err("ViewExport::export() no typecode found in api"
                        "mapping structure: %s"%facet.typecode)
                    exit(0)

                if facet.typecode not in api_module.module_mapping:
                    errtrace("Facet::self_verify() no api module defined for "
                             "typecode %s"%facet.typecode.encode())
                    exit(0)
                cl = api_module.module_mapping[facet.typecode]
                m = cl(facet.id)
                f.url = m.export_html(override=False)
                if f.url is False:
                    f.url = "#"
                else:
                  #f.url = m.export_html(override=True)
                  f.url += "?uuid=%s"%str(settings.uuid)
                tile_html.facets.append(f)
            elements.append(tile_html)

        s = ""
        for e in elements:
            s += e.export() + "\n"
        return s

if __name__ == "__main__":
    handle_argv()
    data_initialize()
    x = 10
    y = 60
    s = ""
    html_title = ('''<div style="top:{0}; left:{1};position:absolute;z-index:1;visibility:show;"><span>{2}</span></div>''')
    for view in settings.master_views:
        v = ViewExport(view)
        vstr = v.export([x, y+20])
        if len(vstr) == 0:
            continue
        s += html_title.format(y, x, view.name)
        y += 20
        
        s += vstr
        y += v.get_whole_height()

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = "poster.tpl"
    template = templateEnv.get_template(template_file)
    output = template.render(content=s, create_time=\
                             str(datetime.now()+timedelta(hours=8))[:19])
    fname = os.path.join(settings.WEB_HOME,
                         "poster_%s_%s.html"%(settings.VENDER.lower(), settings.uuid))
    fd = open(fname, 'w')
    fd.write(output)
    info("write result to %s successfully"%fname)
    fd.close()
    export_poster_list_js()
    info("Done")