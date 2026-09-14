**Table S9. Primary care drug group definitions (regular expressions applied to BNF chemical substance names and BNF codes; drug_groups.py)**

| Drug group | Rule |
|:---|---:|
| Antituberculosis (descriptive) | code: `^0501090` |
| Systemic oral glucocorticoids | code: `^0603020`; name: `^(?:prednisolone\|prednisone\|methylprednisolone\|deflazacort\|dexamethasone)`; exclude: `inj\|infusion\|amp\|vial\|syringe\|pre-filled\|prefilled\|intra-articular\|suspension for injection` |
| Oral hydrocortisone | code: `^0603020`; name: `^hydrocortisone`; exclude: `inj\|infusion\|amp\|vial\|syringe\|pre-filled\|prefilled\|intra-articular\|suspension for injection` |
| Oral dexamethasone | code: `^0603020`; name: `^dexamethasone`; exclude: `inj\|infusion\|amp\|vial\|syringe\|pre-filled\|prefilled\|intra-articular\|suspension for injection` |
| Inhaled corticosteroids | code: `^0302000` |
| Conventional DMARDs | name: `^(?:methotrexate\|leflunomide\|azathioprine\|mercaptopurine)`; code: `^(?:1001030\|0802010\|0801030L0)` |
| Transplant immunosuppressants | name: `^(?:tacrolimus\|ciclosporin\|mycophenol\|sirolimus\|everolimus)`; code: `^0802` |
| Proton pump inhibitors | code: `^0103050` |
| Statins | code: `^0212000`; name: `statin` |
| Metformin | name: `metformin` |
| Insulins | code: `^060101` |
| Fluoroquinolones | name: `^(?:ciprofloxacin\|levofloxacin\|moxifloxacin\|ofloxacin)` |
| All antibacterials | code: `^0501` |
| Vitamin D | name: `^(?:colecalciferol\|ergocalciferol)` |
| Levothyroxine (negative control) | name: `^levothyroxine` |

BNF chapters 11–13 (eye, ear and nose, skin) are excluded unless a code rule applies; injectable presentations are excluded from oral groups. Prednisolone-equivalent factors: prednisolone and prednisone 1, methylprednisolone 1.25, deflazacort 0.83, dexamethasone 6.67. The SCMD product classification with DDDs is in outputs/hospital/vmp_classification.csv.
