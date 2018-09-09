import { linkEvent, Component } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import crossfilter from 'crossfilter.js';
import * as d3  from 'd3.js';

import { i18n } from '../../js/console/i18n.js';

import './metrics.styl';


function makeChart(id, options) {
  // inner chart object
  function chart(div) {
    let width = options.x.range()[1]
      , height = options.y.range()[0]
      ;

    options.y.domain([0, options.group.top(1)[0].value]);
    options.brush.extent([[0, 0], [width, height]]);

    div.each(function() {
      let div = d3.select(this)
        , g = div.select('g')
        ;

      if (g.empty()) {
        let m = options.margin;

        div.select('.title')
          .append('a')
          .attr('href',
            'javascript:reset(' // eslint-disable-line no-script-url
            + id + ')')
          .attr('class', 'reset')
          .text('reset')
          .style('display', 'none');

        g = div.append('svg')
            .attr('width', width + m.left + m.right)
            .attr('height', height + m.top + m.bottom)
            .append('g')
              .attr('transform', 'translate(' + m.left + ',' + m.top + ')');

        g.append('clipPath')
          .attr('id', 'clip_' + id)
          .append('rect')
            .attr('width', width)
            .attr('height', height);

        g.selectAll('.bar')
          .data(['background', 'foreground'])
          .enter()
          .append('path')
            .attr('class', function(d) { return d + ' bar'; })
            .datum(options.group.all());

        g.selectAll('.foreground.bar')
          .attr('clip-path', 'url(#clip_' + id + ')');

        g.append('g')
          .attr('class', 'axis')
          .attr('transform', 'translate(0,' + height + ')')
          .call(options.axis);

        var brush = g.append('g').attr('class', 'brush').call(options.brush);
        brush.selectAll('rect').attr('height', height);
      }

      if (options.brushDirty) {
        options.brushDirty = false;
        g.selectAll('.brush').call(options.brush);

        let isEmpty = (d3.event === null || d3.event.selection === null);
        div.select('.title a').style('display', isEmpty ? 'none' : null);

        if (isEmpty) {
          g.selectAll('#clip_' + id + ' rect')
            .attr('x', 0)
            .attr('width', width);

          // workarround for brush clear
          g.select('.brush .selection').style('display', 'none');
        } else {
          // get values as range from selection
          let selection = d3.event.selection;
          let values = selection.map(options.x.invert, options.x);

          // clip-path
          g.select('#clip_' + id + ' rect')
            .attr('x', selection[0])
            .attr('width', selection[1] - selection[0]);
        }
      }

      g.selectAll('.bar').attr('d', function(groups) {
        let path = []
          , i = -1
          , n = groups.length
          , d
          ;
        while (++i < n) {
          d = groups[i];
          path.push('M', options.x(d.key), ',', height, 'V',
                    options.y(d.value), 'h9V', height);
        }
        return path.join('');
      });
    });
  }

  // brush events
  options.brush.on('start.chart', function() {
    var div = d3.select(this.parentNode.parentNode.parentNode);
    div.select('.title a').style('display', null);
  });

  options.brush.on('brush.chart', function() {
    var g = d3.select(this.parentNode);

    // get values as range from selection
    let selection = d3.event.selection;
    let values = selection.map(options.x.invert, options.x);

    // clip-path
    g.select('#clip_' + id + ' rect')
      .attr('x', selection[0])
      .attr('width', selection[1] - selection[0]);

    options.dimension.filterRange(values);
  });

  options.brush.on('end.chart', function() {
    if (d3.event.selection === null) {
      var div = d3.select(this.parentNode.parentNode.parentNode);
      div.select('.title a').style('display', 'none');
      div.select('#clip_' + id + ' rect')
        .attr('x', null)
        .attr('width', '100%');
      options.dimension.filterAll();
    }
  });

  chart.margin = function(_) {
    if (!arguments.length) return options.margin;
    options.margin = _;
    return this;
  };

  chart.x = function(_) {
    if (!arguments.length) return options.x;
    options.x = _;
    options.axis.scale(options.x);
    d3.brushX(options.x);
    return this;
  }

  chart.y = function(_) {
    if (!arguments.length) return options.y;
    options.y = _;
    return this;
  }

  chart.dimension = function(_) {
    if (!arguments.length) return options.dimension;
    options.dimension = _;
    return this;
  }

  chart.filter = function(_) {
    // TODO: fix brush selection/clear
    if (_) {
      d3.selection.call(
        options.brush.move, [options.x(_[0]), options.x(_[1])]);

      options.dimension.filterRange(_);
    } else {
      // clear brush
      d3.selection.call(options.brush.move, null);

      options.dimension.filterAll();
    }
    options.brushDirty = true;
    return this;
  }

  chart.group = function(_) {
    if (!arguments.length) return options.group;
    options.group = _;
    return this;
  }

  chart.round = function(_) {
    if (!arguments.length) return options.round;
    options.round = _;
    return options.round;
  }

  let rebind = function(source, target, method) {
    return function() {
      let value = source[method].apply(source, arguments);
      return value === source ? target : value;
    };
  }
  chart.on = rebind(options.brush, chart, 'on');
  return chart;
}

class BarChart {
  constructor(id, values) {
    this.id = id;
    this.values = values;

    this.options = {
      margin: {top: 32, right: 24, bottom: 24, left: 24}
    , x: d3.scaleLinear()
    , y: d3.scaleLinear().range([100, 0])
    , axis: d3.axisBottom().scale(this.y)
    , id: 0
    , brush: d3.brushX()
    , brushDirty: false
    , dimension: null
    , group: null
    , round: null
    };
  }

  timeOfDay() {
    return makeChart(this.id, this.options)
      .dimension(this.values.hour)
      .group(this.values.hours)
      .x(d3.scaleLinear().domain([0, 24]).rangeRound([0, 10 * 25]));
  }

  duration() {
    return makeChart(this.id, this.options)
      .dimension(this.values.duration)
      .group(this.values.durations)
      .x(d3.scaleLinear().domain([0, 1800]).rangeRound([0, 10 * 35]));
  }

  rate() {
    return makeChart(this.id, this.options)
      .dimension(this.values.rate)
      .group(this.values.rates)
      .x(d3.scaleLinear().domain([0, 100]).rangeRound([0, 10 * 25]));
  }

  date() {
    let today = new Date()
      , start = new Date(today.getTime())
      ;
    start.setMonth(start.getMonth() - 3);

    return makeChart(this.id, this.options)
      .dimension(this.values.date)
      .group(this.values.dates)
      .x(d3.scaleTime()
        .domain([start, today])
        .rangeRound([0, 10 * 90])
        .nice());
  }
}

function renderChart(data) {
  let formatNumber = d3.format(',d');

  // filter log data
  let parseTime = d3.timeParse('%Y%m%d%H%M%S');
  data.forEach(function(d, i) {
    d.index = i;
    d.date = parseTime(d.date)
    d.duration = +d.duration;
    d.rate = +d.rate;
  });

  let logs = crossfilter(data);
  let all = logs.groupAll()
    , date = logs.dimension(function(d) { return d.date })
    , hour = logs.dimension(function(d) {
        return d.date.getHours() + d.date.getMinutes() / 60;
      })
    , duration = logs.dimension(function(d) {
        return Math.max(0, Math.min(1800, d.duration));
      })
    , rate = logs.dimension(function(d) {
        return Math.max(0, Math.min(100, d.rate));
      })
    ;

  let values = {
    logs
  , all
  , date
  , dates: date.group(d3.timeDay)
  , hour
  , hours: hour.group(Math.floor)
  , duration
  , durations: duration.group(function(d) { return Math.floor(d / 10) * 10; })
  , rate
  , rates: rate.group(function(d) { return Math.round(d, -1); })
  };

  let chartArray = [
    new BarChart('0', values).timeOfDay()
  , new BarChart('1', values).duration()
  , new BarChart('2', values).rate()
  , new BarChart('3', values).date()
  ];

  // charts
  var charts = d3.selectAll('.chart')
    .data(chartArray)
    .each(function(chart) {
      chart.on('brush', renderAll).on('end', renderAll);
    });

  // counts
  d3.select('#totals').text(
    formatNumber(logs.size()));

  renderAll();

  function render(method) {
    d3.select(this).call(method);
  }

  function renderAll() {
    charts.each(render);
    d3.select('#active').text(
      formatNumber(values.all.value()));
  }

  // global interface
  window.filter = function(filters) {
    filters.forEach(function(d, i) {
      chartArray[i].filter(d);
    });
    renderAll();
  }

  window.reset = function(i) {
    chartArray[i].filter(null);
    renderAll();
  }
}

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
                        '/' + this.props.slug + '/insights/metrics.json';
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
    if (typeof data === undefined || data === null) {
      return h('.info.message', null, [
        h('h6', null, i18n.t('metrics.empty.message.title'))
      , h('p', null, i18n.t('metrics.empty.message.description'))
      ]);
    } else if (data.length !== 0) {
      let nights = `javascript:filter([
[20, 24], null, null, null
]);`
        , resetAll = `javascript:filter([
null, null, null, null
])`
        ;
      return  h('#metrics', null, [
        // eslint-disable-line no-script-url
        h('.filters', null, [
          h('span.primary.label', null, 'FILTERS')
        , h('a.nights', {href: nights}, 'Nights')
        , h('a.reset-all', {href: resetAll}, 'Reset all')
        ])
      , h('aside.totals-count', null, [
          h('span#active', null, '-')
        , 'of'
        , h('span#totals', null)
        , 'logs selected'
        ])
      , h('.charts', null, [
          h('#chart_0.chart', null,
            h('.title', null, i18n.t('metrics.title.time_of_day')))
        , h('#chart_1.chart', null,
            h('.title', null, i18n.t('metrics.title.total_duration')))
        , h('#chart_2.chart', null,
            h('.title', null, i18n.t('metrics.title.finish_reading_rate')))
        , h('#chart_3.chart', null,
            h('.title', null, i18n.t('metrics.title.date')))
        ])
      ]);
    }
  }
}

module.exports = Metrics;
