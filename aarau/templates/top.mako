<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="content">
  <div class="grid">

    <div class="row landscape${' user' if req.user else ''}">
      <div class="column-16" align="center">
        ${render_notice()}

        <div class="banner">
        % if not req.user:
          <h1 class="header">Beyond the Scroll</h1>
          <p>Include just a single javascript, get anonymous tracking works, and increase readability</p>
        % endif
        % if req.user and req.user.projects:
          <a class="flat button" href="${req.route_url('console.top')}">Go to Console</a>
        % else:
          <a class="primary button" href="${req.route_url('project.new', namespace=None)}">Create a Project</a>
        % endif
        </div>
        <div id="ticker" class="pride"></div>
      </div>
    </div>

    <div class="row publication">
      <div class="offset-3 column-7 offset-v-2 column-v-8 column-l-16 site-object">
        <div class="tab menu">
          <div class="item active">Publications</div>
          <div class="disabled item">Slides</div>
        </div>

        <p>
        % if site_type == 'publication':
          <span class="rounded label publication active">HOSTED</span>
          <span class="rounded label application"><a href="${req.route_url('top', _query={'type': 'application'})}">INTEGRATED</a></span>
        % else:
          <span class="rounded label publication"><a href="${req.route_url('top')}">HOSTED</a></span>
          <span class="rounded label application active">INTEGRATED</span>
        % endif
        </p>

        % if site_type == 'application':
          % for application in site_objects:
            <div class="flat box">
              <h5 class="header">${util.truncate(application.name, 25)}</h5>
              <div class="description">
                <span class="date">${application.created_at.strftime('%Y-%m-%d %H:%M')}</span>
                <p>${util.truncate(application.description, length=120)}</p>
              </div>
            </div>
          % endfor
        % else:
          % for publication in site_objects:
            <div class="flat box">
              <h5 class="header">${util.truncate(publication.name, length=25)}</h5>
              <div class="description">
                <span class="date">${publication.created_at.strftime('%Y-%m-%d %H:%M')}</span>
                <span class="secondary label">${publication.license.identifier}</span>
                <span class="classification">${util.truncate(publication.classification.name, length=60)}</span>
                <p>${util.truncate(publication.description, length=120)}</p>
              </div>
            </div>
          % endfor
        % endif
      </div>
      <div class="column-3 column-v-4 column-l-16 card">
        <div class="flat box" align="center">
          <div class="header"><h4>How it works</h4></div>
          <div class="description">
            <p>Learn how our readability analysis works.</p>
            <a class="flat button" href="https://doc.scrolliris.com/how_it_works/overview.html" target="_blank">Read Documentation</a>
          </div>
        </div>
        <div class="warn message">
          <div class="description">
            <p>Scrolliris is currently under development as public beta.</p>
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
