const express = require('express');
const legendastv = require('../providers/legendastv');
const router = express.Router();

router.get('/:searchTerm/:page?', (req, res, next) => {
  legendastv.search(req.params.searchTerm, req.params.page || 1)
      .then(result => {
        res.json(result);
      })
});

module.exports = router;
