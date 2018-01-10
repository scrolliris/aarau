<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_announcement"/>

<!DOCTYPE html>
<html lang="${req.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <!--
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    -->
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="keywords" content="">
    <title><%block name='title'/></title>
    <link rel="shortcut icon" type="image/x-icon" href="${req.route_url('console.top', namespace='console') + 'favicon.ico'}">
    <link rel="icon" type="image/x-icon" sizes="16x16 32x32 48x48 64x64 96x96 128x128 192x192" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="192x192" href="${req.util.static_path('img/favicon-192.png')}">
    <link rel="icon" type="image/png" sizes="128x128" href="${req.util.static_path('img/favicon-128.png')}">
    <link rel="icon" type="image/png" sizes="96x96" href="${req.util.static_path('img/favicon-96.png')}">
    <link rel="icon" type="image/png" sizes="64x64" href="${req.util.static_path('img/favicon-64.png')}">
    <link rel="icon" type="image/png" sizes="48x48" href="${req.util.static_path('img/favicon-48.png')}">
    <link rel="icon" type="image/png" sizes="32x32" href="${req.util.static_path('img/favicon-32.png')}">
    <link rel="icon" type="image/png" sizes="16x16" href="${req.util.static_path('img/favicon-16.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="180x180" href="${req.util.static_path('img/touch-icon-180.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="167x167" href="${req.util.static_path('img/touch-icon-167.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="152x152" href="${req.util.static_path('img/touch-icon-152.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="120x120" href="${req.util.static_path('img/touch-icon-120.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="76x76" href="${req.util.static_path('img/touch-icon-76.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="57x57" href="${req.util.static_path('img/touch-icon-57.png')}">
    <link rel="humans" type="text/plain" href="/humans.txt">
    <link rel="robots" type="text/plain" href="/robots.txt">
    <style>html{background-color:#454545;}</style>
    <style>.not-ready{visibility: hidden;}</style>
    <link rel="stylesheet" href="${util.hashed_asset_url('vendor.css')}">
    <link rel="stylesheet" href="${util.hashed_asset_url('author.css')}">
    <script><%include file='aarau:assets/_fouc.js'/></script>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300|Roboto+Slab:300" rel="stylesheet">
  </head>
  <body id="console"<%block name='body_attr'/>>
    <div class="wrapper sidebar-container">
      ## sidebar
      % if cookie.get('console.sidebar', '') == 'locked':
        <input type="checkbox" id="sidebar_checkbox" class="sidebar-checkbox pinned" checked=checked>
      % else:
        <input type="checkbox" id="sidebar_checkbox" class="sidebar-checkbox">
      % endif
      <%block name='sidebar'>
        <%include file='aarau:templates/console/_sidebar.mako'/>
      </%block>

      ## main container
      <section class="content container">
        <header>
          <label class="sidebar-show-button" for="sidebar_checkbox" title="Show Sidebar"></label>
          <div class="top menu">
            <div class="item">
              <%block name='breadcrumb'>
              </%block>
            </div>
            <div class="right menu">
              <a class="item" href="${req.route_url('logout')}">Log out</a>
            </div>
          </div>
        </header>

        <main>
          ${render_announcement()}

          ${self.body()}
        </main>

        <%block name='footer'>
          <%include file='aarau:templates/console/_footer.mako'/>
        </%block>
      </section>
    </div>

    ## <script src="${util.hashed_asset_url('vendor.js')}" charset="utf-8"></script>
    <script src="${util.hashed_asset_url('author.js')}" charset="utf-8" async></script>
    <%block name='script'>
    </%block>
  </body>
</html>
