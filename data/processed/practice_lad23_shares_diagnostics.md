# Practice -> LAD23 apportionment by registered-patient residence: diagnostics

Source: NHS Digital 'Patients Registered at a GP Practice', practice x LSOA files (April snapshots). Earliest LSOA-level release is January 2014 (wide format, pub13365); no LSOA files exist for 2013 or earlier publications, so 2011-2013 must borrow the 2014 shares downstream.

LSOA11 -> LAD23: ONS LSOA11_LSOA21_LAD22_EW_LU_v5 (LAD22 recoded to April 2023 unitaries for Cumbria, North Yorkshire, Somerset; LSOA11s split across LSOA21s are apportioned equally among pieces). LSOA21 -> LAD23: LSOA21_SICBL26_lookup.csv (LAD26; E08000038/39 recoded to E08000016/19), Welsh LSOA21 from v5. English LSOA21s where the two sources disagree on LAD23: 0. Codes not found in the release's own vintage fall back to the other vintage. Welsh residents are kept as W06 LAD codes (so English shares are net of patients living in Wales). Isles of Scilly and City of London keep their codes.

## Releases

| year | release | vintage | raw rows | practice x LSOA rows | patients | unmapped share | fallback-vintage share | Welsh-resident share | E-codes not in LTLA23 list |
|---|---|---|---|---|---|---|---|---|---|
| 2014 | 201404 | LSOA11 (only-21 codes 0, only-11 codes 1034) | 729,516 | 729,516 | 56,442,636 | 0.0507% | 0.0000% | 0.000% | - |
| 2015 | 201504 | LSOA11 (only-21 codes 0, only-11 codes 1037) | 745,396 | 745,396 | 57,011,677 | 0.0447% | 0.0000% | 0.026% | - |
| 2016 | 201604 | LSOA11 (only-21 codes 0, only-11 codes 1037) | 776,309 | 776,309 | 57,631,776 | 0.0510% | 0.0000% | 0.026% | - |
| 2017 | 201704 | LSOA11 (only-21 codes 0, only-11 codes 1037) | 796,587 | 796,587 | 58,328,549 | 0.0757% | 0.0000% | 0.024% | - |
| 2018 | 201804 | LSOA11 (only-21 codes 0, only-11 codes 1037) | 806,289 | 806,289 | 59,039,595 | 0.0921% | 0.0000% | 0.024% | - |
| 2019 | 201904 | LSOA11 (only-21 codes 0, only-11 codes 1038) | 811,948 | 811,948 | 59,759,638 | 0.0984% | 0.0000% | 0.023% | - |
| 2020 | 202004 | LSOA11 (only-21 codes 0, only-11 codes 1039) | 820,367 | 820,367 | 60,458,907 | 0.0583% | 0.0000% | 0.023% | - |
| 2021 | 202104 | LSOA11 (only-21 codes 0, only-11 codes 1039) | 848,713 | 848,713 | 60,744,002 | 0.0545% | 0.0000% | 0.023% | - |
| 2022 | 202204 | LSOA11 (only-21 codes 0, only-11 codes 1038) | 866,879 | 866,879 | 61,625,745 | 0.0447% | 0.0000% | 0.023% | - |
| 2023 | 202304 | LSOA11 (only-21 codes 0, only-11 codes 1037) | 871,114 | 871,114 | 62,418,295 | 0.0380% | 0.0000% | 0.022% | - |
| 2024 | 202404 | LSOA11 (only-21 codes 0, only-11 codes 1037) | 876,044 | 876,044 | 63,227,624 | 0.0335% | 0.0000% | 0.022% | - |

URLs, columns and top unmapped codes:

- 2014: https://files.digital.nhs.uk/publicationimport/pub13xxx/pub13932/gp-reg-patients-04-2014-totals-lsoa-alt.csv (file 201404_gp-reg-patients-04-2014-totals-lsoa-alt.csv; columns: PRACTICE_CODE, ORG_NAME, LSOA_CODE, Male Patients, Female Patients, All Patients; extract date ; top unmapped LSOA codes: {'NO2011': 28641})
- 2015: https://files.digital.nhs.uk/publicationimport/pub17xxx/pub17356/gp-reg-patients-lsoa-alt-tall.csv (file 201504_gp-reg-patients-lsoa-alt-tall.csv; columns: PRACTICE_CODE, ORG_NAME, LSOA_CODE, Male Patients, Female Patients, All Patients; extract date ; top unmapped LSOA codes: {'NO2011': 25483})
- 2016: https://files.digital.nhs.uk/publicationimport/pub20xxx/pub20480/lsoa-alt-format-tall.csv (file 201604_lsoa-alt-format-tall.csv; columns: PRACTICE_CODE, NAME, LSOA_CODE, Male Patients, Female Patients, All Patients; extract date ; top unmapped LSOA codes: {'NO2011': 29402})
- 2017: https://files.digital.nhs.uk/publicationimport/pub23xxx/pub23475/gp-reg-pat-prac-lsoa-all-females-males.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, NUMBER_OF_PATIENTS; extract date ['01-Apr-17']; top unmapped LSOA codes: {'NO2011': 44130})
- 2018: https://files.digital.nhs.uk/62/638799/gp-reg-pat-prac-lsoa-all-females-males.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, Number of Patients; extract date ['01APR2018']; top unmapped LSOA codes: {'NO2011': 54356})
- 2019: https://files.digital.nhs.uk/16/740C9E/gp-reg-pat-prac-lsoa-male-female-apr-19.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, Number of Patients; extract date ['01APR2019']; top unmapped LSOA codes: {'NO2011': 58793})
- 2020: https://files.digital.nhs.uk/93/714E7D/gp-reg-pat-prac-lsoa-male-female-Apr-20.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, Number of Patients; extract date ['01APR2020']; top unmapped LSOA codes: {'NO2011': 35246})
- 2021: https://files.digital.nhs.uk/52/2D964D/gp-reg-pat-prac-lsoa-male-female-Apr-21.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, Number of Patients; extract date ['01APR2021']; top unmapped LSOA codes: {'NO2011': 33095})
- 2022: https://files.digital.nhs.uk/20/64261B/gp-reg-pat-prac-lsoa-male-female-April-22.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, NUMBER_OF_PATIENTS; extract date ['01Apr2022']; top unmapped LSOA codes: {'NO2011': 27535})
- 2023: https://files.digital.nhs.uk/AA/B3CF39/gp-reg-pat-prac-lsoa-male-female-April-23.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, NUMBER_OF_PATIENTS; extract date ['01Apr2023']; top unmapped LSOA codes: {'NO2011': 23689})
- 2024: https://files.digital.nhs.uk/5C/704155/gp-reg-pat-prac-lsoa-male-female-Apr-24.zip (file gp-reg-pat-prac-lsoa-all.csv; columns: PUBLICATION, EXTRACT_DATE, PRACTICE_CODE, PRACTICE_NAME, LSOA_CODE, SEX, NUMBER_OF_PATIENTS; extract date ['01Apr2024']; top unmapped LSOA codes: {'NO2011': 21161})

## Practices and out-of-area share

out_share = share of a practice's registered patients living outside the LAD23 containing the practice postcode (practice postcode from EPD for the release month; postcode LAD from ONSPD cache).

| year | practices | practices_with_home_lad | median_out | p90_out | patient_weighted_out |
|---|---|---|---|---|---|
| 2014 | 7997 | 7955 | 0.0185 | 0.1907 | 0.0617 |
| 2015 | 7859 | 7797 | 0.0192 | 0.1913 | 0.0623 |
| 2016 | 7680 | 7607 | 0.0207 | 0.1943 | 0.0632 |
| 2017 | 7492 | 7377 | 0.0215 | 0.1968 | 0.0641 |
| 2018 | 7241 | 7129 | 0.0221 | 0.1980 | 0.0649 |
| 2019 | 6980 | 6893 | 0.0224 | 0.1979 | 0.0665 |
| 2020 | 6797 | 6715 | 0.0231 | 0.2013 | 0.0677 |
| 2021 | 6623 | 6580 | 0.0240 | 0.2046 | 0.0691 |
| 2022 | 6518 | 6483 | 0.0243 | 0.2077 | 0.0708 |
| 2023 | 6419 | 6379 | 0.0247 | 0.2100 | 0.0718 |
| 2024 | 6309 | 6263 | 0.0244 | 0.2110 | 0.0733 |

## Selected practices

| year | kind | practice_code | home | list | out_share |
|---|---|---|---|---|---|
| 2014 | largest out-of-area share (list>=1000) | L83100 | E06000026 | 11518.000 | 1.000 |
| 2014 | largest out-of-area share (list>=1000) | M82620 | W06000023 | 2180.000 | 1.000 |
| 2014 | largest out-of-area share (list>=1000) | E87717 | E09000033 | 1352.000 | 0.858 |
| 2014 | largest out-of-area share (list>=1000) | E85117 | E09000027 | 3375.000 | 0.844 |
| 2014 | largest out-of-area share (list>=1000) | F83672 | E09000033 | 10430.000 | 0.821 |
| 2014 | largest out-of-area share (list>=1000) | C81018 | E07000035 | 8415.000 | 0.811 |
| 2014 | largest out-of-area share (list>=1000) | E83654 | E09000007 | 2255.000 | 0.804 |
| 2014 | largest out-of-area share (list>=1000) | L83098 | E07000042 | 4708.000 | 0.800 |
| 2014 | largest out-of-area share (list>=1000) | F84041 | E09000019 | 5978.000 | 0.784 |
| 2014 | largest out-of-area share (list>=1000) | E87768 | E09000033 | 9424.000 | 0.756 |
| 2014 | largest lists | B82005 | E06000014 | 53571.000 | 0.019 |
| 2014 | largest lists | K83002 | E06000061 | 47137.000 | 0.014 |
| 2014 | largest lists | M85063 | E08000025 | 38860.000 | 0.014 |
| 2014 | largest lists | C84023 | E06000018 | 36436.000 | 0.146 |
| 2014 | largest lists | C82038 | E07000133 | 35565.000 | 0.010 |
| 2014 | largest lists | B86110 | E08000035 | 35348.000 | 0.000 |
| 2014 | largest lists | L83016 | E07000041 | 34691.000 | 0.056 |
| 2014 | largest lists | Y02423 | E09000032 | 34442.000 | 0.207 |
| 2014 | largest lists | G82071 | E07000106 | 34317.000 | 0.010 |
| 2014 | largest lists | H81133 | E07000208 | 32333.000 | 0.118 |
| 2014 | E85124 (GP at Hand) | E85124 | E09000013 | 3004.000 | 0.010 |
| 2019 | largest out-of-area share (list>=1000) | E87768 | E09000033 | 15745.000 | 0.952 |
| 2019 | largest out-of-area share (list>=1000) | E85124 | E09000013 | 48855.000 | 0.905 |
| 2019 | largest out-of-area share (list>=1000) | E84653 | E09000003 | 2891.000 | 0.876 |
| 2019 | largest out-of-area share (list>=1000) | B87030 | E08000035 | 27104.000 | 0.831 |
| 2019 | largest out-of-area share (list>=1000) | C81018 | E07000035 | 8599.000 | 0.826 |
| 2019 | largest out-of-area share (list>=1000) | L83098 | E07000042 | 5032.000 | 0.805 |
| 2019 | largest out-of-area share (list>=1000) | F83672 | E09000033 | 10239.000 | 0.791 |
| 2019 | largest out-of-area share (list>=1000) | D82048 | E07000148 | 14060.000 | 0.749 |
| 2019 | largest out-of-area share (list>=1000) | M85177 | E08000029 | 6735.000 | 0.748 |
| 2019 | largest out-of-area share (list>=1000) | F84041 | E09000019 | 7842.000 | 0.744 |
| 2019 | largest lists | G85034 | E09000028 | 73175.000 | 0.019 |
| 2019 | largest lists | M85063 | E08000025 | 66349.000 | 0.023 |
| 2019 | largest lists | D81022 | E06000031 | 64481.000 | 0.123 |
| 2019 | largest lists | P81002 | E07000121 | 63455.000 | 0.009 |
| 2019 | largest lists | B82005 | E06000014 | 58704.000 | 0.043 |
| 2019 | largest lists | Y01008 | E07000121 | 54076.000 | 0.000 |
| 2019 | largest lists | M85046 | E08000025 | 50587.000 | 0.179 |
| 2019 | largest lists | K83002 | E06000061 | 49094.000 | 0.010 |
| 2019 | largest lists | E85124 | E09000013 | 48855.000 | 0.905 |
| 2019 | largest lists | M81026 | E06000019 | 47309.000 | 0.000 |
| 2019 | E85124 (GP at Hand) | E85124 | E09000013 | 48855.000 | 0.905 |
| 2024 | largest out-of-area share (list>=1000) | Y06389 | E06000033 | 1251.000 | 0.986 |
| 2024 | largest out-of-area share (list>=1000) | E87768 | E09000033 | 22987.000 | 0.938 |
| 2024 | largest out-of-area share (list>=1000) | E85124 | E09000013 | 98457.000 | 0.929 |
| 2024 | largest out-of-area share (list>=1000) | F83672 | E09000033 | 16231.000 | 0.867 |
| 2024 | largest out-of-area share (list>=1000) | B87030 | E08000035 | 31403.000 | 0.849 |
| 2024 | largest out-of-area share (list>=1000) | C81018 | E07000035 | 8929.000 | 0.840 |
| 2024 | largest out-of-area share (list>=1000) | K83052 | E06000042 | 22677.000 | 0.805 |
| 2024 | largest out-of-area share (list>=1000) | L83098 | E07000042 | 5405.000 | 0.799 |
| 2024 | largest out-of-area share (list>=1000) | E84653 | E09000003 | 3125.000 | 0.778 |
| 2024 | largest out-of-area share (list>=1000) | E82124 | E07000098 | 32293.000 | 0.751 |
| 2024 | largest lists | E85124 | E09000013 | 98457.000 | 0.929 |
| 2024 | largest lists | F85002 | E09000010 | 93463.000 | 0.019 |
| 2024 | largest lists | E84066 | E09000005 | 91720.000 | 0.713 |
| 2024 | largest lists | B83033 | E08000032 | 86775.000 | 0.281 |
| 2024 | largest lists | G85034 | E09000028 | 76111.000 | 0.022 |
| 2024 | largest lists | P81002 | E07000121 | 66089.000 | 0.009 |
| 2024 | largest lists | J82155 | E06000044 | 62279.000 | 0.143 |
| 2024 | largest lists | M85063 | E08000025 | 59418.000 | 0.016 |
| 2024 | largest lists | B82005 | E06000014 | 58372.000 | 0.017 |
| 2024 | largest lists | J81012 | E06000058 | 58325.000 | 0.005 |
| 2024 | E85124 (GP at Hand) | E85124 | E09000013 | 98457.000 | 0.929 |

## Per LAD: share of resident registered patients registered at practices located outside the LAD

Distribution across LADs:

| year | count | mean | std | min | 10% | 50% | 90% | max |
|---|---|---|---|---|---|---|---|---|
| 2014 | 296.000 | 0.072 | 0.061 | 0.000 | 0.012 | 0.055 | 0.155 | 0.297 |
| 2015 | 296.000 | 0.073 | 0.062 | 0.000 | 0.012 | 0.055 | 0.158 | 0.314 |
| 2016 | 296.000 | 0.074 | 0.061 | 0.000 | 0.011 | 0.055 | 0.156 | 0.300 |
| 2017 | 296.000 | 0.075 | 0.062 | 0.000 | 0.012 | 0.057 | 0.158 | 0.304 |
| 2018 | 296.000 | 0.076 | 0.062 | 0.000 | 0.013 | 0.058 | 0.159 | 0.304 |
| 2019 | 296.000 | 0.078 | 0.063 | 0.000 | 0.014 | 0.061 | 0.158 | 0.327 |
| 2020 | 296.000 | 0.079 | 0.064 | 0.000 | 0.014 | 0.062 | 0.158 | 0.340 |
| 2021 | 296.000 | 0.080 | 0.065 | 0.000 | 0.014 | 0.062 | 0.160 | 0.365 |
| 2022 | 296.000 | 0.081 | 0.067 | 0.000 | 0.014 | 0.062 | 0.161 | 0.446 |
| 2023 | 296.000 | 0.082 | 0.068 | 0.000 | 0.013 | 0.064 | 0.161 | 0.470 |
| 2024 | 296.000 | 0.084 | 0.071 | 0.000 | 0.013 | 0.063 | 0.169 | 0.501 |

Top 20 LADs in 2024:

| lad23cd | patients | outside | share_outside | year |
|---|---|---|---|---|
| E09000001 | 12412.000 | 6215.000 | 0.501 | 2024 |
| E07000103 | 119955.000 | 43308.000 | 0.361 | 2024 |
| E07000102 | 101541.000 | 33076.000 | 0.326 | 2024 |
| E07000044 | 93856.000 | 29293.000 | 0.312 | 2024 |
| E07000038 | 106904.000 | 30907.000 | 0.289 | 2024 |
| E07000039 | 116988.000 | 32194.000 | 0.275 | 2024 |
| E07000196 | 112899.000 | 29412.000 | 0.261 | 2024 |
| E07000144 | 139248.000 | 34627.000 | 0.249 | 2024 |
| E07000099 | 136307.000 | 33500.000 | 0.246 | 2024 |
| E07000194 | 110774.000 | 26701.000 | 0.241 | 2024 |
| E07000211 | 154151.000 | 36780.000 | 0.239 | 2024 |
| E07000012 | 182224.000 | 41313.000 | 0.227 | 2024 |
| E07000111 | 124820.000 | 27994.000 | 0.224 | 2024 |
| E07000173 | 124947.000 | 28011.000 | 0.224 | 2024 |
| E07000180 | 151379.000 | 33261.000 | 0.220 | 2024 |
| E07000209 | 158359.000 | 34536.000 | 0.218 | 2024 |
| E07000086 | 144983.000 | 31559.000 | 0.218 | 2024 |
| E07000142 | 100757.000 | 21881.000 | 0.217 | 2024 |
| E09000015 | 320351.000 | 67673.000 | 0.211 | 2024 |
| E07000083 | 103597.000 | 21735.000 | 0.210 | 2024 |

Bottom 10 LADs in 2024:

| lad23cd | patients | outside | share_outside | year |
|---|---|---|---|---|
| E06000063 | 278822.000 | 1531.000 | 0.005 | 2024 |
| E06000026 | 281856.000 | 1410.000 | 0.005 | 2024 |
| E06000045 | 292114.000 | 1348.000 | 0.005 | 2024 |
| E08000026 | 438687.000 | 1876.000 | 0.004 | 2024 |
| E08000015 | 343648.000 | 1421.000 | 0.004 | 2024 |
| E07000178 | 207333.000 | 776.000 | 0.004 | 2024 |
| E06000043 | 326514.000 | 1183.000 | 0.004 | 2024 |
| E07000202 | 156324.000 | 400.000 | 0.003 | 2024 |
| E06000053 | 2395.000 | 5.000 | 0.002 | 2024 |
| E06000046 | 146044.000 | 59.000 | 0.000 | 2024 |
