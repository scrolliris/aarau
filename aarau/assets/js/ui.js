import { render } from 'inferno.js';
import h from 'inferno-hyperscript.js';

import Ticker from '../component/ticker.js';


var ticker = document.getElementById('ticker');
if (ticker !== null) {
  render(h(Ticker), ticker);
}
