<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('New Application')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <%include file='aarau:templates/console/site/publication/_breadcrumb_parent_items.mako'/>
  <span class="active item">New Publication</span>
</div>
</%block>

<%block name='sidebar'>
<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>
  <a class="item active">New Publication</a>
</div>
</%block>

<div id="publication" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-9">
        ${render_notice()}
        <p class="description">Create new publication which is published on Scrolliris.</p>
        <%
          act = req.route_url('console.site.publication.new', project_id=project.id, _query={'type':'publication'})
          ctx = 'new'
          err = form.errors
          obj = site
        %>
        <%include file="aarau:templates/console/site/publication/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
