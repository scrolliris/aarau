<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="content">
  <div class="grid">

    <div class="row landscape${' user' if req.user else ''}">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-16" align="center">
        ${render_notice()}

        % if not req.user:
          <div class="banner">
            <h1 class="header">Beyond the Scroll</h1>
            <p>Include just a single javascript, get anonymous tracking works, and increase readability</p>
            <a class="primary button" href="${req.route_path('project.new', namespace=None)}">Create a Project</a>
          </div>
        % endif
      </div>
    </div>

    <div class="row site">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16">
        <div class="warn message">
          <h5 class="header">NOTE</h5>
          <div class="description">
            <p>Scrolliris is currently under development as public beta. If you have any questions, please contact us <a href="mailto:support@scrolliris.com">support@scrolliris.com</a></p>
          </div>
        </div>
      </div>

      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16">
        <div class="tab menu">
        % if site_type == 'publication':
          <span class="item active">HOSTED</span>
          <a class="item" href="${req.route_path('top', _query={'type': 'application'})}">INTEGRATED</a>
        % else:
          <a class="item" href="${req.route_path('top')}">HOSTED</a>
          <span class="item active">INTEGRATED</span>
        % endif
        </div>

        % if site_type == 'publication':
          <p class="description">Hosted publications on <code>scrolliris.com</code></p>
          <div class="row">
          % for site in sites:
            <% publication = site.publication %>
            <% project = site.project %>

            <div class="column-4 column-v-8 column-l-8 column-s-16">
              <div class="flat publication box" align="left">
                <div class="cover">COMMING SOON</div>
                <span class="primary label">${publication.license.identifier}</span>
                <div class="meta">
                  <span class="date">${publication.created_at.strftime('%Y-%m-%d %H:%M')}</span>
                  <a href="${req.route_path('site.publication.view', slug=site.slug)}"><h5 class="header">${project.name}&nbsp;/&nbsp;${util.truncate(publication.name, length=25)}</h5></a>
                  <span class="classification">${util.truncate(publication.classification.name, length=55)}</span>
                </div>
                <div class="description">
                  <p>${util.truncate(publication.description, length=40)}</p>
                </div>
              </div>
            </div>
          % endfor
          </div>
        % endif

        % if site_type == 'application':
          <p class="description">External applications which is integrated Scrolliris's measure script and heatmap widget.</p>
          <div class="row">

          ## TODO
          <div class="column-4 column-v-8 column-l-8 column-s-16">
            <div class="flat application box" align="left">
              <div class="cover">doc.scrolliris.com</div>

              <div class="meta">
                <span class="date">2017-07-07 10:00</span>
                <a href="https://doc.scrolliris.com/how_it_works/overview.html"><h5 class="header">Scrolliris / How it works</h5></a>
              </div>
              <div class="description">
                <p class="note">Learn how our readability analysis works.</p>
              </div>
            </div>
          </div>

          % for site in sites:
            <% application = site.application %>
            <% project = site.project %>

            <div class="column-4 column-v-8 column-l-8 column-s-16">
              <div class="flat application box" align="left">
                <div class="cover">${site.domain}</div>
                <div class="meta">
                  <span class="date">${application.created_at.strftime('%Y-%m-%d %H:%M')}</span>
                  <a href="${req.route_path('project.view', namespace=project.namespace, _query={'type': 'application'})}"><h5 class="header">${project.name}&nbsp;/&nbsp;${util.truncate(application.name, length=25)}</h5></a>
                </div>
                <div class="description">
                  <p>${util.truncate(application.description, length=65)}</p>
                </div>
              </div>
            </div>
          % endfor
          </div>
        % endif
      </div>
    </div>
  </div>
</div>
