<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="top content">
  <div class="top grid">
    <div class="heading row">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="center">
        ${render_notice()}
      </div>
    </div>

    <div class="banner row">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="center">
        <a href="${req.route_url('top', subdomain=None)}"><img class="logo" width="48" height="48" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
        <h1 class="logo"><span class="logo-type inverse"><span class="scroll">Scroll</span><span class="iris">iris</span></span></h1>
        <p class="description">Publication platform which utilizes text readability analysis.</p>
        <div class="list">
          <a class="link" href="https://log.scrolliris.com/">Learn about recent updates</a>
        </div>
      </div>
    </div>

    <div class="main row">
      <div class="offset-4 column-8 offset-v-2 column-v-12 column-l-16" align="center">
        <div class="menu">
          <div class="item container">
            <a class="grouped primary flat button" href="https://about.scrolliris.com/" target="_blank">About</a>
            <a class="grouped flat button" href="https://help.scrolliris.com/" target="_blank">Support</a>
          </div>
          <div class="item container">
            % if not req.user:
            <a class="positive flat button" href="https://try.scrolliris.com/" target="_blank">Demo</a>
            % endif:
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

        <div id="ticker" class="pride"></div>
        <form id="search_form" class="form" action="${req.route_url('search', subdomain='registry')}" method="GET">
          <div class="field">
            <input id="q" type="text" name="q" placeholder="Title,Abstract">
          </div>
          <input type="submit" class="primary flat button" value="Search">
          <p>&nbsp;Or&nbsp;</p>
          % if not req.user:
          <a class="link" href="${req.route_path('project.new')}">Create a Project</a>,&nbsp;
          % endif
          <a class="link" href="${req.route_url('search', subdomain='registry')}">Check the Registry</a>
        </form>
      </div>

    </div>

    <div class="content row">
      <div class="column-16" align="center">
        % if not req.user or req.user.projects:
        <div class="offset-5 column-6 offset-v-2 column-v-12 column-l-16">
          <div class="warn message">
            <h5 class="header">NOTE</h5>
            <div class="description">
              <p>Scrolliris is developed by <a href="https://lupine-software.com/">Lupine Software LLC</a>. It's still <span class="secondary label">PUBLIC BETA</span>. If you have any questions, please contact us <a href="mailto:support@scrolliris.com">support@scrolliris.com</a></p>
              <p></p>
            </div>
          </div>
        </div>
        % endif
      </div>
    </div>

  </div>
</div>
