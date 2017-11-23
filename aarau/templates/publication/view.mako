<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="content">
  <div class="grid">

    <div class="row publication">
      <div class="column-16" align="center">
        ${render_notice()}
      </div>

      <div class="offset-3 column-7 offset-v-2 column-v-8 column-l-16 site-object">
        <p><span class="rounded active label">HOSTED</span></p>

        <% publication = site.publication %>
        <div class="group flat box">
          <h3 class="header">${publication.name}</h3>
          <p class="author">${site.project.primary_owner.name}</p>
          <div class="description">
            <span class="date">${publication.created_at.strftime('%Y-%m-%d %H:%M')}</span>
            <span class="secondary label">${publication.license.identifier}</span>
          </div>
          <span class="classification">${publication.classification.name}</span>
          <p>${publication.description}</p>
        </div>
        <div class="group flat box">
          <h5>Articles</h5>
        </div>
      </div>
      <div class="column-3 column-v-4 column-l-16">
        % if not req.user:
          <div class="info message">
            <h6 class="header">CREATE A PUBLICATION</h6>
            <p class="description">Publish your articles, get reading intensity, and increase text readability.
              <a href="${req.route_path('signup')}">Signup</a> now, or <a href="${req.route_path('login')}">Login</a>.</p>
          </div>
        % endif
        <div class="container">
          <div class="group flat box" align="left">
            <p>${publication.copyright}</p>
          </div>
          <div class="group flat box" align="left">
            <h6>Languages</h6>
            <p><span class="rounded secondary label">English</span></p>
          </div>
          <div class="group flat box" align="left">
            <h6>Authors</h6>
          </div>
          <div class="group flat box" align="left">
            <h6>Dates</h6>
            <p class="description">
              <span class="label">CREATED</span>
              ${publication.updated_at.strftime('%Y-%m-%d %H:%M')}
            </p>
            <p class="description">
              <span class="label">UPDATED</span>
                ${publication.updated_at.strftime('%Y-%m-%d %H:%M')}
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
