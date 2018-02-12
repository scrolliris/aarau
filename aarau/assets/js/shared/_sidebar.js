import Cookie from './_cookie.js';


let handleSidebar = (cookieKey, doc) => {
  // sidebar
  let sidebar = doc.getElementById('sidebar_checkbox');
  let hideBtn = doc.getElementsByClassName('sidebar-hide-button')[0]
    , holdBtn = doc.getElementsByClassName('sidebar-hold-button')[0]
    ;

  // cookie
  let saveSidebarState = ((c) => {
    return (k, state) => {
      let v = c.read(k);
      if (typeof v === 'undefined' || v === null ||
          v !== state) {
        v = state;
      }
      // set value to cookie, 1 year (60 * 24 * 365 minutes)
      c.write(k, v, 525600);
    };
  })(Cookie);

  hideBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    hideBtn.blur();

    sidebar.checked = false;
  });

  holdBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    holdBtn.blur();

    let isPinned = sidebar.classList.contains('pinned');
    if (isPinned === null || typeof isPinned === 'undefined' ||
        isPinned === false) {
      saveSidebarState(cookieKey, 'locked');

      hideBtn.disabled = true;

      sidebar.checked = 'checked';
      sidebar.classList.add('pinned');

      holdBtn.innerHTML = 'Unpin';
    } else {
      saveSidebarState(cookieKey, 'unlocked');

      hideBtn.disabled = false;
      hideBtn.removeAttribute('disabled');

      sidebar.checked = true;
      sidebar.classList.remove('pinned');

      holdBtn.innerHTML = 'Pin';
    }
  });
};

module.exports = handleSidebar;
