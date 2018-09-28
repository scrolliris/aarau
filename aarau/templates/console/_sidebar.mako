<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>

  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <a class="item${' active' if util.route_name.startswith('console.project') or util.route_name == 'console.top' else ''}" href="${req.route_path('console.top')}">Projects</a>

  % if 'console.settings' in util.route_name:
  <span class="item active expanded">
    <%def name="link_to(route_name, text, matchdict={})">
      %if util.route_name == route_name and req.matchdict == matchdict:
        <a class="active item" href="${req.route_url(route_name, **matchdict)}">${text}</a>
      %else:
        <a class="item" href="${req.route_url(route_name, **matchdict)}">${text}</a>
      %endif
    </%def>
    <span class="item">Settings</span>
    <span class="item-container">
      ${link_to('console.settings', 'Account')}
      ${link_to('console.settings.section', 'Email', matchdict={'section': 'email'})}
      ${link_to('console.settings.section', 'Password', matchdict={'section': 'password'})}
    </span>
  </span>
  % else:
  <a class="item" href="${req.route_url('console.settings')}">Settings</a>
  % endif

  <a class="disabled item" href="#">Preferences</a>
  <a class="disabled item" href="#">Feedback</a>

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
