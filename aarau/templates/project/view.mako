<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16" align="center">
        <div class="row" align="left">
          <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16 breadcrumb">
            <a class="item" href="${req.route_path('top')}">Top</a>
            <span class="diviber">/</span>
            <span class="item">${project.name}</span>
          </div>
        </div>
      </div>

      <div class="offset-3 column-7 offset-v-2 column-v-8 column-l-16">
        <div class="container">
          <div class="attached box">
            <h3 class="header">${project.name}</h3>
            <div class="description">
            </div>
            <p>${project.description}</p>
          </div>
          <div class="attached footer">
            <p><span class="primary label">${project.namespace}</span></p>
          </div>
        </div>


        <div class="tab menu">
        % if site_type == 'publication':
          <span class="item active">HOSTED</span>
          <a class="item" href="${req.route_path('project.view', namespace=project.namespace, _query={'type': 'application'})}">INTEGRATED</a>
        % else:
          <a class="item" href="${req.route_path('project.view', namespace=project.namespace)}">HOSTED</a>
          <span class="item active">INTEGRATED</span>
        % endif
        </div>

        % if site_type == 'application':
          % for site in sites:
            <% application = site.application %>
            <div class="flat application site box">
              <a href="${req.route_path('site.application.view', id=site.hosting_id)}">
                <h5 class="header">${util.truncate(application.name, length=25)}</h5></a>
              <div class="description">
                <p class="note">Registered @&nbsp;<span class="basic line label date">${application.created_at.strftime('%Y-%m-%d %H:%M')}</span></p>
                <p>${util.truncate(application.description, length=120)}</p>
              </div>
            </div>
          % endfor
        % else:
          % for site in sites:
            <% publication = site.publication %>
            <div class="flat publication site box">
              <a href="${req.route_path('site.publication.view', slug=site.slug)}">
                <h5 class="header">${util.truncate(publication.name, length=25)}</h5></a>
              <span class="date">${publication.created_at.strftime('%Y-%m-%d %H:%M')}</span>
              <span class="classification">${util.truncate(publication.classification.name, length=85)}</span>
              <div class="description">
                <p class="note">Published As&nbsp;<span class="primary label">${publication.license.identifier}</span>
                  @&nbsp;<span class="secondary line label date">${publication.created_at.strftime('%Y-%m-%d %H:%M')}</span></p>
                <p>${util.truncate(publication.description, length=120)}</p>
              </div>
            </div>
          % endfor
        % endif
      </div>

      <div class="column-3 column-v-4 column-l-16">
        <div class="container">
          <div class="group flat box" align="left">
            <h6>Members</h6>
            <ul>
            % for user in project.users:
              <li>${user.name}</li>
            % endfor
            </ul>
          </div>
          <div class="group flat box" align="left">
            <h6>Contributors</h6>
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
