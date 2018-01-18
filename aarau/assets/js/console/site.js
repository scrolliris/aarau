((doc) => {
  let setChange = (site) => {
    if (site) {
      let type_ = site.querySelector('#site_type');
      if (type_) {
        type_.addEventListener('change', (e) => {
          let element = (e.target || type_);
          let value = element[element.selectedIndex].value;
          window.location.href = window.location.href.replace(
            /(\?type\=)(\w+)$/, '$1' + value);
        });
      }
    }
  };

  let publication = doc.getElementById('site');
  setChange(publication);
})(document, window);
