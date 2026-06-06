#!/usr/bin/env python

import datetime
import dataclasses

from matplotlib import pyplot, dates

import matplotlib_extras


def create_date(year, month=1, day=1):
    return datetime.date(year, month, day)


@dataclasses.dataclass
class Event:
    date: datetime.date
    offset: float
    label: str
    color: str
    notes: str

OFFSET = 0.25
COLORS = {
    'geoframework': 'deepskyblue',
    'cig': 'yellow',
    'lithomop': 'orange',
    'pylith': "lime",
    }


EVENTS = (
    Event(
        date=create_date(2002, month=6),
        offset=3.5*OFFSET,
        label="Jun 2002: SCEC Fault Systems Workshop #1",
        color=COLORS["geoframework"],
        notes=(
            "Workshop organized by Mark Simons and Brad Hager.",
            "",
            "Brad Aagaard and Matt Knepley attend",
            ),
        ),
    Event(
        date=create_date(2003),
        offset=2.8*OFFSET,
        label="2003: Caltech GeoFramework Project",
        color=COLORS["geoframework"],
        notes=(
            "Re-engineer and couple codes in geophysics using Pyre framework.",
            "",
            "Weekly tutorials at Caltech HPC center led by Michael Aivazis.",
            "Brad Aagaard + Charles Williams + Matt Knepley participate",
            "",
            "Idea formed for developing a community code focused on modeling crustal deformation associated with earthquakes.",
            "Begin converting Tecton to Pyre.",
            ),
        ),
    Event(
        date=create_date(2003, month=8),
        offset=2.0*OFFSET,
        label="Aug 2003: SCEC Fault Systems Workshop #2",
        color=COLORS["geoframework"],
        notes=(
            "Brad Aagaard, Charles Williams, and Matt Knepley participate",
            "",
            "Community forms around annual workshops which eventually become biannual workshops",
            ),
        ),
    Event(
        date=create_date(2004, month=4),
        offset=1.5*OFFSET,
        label="Apr 2004: Begin LithoMop development",
        color=COLORS["lithomop"],
        notes=(
            "LithoMop = Tecton (F77) + Pyre (Python) + PETSc (C)\n",
            "Charles Williams + Matt Knepley",
            "",
            "EqSim (C++) + Pyre(Python) + PETSc(C)"
            "Brad Aagaard"
            ),
    ),
    Event(
        date=create_date(2005, month=6),
        offset=1.5*OFFSET,
        label="2005: Start of CIG",
        color=COLORS["cig"],
        notes=(
            "NSF-funded Computational Infrastructure for Geodynamics (CIG) Project begins",
        ),
    ),
    Event(
        date=create_date(2006),
        offset=OFFSET,
        label=r"2006: LithoMop $\rightarrow$ PyLith",
        color=COLORS["pylith"],
        notes=(
            "LithoMop renamed to PyLith.",
            "Brad Aagaard + Charles Williams + Matt Knepley",
        ),
    ),
    Event(
        date=create_date(2007),
        offset=OFFSET,
        label="2007: PyLith v1.0 released",
        color=COLORS["pylith"],
        notes=(
            "Quasi-static + dynamic; prescribed fault slip",
        ),
    ),
    Event(
        date=create_date(2010),
        offset=OFFSET,
        label="2010: PyLith v1.5 released",
        color=COLORS["pylith"],
        notes=(
            "Fault friction implemented",
        ),
    ),
    Event(
        date=create_date(2014),
        offset=OFFSET,
        label="2014: PyLith v2.0 released",
        color=COLORS["pylith"],
        notes=(
            "Rewrite of PETSc finite-element data structures",
        ),
    ),
    Event(
        date=create_date(2017),
        offset=OFFSET,
        label="2017: Begin work on PyLith v3.0",
        color=COLORS["pylith"],
        notes=(
            "Complete rewrite of PETSc+PyLith finite-element implementation",
        ),
    ),
    Event(
        date=create_date(2022, month=6),
        offset=OFFSET,
        label="2022: PyLith v3.0 released",
        color=COLORS["pylith"],
        notes=(
            "Multiphysics implementation; flexible discretization; PETSc time stepping; update to Python 3.",
        ),
    ),
    Event(
        date=create_date(2023, month=12),
        offset=OFFSET,
        label="2023: PyLith v4.0 released",
        color=COLORS["pylith"],
        notes=(
            "Minor update to user interface",
            "Switch to semantic versioning",
        ),
    ),
    Event(
        date=create_date(2026, month=2),
        offset=1.5*OFFSET,
        label="2026: PyLith v5.0 release",
        color=COLORS["pylith"],
        notes=(
            "Improve scalability and performance",
        ),
    ),
    Event(
        date=create_date(2028, month=4),
        offset=OFFSET,
        label="2028: PyLith v6.0 release",
        color=COLORS["pylith"],
        notes=(
            "Update to current Pyre simulation framework",
        ),
    ),
)

pyplot.style.use(("matplotlib_extras.size-paper", "matplotlib_extras.color-darkbg"))

for i_frame, event in enumerate(EVENTS):

    figure = pyplot.Figure(figsize=(7.0, 3.5), dpi=300)
    rect_factory = matplotlib_extras.axes.RectFactory(figure, margins=((0.2, 0, 1.2), (0.3, 0, 0.1)))

    ax = figure.add_axes(rect_factory.rect(row=1, col=1))

    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.spines[['top', "left", "right"]].set_visible(False)

    locator = dates.AutoDateLocator(minticks=10, maxticks=12)

    ax.xaxis_date()
    ax.set_xlim(create_date(2002), create_date(2029))
    ax.set_ylim((0, 3))
    ax.xaxis.set_major_locator(locator)

    for p_frame, p_event in enumerate(EVENTS[0:i_frame+1]):

        ax.arrow(p_event.date, p_event.offset, 0, -p_event.offset, color=p_event.color, linewidth=0.8)
        font_weight = 'normal' if p_frame < i_frame else 'bold'
        ax.text(p_event.date, p_event.offset, p_event.label, color=p_event.color,
                rotation=45.0,
                horizontalalignment='left',
                verticalalignment='bottom',
                fontweight=font_weight)
        
    ax.text(0.53, 0.95, "\n".join(event.notes),
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes,
            wrap=True,
            linespacing=1.3,
            )

    figure.savefig(f"figs/pylith-timeline-{i_frame:02d}.pdf")
    pyplot.close(figure)
