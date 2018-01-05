<div class="sidebar">
  <div class="item">
    <a href="${req.route_url('console.top')}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
  </div>
  <a class="item" href="${req.route_path('console.site.application.overview', project_id=project.id, id=site.id, _query={'type': 'application'})}">Overview</a>
  <a class="item" href="${req.route_path('console.site.application.insights', project_id=project.id, id=site.id, _query={'type': 'application'})}">Insights</a>
  <a class="disabled item">Downloads</a>

  <span class="item active">
    <%def name="link_to(route_name, text)">
      <a class="${application_settings_item_class(route_name)}" href="${req.route_url(route_name, project_id=project.id, id=site.id, _query={'type': 'application'})}">${text}</a>
    </%def>

    <%def name="application_settings_item_class(route_name)">
      %if util.route_name == route_name:
        <% return 'active item' %>
      %else:
        <% return 'item' %>
      %endif
    </%def>

    <span class="item">Settings</span>
    <span class="item-container">
      ${link_to('console.site.application.settings', 'General')}
      ${link_to('console.site.application.settings.scripts', 'Measure Scripts')}
      ${link_to('console.site.application.settings.widgets', 'Heatmap Widgets')}
      ${link_to('console.site.application.settings.badges', 'Status Badges')}
    </span>
  </span>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
