import Cookie from '../../aarau/assets/js/shared/_cookie.js';

QUnit.testDone(function() {
  Cookie.delete('key');
});


QUnit.test('return value by `write`', function(assert) {
  let value;

  value = Cookie.write('key', 'value', 1);
  assert.ok('value' === value, 'write returns value');
});


QUnit.test('return value by `read`', function(assert) {
  let value;

  value = Cookie.read('key');
  assert.ok(undefined === value, 'read returns default value');

  document.cookie = 'key=value;1;path=/';

  value = Cookie.read('key');
  assert.ok('value' === value, 'read returns value manually set');

  value = Cookie.write('key', 'value', 1);
  assert.ok('value' === value, 'write returns value');

  value = Cookie.read('key');
  assert.ok('value' === value, 'read returns value set via `write`');

  value = Cookie.write('key', 'updated', 1);
  assert.ok('updated' === value, 'write returns updated value');

  value = Cookie.read('key');
  assert.ok('updated' === value, 'read returns value updated');
});


QUnit.test('expires', function(assert) {
  let value
    , done = assert.async();

  // check if expires works
  Cookie.write('key', 'updated', 0.01);
  setTimeout(function() {
    value = Cookie.read('key');
    assert.ok(undefined === value, 'the value is not available anymore');
    done();
  }, 900);
});


QUnit.test('deletion', function(assert) {
  var value;

  Cookie.delete('key');

  value = Cookie.read('key');
  assert.ok(undefined === value, 'read returns default value');

  Cookie.write('key', 'value', 1);
  value = Cookie.read('key');
  assert.ok('value' === value, 'read returns value set via `write`');

  Cookie.delete('key');

  value = Cookie.read('key');
  assert.ok(undefined === value, 'read returns undefined after delete');
});
