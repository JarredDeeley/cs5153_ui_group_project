var Turbolinks = require("turbolinks");
Turbolinks.start();

// https://github.com/turbolinks/turbolinks/issues/272
for(let i = 0; i < document.forms.length; i++) {
  const form = document.forms[i]
  if (form.method == "get" && form.dataset['remote'] == "true") {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const entries = [...new FormData(e.target).entries()]
      const params = "?" + entries.map(e => e.map(encodeURIComponent).join('=')).join('&')
      Turbolinks.visit(form.action + params);
    });
  };
};
