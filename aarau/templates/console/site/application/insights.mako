<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s} - {:s}'.format(_('title.application.insights'), site.instance.name, project.name))}</%block>
<%block name='body_attr'> data-locale-file="${req.util.static_url('{}')|unquote,formatting('locale/{{lng}}/{{ns}}.json'),h}"</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/site/application/_breadcrumb_parent_items.mako'/>
  <span class="item active">Insights</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/application/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="application" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <h4>${instance.name}</h4>
        <label class="application label">${site.domain}</label>
      </div>
    </div>
    <div class="row">
      <div class="column-16">
        <div class="tabbed menu">
          <a class="${'active ' if component_type == 'metrics' else ''}item" href="?tab=metrics">Metrics</a>
          <a class="${'active ' if component_type == 'logs' else ''}item" href="?tab=logs">Logs</a>
        </div>
      </div>

      <div class="column-16">
        % if component_type == 'metrics':
        <div class="secondary message wip">
          <h4 class="header">NOTE</h4>
          <p>Metrics view/graphs is still WIP. It shows dummy records ;)</p>
        </div>
        % endif

        <div id="${component_type}_container" data-namespace="${project.namespace}" data-slug="${site.slug}"></div>
      </div>
    </div>
  </div>
</div>
