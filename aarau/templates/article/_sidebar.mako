<div class="sidebar">
  <% locked = cookie.get('article.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <div class="publication item">
    <div class="cover">COVER IMAGE</div>
    <h6 class="name"><a href="${req.route_path('publication', namespace=site.project.namespace, slug=site.slug)}">${publication.name}</a></h6>
    <p></p>
  </div>

  <hr>
  <h6 class="section-title">CHAPTERS</h6>

  <hr>
  <h6 class="section-title">HEADINGS</h6>

  <hr>
  <h6 class="section-title">PREFERENCES</h6>
  <div class="item">
    <a href="${req.route_url('login')}">Login</a>&nbsp;or&nbsp;<a href="${req.route_url('signup')}">Signup</a>
    <span class="description">Scrolliris, a publication platform which utilizes text readability analysis</span>
  </div>

  <hr>
  <a class="item" href="${req.route_url('top', subdomain=None)}">
    Publication Registry
    <span class="description">search & browse stats</span>
  </a>
</div>
