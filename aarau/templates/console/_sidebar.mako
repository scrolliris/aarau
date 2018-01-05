<div class="sidebar">
  <div class="item">
    <a href="${req.route_url('console.top')}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
  </div>
  <a class="item${' active' if util.route_name.startswith('console.project') or util.route_name == 'console.top' else ''}" href="${req.route_path('console.top')}">Projects</a>
  <a class="disabled item" href="#">Preferences</a>
  <a class="disabled item" href="#">Feedback</a>
  <hr>
  <a class="item" href="${req.route_url('top', subdomain=None)}">Scrolliris Top</a>
  <a class="item" href="${req.route_url('settings', subdomain=None)}">Account Settings</a>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
