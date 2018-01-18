<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Edit Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_url('console.project.overview', namespace=project.namespace)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="active item">Edit</span>
</div>
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-8">
        <%
          act = req.route_path('console.project.edit', namespace=project.namespace)
          ctx = 'edit'
          err = ''
          obj = project
        %>
        <%include file="aarau:templates/console/project/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
