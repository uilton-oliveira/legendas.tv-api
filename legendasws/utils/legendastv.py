#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
from . import util


def search(search, page=1, load_description=True):
    page_template = ""
    page = int(page)
    if page > 1:
        page_template = f"/-/{page}"

    url = f"http://legendas.tv/util/carrega_legendas_busca/{urllib.parse.quote(search)}/1{page_template}"
    source = urllib.request.urlopen(url).read().decode('utf-8')
    result = util.searchcut(source, '<div class="middle', '<div class="clear">')
    load_more = source.find("load_more") > 0
    load_more = "1" if load_more else "0"
    start_pos = 0
    title = ""
    description = ""
    img = ""
        
    show_list = []

    ret2 = util.searchcut(source, '<div class="f_left"><p><a href="', '</a>', start_pos)
    if ret2['pos'] == -1:
        return None

    loaded_description = False
    if page > 1:
        loaded_description = True

    while ret2['pos'] != -1:
        
        show = {}
        show_id = util.searchcut(ret2['txt'], "download/", "/")['txt']
        nome = util.searchcut(ret2['txt'], ">", "")['txt']
        download = f"http://legendas.tv/downloadarquivo/{show_id}"

        if not loaded_description and load_description:
            loaded_description = True
            url2 = f"http://legendas.tv/download/{show_id}"
            source2 = urllib.request.urlopen(url2).read().decode('utf-8')
            ret3 = util.searchcut(source2, '<section class="first">', '</section>')

            img = util.searchcut(ret3['txt'], '<img src="', '"')['txt']
            if img.find("http") == -1:
                img = f"http://legendas.tv/{img}"

            title = util.searchcut(ret3['txt'], '<h5>', '</h5>')['txt']
            description = util.searchcut(ret3['txt'], '<p>', '</p>')['txt']\
                .replace('<br>', '').replace('<br/>', '').replace('<br />', '')\
                .replace('\r', '').replace('\n', '')

        show['id'] = show_id
        show['nome'] = nome
        show['download'] = download
        show['service'] = 'Legendas.tv'

        start_pos = ret2['pos']
        ret2 = util.searchcut(source, '<div class="f_left"><p><a href="', '</a>', start_pos)
        show_list.append(show)
        
    return {'list': show_list, 'descricao': description, 'poster': img, 'titulo': title, 'mais_paginas': load_more}
