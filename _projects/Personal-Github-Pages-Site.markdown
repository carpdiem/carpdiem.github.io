---
layout: project
title: Personal Github Pages Site
date: 2020-06-11
last_modified: 2020-06-11
image: projects/personal_site/personal_site_screenshot_2020_06.png
---

I've been meaning to put together a reasonable personal website for ages, but it wasn't until I encountered a pointer for [GitHub Pages](https://pages.github.com) in combination with a discussion of [Digital Gardens](https://tomcritchlow.com/2019/02/17/building-digital-garden/) that the stars finally aligned. Here I had a tool that made building a hosting a site extremely simple, while simultaneously giving me extremely detailed control over the content/layout/organization. *And* I now had a fancy-sounding name to use as an excuse to build out whatever organizational scheme I felt like, with no need to try to fit it into someone else's ontology. Score!

![Site screenshot, June 2020, edited for size]({{ site.url }}/images/projects/personal_site/personal_site_screenshot_2020_06.png)

If you want to check out the codebase, you can [view the github repo here](https://github.com/carpdiem/carpdiem.github.io).

### I'd like to call some credit to a few special resources.

#### Fonts

This site uses the beautiful [Crimson Pro](https://fonts.google.com/specimen/Crimson+Pro#standard-styles) for almost everything (specifically, the Crimson Pro Light variant). Code blocks, however, are rendered in [Iosevka Term Slab Light](https://typeof.net/Iosevka/). These are the same fonts I use and prefer for my personal laptop's configuration, and I'm happy to spread the word about them. Long live serifs!

#### RSS

RSS is a wonderful tool for consuming the web, especially when paired with a high quality reader app like [Feedly](https://feedly.com/). However, putting the RSS feed together corectly for this site was a pain, mostly due to my custom site organization (GitHub Pages natively only supports an RSS feed for a single, dedicated "posts" collection), but also due to compatibility issues and format requirements for the RSS feed itself.

I worked off of [this post](https://joelglovier.com/writing/rss-for-jekyll) from Joel Glovier on adding an RSS feed to a Jekyll site without relying on plugins, and then spent plenty of time with [this RSS feed validator](http://www.feedvalidator.org/) to get it right.

#### Post Excerpts

Oh boy. At first, I set this up using some simple word-counting and truncating logic in the Liquid templating language wherever relevant. This quickly ran into edge cases because the content being parsed by Liquid included html for some posts (e.g., \<img\> elements, \<iframe\>'s from embedded youtube videos, and even \<td\>'s and \<tr\>'s from code blocks). As a result, the simple truncating logic would often select a break point in the middle of an html tag, leaving the excerpt containing the useless and ugly half-carcass of some poor \<img\>.

Thankfully, I came across [this solution](https://coderwall.com/p/eazb7w/easily-create-blog-post-excerpts-for-jekyll-and-github-pages) by Garrett Miller, which I've adopted alongside a fallback to the .excerpt method (which deserves a shout out to another blog post I had encountered, but can no longer find).

#### Infinite Scroll on /blog

In yet another example of what would become a running theme, if you're building a site exactly how Jekyll assumes you want to build a site, you'll be fine. If you depart from that, beware.

In this case, I wanted to apply some sort of pagination or progressive content loading for my /blog section, but Jekyll only natively supports pagination for your "posts" collection (which, for other reasons, I didn't want to use... thus rolling my own "blog" collection).

I found a good solution with [Infinite Jekyll](https://github.com/tobiasahlin/infinite-jekyll), a simple json/CSS/javascript trick for easily enabling infinite scrolling, and which only required minor modifications to get it working [here]({{ site.url }}/blog).
