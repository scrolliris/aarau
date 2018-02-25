let handleToolbar = (doc) => {
  // toolbar (checkbox)
  let toolbar = doc.getElementById('toolbar_checkbox');
  if (toolbar === null || sidebar === undefined) {
    return;
  }
  // controls
  let hideBtn = doc.getElementsByClassName('toolbar-hide-button')[0]
    ;

  if (hideBtn === null || hideBtn === undefined) {
    return;
  }

  hideBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    hideBtn.blur();

    toolbar.checked = false;
  });
};

module.exports = handleToolbar;
