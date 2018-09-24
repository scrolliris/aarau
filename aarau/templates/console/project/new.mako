<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('New Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <span class="active item">New</span>
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
      <div class="container column-16">
        <div class="attached header">
          <h5>New Project</h5>
        </div>

        <div class="attached box">
          <%
            act = req.route_path('console.project.new')
            ctx = 'new'
            err = ''
            obj = None
          %>
          <%include file="aarau:templates/console/project/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
        </div>
      </div>
    </div>
  </div>
</div>
