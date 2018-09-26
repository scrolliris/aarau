import { render } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import { loadI18n } from './i18n.js';

// components
import ClassificationTree from
  '../../component/console/classification_tree.js';
import Metrics from '../../component/console/metrics.js';
import PageTable from '../../component/console/page.js';
import ArticleEditorForm from '../../component/console/article_editor_form.js';
import ArticleSettingsForm from '../../component/console/article_settings_form.js';

import handleSidebar from '../shared/_sidebar.js';
import handleToolbar from '../shared/_toolbar.js';


((doc) => {
  if (doc === undefined || doc === null ||
      doc.body === null) {
    return;
  }

  let loadPath = doc.body.getAttribute('data-locale-file');
  if (loadPath !== null) {
    loadI18n((err, t) => {
      if (err) {
        // pass
        // console.log(err)
      }

      { // publication settings
        let container = doc.getElementById('classification_tree');
        if (container !== null) {
          render(h(ClassificationTree, container.dataset), container);
        }
      }

      { // application insights (metrics)
        let container = doc.getElementById('metrics_container');
        if (container !== null) {
          render(h(Metrics, container.dataset), container);
        }
      }

      { // application insights (logs)
        let container = doc.getElementById('logs_container');
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

      {  // article settings form
        let container = doc.getElementById('article_settings_form_container');
        if (container !== null) {
          render(h(ArticleSettingsForm, container.dataset), container);
        }
      }
    }, loadPath);
  }

  handleSidebar('console.sidebar', doc);
  handleToolbar(doc);
})(document);
