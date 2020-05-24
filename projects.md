---
layout: default
title: Projects
permalink: /projects
---
<h2 style="text-align: center">significant efforts I'd like to share with you</h2>

{% assign sorted = site.projects | sort: 'last_modified' | reverse %}
{% for p in sorted %}
<div class="index_item_title">
<h2 class="no_break_title inline"><a href="{{ p.url }}">{{ p.title }}</a></h2>
<div class="metadata inline">-- Last Updated: {{ p.last_modified | date: '%B %d, %Y' }}</div>
</div>
<div class="indent_from_left">
{{ p.content | truncatewords: 70 | markdownify }}

{% assign wc = p.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ p.url }}">See Full</a>
{% endif %}
</div>
{% endfor %}
