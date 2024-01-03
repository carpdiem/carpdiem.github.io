---
layout: blog_post
title: Thoughts on "The Twelve-Factor App"
date: 2024-01-02
last_modified: 2024-01-02
---

These notes are a stream-of-consciousness response to reading through [The Twelve-Factor App](https://12factor.net/) at the suggestion of a good friend of mine.

### Introduction and Background

Nothing particularly special here. At this high of a level of abstraction, everything sounds like a good and reasonable idea!

### Section 1: Codebase

Not too much controversial in here (I hope!). I like the emphasis on strict delineation of codebases between apps, and factoring out shared code into separate libraries under dependency management.

### Section 2: Dependencies<!--more-->

This one requires some rigor and automated test tools for enforcement!

Their ending note about extending the philosophy to system tools makes plenty of sense, though it does start to make me wonder how they would handle system tools that might need to be rebuilt for different micro architectures... seems troublesome to end up with nested system compatibility issues...

### Section 3: Config

This one is an interesting distinction. Of course you don't want to save credentials and the like into your code repo, but storing all config as environment variables feels a little like you're just pushing the problem down the road... you still need tools to set up and manage those env vars for any sufficiently complicated setup, and especially if a single user might need to switch between various configs (when, say, deploying to dev vs test vs qa) it feels like it would be very easy to accidentally end up in a world where your config is now stored in a management program or downloaded from a source location.

### Section 4: Backing Services

This is a reasonable set of definitions and goals, but leaves a little bit of documentation and organization discussion to be desired. For example, if you're using a SQL database as a resource, you may also need to track specific version requirements for that database implementation--especially if you're relying on specific and/or unusual functionality--but even in the general case, you may want to specify version requirements to align with your testing environment, even if only to make sure to be able to replicate behavior where bugs may be concerned.

These sorts of situations would require some extra state to be stored somewhere beyond just the resource handle.

### Section 5: Build, release, run

Again reasonable, with some additional potential trickery around dealing with exploding database sizes in cases where the release may include large binaries / etc. 

### Section 6: Processes

Very reminiscent of my time with Haskell. I dig it, but there are probably consequences of this approach that I'm not immediately appreciating.

### Section 7: Port Binding

This is one I'll tag for deeper discussion. There's definitely some stuff I don't fully grok about sentences like "does not rely on runtime injection of a webserver into the execution environment to create a web-facing service".

For example, what would doing so even mean or entail? Why might you be tempted to do so?

### Section 8: Concurrency

A few questions in here also. What does "daemonizing" mean? What are PID files? Is there some formalism for "process types" that I should be aware of, or is it just a question of nomenclature, fully under the control of the devs?

### Section 9: Disposability

This again seems like a "mathematically pure" thought, but one that's devilish to police via testing in practice. In particular, the linked wikipedia page on "reentrant" was surprisingly subtle.

### Section 10: Dev/prod parity

Nice, here's some discussion of the issues I was thinking about from the "Backing Services" section. Overall this seems like an obviously good idea. I wonder what situations would make it maximally difficult.

### Section 11: Logs

Huh. This is definitely an idea in the same vein as the previous ten sections, but it surprised me on first read nonetheless. Just logging everything straight to stdout and leaving log routing and collection to the execution environment definitely makes sense given the rest of this framework. I'll have to chew on this one a little more to see what I really think of it, but so far no objections, even if it is a change in how I've been thinking.

### Section 12: Admin processes

This doesn't actually seem like it's _saying_ much of anything at all. Basically the message is "standardize everything you can, and use tools to make sure of it".

Is there something more to this that I'm missing?
