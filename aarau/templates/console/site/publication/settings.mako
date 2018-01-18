<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Site | Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <%include file='aarau:templates/console/site/publication/_breadcrumb_parent_items.mako'/>
  <span class="item active">General Settings</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/publication/_sidebar_settings.mako'/>
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
        <label class="primary rounded label">${site.domain}</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="attached header">
          <h5>Publication Settings</h5>
        </div>

        <div class="attached box">
          <%
            act = req.route_url('console.site.settings', namespace=project.namespace, slug=site.slug)
            ctx = 'edit'
            err = form.errors
            obj = site
          %>
          <%include file="aarau:templates/console/site/publication/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
        </div>
      </div>

      <div class="column-16">
      </div>
    </div>
  </div>
</div>
