import { render } from 'inferno.js';
import h from 'inferno-hyperscript.js';

import { loadI18n } from './i18n.js';
import PageTable from '../../component/console/page.js';

import handleSidebar from '../shared/_sidebar.js';


((doc) => {
  let container = doc.getElementById('page_table_container');
  if (container !== null) {
    let loadPath = doc.body.getAttribute('data-locale-file');
    loadI18n((err, t) => {
      if (err) {
        // pass
        // console.log(err)
      }
      render(h(PageTable, container.dataset), container);
    }, loadPath);
  }

  handleSidebar('console.sidebar', doc);
})(document);
