/**
 *
 *
 * @return String query string
 */
function buildQueryString(data) {
  let params = [];
  for (let d in data) {
    if (data.hasOwnProperty(d)) {
      params.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    }
  }
  return params.join('&');
}

/**
 * e.g.
 *   - progress_state -> progressState
 *   - title -> title
 *
 * @return String (camelCase)
 */
function toCamelCase(s) {
  return s.split('_').map((w, i) => {
    if (i === 0) { return w.toLowerCase(); }
    return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
  }).join('');
}

module.exports = { buildQueryString, toCamelCase };
