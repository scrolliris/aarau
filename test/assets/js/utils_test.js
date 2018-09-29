import {
  buildQueryString, toCamelCase
} from '../../../aarau/assets/js/shared/_utils.js';

QUnit.testDone(function() {
  // pass
});

QUnit.test('Returns query params as string', function(assert) {
  let value;

  value = buildQueryString({foo: 1, bar: 2});
  assert.ok('foo=1&bar=2' === value, 'query string');

  value = buildQueryString({'?foo': 'bar', '/baz': 'qux'});
  assert.ok('%3Ffoo=bar&%2Fbaz=qux' === value, 'encodeURIComponent for keys');

  value = buildQueryString({foo: '/', bar: '?'});
  assert.ok('foo=%2F&bar=%3F' === value, 'encodeURIComponent for values');
});

QUnit.test('Converts under_score_case to cammelCase', function(assert) {
  let value;

  value = toCamelCase('progress_state');
  assert.ok('progressState' === value, 'under_score to camelCase');

  value = toCamelCase('title');
  assert.ok('title' === value, 'don\'t change lower case only word');
});
