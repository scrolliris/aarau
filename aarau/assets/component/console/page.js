import Component from 'inferno-component.js';
import h from 'inferno-hyperscript.js';

import { i18n } from '../../js/console/i18n.js';

import './page.styl';


class API {
  constructor(projectId, siteId) {
    this.url = this._buildURL(projectId, siteId);
  }

  _buildURL(projectId, siteId) {
    return '/api/project/' + projectId + '/site/' + siteId + '/result.json';
  }

  fetch(isAsync) {
    if (isAsync === undefined) {
      isAsync = true;
    }
    return new Promise((resolve, reject) => {
      let xhr = new XMLHttpRequest();
      xhr.open('GET', this.url, isAsync);
      xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          return resolve(JSON.parse(xhr.responseText || '{}'));
        } else {
          return reject({
            status: xhr.status
          , statusText: xhr.statusText
          });
        }
      };
      xhr.onerror = () => {
        return reject({
          status: xhr.status
        , statusText: xhr.statusText
        });
      };
      xhr.send();
    });
  }
}


class PageTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }

  componentDidMount() {
    let api = new API(this.props.projectId, this.props.siteId);
    api.fetch().then((res) => {
      let data = [];
      if ('data' in res) {
        data = res['data'];
      }
      this.setState({
        data
      });
    }).catch((reason) => {
      // pass
      // console.log(reason.status);
    });
  }

  _buildPageURL(pageId) {
    return '/project/' + this.props.projectId + '/site/' +
      this.props.siteId + '/page/' + pageId;
  }

  _linkTo(pageId, text) {
    // TODO: set link to page view
    //return h('a', {'href': this._buildPageURL(pageId)}, text);
    return text;
  }

  render() {
    if (!this.state.data) {
      return h('.info.message', null, [
        h('h6', null, i18n.t('pageEmptyMessageTitle'))
      , h('p', null, i18n.t('pageEmptyMessageDescription'))
      ]);
    } else {
      return h('table', {'class': 'bordered table'}, [
        h('thead', null,
          h('tr', null, [
            h('th', i18n.t('page.table.header.path'))
          , h('th', i18n.t('page.table.header.paragraph'))
          , h('th', i18n.t('page.table.header.total_count'))
          ])
        )
      , h('tbody', null,
          this.state.data.map(row => {
            return h('tr', [
              h('td', null, this._linkTo(row.code, row.path))
            , h('td', null, this._linkTo(row.code, row.paragraph_numbers))
            , h('td', null, this._linkTo(row.code, row.total_count))
            ]);
          })
        )
      ]);
    }
  }
}

module.exports = PageTable;
