import { linkEvent, Component } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import './metrics.styl';


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


class Metrics extends Component {
  constructor(props) {
    super(props);
    this.props['url'] = '/api/' + this.props.namespace +
                        '/' + this.props.slug + '/insights.json';
    this.state = {
      data: []
    };
  }

  componentDidMount() {
    this.update();
  }

  update() {
    let url = this.props.url;
    let { data } = this.state;
    let api = new API(url);
    api.fetch().then((res) => {
      if ('data' in res) { data = res['data']; }
      this.setState({
        data
      });
    }).catch((reason) => {
      // pass
      //console.log(reason.status);
    });
  }

  render() {
    const url = this.props.url;
    const data = this.state;
    if (!data) {
      return h('.info.message', null, [
        h('h6', null, i18n.t('metrics.empty.message.title'))
      , h('p', null, i18n.t('metrics.empty.message.description'))
      ]);
    } else {
      return h('div', null, []);
    }
  }
}

module.exports = Metrics;
