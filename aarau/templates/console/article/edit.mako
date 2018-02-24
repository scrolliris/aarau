<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Edit Article')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <%include file='aarau:templates/console/article/_breadcrumb_parent_items.mako'/>
  <a class="item" href="${req.route_path('console.article.list', namespace=project.namespace, slug=site.slug)}">Articles</a>
  <span class="divider">/</span>
  <span class="active item">Edit</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/article/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="article" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-8">
        <%
          act = req.route_path('console.article.edit', namespace=project.namespace, slug=site.slug, path=article.path)
          ctx = 'edit'
          err = ''
          obj = None
        %>
        <%include file="aarau:templates/console/article/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
