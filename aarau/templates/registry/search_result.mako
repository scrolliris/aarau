<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/registry/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="registry content">
  <div class="registry grid">

    <div class="main row">
      <div class="offset-4 column-8 offset-v-2 column-v-12 column-l-16" align="center">
        ${render_notice()}

        <div class="menu">
          <div class="item container">
            <a class="grouped secondary flat button" href="${req.route_url('top', namespace=None)}" title="Back to Toppage">←&nbsp;&nbsp;Back</a>
            % if not req.user:
              <a class="grouped flat button" href="${req.route_url('project.new', subdomain='None')}">Create a Project</a>
            % endif
          </div>

          <div class="right menu">
            % if not req.user:
            <a class="item" href="${req.route_url('signup', subdomain=None)}">Signup</a>
            <a class="item" href="${req.route_url('login', subdomain=None)}">Login</a>
            % endif
          </div>
        </div>

        <form id="search_form" class="form" action="${req.route_path('registry.search', subdomain='registry')}" method="GET">
          <div class="search field">
            <input id="q" type="text" name="q" value="${req.params.get('q', '')}" placeholder="Title,Abstract">
          </div>
        </form>
      </div>
    </div>

    % if pq:
    <div class="content row" align="center">
      <div class="offset-4 column-8" align="center">
        <span class="search-result-count">Found ${pq.total_count} Publication(s)</span>
      </div>

      <div class="offset-4 column-8 offset-v-2 column-v-12 column-l-16" align="center">
        % for site in pq.get_objects():
          % if site.publication:
            <% publication = site.publication %>
          <div class="embedded flat box" align="left">
            <a href="${req.route_path('registry.site.overview', namespace=site.project.namespace, slug=site.slug)}">
            <h5 class="title">${util.truncate(publication.name, length=80)}</h5>
            <p class="description">${util.truncate(publication.description, length=200)}</p>
            <span class="url">${req.route_url('registry.site.overview', namespace=site.project.namespace, slug=site.slug)}</span>
            </a>
          </div>
          % endif
        % endfor

        % if pq.page_count > 1:
        <div class="pagination">
          % if not pq.prev_page:
            <span class="prev item">Prev</span>
          % else:
            <a class="prev item" href="?q=${req.params.get('q')}&page=${pq.prev_page}">Prev</a>
          % endif

          % if not pq.next_page:
            <span class="next item">Next</span>
          % else:
            <a class="next item" href="?q=${req.params.get('q')}&page=${pq.next_page}">Next</a>
          % endif
        </div>
        % endif
      </div>
    </div>
    % endif
  </div>
</div>
