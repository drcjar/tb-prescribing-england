## Discussion

An unguided scan of English prescribing against disease produced thousands of associations at
every level of analysis we tried, and essentially none of them can be believed. The reason differs
by level, and both reasons are instructive.

At area level the problem is that there is nothing left to see. The relationship between a drug
and the disease it treats, which should be the easiest signal in these data, is almost
deterministic between areas and absent within them. Fixed effects are not an optional refinement
here: without them, prescribing is a proxy for the age, deprivation and morbidity of a population
and every association is confounded. With them, the remaining variation is too small to carry
anything. Power in aggregate studies depends mainly on the number of units, and 151 or 294 is not
many.

At practice level the data do carry signal, which was the encouraging finding, but the signal is
pointing the wrong way. Every indication pair showed a stronger association with prescribing in
the year after the outcome than the year before. That is what reverse causation looks like:
practices diagnose, then prescribe. The pervasive inflation on top of it, with roughly half of all
pairs significant, reflects practices drifting together in coding, list composition and activity.
Both effects are strongest for exactly the outcomes drawn from the practice's own records, though
the pattern persisted for externally recorded outcomes such as admissions and screening.

The tuberculosis example shows that the problem is not solved by doing the conventional thing
carefully. That analysis was pre-specified in part, used a disease-specific positive control,
negative-control exposures, falsification tests and a power simulation, and still could only have
detected effects one to several hundred times larger than any that plausibly exist. The positive
control there is instructive in a different way: a drug given almost exclusively to people with
the outcome was recovered with an elasticity of 0.36, so even a perfect exposure is heavily
attenuated by the way these data are assembled.

A natural response to a scan of this size is to demand a stricter threshold. That response fails
here: 1,869 pairs survive Bonferroni correction. Multiplicity corrections assume the null
distribution is right, and the whole difficulty is that it is not. Nor is the problem solved by
looking further back in time, or by adjusting for how sick and active a practice is; both reduce
the inflation without removing it or changing the direction of the asymmetry.

**What follows for practice.** We would not argue that ecological analyses of open prescribing
data are never worth doing; they are excellent for describing prescribing and its variation. But
an analysis that relates prescribing to disease should report, alongside any association:

- an empirical null, most simply the same analysis with the exposure measured after the outcome;
- a positive control, a drug paired with its own indication, demonstrating the design can detect
  something;
- where the variation lies, between units and within them, since fixed effects may have removed
  all of it;
- the smallest effect the design could detect, next to the effect size that is actually plausible.

Had we reported only our primary estimates, this work would have yielded roughly 2,000
false-discovery-rate-significant findings at area level and several thousand at practice level,
any of which could have been written up with a mechanism attached. The diagnostics are what
separate those from nothing, and they are cheap.

**Limitations.** The outcomes are those published in Fingertips, which are weighted towards
registers, mortality and service measures rather than incident disease; only a minority are
recorded outside the practice. Exposure is prescribing volume, not people treated, and additional
volume may lengthen existing courses rather than reach new patients. Our scan used a single
one-year lag; effects with longer or shorter latency would be missed, though the positive controls
suggest the limitation is not timing. The practice panel is unbalanced because practices merge and
close. Finally, this is an ecological analysis throughout and its conclusions concern what these
data can support, not whether any particular medicine affects any particular disease.

## Conclusions

Open English prescribing and disease data cannot support inference about the effects of medicines
on disease. At area level the adjustment required to make the comparison fair removes the
information needed to make it at all. At practice level information survives, but what it measures
is diagnosis driving prescribing, and the drift of practices over time. A scan of 23,000 pairs
produced as many associations running backwards in time as forwards, and its strongest candidate
was patient satisfaction. Analyses of these data that do not report an empirical null and a
positive control should be assumed to be measuring confounding.
