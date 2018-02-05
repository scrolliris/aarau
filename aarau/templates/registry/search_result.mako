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
              <a class="grouped flat button" href="${req.route_url('project.new', subdomain=None)}">Create a Project</a>
            % endif
          </div>

          <div class="right menu">
            % if not req.user:
            <a class="item" href="${req.route_url('signup', subdomain=None)}">Signup</a>
            <a class="item" href="${req.route_url('login', subdomain=None)}">Login</a>
            % else:
            <a class="item" href="${req.route_url('console.top')}">Console</a>
            <a class="item" href="${req.route_url('logout', subdomain=None)}">Logout</a>
            % endif
          </div>
        </div>

        <form id="search_form" class="form" action="${req.route_url('search', subdomain='registry')}" method="GET">
          <div class="search field">
            <input id="q" type="text" name="q" value="${req.params.get('q', '')}" placeholder="Title,Abstract">
          </div>
        </form>
      </div>
    </div>

    <div class="banner row" align="center">
      <div class="offset-4 column-8 offset-v-2 column-v-12 column-l-16" align="center">
        <img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}">
      </div>
    </div>

    <div class="content row" align="center">
      <div class="offset-4 column-8 offset-v-2 column-v-12 column-l-16" align="center">
        <p>Under Development</p>
      </div>
    </div>
  </div>
</div>
