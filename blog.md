---
layout: blog_index
title: Blog
permalink: /blog
---
<h2 style="text-align: center">shortform blog entries</h2>

{% assign sorted = site.blog | sort: 'date' | reverse %}
<div class="post-list">
{% for b in sorted limit: 5 %}
<div class="post">
<div class="index_item_title">
<h2 class="no_break_title"><a href="{{ b.url }}">{{ b.title }}</a></h2>
{% assign written_date = b.date | date: '%s' %}
{% assign updated_date = b.last_modified | date: '%s' %}
{% if written_date < updated_date %}
<div class="metadata">Last Updated: {{ b.last_modified | date: '%B %d, %Y' }}</div>
{% else %}
<div class="metadata">Written: {{ b.date | date: '%B %d, %Y' }}</div>
{% endif %}
</div>
{{ b.content | markdownify }}
<hr>
</div>
{% endfor %}
</div>

<div class="infinite-spinner"></div>
