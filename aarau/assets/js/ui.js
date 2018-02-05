import { render } from 'inferno.js';
import h from 'inferno-hyperscript.js';

import Ticker from '../component/ticker.js';


var ticker = document.getElementById('ticker');
if (ticker !== null) {
  render(h(Ticker), ticker);
}

var searchForm = document.getElementById('search_form');
if (searchForm !== null) {
  searchForm.onsubmit = function(e) {
    var q = document.getElementById('q');
    if (q === undefined || q === null ||
        q.value === null || q.value === '') {
      e.preventDefault();
      return false;
    }
  }
}
