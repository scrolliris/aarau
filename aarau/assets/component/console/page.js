import { linkEvent, Component } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import { i18n } from '../../js/console/i18n.js';

import Paginator from './paginator.js';

import './page.styl';


class API {
  constructor(url) {
    this.url = url;
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


let handlePageLinkClick = (instance, page) => {
  if (page !== instance.state.page) {
    // NOTE: instance.setState({page}) won't work here.
    instance.update(page);
  }
};


class PageTable extends Component {
  constructor(props) {
    super(props);
    this.props['url'] = '/api/' + this.props.namespace +
                        '/' + this.props.slug + '/insights.json';
    this.props['pageWindow'] = 2;
    this.state = {
      data: []
    , page: 1
    , pageCount: 1
    };
  }

  componentDidMount() {
    this.update();
  }

  update(page) {
    let url = this.props.url;
    let { data, pageCount } = this.state;
    if (page === undefined) {
      page = this.state.page;
    }
    if (page !== 1) {
      url = url + '?page=' + Number.parseInt(page, 10);
    }
    let api = new API(url);
    api.fetch().then((res) => {
      if ('data' in res) { data = res['data']; }
      if ('page' in res) { page = res['page']; }
      if ('page_count' in res) { pageCount = res['page_count']; }
      this.setState({
        data
      , page
      , pageCount
      });
    }).catch((reason) => {
      // pass
      //console.log(reason.status);
    });
  }

  _linkTo(pageId, text) {
    // TODO: set link to page view
    return text;
  }

  render() {
    const url = this.props.url;
    const { data, page, pageCount } = this.state;
    if (!data) {
      return h('.info.message', null, [
        h('h6', null, i18n.t('page.empty.message.title'))
      , h('p', null, i18n.t('page.empty.message.description'))
      ]);
    } else {
      return h('div', null, [
        h('table', {'class': 'bordered table'}, [
          h('thead', null,
            h('tr', null, [
              h('th', i18n.t('page.table.header.path'))
            , h('th', i18n.t('page.table.header.paragraph'))
            , h('th', i18n.t('page.table.header.total_count'))
            ])
          )
        , h('tbody', null,
            data.map(row => {
              return h('tr', [
                h('td', null, this._linkTo(row.code, row.path))
              , h('td', null, this._linkTo(row.code, row.paragraph_numbers))
              , h('td', null, this._linkTo(row.code, row.total_count))
              ]);
            })
          )
        ])
      , h('div', null, h(Paginator, {
          url: url
        , page: page // current page
        , pageWindow: this.props.pageWindow
        , pageCount: pageCount // total page count
        , handleClick: linkEvent(this, handlePageLinkClick)
        }))
      ]);
    }
  }
}

module.exports = PageTable;
