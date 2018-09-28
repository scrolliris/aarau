import { linkEvent, Component } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import { TreeSelect } from 'inferno-tree-select.js';

import './classification_tree.styl';


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


class ClassificationTree extends Component {
  constructor(props) {
    super(props);
    this.props['url'] = '/api/projects/' + this.props.namespace +
      '/sites/' + this.props.slug + '/classifications/tree.json';
    this.state = {
      data: []
    };
  }

  componentWillMount() {
    this.fetch();
  }

  componentDidMount() {
  }

  componentDidUpdate() {
    const { data } = this.state;

    if (typeof data !== undefined && data !== null && data.length !== 0) {
      renderChart(data);
    }
  }

  fetch() {
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
    const { data } = this.state;
    const { selected } = this.props;

    if (typeof data === undefined || data === null || data.length === 0) {
      return  h('.loader', null);
    } else if (data.length !== 0) {
      return h(TreeSelect, {
        options: data
      , selected: selected
      , onSelect: (node) => {
          let input = document.querySelector('#publication_classification');
          input.value = node.value;
        }
      });
    }
  }
}

module.exports = ClassificationTree;
