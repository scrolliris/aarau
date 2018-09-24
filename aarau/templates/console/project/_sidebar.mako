<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  % if 'settings' not in util.route_name:
  <span class="item active expanded">
    <%def name="link_to(route_name, text)">
      %if (util.route_name == route_name):
        <a class="active item" href="${req.route_url(route_name, namespace=project.namespace)}">${text}</a>
      %else:
        <a class="item" href="${req.route_url(route_name, namespace=project.namespace)}">${text}</a>
      %endif
    </%def>

    <span class="item">Overview</span>
    <span class="item-container">
      ${link_to('console.project.overview', 'Publications')}
      <a class="disabled item">Activities</a>
    </span>
  </span>
  % else:
  ${link_to('console.project.overview', 'Overview')}
  % endif

  <a class="disabled item">Members</a>

  % if 'settings' not in util.route_name:
  ${link_to('console.project.settings', 'Settings')}
  % else:
  <span class="item active expanded">
    <span class="item">Settings</span>
    <span class="item-container">
      ${link_to('console.project.settings', 'General')}
      <a class="disabled item">Plan</a>
    </span>
  </span>
  % endif


  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
