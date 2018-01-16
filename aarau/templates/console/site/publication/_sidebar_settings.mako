<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

  <a class="item" href="${req.route_path('console.site.publication.overview', project_id=project.id, id=site.id, _query={'type':'publication'})}">Overview</a>
  <a class="disabled item">Articles</a>
  <a class="disabled item">Insights</a>
  <a class="disabled item">Downloads</a>

  <span class="item active expanded">
    <%def name="link_to(route_name, text)">
      <a class="${publication_settings_item_class(route_name)}" href="${req.route_url(route_name, project_id=project.id, id=site.id, _query={'type': 'publication'})}">${text}</a>
    </%def>

    <%def name="publication_settings_item_class(route_name)">
      %if util.route_name == route_name:
        <% return 'active item' %>
      %else:
        <% return 'item' %>
      %endif
    </%def>

    <span class="item">Settings</span>
    <span class="item-container">
      ${link_to('console.site.publication.settings', 'General')}
    </span>
  </span>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
