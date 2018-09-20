<div class="sidebar">
  <% locked = cookie.get('article.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <div class="publication item">
    <div class="cover">COVER IMAGE</div>
    <h6 class="name"><a href="${req.route_path('publication', namespace=site.project.namespace, slug=site.slug)}">${publication.name}</a></h6>
    <p></p>
  </div>

  % if util.route_name == 'article':
  <hr>
  <h6 class="section-title">CHAPTERS</h6>

  <hr>
  <h6 class="section-title">HEADINGS</h6>

  <hr>
  % elif util.route_name == 'publication':

  % if req.user:
  <hr class="divider">

  <h6 class="section-title">REGISTRY</h6>
  <a class="item" href="${req.route_url('registry.site.overview', namespace=site.project.namespace, slug=site.slug)}">Public Insights</a>
  % else:
  <br />
  % endif

  % endif

  % if not req.user:
  <span class="item">
    <a href="${req.route_url('login')}">Login</a>&nbsp;or&nbsp;<a href="${req.route_url('signup')}">Signup</a>
    <span class="description">Scrolliris, a publication platform which utilizes text readability analysis</span>
  </span>
  % endif

  <hr class="divider">

  % if req.user:
  <a class="item" href="${req.route_url('carrell.top')}">Bookmarks</a>
  <a class="item" href="${req.route_url('carrell.top')}">Preferences</a>
  <a class="item" href="${req.route_url('carrell.settings')}">Settings</a>

  <br/>
  <h6 class="section-title">LEAVE CARRELL</h6>
  <a class="item" href="${req.route_url('console.top')}">
    Console
    <span class="description">writing space</span>
  </a>
  % endif
  <a class="item" href="${req.route_url('top', subdomain=None)}">
    Publication Registry
    <span class="description">search & browse stats</span>
  </a>
</div>
