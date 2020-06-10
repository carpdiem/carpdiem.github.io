---
layout: default
title: Projects
permalink: /projects
---
<h2 style="text-align: center">significant efforts I'd like to share with you</h2>

{% assign sorted = site.projects | sort: 'last_modified' | reverse %}
{% for p in sorted %}
<div class="index_left_indent">
<div class="index_item_title">
<h2 class="no_break_title inline"><a href="{{ p.url }}">{{ p.title }}</a></h2>
<div class="metadata inline">-- Last Updated: {{ p.last_modified | date: '%B %d, %Y' }}</div>
</div>
{% if p.image %}
<img src="{{ site.baseurl }}/images/{{ p.image }}" class="excerpt_image">
{% endif %}

{% if p.content contains '<!--more-->' %}
{{ p.content | split:'<!--more-->' | first | markdownify }}
{% else %}
{{ p.excerpt | markdownify }}
{% endif %}

<a href="{{ p.url }}">…read more</a>
</div>
<hr>
{% endfor %}
