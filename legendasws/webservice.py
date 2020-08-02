#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from .lib import legendastv
from guessit import guessit
from guessit.jsonutils import GuessitEncoder
import operator


def guess(filename):
    output = guessit(filename)
    jobj = json.dumps(output, indent=4, cls=GuessitEncoder, ensure_ascii=False).encode('utf-8')
    return jobj


def choosebest(list, filename):
    guess = guessit(filename)
    rating = {}

    for i, leg in enumerate(list):
        guessCmp = guessit(leg.lower())
        legLower = leg.lower()

        if 'release_group' in guess and guess['release_group'].lower() in legLower:
            rating[i] = rating.get(i, 0) + 7

        if 'screen_size' in guess and guess['screen_size'].lower() in legLower:
            rating[i] = rating.get(i, 0) + 3

        if ('format' in guessCmp and 'format' in guess and guessCmp['format'] == guess['format']) \
                or ('format' in guess and guess['format'].lower() in legLower):
            rating[i] = rating.get(i, 0) + 1

        if ('video_codec' in guessCmp and 'video_codec' in guess and guessCmp['video_codec'] == guess['video_codec']) \
                or ('video_codec' in guess and guess['video_codec'].lower() in legLower):
            rating[i] = rating.get(i, 0) + 2
        print('[{0}] Score: {1}'.format(i, rating.get(i, 0)))

    if rating:
        bestMatch = max(rating.iteritems(), key=operator.itemgetter(1))[0]

        if rating[bestMatch] >= 7:
            print("Melhor resultado: ", str(bestMatch))
            return list[bestMatch]

        else:
            print("Melhor nao tem o mesmo release_group...")
            return ''
    else:
        print("TODOS 0 (empate geral)")
        return ''


def autodetect(filename):
    guess = guessit(filename)

    if guess['type'] == 'episode':
        if 'episode' in guess:
            search = "{} S{:02d}E{:02d}".format(guess['title'], guess['season'], guess['episode'])
        else:
            search = "{} S{:02d}".format(guess['title'], guess['title'])

    else:
        if 'year' in guess:
            search = "{} {}".format(guess['title'], guess['year'])
        else:
            search = "{}".format(guess['title'])

    result = gerar(search, 1)

    result = json.loads(result)

    result['type'] = guess['type']
    if guess['type'] == 'episode':
        season = "{:02d}".format(guess['season'])
        result['season'] = str(season)

        if 'episode' in guess:
            episode = "{:02d}".format(guess['season'])
            result['episode'] = str(episode)

        result['title'] = guess['title']
    else:
        if 'year' in guess:
            result['year'] = guess['year']
    bestMatch = []

    rating = {}
    if result['legendas'] and len(result['legendas']) > 1:
        for i, leg in enumerate(result['legendas']):
            guessCmp = guessit(leg['nome'].lower() + ".srt")
            legLower = leg['nome'].lower()

            if ('release_group' in guessCmp and 'release_group' in guess and guessCmp['release_group'].lower() == guess[
                'release_group'].lower()) \
                    or 'release_group' in guess and guess['release_group'].lower() in legLower:
                rating[i] = rating.get(i, 0) + 7

            if 'screen_size' in guess and guess['screen_size'].lower() in legLower:
                rating[i] = rating.get(i, 0) + 3

            if ('format' in guessCmp and 'format' in guess and guessCmp['format'] == guess['format']) \
                    or ('format' in guess and guess['format'].lower() in legLower):
                rating[i] = rating.get(i, 0) + 1

            if ('video_codec' in guessCmp and 'video_codec' in guess and guessCmp['video_codec'] == guess['video_codec']) \
                    or ('video_codec' in guess and guess['video_codec'].lower() in legLower):
                rating[i] = rating.get(i, 0) + 2

            print('[{}] Score: {}'.format(i, rating.get(i, 0)))
        if rating:
            bestMatch = max(rating.items(), key=operator.itemgetter(1))[0]
            print("Melhor resultado: ", str(bestMatch))
            best = result['legendas'][bestMatch]
            bestList = []

            if type(best) is list:
                bestList = best
            else:
                bestList.append(best)

            result['legendas'] = bestList
            print(result['legendas'])
        else:
            result['legendas'] = result['legendas'][0]

    jobj = json.dumps(result, indent=4, ensure_ascii=False).encode('utf-8')
    return jobj


def gerar(search_legendastv, pagina=1):
    show_list = []
    pagina = int(pagina)

    if search_legendastv:
        lgtv = legendastv.buscar(search_legendastv, pagina)
        if lgtv:
            show_list += lgtv['list']
        else:
            lgtv = {'descricao': '', 'poster': '', 'titulo': '', 'mais_paginas': '0'}

    else:
        lgtv = {'descricao': '', 'poster': '', 'titulo': '', 'mais_paginas': '0'}

    jsdict = {'legendas': show_list, 'descricao': lgtv['descricao'], 'poster': lgtv['poster'], 'titulo': lgtv['titulo'],
              'mais_paginas': lgtv['mais_paginas']}

    jobj = json.dumps(jsdict, indent=4, ensure_ascii=False).encode('utf-8')
    return jobj






