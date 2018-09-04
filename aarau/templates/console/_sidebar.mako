<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>

  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <a class="item${' active' if util.route_name.startswith('console.project') or util.route_name == 'console.top' else ''}" href="${req.route_path('console.top')}">Projects</a>
  <a class="disabled item" href="#">Preferences</a>
  <a class="disabled item" href="#">Feedback</a>

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
