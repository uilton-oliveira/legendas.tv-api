const express = require('express');
const guessit = require('../providers/guessit');
const router = express.Router();

router.post('/choosebest', (req, res, next) => {
    return guessit.chooseBest(req.body.names, req.body.filename)
        .then(result => {
            res.type("text");
            res.send(result);
        })
});

router.get('/guess/:filename', (req, res, next) => {
    return guessit.guess(req.params.filename)
        .then(result => result.data)
        .then(result => {
            res.json(result);
        })
});

module.exports = router;
