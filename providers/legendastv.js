const axios = require('../axiosConfig');
const guessit = require('./guessit');
const querystring = require('querystring');
const cheerio = require('cheerio');


const provider = {}
provider.search = (searchTerm, page = 1, fetchExtraData = true) => {
    const pageTemplate = page <= 1 ? '' : `/-/${page}`;
    const escapedSearch = querystring.escape(searchTerm);

    return axios.get(`/util/carrega_legendas_busca/${escapedSearch}/1${pageTemplate}`)
        .then(response => {
            const $ = cheerio.load(response.data);
            let releases = [];

            $('.f_left p:not(".data") a').each((i, elem) => {
                releases.push(parseRelease(elem));
            });
            return {
                releases: releases,
                last_page: $('.load_more').length <= 0
            };
        })
}

provider.autoDetect = filename => {
    return buildSearchTerm(filename)
        .then(searchTerm => {
            return provider.search(searchTerm, 1, false)
                .then(searchResult => {
                    return searchResult;
                })
        })
        .then(searchResult => {
            return guessit.chooseBest(
                searchResult.releases.map(obj => obj.name), filename
            ).then(matched => {
                return {
                    searchResult: searchResult,
                    bestMatch: matched
                }
            })

        })
        .then(result => {
            return result.searchResult.releases.find(release => release.name === result.bestMatch);
        })

}

const parseRelease = node => {
    const href = node.attribs.href;
    const showId = href.split("/")[2];

    return {
        id: showId,
        name: cheerio.load(node).text(),
        download: `${axios.defaults.baseURL}/downloadarquivo/${showId}`
    }
}

const buildSearchTerm = filename => {
    return guessit.guess(filename)
        .then(response => response.data)
        .then(predict => {
            let searchTerm = ""
            if (predict.type === 'episode') {
                if (predict.episode) {
                    searchTerm = `${predict.title} S${String(predict.season).padStart(2, '0')}E${String(predict.episode).padStart(2, '0')}`
                } else {
                    searchTerm = `${predict.title} S${String(predict.season).padStart(2, '0')}`
                }

            } else {
                if (predict.year) {
                    searchTerm = `${predict.title} ${predict.year}`
                } else {
                    searchTerm = `${predict.title}`
                }
            }

            return searchTerm;
        })
}

module.exports = provider;