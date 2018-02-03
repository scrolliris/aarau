<%block name='header'>
% if req.path != req.route_path('top'):
<header>
  <div class="menu">
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
        % if req.user.memberships:
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
% endif

<div class="global-message${' user' if req.user else ''}">
% if not req.user:
  <p>Increase your Text Readability</p>

% else:
  <div id="ticker" class="pride"></div>
% endif
</div>
</%block>
