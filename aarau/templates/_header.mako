<%block name='header'>
<header>
  <div class="top menu">
    <a href="${req.route_url('top', namespace=None)}"><h1 class="item">
        <img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}" onmouseover="this.src='${util.static_url('img/scrolliris-logo-32x32.png')}';" onmouseout="this.src='${util.static_url('img/scrolliris-logo-64x64.png')}'">
        <span class="logo-type">Scrolliris</span>
    </h1></a>
    % if not req.user:
      <a class="item" href="https://about.scrolliris.com/">About</a>
    % endif
    <a class="item" href="https://log.scrolliris.com/">Changelog</a>

    <nav class="right menu">
    % if req.user:
      % if req.user.projects:
        <a class="item" href="${req.route_url('console.top')}">Console</a>
      % endif
      <a class="item${' active' if util.route_name.startswith('settings') else ''}" href="${req.route_url('settings')}">Settings</a>
      <a class="item" href="${req.route_url('logout')}">Log out</a>
    % else:
      <a class="item" href="${req.route_url('signup')}">Sign up</a>
      <a class="item" href="${req.route_url('login')}">Log in</a>
    % endif
    </nav>
  </div>
</header>
<div class="global-message">
% if not req.path.startswith('/settings'):
  Beyond the Scroll - Extend your Publication <i class="_r">R</i><i class="_e">e</i><i class="_a">a</i><i class="_d">d</i><i class="_a">a</i><i class="_b">b</i><i class="_i">i</i><i class="_l">l</i><i class="_i">i</i><i class="_t">t</i><i class="_y">y</i>
% elif req.user:
  Hoi! If you have question, Please contact us support@scrolliris.com
% endif
</div>
</%block>
