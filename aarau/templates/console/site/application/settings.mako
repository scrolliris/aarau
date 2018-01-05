<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Site | Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.site.application.overview', project_id=project.id, id=site.id, _query={'type': 'application'})}">${application.name}</a>
  <span class="divider">/</span>
  <span class="item active">General Settings</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/application/_sidebar_settings.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="application" class="content">
  ${render_notice()}

  <div class="grid">
    <div class="row">
      <div class="column-16">
        <h4>${application.name}</h4>
        <label class="primary rounded label">${site.domain}</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="attached header">
          <h5>Application Settings</h5>
        </div>

        <div class="attached box">
          <%
            act = req.route_url('console.site.application.settings', project_id=project.id, id=site.id, _query={'type':'application'})
            ctx = 'edit'
            err = form.errors
            obj = site
          %>
          <%include file="aarau:templates/console/site/application/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
        </div>
      </div>

      <div class="column-16">
        <div class="attached header">
          <h5>API KEYS</h5>
        </div>

        <div class="attached box">
          <div class="row">
            <div class="column-8 column-v-16">
              <h6>Project ID</h6>
              <p class="text">This is unique key for the project. All sites in your project use same value.</p>
            </div>
            <div class="column-8 column-v-16">
              <br>
              <pre>PROJECT_ID: ${project.access_key_id}</pre>
            </div>
          </div>

          <div class="row">
            <div class="column-8 column-v-16">
              <h6>API KEYs</h6>
              <p class="text">These keys are needed to put/fetch data via our API.</p>
            </div>
            <div class="column-8 column-v-16">
              <br>
              <p><label class="negative label">WRITE_KEY</label><code>${site.write_key}</code></p>
              <p><label class="positive label">READ_KEY</label><code>${site.read_key}</code></p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
