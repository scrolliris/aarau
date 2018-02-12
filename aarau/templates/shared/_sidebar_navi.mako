<%page args="locked=None"/>
<div class="right item">
  % if locked == 'locked':
    <button class="sidebar-hide-button flat button" title="Hide Sidebar" disabled>Hide</button>
    <button class="sidebar-hold-button flat button" title="Unpin Sidebar">Unpin</button>
  % else:
    <button class="sidebar-hide-button flat button" title="Hide Sidebar">Hide</button>
    <button class="sidebar-hold-button flat button" title="Pin Sidebar">Pin</button>
  % endif
</div>
