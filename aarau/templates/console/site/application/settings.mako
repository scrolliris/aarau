<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s} - {:s}'.format(_('title.settings.general'), site.instance.name, project.name))}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/site/application/_breadcrumb_parent_items.mako'/>
  <span class="item active">${_('title.settings.general')}</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/application/_sidebar_settings.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="application" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <h4>${instance.name}</h4>
        <label class="application label">${site.domain}</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="attached header">
          <h5>Application Settings</h5>
        </div>

        <div class="attached box">
          <%
            act = req.route_url('console.site.settings', namespace=project.namespace, slug=site.slug)
            ctx = 'edit'
            err = form.errors
            obj = site
          %>
          <%include file="aarau:templates/console/site/application/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
        </div>
      </div>

      <div class="column-16">
        <div class="attached header">
          <h5>API Keys</h5>
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
              <p><label class="primary label">WRITE_KEY</label><code>${site.write_key}</code></p>
              <p><label class="primary label">READ_KEY</label><code>${site.read_key}</code></p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
