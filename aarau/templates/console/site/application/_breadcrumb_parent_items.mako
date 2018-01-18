% if not application:
<a class="item" href="${req.route_path('console.top')}">Projects</a>
<span class="divider">/</span>
% endif

<a class="item" href="${req.route_path('console.project.overview', namespace=project.namespace)}">${project.name}</a>
<span class="divider">/</span>

% if application:
<a class="item" href="${req.route_path('console.site.overview', namespace=project.namespace, slug=site.slug)}">${application.name}</a>
<span class="divider">/</span>
% endif
