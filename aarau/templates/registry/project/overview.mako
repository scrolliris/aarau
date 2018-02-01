<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/registry/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div id="project" class="content">
  <div class="grid">

    <div class="row">
      <div class="offset-3 column-10">
        ${render_notice()}
      </div>
    </div>

    <div class="row" align="left">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16 breadcrumb">
        <span class="item">${project.name}</span>
        <span class="diviber">/</span>
        <span class="item">Overview</span>
      </div>
    </div>

    <div class="row">
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

        <div class="tabbed menu">
        % if site_type == 'application':
          <a class="item" href="${req.route_path('project.overview', namespace=project.namespace, _query={'type': 'publication'})}">HOSTED</a>
          <span class="item active">INTEGRATED</span>
        % else:
          <span class="item active">HOSTED</span>
          <a class="item" href="${req.route_path('project.overview', namespace=project.namespace, _query={'type': 'application'})}">INTEGRATED</a>
        % endif
        </div>

        % for site in sites:
          % if site.type == 'application':
            <div class="flat application site box">
              <a href="${req.route_path('site.overview', namespace=project.namespace, slug=site.slug)}">
                <h5 class="header">${util.truncate(site.instance.name, length=25)}</h5></a>
              <div class="description">
                <p class="note">Registered @&nbsp;<span class="basic lined label date">${site.instance.created_at.strftime('%Y-%m-%d %H:%M')}</span></p>
                <p>${util.truncate(site.instance.description, length=120)}</p>
              </div>
            </div>
          % else:
            <div class="flat publication site box">
              <a href="${req.route_path('site.overview',  namespace=project.namespace, slug=site.slug)}">
                <h5 class="header">${util.truncate(site.instance.name, length=25)}</h5></a>
              <span class="date">${site.instance.created_at.strftime('%Y-%m-%d %H:%M')}</span>
              <span class="classification">${util.truncate(site.instance.classification.name, length=85)}</span>
              <div class="description">
                <p class="note">Published As&nbsp;<span class="primary label">${site.instance.license.identifier}</span>
                  @&nbsp;<span class="secondary lined label date">${site.instance.created_at.strftime('%Y-%m-%d %H:%M')}</span></p>
                <p>${util.truncate(site.instance.description, length=120)}</p>
              </div>
            </div>
          % endif
        % endfor
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
