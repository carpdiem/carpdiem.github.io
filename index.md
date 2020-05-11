---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
permalink: /
---

{% for c in site.collections %}
#{{ c.label }}
<ul>
{% assign sorted = {site.c.label | sort: 'last_modified'} | reverse %}
{% for item in sorted %}
<li>{{ item.title }}</li>
{% endfor %}
</ul>
{% endfor %}
