(function(d, w, name) {
  'use strict';
  // back or forward
  if (!!w.performance && w.performance.navigation.type === 2) {
    return;
  }
  d.documentElement.className = name;
  var c
    , r = (function(_d) {
      return function() {
        _d.documentElement.classList.remove(name);
      };
    })(d);
  if (d.addEventListener) {
    c = (function(_c, _d, _r) {
      return function() {
        _d.removeEventListener('DOMContentLoaded', _c, false);
        _r();
      }
    })(c, d, r);
    d.addEventListener('DOMContentLoaded', c, false);
  } else if (d.attachEvent) {
    c = (function(_c, _d, _r) {
      return function() {
        if (_d.readyState === 'complete') {
          _d.detachEvent('onreadystatechange', _c);
          _r();
        }
      }
    })(c, d, r);
    d.attachEvent('onreadystatechange', c);
  } else {
    w.onload = r;
  }
})(document, window, 'not-ready');
