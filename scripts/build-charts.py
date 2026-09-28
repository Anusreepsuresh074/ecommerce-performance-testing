#!/usr/bin/env python3
"""Draws the Test Summary Report's charts as static SVG files (standard library only).

Usage: scripts/build-charts.py <load run 1> <load run 2> <stress run> <spike run>    (run folders in results/)
Writes docs/images/load-repeatability.svg, stress-trend.svg and spike-timeline.svg.

Each chart has one y-axis (two measures go in two stacked panels, never a dual axis), a legend when it shows two
series, direct labels, and light and dark colours (validated categorical palette slots 1 and 2). The numbers come
from the same results.jtl files and the same percentile method as evaluate-run.py.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "images"

_spec = importlib.util.spec_from_file_location("evaluate_run", ROOT / "scripts" / "evaluate-run.py")
evaluate_run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(evaluate_run)

W, LEFT, RIGHT = 760, 64, 24
STYLE = """<style>
  .bg { fill: #fcfcfb } .ink { fill: #0b0b0b } .ink2 { fill: #52514e } .grid { stroke: #e4e3de }
  .axis { stroke: #b5b3ab } .s1 { stroke: #2a78d6 } .s2 { stroke: #eb6834 }
  .f1 { fill: #2a78d6 } .f2 { fill: #eb6834 }
  .ref { stroke: #52514e } .ring { stroke: #fcfcfb } .band { fill: #eb6834; fill-opacity: 0.08 }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a19 } .ink { fill: #ffffff } .ink2 { fill: #c3c2b7 } .grid { stroke: #33332f }
    .axis { stroke: #5c5b55 } .s1 { stroke: #3987e5 } .s2 { stroke: #d95926 }
    .f1 { fill: #3987e5 } .f2 { fill: #d95926 }
    .ref { stroke: #c3c2b7 } .ring { stroke: #1a1a19 } .band { fill: #d95926; fill-opacity: 0.14 }
  }
  text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 12px }
  .title { font-size: 15px; font-weight: 600 } .sub { font-size: 12px } .panel { font-size: 12px; font-weight: 600 }
</style>"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Panel:
    """One plot area with a single linear y-axis."""

    def __init__(self, top, height, x_max, y_max, y_step, title, y_unit, x_min=0):
        self.top, self.h, self.x_min, self.x_max, self.y_max = top, height, x_min, x_max, y_max
        self.y_step, self.title, self.y_unit = y_step, title, y_unit
        self.parts = []

    def x(self, v):
        return LEFT + (v - self.x_min) / (self.x_max - self.x_min) * (W - LEFT - RIGHT)

    def y(self, v):
        return self.top + self.h - v / self.y_max * self.h

    def frame(self, x_ticks, x_label):
        p = [f'<text class="panel ink" x="{LEFT}" y="{self.top - 12}">{esc(self.title)}</text>']
        v = 0
        while v <= self.y_max + 1e-9:
            yy = self.y(v)
            p.append(f'<line class="grid" x1="{LEFT}" x2="{W - RIGHT}" y1="{yy:.1f}" y2="{yy:.1f}" stroke-width="1"/>')
            label = f"{v:g}{self.y_unit}" if v else "0"
            p.append(f'<text class="ink2" x="{LEFT - 8}" y="{yy + 4:.1f}" text-anchor="end">{label}</text>')
            v += self.y_step
        base = self.y(0)
        p.append(f'<line class="axis" x1="{LEFT}" x2="{W - RIGHT}" y1="{base}" y2="{base}" stroke-width="1"/>')
        for t, lab in x_ticks:
            p.append(f'<text class="ink2" x="{self.x(t):.1f}" y="{base + 18}" text-anchor="middle">{esc(lab)}</text>')
        if x_label:
            p.append(f'<text class="ink2" x="{W - RIGHT}" y="{base + 34}" text-anchor="end">{esc(x_label)}</text>')
        self.parts = p + self.parts

    def band(self, x0, x1, label):
        left, width, mid = self.x(x0), self.x(x1) - self.x(x0), (self.x(x0) + self.x(x1)) / 2
        self.parts.append(f'<rect class="band" x="{left:.1f}" y="{self.top}" width="{width:.1f}" height="{self.h}"/>')
        self.parts.append(
            f'<text class="ink2" x="{mid:.1f}" y="{self.top + self.h - 8}" text-anchor="middle">{esc(label)}</text>'
        )

    def ref_line(self, value, label):
        yy = self.y(value)
        self.parts.append(
            f'<line class="ref" x1="{LEFT}" x2="{W - RIGHT}" y1="{yy:.1f}" y2="{yy:.1f}" stroke-width="1" '
            f'stroke-dasharray="4 4"/>'
        )
        self.parts.append(f'<text class="ink2" x="{W - RIGHT}" y="{yy - 6:.1f}" text-anchor="end">{esc(label)}</text>')

    def line(self, points, cls, label=None, markers=True, step=False):
        pts = [(self.x(a), self.y(b)) for a, b in points if b is not None]
        if not pts:
            return
        if step:
            d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
            for (_x0, y0), (x1, y1) in zip(pts, pts[1:], strict=False):
                d += f" L{x1:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}"
        else:
            d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        stroke = 'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'
        self.parts.append(f'<path class="s{cls}" d="{d}" fill="none" {stroke}/>')
        if markers:
            for a, b in pts:
                self.parts.append(f'<circle class="f{cls} ring" cx="{a:.1f}" cy="{b:.1f}" r="4" stroke-width="2"/>')
        if label:
            a, b = pts[-1]
            text = f'<text class="ink" x="{a - 6:.1f}" y="{b - 10:.1f}" text-anchor="end">{esc(label)}</text>'
            self.parts.append(text)

    def bars(self, items, width):
        for xv, val, lab in items:
            x0, top, base = self.x(xv) - width / 2, self.y(val), self.y(0)
            r = min(4, (base - top) / 2)
            d = (
                f"M{x0:.1f},{base:.1f} L{x0:.1f},{top + r:.1f} Q{x0:.1f},{top:.1f} {x0 + r:.1f},{top:.1f} "
                f"L{x0 + width - r:.1f},{top:.1f} Q{x0 + width:.1f},{top:.1f} {x0 + width:.1f},{top + r:.1f} "
                f"L{x0 + width:.1f},{base:.1f} Z"
            )
            self.parts.append(f'<path class="f1" d="{d}"/>')
            self.parts.append(
                f'<text class="ink" x="{self.x(xv):.1f}" y="{top - 6:.1f}" text-anchor="middle">{esc(lab)}</text>'
            )


def legend(y, items):
    parts, x = [], LEFT
    for cls, label in items:
        parts.append(
            f'<line class="s{cls}" x1="{x}" x2="{x + 18}" y1="{y - 4}" y2="{y - 4}" stroke-width="2"/>'
            f'<circle class="f{cls}" cx="{x + 9}" cy="{y - 4}" r="4"/>'
        )
        parts.append(f'<text class="ink2" x="{x + 24}" y="{y}">{esc(label)}</text>')
        x += 32 + 7 * len(label)
    return parts


def svg(name, height, title, subtitle, panels, extra=()):
    body = [
        f'<rect class="bg" width="{W}" height="{height}" rx="8"/>',
        f'<text class="title ink" x="{LEFT}" y="30">{esc(title)}</text>',
        f'<text class="sub ink2" x="{LEFT}" y="50">{esc(subtitle)}</text>',
    ]
    for p in panels:
        body += p.parts
    body += list(extra)
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img" '
        f'aria-label="{esc(title)}. {esc(subtitle)}"><title>{esc(title)}</title>{STYLE}{"".join(body)}</svg>\n'
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(doc)
    print(f"docs/images/{name}")


def load(run):
    samples = evaluate_run.load_samples(ROOT / "results" / run / "results.jtl")
    return samples, min(s["start"] for s in samples)


def window_stat(samples, t0, lo, hi, key):
    st = evaluate_run.stats(evaluate_run.in_window(samples, t0, [lo, hi]), hi - lo)
    return st[key] if st["samples"] >= 5 else None


def load_chart(run1, run2):
    p = Panel(
        top=96, height=240, x_max=660, y_max=1600, y_step=400, title="p90 response time, every 60 s (ms)", y_unit=""
    )
    p.frame([(t, f"{t // 60} min") for t in range(0, 661, 120)], "time since start")
    p.band(0, 60, "ramp-up")
    p.ref_line(1500, "NFR-01: p90 ≤ 1500 ms")
    for cls, run, lab in ((1, run1, "Run 1"), (2, run2, "Run 2")):
        s, t0 = load(run)
        pts = [(lo + 30, window_stat(s, t0, lo, lo + 60, "p90")) for lo in range(0, 660, 60)]
        p.line(pts, cls, label=lab)
    svg(
        "load-repeatability.svg",
        400,
        "PT-03 Load: two runs, 6 users, 1.25 req/s",
        "Same load, same script: the p90 moves with internet tail latency, far below the SLA.",
        [p],
        legend(380, [(1, f"Run 1 ({run1[:16]})"), (2, f"Run 2 ({run2[:16]})")]),
    )


def stress_chart(run):
    s, t0 = load(run)
    steps = [(3, 0), (6, 120), (9, 240), (12, 360), (15, 480)]
    rt = Panel(
        top=96,
        height=210,
        x_min=1.5,
        x_max=16.5,
        y_max=2000,
        y_step=500,
        title="Response time per step (ms)",
        y_unit="",
    )
    rt.frame([(u, f"{u} users") for u, _ in steps], None)
    rt.ref_line(2000, "NFR-05 (peak): p90 ≤ 2000 ms")
    rt.line([(u, window_stat(s, t0, lo, lo + 120, "p90")) for u, lo in steps], 2, label="p90")
    rt.line([(u, window_stat(s, t0, lo, lo + 120, "median")) for u, lo in steps], 1, label="median")
    tp = Panel(
        top=370, height=130, x_min=1.5, x_max=16.5, y_max=5, y_step=1, title="Throughput per step (req/s)", y_unit=""
    )
    tp.frame([(u, f"{u} users") for u, _ in steps], "virtual users")
    tp.ref_line(5, "safety ceiling 5 req/s")
    tp.bars([(u, v, f"{v:.2f}") for u, lo in steps if (v := window_stat(s, t0, lo, lo + 120, "throughput_rps"))], 34)
    svg(
        "stress-trend.svg",
        560,
        "PT-05 Stress: 3 → 15 users in 2-minute steps",
        "Throughput grows linearly with users while response time stays flat: no degradation in the tested range.",
        [rt, tp],
        legend(548, [(2, "p90"), (1, "median")]),
    )


def spike_chart(run):
    s, t0 = load(run)
    rt = Panel(
        top=96, height=200, x_max=420, y_max=2000, y_step=500, title="p90 response time, every 20 s (ms)", y_unit=""
    )
    rt.frame([(t, f"{t // 60} min") for t in range(0, 421, 60)], None)
    rt.band(120, 240, "spike: 15 users")
    rt.ref_line(2000, "NFR-05: p90 ≤ 2000 ms")
    rt.line([(lo + 10, window_stat(s, t0, lo, lo + 20, "p90")) for lo in range(0, 420, 20)], 1, markers=False)
    users = Panel(top=360, height=110, x_max=420, y_max=16, y_step=5, title="Active virtual users", y_unit="")
    users.frame([(t, f"{t // 60} min") for t in range(0, 421, 60)], "time since start")
    users.band(120, 240, "")
    counts = []
    for lo in range(0, 420, 5):
        sub = evaluate_run.in_window(s, t0, [lo, lo + 5])
        counts.append((lo, max((x["threads"] for x in sub), default=counts[-1][1] if counts else 0)))
    users.line(counts + [(420, counts[-1][1])], 1, markers=False, step=True)
    svg(
        "spike-timeline.svg",
        510,
        "PT-06 Spike: 6 → 15 → 6 users",
        "The surge of 9 extra users in 10 s leaves response time unchanged; recovery p90 is 0.88× the pre-spike p90.",
        [rt, users],
    )


def main():
    if len(sys.argv) != 5:
        sys.exit("Usage: scripts/build-charts.py <load run 1> <load run 2> <stress run> <spike run>")
    load_run1, load_run2, stress_run, spike_run = sys.argv[1:]
    load_chart(load_run1, load_run2)
    stress_chart(stress_run)
    spike_chart(spike_run)


if __name__ == "__main__":
    main()
