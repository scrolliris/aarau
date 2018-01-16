% if not application:
<a class="item" href="${req.route_path('console.top')}">Projects</a>
<span class="divider">/</span>
% endif

<a class="item" href="${req.route_path('console.project.view', id=project.id, _query={'type': 'application'})}">${project.name}</a>
<span class="divider">/</span>

% if application:
<a class="item" href="${req.route_path('console.site.application.overview', project_id=project.id, id=site.id, _query={'type': 'application'})}">${application.name}</a>
<span class="divider">/</span>
% endif
