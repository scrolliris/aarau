import { render } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import handleSidebar from '../shared/_sidebar.js';


((doc) => {
  handleSidebar('carrell.sidebar', doc);
})(document);
