#!/usr/bin/env bash
# Build the manuscript from paper/manuscript.md: Word, PDF, and the HTML page for the Artifact.
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p figures
cp ../outputs/panel_annual/panel_annual_forest_plot.png \
   ../outputs/panel_annual_ltla/panel_annual_ltla_forest_plot.png \
   ../outputs/hospital/hospital_positive_control.png \
   ../outputs/steroids/ocs_national_trends.png \
   ../outputs/steroids/ocs_ukborn_tb_by_region.png \
   ../outputs/panel/panel_forest_plot.png \
   ../outputs/forest_plot.png \
   ../outputs/steroids/ocs_tb_long_difference.png figures/

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
