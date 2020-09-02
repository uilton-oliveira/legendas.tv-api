#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from .utils import legendastv
from guessit import guessit
from guessit.jsonutils import GuessitEncoder
import operator


def guess(filename):
    output = guessit(filename)
    jobj = json.dumps(output, indent=4, cls=GuessitEncoder, ensure_ascii=False).encode('utf-8')
    return jobj


def choose_best(list, filename):
    predict = guessit(filename)
    rating = {}

    for i, leg in enumerate(list):
        predict_cmp = guessit(leg.lower())
        leg_lower = leg.lower()

        if 'release_group' in predict and predict['release_group'].lower() in leg_lower:
            rating[i] = rating.get(i, 0) + 7

        if 'screen_size' in predict and predict['screen_size'].lower() in leg_lower:
            rating[i] = rating.get(i, 0) + 3

        if ('format' in predict_cmp and 'format' in predict and predict_cmp['format'] == predict['format']) \
                or ('format' in predict and predict['format'].lower() in leg_lower):
            rating[i] = rating.get(i, 0) + 1

        if ('video_codec' in predict_cmp and 'video_codec' in predict and predict_cmp['video_codec'] == predict['video_codec']) \
                or ('video_codec' in predict and predict['video_codec'].lower() in leg_lower):
            rating[i] = rating.get(i, 0) + 2

        print('[{0}] Score: {1}'.format(i, rating.get(i, 0)))

    if rating:
        best_match = max(rating.iteritems(), key=operator.itemgetter(1))[0]

        if rating[best_match] >= 7:
            print("Melhor resultado: ", str(best_match))
            return list[best_match]

        else:
            print("Melhor nao tem o mesmo release_group...")
            return ''
    else:
        print("TODOS 0 (empate geral)")
        return ''


def auto_detect(filename):
    predict = guessit(filename)

    if predict['type'] == 'episode':
        if 'episode' in predict:
            search_term = "{} S{:02d}E{:02d}".format(predict['title'], predict['season'], predict['episode'])
        else:
            search_term = "{} S{:02d}".format(predict['title'], predict['title'])

    else:
        if 'year' in predict:
            search_term = "{} {}".format(predict['title'], predict['year'])
        else:
            search_term = "{}".format(predict['title'])

    result = search(search_term, 1)

    result = json.loads(result)

    result['type'] = predict['type']
    if predict['type'] == 'episode':
        season = "{:02d}".format(predict['season'])
        result['season'] = str(season)

        if 'episode' in predict:
            episode = "{:02d}".format(predict['season'])
            result['episode'] = str(episode)

        result['title'] = predict['title']
    else:
        if 'year' in predict:
            result['year'] = predict['year']

    best_match = []

    rating = {}
    if result['legendas'] and len(result['legendas']) > 1:
        for i, leg in enumerate(result['legendas']):
            predict_cmp = guessit(leg['nome'].lower() + ".srt")
            leg_lower = leg['nome'].lower()

            if ('release_group' in predict_cmp and 'release_group' in predict and predict_cmp['release_group'].lower()
                == predict['release_group'].lower()) \
                    or 'release_group' in predict and predict['release_group'].lower() in leg_lower:
                rating[i] = rating.get(i, 0) + 7

            if 'screen_size' in predict and predict['screen_size'].lower() in leg_lower:
                rating[i] = rating.get(i, 0) + 3

            if ('format' in predict_cmp and 'format' in predict and predict_cmp['format'] == predict['format']) \
                    or ('format' in predict and predict['format'].lower() in leg_lower):
                rating[i] = rating.get(i, 0) + 1

            if ('video_codec' in predict_cmp and 'video_codec' in predict and predict_cmp['video_codec'] == predict['video_codec']) \
                    or ('video_codec' in predict and predict['video_codec'].lower() in leg_lower):
                rating[i] = rating.get(i, 0) + 2

            print('[{}] Score: {}'.format(i, rating.get(i, 0)))

        if rating:
            best_match = max(rating.items(), key=operator.itemgetter(1))[0]
            print("Melhor resultado: ", str(best_match))
            best = result['legendas'][best_match]
            best_list = []

            if type(best) is list:
                best_list = best
            else:
                best_list.append(best)

            result['legendas'] = best_list
            print(result['legendas'])
        else:
            result['legendas'] = result['legendas'][0]

    jobj = json.dumps(result, indent=4, ensure_ascii=False).encode('utf-8')
    return jobj


def search(search_term, page=1):
    show_list = []
    page = int(page)

    if search_term:
        result = legendastv.search(search_term, page)
        if result:
            show_list += result['list']
        else:
            result = {'descricao': '', 'poster': '', 'titulo': '', 'mais_paginas': '0'}

    else:
        result = {'descricao': '', 'poster': '', 'titulo': '', 'mais_paginas': '0'}

    jsdict = {'legendas': show_list, 'descricao': result['descricao'], 'poster': result['poster'], 'titulo': result['titulo'],
              'mais_paginas': result['mais_paginas']}

    jobj = json.dumps(jsdict, indent=4, ensure_ascii=False).encode('utf-8')
    return jobj






