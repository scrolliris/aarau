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
  <span class="item active">Status Badges</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/application/_sidebar_settings.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="site_badge" class="content">
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
          <h5>Status Badges</h5>
        </div>

        <div class="attached box">
          <div class="row">
            <div class="column-16 column-v-16">
              <h5 class="title">General Badges</h5>
              <h6 calss="title">STATIC</h6>
              <p class="text">These badges are static svg. You can embed it on your article to describe tracking status. Choose <code>{on|off}.svg</code>.</p>
              <p class="badges"><img src="https://img.scrolliris.com/badge/tracking/on.svg">&nbsp;<img src="https://img.scrolliris.com/badge/tracking/off.svg"></p>
              <pre>
# AsciiDoc
image:https://img.scrolliris.com/badge/tracking/off.svg[link="https://about.scrolliris.com/",title="tracking status"]

# Markdown
[![tracking status](https://img.scrolliris.com/badge/tracking/off.svg)](https://about.scrolliris.com/)

# HTML
&lt;a href="https://about.scrolliris.com/"&gt;&lt;img src="https://img.scrolliris.com/badge/tracking/off.svg" alt="tracking status"&gt;&lt;/a&gt;
</pre>

              <h6 calss="title">DYNAMIC</h6>
              <p class="text">These badges are dynamically rendered svg. The status will be changed condition or context.</p>
              <p class="badges"><code>comming soon</code></p>
            </div>
            <div class="column-16 column-v-16">
              <h5 class="title">Reading Finish Rate Badges</h5>
              <p class="text"><code>comming soon</code></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
