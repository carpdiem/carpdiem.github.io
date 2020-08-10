---
layout: blog_post
title: How do you solve a puzzle with only white pieces left?
date: 2020-08-10
last_modified: 2020-08-10
---

Sometimes, you end up doing a puzzle, and you get to a spot where you have only blank, featureless pieces left.

![]({{ site.url }}/images/blog/great_wave_puzzle.jpg)

And it's like, "Seriously? Do I really have to hate my life now?"

Well, naively, if you've got n pieces left—leaving you also with n spots left—and you just go testing each piece in each spot, you end up running an algorithm that takes (n spots) * (n/2 pieces to check on average before finding the correct one) * (2 orientations per piece) = O(n²) steps. So, yes, with this method, you *are* obligated to hate your life, and I only hope you're not stuck trying to do [this puzzle](https://mymodernmet.com/all-white-jigsaw-puzzle/).<!--more-->

In my case, we got to this point with ~120 pieces left, so, assuming a speedy and dedicated 5 seconds per test, it would take ~20 hours to finish the remainder.

There are many different strategies that let you improve on the naive, "just try them all" algorithm, but I own a set of digital calipers, so here's mine.

First, we need to identify relatively reliable measurements that we can take both from the leftover pieces themselves, as well as from the empty spots still-to-be-filled on the puzzle itself. I settled on measuring the two "legs" of each piece, as defined in the image below.

![]({{ site.url }}/images/blog/piece_measurements.jpg)

Given that, I assigned each piece a 2D coordinate value of the form (length-of-long-leg, length-of-short-leg), and then sorted the pieces on the extra space on the table.

![]({{ site.url }}/images/blog/piece_sorting.jpg)

Here, the individual post-its and larger piles on the right side are a kludge I had to use for especially large pieces as my table didn't have enough room to continue my original axes at the resolution I was using (0.2mm steps).

Now that I've gotten this done, finding pieces has become simple: measure one—or two, if you have access to them!—leg length(s) from the empty spaces remaining on the puzzle; then go look up those measurements on the chart and try the pieces matching (and nearby! your measurements are unlikely to be perfect!) them.

This has been a big improvement, and while it does often get pieces exactly correct on the first try, it's not always perfect (mostly measurement errors and situations on the board where you only have one leg measurement to go by), so I'd estimate it takes about 10 tests on average to find any particular piece.

Assuming 10 seconds / piece for the original measurements, and again, 5 seconds / piece for testing, that leaves a total time of about 2 hours for the remaining work, a 10x speedup. O(n) algorithms for the win!

I'll let you know how it goes in practice.
