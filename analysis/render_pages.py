"""Render every report page to output/pages/{lang}_NN.png for visual QA."""
import os
import matplotlib.pyplot as plt
import build_report as B
import report_content as C

LANG = "nl" if C.NL else "en"
OUTDIR = os.path.join(os.path.dirname(__file__), "..", "output", "pages")
os.makedirs(OUTDIR, exist_ok=True)

PAGES = [B.page_cover, B.page_exec, B.page_probable_xi, B.page_form,
         B.page_possession, B.page_attack, B.page_press, B.page_vuln,
         B.page_setpiece, B.page_players, B.page_plan, B.page_week, B.page_method]


class Shim:
    def __init__(self):
        self.i = 0

    def savefig(self, fig, **kw):
        self.i += 1
        p = os.path.join(OUTDIR, f"{LANG}_{self.i:02d}.png")
        fig.savefig(p, facecolor=B.T.INK, dpi=110)
        plt.close(fig)
        print("wrote", os.path.basename(p))


sh = Shim()
for fn in PAGES:
    fn(sh)
print("done", LANG)
