const express = require('express');
const legendastv = require('../providers/legendastv');
const router = express.Router();

router.get('/:filename', (req, res, next) => {
  legendastv.autoDetect(req.params.filename)
      .then(result => {
        res.json(result || {});
      })
});

module.exports = router;
