<%block name='header'>
<header>
  <div class="top menu">
    <a href="${req.route_url('top', namespace=None)}">
      <h1 class="logo item">
        <img class="logo-mark" width="26" height="26" src="${util.static_url('img/scrolliris-logo-fbfaf8-64x64.png')}">
        <span class="logo-type"><span class="scroll">Scroll</span><span class="iris">iris</span></span>
      </h1>
    </a>
    % if not req.user:
      <a class="item" href="https://about.scrolliris.com/">About</a>
      <a class="item" href="https://log.scrolliris.com/" target="_blank">Changelog</a>
    % else:
      <a class="item" href="https://help.scrolliris.com/" target="_blank">Help</a>
    % endif

    <nav class="right menu">
      % if req.user:
        % if req.user.projects:
          <a class="mobile hidden item" href="${req.route_url('console.top')}">Console</a>
        % endif
        <a class="item${' active' if util.route_name.startswith('settings') else ''}" href="${req.route_url('settings')}">Settings</a>
        <a class="item" href="${req.route_url('logout')}">Log out</a>
      % else:
        % if not req.path.startswith('/signup'):
          <a class="item" href="${req.route_url('signup')}">Sign up</a>
        % endif
        <a class="item" href="${req.route_url('login')}">Log in</a>
      % endif
    </nav>
  </div>
</header>

<div class="global-message${' user' if req.user else ''}">
% if not req.user:
  <p>Extend your Publication <i class="_r">R</i><i class="_e">e</i><i class="_a">a</i><i class="_d">d</i><i class="_a">a</i><i class="_b">b</i><i class="_i">i</i><i class="_l">l</i><i class="_i">i</i><i class="_t">t</i><i class="_y">y</i></p>
% else:
  <p class="user">Ahoj! If you have any questions, Please contact us support@scrolliris.com</p>
% endif
</div>
</%block>
