class Cookie {
  static write(name, value, minutes) {
    let expires = '';
    let date = new Date();
    date.setTime(date.getTime() + (minutes * 60 * 1000));
    expires = 'expires=' + date.toUTCString();
    document.cookie = name + '=' + value + '; ' + expires + '; path=/';
    return value;
  }

  static read(name) {
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; ++i) {
      let c = ca[i];
      while (c.charAt(0) === ' ') {
        c = c.substring(1, c.length);
      }
      if (c.indexOf(name + '=') === 0) {
        return c.substring(name.length + 1, c.length);
      }
    }
  }

  static delete(name) {
    this.write(name, undefined, -4320); // -3 * 24 * 60 (3days ago)
  }
}

module.exports = Cookie;
