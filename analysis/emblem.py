"""
Provide the Feyenoord crest used in the dossier.

We use the real club crest supplied in the repo (Feyenoord.png, a 500x500
transparent PNG) and copy it to output/figures/emblem.png, which the report
reads. Kept as a tiny step so the asset pipeline is reproducible.
"""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "Feyenoord.png")
DST = os.path.join(ROOT, "output", "figures", "emblem.png")


def build(px=None):
    # The supplied file is WEBP with a .png extension; re-encode to a real PNG
    # (transparent background preserved) so matplotlib can read it.
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    Image.open(SRC).convert("RGBA").save(DST, "PNG")
    print(f"emblem <- {os.path.basename(SRC)} (re-encoded to PNG)")


# backward-compatible alias
def save_emblem(path=DST, px=None):
    build()


if __name__ == "__main__":
    build()
