#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (c)  2015 Denny Wang (wangliang8@hisense.com)
# License: Hisense Cloud
'''
this file will be used to generate the vod poster for masterview, all data
will be parsed from the json format data.

Note, only the first Facet will be postered when there is more than one
Facet in one Tile
'''

import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import json
import jinja2
import launcher_monitor
from datetime import datetime, timedelta

from utils import (info, debug, err, errtrace,
                   export_poster_list_js, validate_pic)
from launcher_monitor import data_initialize, handle_argv
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)
import api_module
import settings

def gen_caro_html_code(top, left, width, height, image_list, title_list, link_list, index):
    caro_id = "myCarousel-"+str(index)
    html_text_head = '''
    <div style="top: {top}px;left: {left}px; position:absolute;max-width:{width}px; max-height:{height}px" id="{caro_id}" class="carousel slide">
      <!-- 轮播（Carousel）指标 -->
      <ol class="carousel-indicators">
        <li data-target="#{caro_id}" data-slide-to="0"
            class="active"></li>
        <li data-target="#{caro_id}" data-slide-to="1"></li>
        <li data-target="#{caro_id}" data-slide-to="2"></li>
      </ol>
      <!-- 轮播（Carousel）项目 -->
      <div class="carousel-inner">
      '''
    item_text = '''
        <div class="item{active}">
        <a href={link}><img src="{pic}" alt="{title}" title="{title}" style="width:{width}px;height:{height}px;"></a>
        </div>
      '''
    #html_text_tail = '''
    #  </div>
    #  <!-- 轮播（Carousel）导航 -->
    #  <a class="carousel-control left" href="#{caro_id}"
    #     data-slide="prev">&lsaquo;</a>
    #  <a class="carousel-control right" href="#{caro_id}"
    #     data-slide="next">&rsaquo;</a>
    #</div>
    #'''
    html_text_tail = '''
      </div>
    </div>
    '''
    num = len(image_list)
    if num == 0:
        return ""
    s = ""
    isactive = True
    for i in range(0, num):
        if isactive is True:
            s += item_text.format(pic=image_list[i], active=" active",
                                  title=title_list[i], width=width,
                                  height=height, link=link_list[i])
        else:
            s += item_text.format(pic=image_list[i], active="",
                                  title=title_list[i], width=width,
                                  height=height, link=link_list[i])
        # only isactive will be true for the first item
        if isactive is True:
            isactive = False
    return html_text_head.format(top=top, left=left, width=width,
                                 height=height, caro_id=caro_id) + s + html_text_tail.format(caro_id=caro_id)

rate = 0.7
caro_seq = 0
class TileHtmlElement(object):
    #html_tag = ('''<div style="top:{top};left:{left};width:{width};height:{height};'''
    #            '''position:absolute;z-index:1;visibility:show;"><img src={pic} '''
    #            '''width={width} heigtht={height}></img></div>''')
    html_tag = ('''<div style="top:{top};left:{left};width:{width};height:{height};'''
                '''position:absolute;z-index:1;visibility:show;">'''
                '''<a href="{url}"><img src="{pic}" title="{title}" alt="{alt}" style="width:100%; height:100%"></img></a></div>''')
    def __init__(self):
        self.pos = []
        self.size = []
        self.facets = []

    def export(self):
        if len(self.facets) > 1:
            return self.export_multi_facets()
        else:
            return self.export_one_facet()

    def export_one_facet(self):
        picture = self.facets[0].pic
        title = self.facets[0].title
        alt = title
        ret, msg = validate_pic(picture)
        if not ret:
            alt += " (no picture loaded)"
        return TileHtmlElement.html_tag.format(top=self.pos[1]*rate,
                                               left=self.pos[0]*rate,
                                               width=self.size[1]*rate,
                                               height=self.size[0]*rate,
                                               pic=picture,
                                               title=title,
                                               alt=alt,
                                               url=self.facets[0].url)
    def export_multi_facets(self):
        global caro_seq
        caro_seq += 1
        image_list = []
        title_list = []
        alt_list = []
        link_list = []
        for f in self.facets:
            picture = f.pic
            title = f.title
            alt = title
            link =  f.url
            ret, msg = validate_pic(picture)
            if not ret:
                alt += " (no picture loaded)"
            image_list.append(picture)
            title_list.append(title)
            alt_list.append(alt)
            link_list.append(link)
        return gen_caro_html_code(self.pos[1]*rate,
                                  self.pos[0]*rate,
                                  self.size[1]*rate,
                                  self.size[0]*rate,
                                  image_list,
                                  title_list,
                                  link_list,
                                  caro_seq)
        

class FacetHtmlElement(object):
    def __init__(self, pic, title):
        self.pic = pic
        self.title = title
        self.link = ""

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
        return 800

    def export(self, pos):
        elements = []
        delta_pos = self.gen_pos_delta(pos)
        for tile in self.view.tiles:
            tile_html = TileHtmlElement()
            tile_html.pos = list(map(lambda x: x[0]+x[1],
                                     zip(tile.pos, delta_pos)))
            tile_html.size = tile.size
            for facet in tile.facets:
                f = FacetHtmlElement(facet.pic, facet.title)
                if facet.typecode not in api_module.api_mapping:
                    err("ViewExport::export() no typecode found in api mapping "
                        "structure: %s"%facet.typecode)
                    exit(0)
                if facet.typecode not in api_module.module_mapping:
                    errtrace("Facet::self_verify() no api module defined for "
                             "typecode %s"%facet.typecode.encode())
                    exit(0)
                cl = api_module.module_mapping[facet.typecode]
                m = cl(facet.id, facet.title)
                f.url = m.export_html(settings.POSTER_HOME, settings.override)
                om_output("Facet %s export html %s"%(facet.title, f.url))
                if f.url is False:
                    f.url = "#"

                tile_html.facets.append(f)
            elements.append(tile_html)

        s = ""
        for e in elements:
            s += e.export() + "\n"
        return s
        

if __name__ == "__main__":
    handle_argv()
    settings.set_module_name("HTML_EXPORT_%s"
                             %(settings.VENDER))
    # setting the static file prefix for different vender
    if settings.VENDER.lower().find('wasu') != -1:
        settings.set_file_prefix('w_')
    elif settings.VENDER.lower().find('cntv') != -1:
        settings.set_file_prefix('c_')
    else:
        settings.set_file_prefix('un_')
    data_initialize()
    x = 10
    y = 80
    s = ""
    for view in settings.master_views:
        v = ViewExport(view)
        s += v.export([x, y])
        y += v.get_whole_height()

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = "poster.tpl"
    template = templateEnv.get_template(template_file)
    output = template.render(content=s, create_time=str(datetime.now())[:19])
    fname = os.path.join(settings.POSTER_HOME, 'poster_%s.html'%settings.VENDER)
    fd = open(fname, 'w')
    fd.write(output)
    info("write result to %s successfully"%fname)
    fd.close()
    export_poster_list_js()
    info("Done")

    
