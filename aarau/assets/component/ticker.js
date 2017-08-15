'use strict';

import Component from 'inferno-component';
import h from 'inferno-hyperscript';

import './ticker.styl';


class Ticker extends Component {
  constructor(props) {
    super(props)
    this.state = {
      publications: 0
    , articles: 0
    }
  }

  render() {
    return h('p', null, [
      h('span', null, [(new Date()).toUTCString()])
    , h('span', null, [
      this.state.publications, ' publications, '
    , this.state.articles, ' articles;'
    ])
    , 'Scrolliris — Found 2017'
    ])
  }
}

module.exports = Ticker;
