---
layout: project
title: Generating Color Temperature Equivalent Light with RGB LEDs
date: 2020-08-13
last_modified: 2020-08-13
---

Too much blue light at night sucks. That's why people use software like f.lux on their computers and night modes on their phones, but that doesn't solve the problem of ambient light. The problem is that for ambient light, you really want to be able to generate a gradual transition of the light color through different color temperatures, and while you can buy standard bulbs designed to mimic particular color temperatures, there are no good solutions for the variable case.

But we've got RGB LEDs, right? You'd think that somewhere in all those color combinations we could find something equivalent to any particular color temperature.

Here, the naive approach of googling fails you, as, at best, you land on websites that say things like "here are some example colors and matching RGB values that I eyeballed", and at worst, "you can't do it without trial and error, so good luck".

Well, I'm here to tell you that there's a better way, and hopefully we'll learn something about sensory perception and colors along the way.

## First, the tl;dr - 

I wrote a python module called Color_Match. You can find it [here]().

Once you've installed it, go look up the emission wavelengths of your RGB LEDs on their datasheet. If you can't find it, you can try starting with something like 623nm, 528nm, and 470nm (some example wavelength values from some RGB LEDs I happen to have on hand right now), but your results may be a little off and require some tuning of the specific wavelengths.

Then, let's say that you're trying to generate the equivalent of 1900K light (roughly candle-light), you would use the following code.

```python

import Color_Match as cm

# using the sample wavelength values from above, converted into units of meters
relative_intensities = cm.rgb_composition(623e-9, 528e-9, 470e-9, cm.sense_vector(cm.planck_spectrum(1900)))

# full_brightness_limit is whatever value corresponds to a maximum output on an individual RGB channel, typically this is 255
full_brightness_limit = 255

# desired_brightness is a value between 0.0 and 1.0 that represents how bright you want your LEDs to be running; e.g., use 0.5 for 50% brightness
desired_brightness = 0.5

# since the values stored in relative_intensities are... relative intensities, we need to scale them to produce the correct absolute settings for your RGB channels
absolute_rgb_levels = (desired_brightness * full_brightness_limit) * relative_intensities

```

## Now let's talk details

### What is light, really?

### Then what are colors?

### What do we mean when we talk about "what a color looks like"?

### So when we talk about matching the appearance of a particular color temperature…?

## Ok. How do we do that?

## Some other interesting, related things…

### Color vision in humans vs other animals

### Humans are practically blind!
