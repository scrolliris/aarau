<script>
(function(d) {
  var config = {
        kitId: '${util.typekit_id}'
      , scriptTimeout: 3000
      , async: true
      }
    , h=d.documentElement,t=setTimeout(function(){h.className=h.className.replace(/\bwf-loading\b/g,"")+" wf-inactive";},config.scriptTimeout),tk=d.createElement("script"),f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";tk.src='https://use.typekit.net/'+config.kitId+'.js';tk.async=true;tk.onload=tk.onreadystatechange=function(){a=this.readyState;if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}catch(e){}};s.parentNode.insertBefore(tk,s)
})(document);
</script>
<script>
(function(d) {
  var families = [
    'Open Sans'
  , 'Roboto Slab:300'
  ].join('|').replace(/\b\s\b/g, '+');
  var loadFont = function(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var style = d.createElement('style');
        style.innerHTML = xhr.responseText;
        d.head.appendChild(style);
      }
    };
    xhr.send();
  }
  d.body.onload = function() {
    var url = 'https://fonts.googleapis.com/css?family=' + families;
    loadFont(url);
  }
})(document);
</script>
