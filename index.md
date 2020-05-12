---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
permalink: /
title: Recent Updates
---

{% for c in site.collections %}
{% if c.label != "posts" %}
## <a href="{{ c.label }}">{{ c.label }}</a>
<ul>
{% assign sorted = site[c.label] | sort: 'last_modified' | reverse | slice: 0, 3 %}
{% for item in sorted %}
<li><a href="{{ item.url }}">{{ item.title }}</a></li>
{% endfor %}
<li><a href="{{ c.label }}">See More</a></li>
</ul>
<hr>
{% endif %}
{% endfor %}
