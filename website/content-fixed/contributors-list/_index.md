---
title: Contributors list
weight: 3
draft: false
---

<div id="contributorsList"></div>
<script type="text/javascript">
  const apiUrl = 'https://api.github.com/repos/kislerdm/data-engineering-interviews/contributors?anon=1';
  (() => {
    let ul = document.createElement('ul');
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        contributorsList = data.map(el => `<a href="${el.html_url}" target="_blank">${el.login}</a>`);
        contributorsList.forEach(renderProductList);
      })
      .catch(err => {
        console.error(`Error fetching from ${apiUrl}: ${err}`)
      });
    function renderProductList(element, index, arr) {
      let li = document.createElement('li');
      li.setAttribute('class', 'item');
      ul.appendChild(li);
      li.innerHTML += element;
    };
    document.getElementById('contributorsList').appendChild(ul);
  })();
</script>

##### Thank you for contributing to the project!
