import { render } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import { loadI18n } from './i18n.js';
// components
import PageTable from '../../component/console/page.js';
import ArticleEditorForm from '../../component/console/article_editor_form.js';
import ArticleConfigForm from '../../component/console/article_config_form.js';

import handleSidebar from '../shared/_sidebar.js';
import handleToolbar from '../shared/_toolbar.js';


((doc) => {
  let loadPath = doc.body.getAttribute('data-locale-file');
  if (loadPath !== null) {
    loadI18n((err, t) => {
      if (err) {
        // pass
        // console.log(err)
      }

      { // application insights
        let container = doc.getElementById('page_table_container');
        if (container !== null) {
          render(h(PageTable, container.dataset), container);
        }
      }

      {  // article editor form
        let container = doc.getElementById('article_editor_form_container');
        if (container !== null) {
          render(h(ArticleEditorForm, container.dataset), container);
        }
      }

      {  // article config form
        let container = doc.getElementById('article_config_form_container');
        if (container !== null) {
          render(h(ArticleConfigForm, container.dataset), container);
        }
      }
    }, loadPath);
  }

  handleSidebar('console.sidebar', doc);
  handleToolbar(doc);
})(document);
