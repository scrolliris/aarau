<div class="right item">
  % if cookie.get('console.sidebar', '') == 'locked':
    <button class="sidebar-hide-button flat button" title="Hide Sidebar" disabled>Hide</button>
    <button class="sidebar-hold-button flat button" title="Unpin Sidebar">Pinned</button>
  % else:
    <button class="sidebar-hide-button flat button" title="Hide Sidebar">Hide</button>
    <button class="sidebar-hold-button flat button" title="Pin Sidebar">Pin</button>
  % endif
</div>