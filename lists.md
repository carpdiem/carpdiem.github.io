---
layout: default
title: Lists
permalink: /lists
---
<h2 style="text-align: center">curious collections</h2>

{% assign sorted = site.lists | sort: 'last_modified' | reverse %}
{% for l in sorted %}
<div class="index_item_title">
<h2 class="no_break_title inline"><a href="{{ l.url }}">{{ l.title }}</a></h2>
<div class="metadata inline">-- Last Updated: {{ l.last_modified | date: '%B %d, %Y' }}</div>
</div>

{% if l.content contains '<!--more-->' %}
{{ l.content | split:'<!--more-->' | first | markdownify }}
{% else %}
{{ l.excerpt | markdownify }}
{% endif %}

<a href="{{ l.url }}">Read More</a>
<hr>
{% endfor %}
