<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s} - {:s}'.format(_('title.chapter.tree'), site.instance.name, project.name))}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/chapter/_breadcrumb_parent_items.mako'/>
  <span class="item active">${chapter.name}</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/chapter/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="chapter" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-8">
        <h4>${site.instance.name}</h4>
        <label class="publication label">scrolliris.com</label>
      </div>
      <div class="column-8" align="right">
        <a class="primary flat disabled button" href="${req.route_path('console.chapter.new', namespace=project.namespace, slug=site.slug)}" disabled=disabled>New Chapter</a>
      </div>
    </div>

    <div class="row">
      <div class="chapter-list column-16"></div>
    </div>
  </div>
</div>
