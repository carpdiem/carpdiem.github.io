---
layout: misc
title: Logarithmic Birthdays
date: 2020-06-29
last_modified: 2020-06-29
use_math: true
use_jquery: true
---

### Birthdays are crap.

Now, don't get me wrong. I love a party. And I think it's a great idea to bring people together in celebration, so I'm not saying that *the concept of regularly celebrating the evolution of one's life* is crap, just that trying to measure the evolution of your life in time periods defined by how long it takes a particular rock to orbit around a particular ball of fusion-plasma is crap.

In practice, paying a lot of attention to each particular birthday gets swapped with gradually focusing your attention on birthdays that fall on nice, round number sort of years. Like numbers divisible by 5, or 10. And, let's be honest, this is a cudgel, and the only reason it's not totally ridiculous is because humans currently only live for about 100 years, max, so we don't really have to deal with the breakdown of this system as t→∞.

### So, how do we fix it? <!--more-->

[Scale invariance](https://en.wikipedia.org/wiki/Scale_invariance).

> tl;dr -- if we switch our definition of age to one based on *ratios* of time rather than *absolute measures* of time, we can do a whole lot better.

### So, what ratio to pick?

Since we're scientists, there's really only one number to start with: [e](https://en.wikipedia.org/wiki/E_(mathematical_constant)).

Equally naturally¹, we therefore might first try to use a plain $ age(t) = ln(t) $ function to define our age in "proper years" as a function of t, our age in days². This, of course, famously fails because it falls off to -∞ as t→0, so we need to make an adjustment. And what's the simplest adjustment we can make here? Shift the function over by one!

++ age(t) = ln(t+1) ++

### What does this look like in practice?

| Proper Age: age(t) = ln(t+1) |       Calendar Age       |
|:---------------------------:|:------------------------:|
|              0              |          0 days          |
|              1              |         1.7 days         |
|              2              |         6.4 days         |
|              3              |      2 weeks, 5 days     |
|              4              | 1 month, 3 weeks, 2 days |
|              5              |         ~5 months        |
|              6              |     ~1 year, 1 month     |
|              7              |         ~3 years         |
|              8              |    ~8 years, 4 months    |
|              9              |    ~22 years, 6 months   |
|              10             |         ~61 years        |
|              11             |        ~166 years        |
|              12             |        ~452 years        |

Now, I'm not a monster, so I recognize that that's probably a little too widely spaced for modern humans.

### What's the simplest way we can fix it?

After some trial and error, I've decided I quite like the spacing inherent in celebrating every deci-birthday³ (such that celebrations will happen every time you add ~10% to your age), and keeping the original, simple formula $ age(t) = ln(t+1) $.

### And what do deci-birthdays on this schedule look like?

Well, rather than bore you with a too-long table, I've added some simple javascript to this page to calculate the dates of your next five deci-birthdays, just put in your current birthday below!

### <label for="birthdate">If you were born on:</label>

<input type="date" id="birthdate" value="1980-01-01">

You are currently <span id="current_age" style="font-weight: bold">\<number\></span> proper years old, to the nearest deci-proper-year.

### Your next five deci-proper-birthdays will be:

<table id="age_table">
<thead>
<tr>
<th style='text-align: center'>Proper Age: age(t) = ln(t+1)</th>
<th style='text-align: center'>Calendar Date</th>
</tr>
</thead>
<tbody>
<tr>
<td style='text-align:center'></td>
<td style='text-align:center'></td>
</tr>
<tr>
<td style='text-align:center'></td>
<td style='text-align:center'></td>
</tr>
<tr>
<td style='text-align:center'></td>
<td style='text-align:center'></td>
</tr>
<tr>
<td style='text-align:center'></td>
<td style='text-align:center'></td>
</tr>
<tr>
<td style='text-align:center'></td>
<td style='text-align:center'></td>
</tr>
</tbody>
</table>

<script type="text/javascript">
$(document).ready(function() {
calc_bdays();
$("#birthdate").change(calc_bdays);
});

function calc_bdays() {
var frac = 10.0;
var today = new Date();
var bday = new Date($('#birthdate').val());
var days_between = (today.getTime() - bday.getTime())/(1000. * 60. * 60. * 24.);
var age_in_qbds = Math.floor(frac * Math.log(days_between + 1));
$("#current_age").text(age_in_qbds/frac);
let next_ages = [(age_in_qbds + 1)/frac, (age_in_qbds + 2)/frac, (age_in_qbds + 3)/frac, (age_in_qbds + 4)/frac, (age_in_qbds + 5)/frac]
let next_qbds = []
next_ages.forEach(function(item, index, array) {
next_qbds.push(new Date(bday.getTime() + (Math.exp(item) - 1.0) * 24 * 60 * 60 * 1000))
});
var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
for (var i = 0; i < 5; i++) {
$("#age_table tbody tr:eq(" + i + ") td:eq(0)").text(next_ages[i]);
$("#age_table tbody tr:eq(" + i + ") td:eq(1)").text(months[next_qbds[i].getMonth()] + " " + next_qbds[i].getDate() + ", " + next_qbds[i].getFullYear());
};
}
</script>

---

1. Ok, I admit it. This was intentional.

2. Why do I use days, given how much I've hated on years? Simple: days are actually a relatively uniquely defined time period for human beings even in the absence of the planet Earth, based on our evolved circadian rhythms. And who knows, maybe with time even the traditional 24-hour day will appear silly.

3. This actually presents a bit of unintuitive trouble if you try to extend deci-birthday celebrations to infants. After all, should they _really_ be celebrating ten times in the first two days of life? And, sure, they grow quickly, but that still seems a bit too rapid to match the pace of their development, doesn't it?

    The solution to this is that really, we should be counting age from conception, not birth. Measured correctly, a newborn won't reach their next deci-conceptionday for about three and a half weeks (remember, each deci-X-day is ~10% extra lifespan from whatever X you're measuring from). While that makes the numbers make more sense, there are obvious difficulties with knowing anyone's exact date of conception, so it's probably best to just stick with normal birthdays until you start to feel like they're showing up too rapidly, and then switch to deci-proper-birthdays.

    Alternatively, if you're ambitious, you can do the age-from-conception calculations yourself.
