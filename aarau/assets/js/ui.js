'use strict';

import { render } from 'inferno';
import h from 'inferno-hyperscript';
import Ticker from '../component/ticker';

var ticker = document.getElementById('ticker');
if (ticker !== null) {
  render(h(Ticker), ticker);
}
