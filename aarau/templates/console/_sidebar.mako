<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

  <a class="item${' active' if util.route_name.startswith('console.project') or util.route_name == 'console.top' else ''}" href="${req.route_path('console.top')}">Projects</a>
  <a class="disabled item" href="#">Preferences</a>
  <a class="disabled item" href="#">Feedback</a>
  <hr>
  <h6 class="section-title">LEAVE CONSOLE</h6>
  <a class="item" href="${req.route_url('carrell.settings')}">Your Carrell</a>
  <a class="item" href="${req.route_url('top', subdomain=None)}">Publication Registry</a>

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
