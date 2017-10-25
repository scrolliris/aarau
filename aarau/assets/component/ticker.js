import Component from 'inferno-component.js';
import h from 'inferno-hyperscript.js';

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
    , 'Scrolliris — Found 2017'
    ])
  }
}

module.exports = Ticker;
