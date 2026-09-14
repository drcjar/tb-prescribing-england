#!/usr/bin/env bash
# Build the manuscript from paper/manuscript.md: Word, PDF, and the HTML page for the Artifact.
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p figures
dot -Tpng -Gdpi=200 dag.dot -o figures/dag.png
# draft 3 figures (revised pipeline); each is copied under a stable name if present
copy_fig() { if [ -f "$1" ]; then cp "$1" "figures/$2"; else echo "missing figure: $1" >&2; fi; }
copy_fig ../outputs/panel_annual_ltla_residence/panel_forest_plot.png panel_forest_ltla_residence.png
copy_fig ../outputs/panel_annual_utla_residence/panel_forest_plot.png panel_forest_utla_residence.png
copy_fig ../outputs/descriptives/within_between_variation.png within_between_variation.png
copy_fig ../outputs/hospital/hospital_positive_control.png hospital_positive_control.png
copy_fig ../outputs/steroids/ocs_national_trends.png ocs_national_trends.png
copy_fig ../outputs/steroids/ocs_ukborn_tb_by_region.png ocs_ukborn_tb_by_region.png

pandoc manuscript.md -o manuscript.docx

MAINFONT="DejaVu Serif"
fc-list | grep -qi "Source Serif 4" && MAINFONT="Source Serif 4"
pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex \
  -V geometry:margin=2.3cm -V mainfont="$MAINFONT" -V fontsize=10pt -V colorlinks=true

pandoc manuscript.md -t html5 --section-divs --template=artifact_template.html -o manuscript_page.html
# wrap tables so wide tables scroll inside their own container
python3 - <<'EOF'
import re
from pathlib import Path
p = Path("manuscript_page.html")
html = p.read_text()
html = re.sub(r"(<table\b[^>]*>)", r'<div class="table-wrap">\1', html).replace("</table>", "</table></div>")
p.write_text(html)
print("tables wrapped:", html.count('class="table-wrap"'))
EOF
ls -la manuscript.docx manuscript.pdf manuscript_page.html figures/
