## Results

### What the scan produces

The scan covered 32,608 drug-outcome pairs at upper-tier level, 20,112 at lower-tier level and
12,296 at practice level, each estimated twice (table 1).

{{table:table1_scan_summary}}

At area level, 18.8% of pairs reached conventional significance with prescribing in the year
before the outcome. Prescribing in the year *after* the outcome produced 19.2%. The inflation
factor was 2.1 for both. Lower-tier authorities gave 21.6% and 21.2%, inflation 2.3 for both. On
a quantile plot the two distributions lie on top of one another (figure 2, left), both at roughly
twice the null. Taken at face value the lag scan yields 1,885 associations surviving false
discovery rate correction; the nonsense control yields 2,074.

### Why: the fixed effects remove the signal

The positive controls explain this. Within areas over time, prescribing of a drug was unrelated
to the prevalence of the disease it treats: diabetes drugs against the diabetes register r = 0.03,
inhaled therapy against COPD r = 0.01, antihypertensives against hypertension r = -0.08,
antiplatelets against stroke r = -0.00. Between areas the same pairs correlate at 0.73 to 0.89
(figure 1, table 2).

{{figure:fig1}}

{{table:table2_between_within}}

Almost all the information in these data is cross-sectional. Area and year fixed effects, which
are needed to deal with the obvious confounding by population composition and deprivation, remove
it. What remains is too small to carry even the strongest relationship in the data, that between a
drug and its own indication, and the associations that survive are not distinguishable from those
of an impossible exposure.

### Practices: sensitivity, but the signal runs backwards

Moving to practices increases the units from 151 to about 6,200 and the period from 11 years to
16. Here the positive controls succeed, and strongly: diabetes drugs against the diabetes register
z = 6.5, inhaled therapy against COPD z = 7.3, antiepileptics against epilepsy z = 10.6, dementia
drugs against dementia z = 16.0 (table 3). The design can detect relationships when they exist.

{{table:table3_indication_controls}}

Two features undermine it. First, in every indication pair the association with prescribing in the
*following* year was larger than with the preceding year, decisively so for dementia (z = 25.7
against 16.0). This is the expected direction if diagnosis drives prescribing, and it means the
temporal ordering in these data points the opposite way to a drug effect. Second, 44.9% of all
pairs were significant with the preceding year and 49.7% with the following year, inflation 6.4
and 8.3 (figure 2, right); practices that grow, merge or improve their coding do more of
everything at once.

{{figure:fig2}}

We checked whether the inflation was an artefact of a shared denominator, since both exposure and
outcome are expressed per registered patient and list sizes are known to be inflated. It is not:
adding log list size as a covariate moved the diabetes positive control from z = 9.9 to 9.8, and
models using numerators with list size as a covariate agreed.

### The candidates that survive filtering

Restricting to pairs where the preceding year beats the following year, which is where a genuine
drug effect would sit, does not produce a plausible shortlist. The strongest such signal in the
entire scan was patient satisfaction with the practice, apparently produced by ear preparations,
antifungals and vaccines (table 4). Restricted to disease outcomes, the leading candidates were
peak flow meters against chronic kidney disease, night drainage bags and leg bags against bowel
cancer screening coverage, and gluten-free foods against cancer referral conversion (table 5).
These are markers of how sick and how intensively managed a practice's population is.

{{table:table4_top_hits}}

{{table:table5_top_disease_hits}}

### Worked example: immunosuppressants and tuberculosis

The hypothesis-driven analysis reached the same place by a different route. No medicine was
associated with notifications in the following year after correction for multiple testing;
systemic oral glucocorticoids gave an incidence rate ratio of 0.969 (95% CI 0.929 to 1.012) per
10% within-area increase. The negative-control exposure, levothyroxine, was inversely associated
to the same degree as metformin, and prescribing in the following year predicted fewer
notifications for several drug groups.

The quantitative version of the problem is stark. For oral glucocorticoids the smallest detectable
effect was 6.3% per 10% increase in prescribing, against 0.34% expected from published relative
risks and prevalence of use, and 0.04 to 0.09% implied by national records of steroid-associated
tuberculosis: a gap of 18 to 140 times. Across drug groups the gap ranged from 11 to 272 times. In
a simulation that preserved the real notification counts, the established glucocorticoid effect
was detected in 8.3% of replicates against 7.8% when there was no effect at all.

The one element that did work was the disease-specific positive control. Hospital treatment for
active tuberculosis tracked notifications between areas (Spearman rho 0.81) and within areas in
the same year (1.035, 1.009 to 1.061 per 10% increase). Even that, a drug used almost exclusively
for the outcome, was recovered with an elasticity of only 0.36 to 0.40.
