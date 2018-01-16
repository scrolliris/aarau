<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('New Application')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <%include file='aarau:templates/console/site/application/_breadcrumb_parent_items.mako'/>
  <span class="active item">New Application</span>
</div>
</%block>

<%block name='sidebar'>
<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>
  <a class="item active">New Application</a>
</div>
</%block>

<div id="application" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-9">
        <p class="description">Enter your external web application (or website) which is integrated with Scrolliris&apos;s readability analysis.</p>
        <%
          act = req.route_url('console.site.application.new', project_id=project.id, _query={'type':'application'})
          ctx = 'new'
          err = form.errors
          obj = site
        %>
        <%include file="aarau:templates/console/site/application/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
