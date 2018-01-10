<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

  <%def name="link_to(route_name, text)">
    <a class="${application_item_class(route_name)}" href="${req.route_url(route_name, project_id=project.id, id=site.id, _query={'type': 'application'})}">${text}</a>
  </%def>

  <%def name="application_item_class(route_name)">
    %if util.route_name == route_name:
      <% return 'active item' %>
    %else:
      <% return 'item' %>
    %endif
  </%def>

  ${link_to('console.site.application.overview', 'Overview')}
  ${link_to('console.site.application.insights', 'Insights')}
  <a class="disabled item">Downloads</a>
  ${link_to('console.site.application.settings', 'Settings')}

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
