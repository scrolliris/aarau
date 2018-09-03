<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <%def name="link_to(route_name, text)">
    % if util.route_name == route_name:
    <a class="active item" href="${req.route_url(route_name, namespace=project.namespace, slug=site.slug)}">${text}</a>
    % else:
    <a class="item" href="${req.route_url(route_name, namespace=project.namespace, slug=site.slug)}">${text}</a>
    % endif
  </%def>

  ${link_to('console.site.overview', 'Overview')}
  ${link_to('console.site.insights', 'Insights')}
  <a class="disabled item">Downloads</a>
  ${link_to('console.site.settings', 'Settings')}

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
