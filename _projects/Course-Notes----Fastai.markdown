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
- [Python decorators]({{ site.url }}{% link _blog/2024-04-22-Python-decorators-for-fun-and-profit.markdown %}), which have been on my "to-learn" list *forever*, and have finally drifted to the top.
- The use of [* and /](https://realpython.com/python-asterisk-and-slash-special-parameters/) in python argument lists in order to enforce the allowable order of positional vs keyword arguments.
- Nice to use `log()` for reducing the domain of distributions. (But more important to just be aware of, and interrogate, your data distributions!)
- Somehow, I missed that list comprehensions in python also extend to dictionaries and sets! Cute.
- I had not encountered the book [Python for Data Analysis](https://wesmckinney.com/book/) before, but it's a solid resource on some of the internals and tools (especially in pandas) that I was less familiar with.
- I was not previously familiar with [SymPy](https://www.sympy.org/en/index.html) at all. Seems legit.
- **Random Forests:** I had *heard* of these before, but never actually *learned* them. To be honest, I'm a little disappointed. The process is cute, elegant, and simple. But damnit, it's about as crude as a blunt rock. Chop your dataset into random subsets, each with a random subset of all of the features, and train a bunch of decision trees (one on each subset of your data). For predicting, take the average value of all of them. Or maybe the mode, depending on whether you want a quantized result or not. It works, but it's literally just duct-taping random shit together. Though sometimes, that's all you need.
- [Test Time Augmentation](https://arxiv.org/pdf/2011.11156v1.pdf) is a cute trick that seems especially amenable to image models for potentially improving output accuracy.
 
### Part 1 - Project

*This is a transformer-based number-classifier, trained on MNIST. More details about the specific architecture I experimented with below. To use, draw a digit 0-9, and click submit.*

<div style="margin-left: 5%; display: flex; justify-content: center; align-items: start; gap: 5%;">
    <canvas id="userInput" style="display: flex; flex-direction: column; gap: 10px; border: 2px solid black; aspect-ratio: 1 / 1; width: 60%;"></canvas>
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <button id="clearButton">Clear</button>
        <button id="saveButton">Save</button>
        <button id="submitButton">Submit</button>
        <div id="prob0">
            0: 0%
        </div>
        <div id="prob1">1: </div>
        <div id="prob2">2: </div>
        <div id="prob3">3: </div>
        <div id="prob4">4: </div>
        <div id="prob5">5: </div>
        <div id="prob6">6: </div>
        <div id="prob7">7: </div>
        <div id="prob8">8: </div>
        <div id="prob9">9: </div>
    </div>
</div>

<script type="text/javascript">
    // create canvas element and append it to document body
    const canvas = document.getElementById("userInput");
    canvas.width = 560;
    canvas.height = 560;

    // get canvas 2D context
    const context = canvas.getContext('2d');
    
    document.addEventListener('mousemove', draw);
    document.addEventListener('mousedown', startDrawing);
    document.addEventListener('mouseout', stopDrawing);
    document.addEventListener('mouseup', stopDrawing);
    document.addEventListener('touchstart', startDrawing);
    document.addEventListener('touchmove', draw);
    document.addEventListener('touchend', stopDrawing);

    let isDrawing = false;

    function getMousePos(canvas, event) {
        var rect = canvas.getBoundingClientRect();
        return {
            x: (event.clientX - rect.left) / (rect.right - rect.left) * canvas.width,
            y: (event.clientY - rect.top) / (rect.bottom - rect.top) * canvas.height
        };
    }

    function startDrawing(event) {
        isDrawing = true;
        //var pos = getMousePos(canvas, event);
        // context.fillStyle = "#000000";
        // context.fillRect(pos.x, pos.y, 4, 4);
        draw(event);
    }

    function draw(event) {
        if (!isDrawing) return;

        context.lineWidth = 30;
        context.lineCap = 'round';

        var pos = getMousePos(canvas, event);
        context.lineTo(pos.x, pos.y);
        context.stroke();
        context.beginPath();
        context.moveTo(pos.x, pos.y);
    }

    function stopDrawing() {
        isDrawing = false;
        context.beginPath();
    }

    function getTinyImageURL() {
        var tmpCanvas = document.createElement('canvas');
        var tmpCtx = tmpCanvas.getContext('2d');

        tmpCanvas.width = 560;
        tmpCanvas.height = 560;

        var w = tmpCanvas.width;
        var h = tmpCanvas.height;

        var tmpCanvas2 = document.createElement('canvas');
        var tmpCtx2 = tmpCanvas2.getContext('2d');
        tmpCanvas2.width = 560;
        tmpCanvas2.height = 560;

        var destCanvas = document.createElement('canvas');
        var destCtx = destCanvas.getContext('2d');
        destCanvas.width = 28;
        destCanvas.height = 28;

        tmpCtx.drawImage(canvas, 0, 0, w / 2, h / 2);
        tmpCtx2.drawImage(tmpCanvas, 0, 0, w / 2, h / 2, 0, 0, w / 4, h / 4);
        tmpCtx.clearRect(0, 0, w, h);
        tmpCtx.drawImage(tmpCanvas2, 0, 0, w / 4, h / 4, 0, 0, w / 8, h / 8);
        tmpCtx2.clearRect(0, 0, w, h);
        tmpCtx2.drawImage(tmpCanvas, 0, 0, w / 8, h / 8, 0, 0, w / 16, h / 16);
        destCtx.drawImage(tmpCanvas2, 0, 0, w / 16, h / 16, 0, 0, w / 20, h / 20);

        return destCanvas.toDataURL('image/png');
    }

    function updateProbabilities() {
        const dataURL = getTinyImageURL();
        const payload = {data: dataURL};
        fetch('https://mnistbyhand-carpdiem.replit.app/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                const probabilities = data.output;
                updateProbabilitiesOnPage(probabilities);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function updateProbabilitiesOnPage(probabilities) {
        for (let i = 0; i <= 9; i++) {
            const probElem = document.getElementById(`prob${i}`);
            probElem.textContent = `${i}: ${(probabilities[i] * 100).toFixed(1)}%`;
        }
    }

    // Implement "Clear" button
    const clearButton = document.getElementById("clearButton");
    clearButton.addEventListener("click", function() { 
        context.clearRect(0, 0, canvas.width, canvas.height);
        });

    // Implement "Save" button for testing
    const saveButton = document.getElementById("saveButton");
    saveButton.addEventListener("click", function() {
        var imgDataURL = getTinyImageURL();

        var downloadLink = document.createElement('a');
        downloadLink.href = imgDataURL;
        downloadLink.download = 'canvasImage.png';

        downloadLink.click();
    })

    // Implement "Submit" button
    const submitButton = document.getElementById("submitButton");
    submitButton.addEventListener("click", function() {
        updateProbabilities();
    })


</script>
