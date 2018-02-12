import { render } from 'inferno.js';
import h from 'inferno-hyperscript.js';

import Ticker from '../component/ticker.js';

import handleSidebar from './shared/_sidebar.js';


((doc) => {
  var ticker = doc.getElementById('ticker');
  if (ticker !== null) {
    render(h(Ticker), ticker);
  }

  var searchForm = doc.getElementById('search_form');
  if (searchForm !== null) {
    searchForm.onsubmit = function(e) {
      var q = doc.getElementById('q');
      if (q === undefined || q === null ||
          q.value === null || q.value === '') {
        e.preventDefault();
        return false;
      }
    }
  }

  handleSidebar('article.sidebar', doc);
})(document);
