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

    <div class="row card">
      <div class="column-3 offset-3 column-v-8 column-l-16" align="center">
        <div class="box">
          <div class="header"><h3>How it works</h3></div>
          <div class="description">
            <p>Learn how our readability analysis works.</p>
            <a class="flat button" href="https://doc.scrolliris.com/how_it_works/overview.html" target="_blank">Read Documentation</a>
          </div>
        </div>
      </div>
      <div class="column-4 column-v-8 column-l-16" align="center">
        <div class="box">
          <div class="header"><h3>Demo</h3></div>
          <div class="description">
            <p>Check our concept draft document on online. It works as a demo.</p>
            <a class="flat primary button" href="https://try.scrolliris.com" target="_blank">Try Demo</a>
          </div>
        </div>
      </div>
      <div class="column-3 column-v-8 offset-v-4 column-l-16" align="center">
        <div class="box">
          <div class="header"><h3>Our Updates</h3></div>
          <div class="description">
            <p>Scrolliris is currently under development as public beta.</p>
            <a class="flat secondary button" href="https://log.scrolliris.com/" target="_blank">Check the Log</a>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
