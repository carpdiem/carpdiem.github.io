---
layout: project
title: Course Notes -- UC Berkeley CS 162 - Operating Systems
date: 2020-07-27
last_modified: 2020-07-27
---

### Here's yet another set of course notes, coming at you from [UC Berkeley's CS 162 - Operating Systems](https://inst.eecs.berkeley.edu/~cs162/fa13/) course from the fall of 2013.

Curiously, while the direct link above is to the main class homepage from that session, it *doesn't* include links to the actual lecture videos themselves. Those, however, can be found on [this Youtube playlist](https://www.youtube.com/playlist?list=PLRdybCcWDFzCag9A0h1m9QYaujD0xefgM).

### Once I finished the lectures, it occurred to me that it might be interesting to look at the Youtube viewing statistics for the course. I figured, "hey! maybe we'll see some dropoff patterns!".

![]({{ site.url }}/attachments/projects/cs162/cs162-view_statistics.png)

Hahahah. Oh man...

The first lecture has more than 3x the views of any other lecture, with 31,615 views logged.

Meanwhile, the *least-viewed* lecture is Lecture #22 - "Security, Part 2", with only 345 views!

This suggests that for every 100 people who start watching these lectures, only maybe 1 person¹ will actually make it all the way through.

Another interesting point about the view numbers is that we can see several sudden peaks later in the distribution. These are lectures that for some reason or other drew significant extra attention:

- Lecture #8 - "Thread Scheduling": 4,117 views

    I have no idea why this one in particular gets so much extra attention. Lecture #7 - "Language Support for Concurrent Programming; Deadlocks" only has 1,003 views, and it's pretty equally fascinating. Maybe thread scheduling just isn't covered elsewhere on the internet, so this video gets a lot of search results? Maybe there's a popular blog somewhere linking to this video? Who knows.

- Lecture #17 - "TCP, Flow Control, Reliability": 1,467 views

    Ok. This one I get. TCP is a **big deal**, and this is a reasonable explanation of how it works and why it's important. Doesn't get into as much of the implementation details as [6.02]({{ site.url }}/projects/Course-Notes----MIT-602---Digital-Communication-Systems.html) does, but a lot of people probably care plenty about this. Bonus points to Lecture #17 for covering that classic CS interview question: "What is the three-way handshake?".

- Lecture #19 - "Transactions, Two Phase Locking (2PL), Two Phase Commit (2PC)": 2,461 views

    Uhh... people... really like... databases? And rather than learning about them in, say, a course dedicated to databases, they prefer to jump into the last third of a course on operating systems?

### Finally, if you're tackling this course on your own, I'll leave you with some brief advice:

> -- *Operating Systems tl;dr* --
> {: style="text-align: center;" }
> 
> The core of this class is the idea that sharing *resources* (CPU time, memory, I/O, etc) among many *processes* (i.e. - running programs) is tricky but necessary for good performance (after all, who wants their expensive new computer to be sitting idle most of the time?).
>
> In practice, there are many ways to determine which processes get access to which resources, and when, but most of them are essentially some form of lockout flags ("resource A is IN USE, no one else can use it right now!") or lookup tables ("resource A is currently assigned to process 1; resource B to process 2; …). There are variations on this core theme (like "multiple readers / one writer" locks for databases or multi-level translation for page tables), but those are just window dressing on the core ideas.
> 
> This is important to do correctly because if you mess it up, you can corrupt your data / let hackers take control of your system with buffer overflow attacks / [accidentally deliver 100x the safe dose of x-rays to a patient](https://en.wikipedia.org/wiki/Therac-25).
>
> Normally, the Operating System handles this for all the processes on your computer, and likewise, there are cloud/etc operating systems for handling these sorts of issues for datacenters/etc, but if you're working on any sort of application with multiple parts that have to communicate and/or share resources, you should give it some thought too, lest you end up in trouble someday.

<object data="{{ site.url }}/attachments/projects/cs162/CS_162_-_Operating_Systems_-_Berkeley.pdf" type="application/pdf" style="min-height:100vh;width:100%">Fallback: this browser does not support PDFs. Please <a href="{{ site.url }}/attachments/projects/cs162/CS_162_-_Operating_Systems_-_Berkeley.pdf">download the PDF</a> to view it.
</object>

[Download my course notes as a PDF.]({{ site.url }}/attachments/projects/cs162/CS_162_-_Operating_Systems_-_Berkeley.pdf)

---

1. This suggests an easier than ever way to join the global 1%! Forget about working long and hard to stash away millions of dollars, just watch two-dozen lectures on computer science! Shouldn't take any longer than binge-watching a few seasons of a new show, and it's much less likely to leave you as a target for global anticapitalist ire.
