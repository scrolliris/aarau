import { linkEvent } from 'inferno.js';
import Component from 'inferno-component.js';
import h from 'inferno-hyperscript.js';


import './paginator.styl';


let range = (j, k) => {
  return Array
    .apply(null, Array((k - j) + 1))
    .map((_, n) => { return n + j; });
}


let handleClick = (instance, event) => {
  event.preventDefault();
  let page = Number.parseInt(
    String(event.target.id).replace(/[^0-9]*/gi, ''), 10);
  instance.state.page = page;
  // call parent's handleClick
  return instance.props.handleClick.event.call(
    instance, instance.props.handleClick.data, page);
}


class Paginator extends Component {
  constructor(props) {
    super(props);
    this.state = {
      page: 1  // active page
    };
  }

  _linkTo(page, isActive) {
    if (isActive === undefined) {
      isActive = false;
    }
    let attributes = {
      id: 'page_' + page
    , onClick: linkEvent(this, handleClick)
    };
    if (isActive) {
      attributes['class'] = 'item active';
    }
    return h('a', attributes, page);
  }

  componentDidMount() {
    this.setState({
      page: this.props.page
    });
  }

  render() {
    const {pageCount, pageWindow} = this.props
    const {page} = this.state;

    if (pageCount === 1) {
      return;
    }

    let list = [];
    let startPage = Math.max(page - pageWindow, 1);
    if (startPage < 4) {
      startPage = 1;
    } else {
      list = [
        h('li', {class: 'item'}, this._linkTo(1))
      , h('li', {class: 'item'}, '...')
      ];
    }
    let endPage = Math.min(page + pageWindow, pageCount);
    if ((pageCount - pageWindow) <= endPage) {
      endPage = pageCount;
    }
    list.push.apply(list, range(startPage, endPage).map(n => {
      return h('li', {class: 'item'}, this._linkTo(n, (n === this.state.page)));
    }));
    if ((pageCount - pageWindow) > (page + pageWindow)) {
      list.push.apply(list, [ // eslint-disable-line no-useless-call
        h('li', {class: 'item'}, '...')
      , h('li', {class: 'item'}, this._linkTo(pageCount))
      ]);
    }
    return h('ul', {class: 'pagination'}, list);
  }
}

module.exports = Paginator;
