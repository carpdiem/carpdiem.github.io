---
layout: project
title: Course Notes -- Fast.ai
date: 2024-03-18
last_modified: 2024-03-19
---

### Intro

I've been meaning to run through the [Fast.ai](https://course.fast.ai/) course on practical deep learning for about a year now, since I first learned of it, and it's finally time. As usual, I'll be burning down through this quickly, and thankfully have a pretty deep background in the gnarlier, more mathematical aspects of the field... (I've derived and implemented backprop by hand a number of times, and most recently on the professional side, was SVP product for a startup building LLM Inference HW, so I've become quite familiar with the underlying theory and architectures).

But now it's time to roll my sleeves up and learn the hands-on tools.<!--more-->

I'll be using this space to track and update any particularly interesting things I learn along the way.

### Part 1

*My goal here will be to go through the fast.ai Part 1 sequence and produce and deploy an ML model accessible directly from this project page.*

**Things I learned:**
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) is a *great* command line tool for downloading youtube videos. Highly useful for making it easy to adjust playback speed (using `[` and `]` keyboard shortcuts) with [mpv](https://mpv.io/) (a close analog to mplayer with good mac support).
- [timm](https://timm.fast.ai/) is a pytorch-based deep learning library collecting a number of pre-existing image models.
- I cannot believe I hadn't encountered [python's functools.partial()](https://docs.python.org/3/library/functools.html#functools.partial) before. I've been used to this sort of functionality since my days messing around with making a solver for [hateris](https://qntm.org/files/hatetris/hatetris.html) in haskell ages ago, and I've always rolled my own in python using lambda functions. *But of course* there's a built-in for that now.
- [ipywidgets.interact](https://i]pywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html) is another major quality of life improvement. However, as a reminder to myself, this *is not enabled by default* in jupyterlab.
- [python decorators](LINK HERE), which have been on my "to-learn" list *forever*, and have finally drifted to the top.
- The use of [* and /](https://realpython.com/python-asterisk-and-slash-special-parameters/) in python argument lists in order to enforce the allowable order of positional vs keyword arguments.
- Nice to use `log()` for reducing the domain of distributions. (But more important to just be aware of, and interrogate, your data distributions!)
- Somehow, I missed that list comprehensions in python also extend to dictionaries and sets! Cute.
- I had not encountered the book [Python for Data Analysis](https://wesmckinney.com/book/) before, but it's a solid resource on some of the internals and tools (especially in pandas) that I was less familiar with.
- 