<%inherit file='../../_layout.mako'/>

<%block name='title'>
  Site | Project | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="item active">${application.name}</span>
</div>
</%block>

<div id ="project" class="content">
  <%namespace name='msg' file='../../../shared/_message.mako'/>
  ${msg.form()}

  <div class="grid">
    <div class="row">
      <div class="column-16">
        <h3>${application.name}</h3>
        <label class="primary label">${site.domain}</label>
      </div>
    </div>
    <div class="row">
      <div class="column-16">
        <div class="tab menu">
          <a class="item" href="${req.route_path('console.site.application.view.result', project_id=project.id, id=site.id, _query={'type': 'application'})}">Results</a>
          <a class="item" href="${req.route_path('console.site.application.view.script', project_id=project.id, id=site.id, _query={'type': 'application'})}">Scripts</a>
          <a class="active item">Badges</a>
        </div>
      </div>
      <div class="column-16">
        <div class="flat box">
          <div class="row">
            <div class="column-16 column-v-16">
              <h5 class="title">General Badges</h5>
              <p class="text">These badges are static svg. You can embed it on your article to describe tracking status. (choose `{on|off}.svg`)</p>
              <p class="badges"><img src="https://badge.scrolliris.io/img/tracking/on.svg">&nbsp;<img src="https://badge.scrolliris.io/img/tracking/off.svg"></p>
              <pre>
# AsciiDoc
image:https://badge.scrolliris.io/img/tracking/off.svg[link="https://about.scrolliris.com/",title="tracking status"]

# Markdown
[![tracking status](https://badge.scrolliris.io/img/tracking/off.svg)](https://about.scrolliris.com/)

# HTML
&lt;a href="https://about.scrolliris.com/"&gt;&lt;img src="https://badge.scrolliris.io/img/tracking/off.svg" alt="tracking status"&gt;&lt;/a&gt;
</pre>
            </div>
            <div class="column-16 column-v-16">
              <h5 class="title">Reading Finish Rate Badges</h5>
              <p class="text">Comming soon</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<%block name='footer'>
</%block>
