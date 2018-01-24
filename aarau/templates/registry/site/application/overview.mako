<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/registry/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div id="application" class="content">
  <div class="grid">
    <% application = site.application %>

    <div class="row">
      <div class="offset-3 column-10">
        ${render_notice()}
      </div>
    </div>

    <div class="row" align="left">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16 breadcrumb">
        <a class="item" href="${req.route_path('project.overview', namespace=site.project.namespace, _query={'type': 'application'})}">${site.project.name}</a>
        <span class="diviber">/</span>
        <span class="item">${application.name}</a>
        <span class="diviber">/</span>
        <span class="item">Overview</a>
      </div>
    </div>

    <div class="row">
      <div class="offset-3 column-7 offset-v-2 column-v-8 column-l-16">
        <span class="active integrated primary label">INTEGRATED</span>

        <div class="container">
          <div class="group flat box">
            <h3 class="header">${application.name}</h3>
            <p class="author">${site.project.primary_owner.name}</p>
            <div class="description">
              <span class="date">${application.created_at.strftime('%Y-%m-%d %H:%M')}</span>
              <span class="secondary line label">${site.domain}</span>
            </div>
            <p>${application.description}</p>
          </div>
        </div>
      </div>

      <div class="column-3 column-v-4 column-l-16 right-side-bar">
        % if not req.user:
          <div class="info message">
            <h6 class="header">Create a Project</h6>
            <p class="description">Include just a single javascript, get anonymous tracking works, and increase readability.
              <a href="${req.route_path('signup')}">Signup</a> now, or <a href="${req.route_path('login')}">Login</a>.</p>
          </div>
        % endif
        <div class="container">
          <div class="group flat box" align="left">
            <h6>Languages</h6>
            <p><span class="rounded secondary label">English</span></p>
          </div>
          <div class="group flat box" align="left">
            <h6>Dates</h6>
            <p class="description">
              <span class="label">CREATED</span>
              ${application.updated_at.strftime('%Y-%m-%d %H:%M')}
            </p>
            <p class="description">
              <span class="label">UPDATED</span>
                ${application.updated_at.strftime('%Y-%m-%d %H:%M')}
            </p>
          </div>
        </div>

        <div class="container">
          <div class="attached box" align="left">
            <p><span class="positive label">Finish Reading Rate</span>&nbsp; avr. 0%</p>
            <p><span class="positive line label">Reading Intensity</span>&nbsp; 0</p>
          </div>
          <div class="attached warn message">
            <h6 class="header">NOTE</h6>
            <p>Stats based on anonymous tracking for readability analysis is under development.</p>
          </div>
        </div>

        <div class="attached header">
          <h6 class="header">Data</h6>
        </div>
        <div class="attached box" align="center">
          <div>
            <p>Open Tracking Data</p>
            <a class="disabled button">Go to data directory</a>
          </div>
        </div>
      </div>
    </div>

    <div class="row card">
      <div class="column-3 column-v-8 offset-v-4 column-l-16" align="center">
      </div>
    </div>

  </div>
</div>
