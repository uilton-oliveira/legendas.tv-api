const axios = require('axios');

const instance = axios.create({
    baseURL: 'http://legendas.tv'
});

instance.defaults.headers.common['User-Agent'] = process.env.USER_AGENT || "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36";

module.exports = instance;