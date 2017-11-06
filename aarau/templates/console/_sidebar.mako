<div class="sidebar">
  <div class="item">
    <a href="${req.route_url('top', namespace=None)}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
  </div>
  <a class="item${' active' if util.route_name.startswith('console.project') or util.route_name == 'console.top' or req.path.startswith('/project/') else ''}" href="${req.route_path('console.top')}">Projects</a>
  <a class="disabled item" href="#">Preferences</a>
  <a class="disabled item" href="#">Feedback</a>
  <hr>
  <a class="item" href="${req.route_url('settings', subdomain='')}">Account Settings</a>

  <div class="bottom item">
    <div class="warn message">
      <h6 class="header">Scrolliris is beta!</h6>
      <p>Thank you for using us! Please send us <a href="mailto:feedback@lupine-software.com">feedback</a></p>
    </div>
  </div>
</div>
