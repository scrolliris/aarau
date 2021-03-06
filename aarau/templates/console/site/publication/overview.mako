<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s}'.format(site.instance.name, project.name))}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/site/publication/_breadcrumb_parent_items.mako'/>
  <span class="item active">Overview</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/publication/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="publication" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <h4>${instance.name}</h4>
        <label class="publication label">scrolliris.com</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="tabbed menu">
          <a class="active item">Repository</a>
          <a class="disabled item">Authors</a>
        </div>
      </div>

      <div class="column-16">
      </div>
    </div>
  </div>
</div>
