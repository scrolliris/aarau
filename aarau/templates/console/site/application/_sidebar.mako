<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

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

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
