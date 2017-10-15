<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('New Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <span class="active item">New</span>
</div>
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-8">
        ${render_notice()}

        <%
          act = req.route_path('console.project.new')
          ctx = 'new'
          # FIXME
          err = ''
          obj = None
        %>
        <%include file="aarau:templates/console/project/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
