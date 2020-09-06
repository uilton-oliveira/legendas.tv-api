const axios = require('../axiosConfig');
const querystring = require('querystring');

const baseUrl = process.env.GUESSIT_HOST || "http://localhost:5000";

const provider = {}
provider.guess = filename => {
    return axios.get(`${baseUrl}?${querystring.encode({
        filename: filename
    })}`);
}

provider.batch = filenames => {
    return axios.post(`${baseUrl}/list`, {
        filename: filenames
    });
}

provider.chooseBest = (names = [], filename) => {
    if (names.length <= 1) {
        return Promise.resolve(names.shift());
    }

    const match = (src, dst, key) => {
        return src[key] && dst[key] && String(src[key]).toLowerCase() === String(dst[key]).toLowerCase();
    }

    return provider.batch([filename, ...names])
        .then(result => result.data)
        .then(data => {
            const base = data.shift();
            const scoreResult = [];

            data.forEach((el, i) => {
                let score = 0;
                score += match(base, el, 'season') ? 20 : 0;
                score += match(base, el, 'episode') ? 20 : 0;
                score += match(base, el, 'release_group') ? 7 : 0;
                score += match(base, el, 'screen_size') ? 3 : 0;
                score += match(base, el, 'format') ? 1 : 0;
                score += match(base, el, 'video_codec') ? 2 : 0;
                score += match(base, el, 'source') ? 2 : 0;
                score += match(base, el, 'audio_codec') ? 1 : 0;
                score += match(base, el, 'audio_channels') ? 1 : 0;

                scoreResult.push({
                    score: score,
                    release: names[i]
                })
            });

            return scoreResult
                .sort(((a, b) => b.score - a.score))
                .shift()
                .release;

        })
}

module.exports = provider;