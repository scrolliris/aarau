<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Edit Application')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="active item">Edit Site</span>
</div>
</%block>

<div id="publication" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-9">
        ${render_notice()}

        <h2 class="header">Edit Site</h2>
        <p class="description"></p>
        <%
          act = req.route_url('console.site.application.edit', project_id=project.id, id=site.id, _query={'type':'application'})
          ctx = 'edit'
          err = ''
        %>
        <%include file="aarau:templates/console/site/_form.mako" args="f=form, act=act, ctx=ctx, err=err"/>
      </div>
    </div>
  </div>
</div>
