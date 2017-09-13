<%inherit file='../../_layout.mako'/>

<%block name='title'>
  Edit Application | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="active item">Edit Site</span>
</div>
</%block>

<div id="publication" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-9">
        <%namespace name='msg' file='../../../shared/_message.mako'/>
        ${msg.form()}
        <h2 class="header">Edit Site</h2>
        <p class="description"></p>
        <%
          act = req.route_url('console.site.application.edit', project_id=project.id, id=site.id, _query={'type':'application'})
          ctx = 'edit'
          # FIXME
          err = ''
        %>
        <%include file="../_form.mako" args="f=form, act=act, ctx=ctx, err=err"/>
      </div>
    </div>
  </div>
</div>
