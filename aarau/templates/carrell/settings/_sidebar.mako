<div class="sidebar">
  <% locked = cookie.get('carrell.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <h6 class="section-title">ACTIONS IN CARRELL</h6>
  <a class="item${' active' if util.route_name.startswith('carrell.bookmark') or util.route_name == 'carrell.top' else ''}" href="${req.route_path('carrell.top')}">Bookmarks</a>
  <a class="disabled item" href="#">Preferences</a>

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
      ${link_to('carrell.settings', 'Account')}
      ${link_to('carrell.settings.section', 'Email', matchdict={'section': 'email'})}
      ${link_to('carrell.settings.section', 'Password', matchdict={'section': 'password'})}
    </span>
  </span>

  <hr>
  <h6 class="section-title">LEAVE CARRELL</h6>
  % if req.user.projects:
  <a class="item" href="${req.route_url('console.top')}">
    Console
    <span class="description">writing space</span>
  </a>
  % endif
  <a class="item" href="${req.route_url('top', subdomain=None)}">
    Publication Registry
    <span class="description">search & browse stats</span>
  </a>
</div>
