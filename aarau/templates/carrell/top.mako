<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/carrell/_layout.mako'/>

<%block name='title'>${render_title('Reader')}</%block>

<div class="site content">
  <div class="site grid">

    <div class="row">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="center">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="center">
        <p>You don't have bookmark yet. Please find something to read on the <a href="${req.route_url('registry.search')}">Registry</a>.<br>
          Happy scrolling !-)</p>
      </div>
    </div>

  </div>
</div>
