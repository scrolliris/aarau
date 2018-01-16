% if not publication:
<a class="item" href="${req.route_path('console.top')}">Projects</a>
<span class="divider">/</span>
% endif

<a class="item" href="${req.route_path('console.project.view', id=project.id, _query={'type': 'publication'})}">${project.name}</a>
<span class="divider">/</span>

% if publication:
<a class="item" href="${req.route_path('console.site.publication.overview', project_id=project.id, id=site.id, _query={'type': 'publication'})}">${publication.name}</a>
<span class="divider">/</span>
% endif
