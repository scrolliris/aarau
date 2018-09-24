<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Project Settings')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_url('console.project.overview', namespace=project.namespace)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="active item">Settings</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/project/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="attached header">
          <h5>Project Settings</h5>
        </div>

        <div class="attached box">
          <%
            act = req.route_path('console.project.settings', namespace=project.namespace)
            ctx = 'edit'
            err = ''
            obj = project
          %>
          <%include file="aarau:templates/console/project/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
        </div>
      </div>
    </div>
  </div>
</div>
