<%inherit file='../_layout.mako'/>

<%block name='title'>
 New Application | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="active item">New Site</span>
</div>
</%block>

<div id="publication" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-9">
        <%namespace name='msg' file='../../shared/_message.mako'/>
        ${msg.form()}
        <h2 class="header">New Site</h2>
        <p class="description">Each sites in the project should have same contents or comparable articles which are written by you. Normally, you need only one site.</p>
        <%
          act = req.route_url('console.site.new', project_id=project.id, _query={'type':'application'})
          ctx = 'new'
          # FIXME
          err = ''
        %>
        <%include file="_form.mako" args="f=form, act=act, ctx=ctx, err=err"/>
      </div>
    </div>
  </div>
</div>
