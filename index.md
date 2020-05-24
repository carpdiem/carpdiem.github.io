---
layout: home
title: recent updates
permalink: /
---

{% for c in site.collections %}

{% if c.label != "posts" %}

## <a href="{{ c.label }}">{{ c.label }}</a>
<div>
{% assign sorted = site[c.label] | sort: 'last_modified' | reverse | slice: 0, 3 %}
{% for item in sorted %}
<div class="index_left_indent">
<div class="index_item_title">
<h3 class="no_break_title"><a href="{{ item.url }}">{{ item.title }}</a></h3>
<div class="metadata">Last Updated: {{ item.last_modified | date: '%B %d, %Y' }}</div>
</div>
{% assign wc = item.content | number_of_words %}
<div class="indent_from_left">
{% if wc > 70 %}
{% assign link = '<a href="' | append: item.url | append: '"> See Full</a>' %}
{{ item.content | truncatewords: 70 | append: link | markdownify }}
{% else %}
{{ item.content | truncatewords: 70 | markdownify }}
{% endif %}
</div>
</div>
{% endfor %}
<a href="{{ c.label }}">See More</a>
<hr>
</div>
{% endif %}

{% endfor %}
