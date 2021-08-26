#!/usr/bin/env python

import sys

model = sys.argv[1]

if not model in ['slipweak', 'timeweak', 'ratestate']:
    raise ValueError("Unknown friction model '%s'." % model)

# ======================================================================
import matplotlib.pyplot as pyplot
import numpy
from math import exp
import os

sys.path.append("%s/projects/pylith/benchmarks/figures" % os.environ['HOME'])
import matplotlibext

# ----------------------------------------------------------------------
if model == "slipweak" or model == "timeweak":
    slip = numpy.linspace(0.0, 2.0, num=201)
    mu_s = 0.6
    mu_d = 0.1
    d0 = 0.2
    mask = slip < d0
    mu_f = mask*(mu_d + (1.0-slip/d0)*(mu_s-mu_d)) + ~mask*mu_d
elif model == "ratestate":
    sliprate = numpy.logspace(-14, 1.0, num=401)
    mu_0 = 0.6
    a = 0.002
    b = 0.08
    L = 0.05
    V0 = 1.0e-10
    Vlinear = 1.0e-11
    mask = sliprate < Vlinear
    theta = L / (1.0e+2*Vlinear)
    mu_f = mu_0 + mask*(a*numpy.log(Vlinear/V0) + b*numpy.log(V0*theta/L)-a*(1.0-sliprate/Vlinear)) + ~mask*(a*numpy.log(sliprate/V0) + b*numpy.log(V0*theta/L))
    mu_f2 = mu_0 + a*numpy.log(sliprate/V0) + b*numpy.log(V0*theta/L)

else:
    raise ValueError("Unknown friction model '%s'." % model)



# ----------------------------------------------------------------------
figure = matplotlibext.Figure()
figure.open(3.0, 1.65, margins=[[0.55, 0, 0.15], [0.42, 0.4, 0.05]], dpi=150)

ax = figure.axes(1, 1, 1, 1)

if model == "slipweak":
    ax.plot(slip/d0, mu_f, linewidth=1, color='blue')
    ax.set_xlabel("Slip, $D / D_0$")
    ax.set_ylabel("Coef. of Friction, $\mu_f$")
    ax.set_xlim((0,5))
    ax.set_ylim((0,1))

elif model == "timeweak":
    ax.plot(slip/d0, mu_f, linewidth=1, color='blue')
    ax.set_xlabel("Time, $t / t_0$")
    ax.set_ylabel("Coef. of Friction, $\mu_f$")
    ax.set_xlim((0,5))
    ax.set_ylim((0,1))

elif model == "ratestate":
    ax.semilogx(sliprate, mu_f, linewidth=1, color='blue')
    ax.plot(sliprate, mu_f2, linewidth=0.5, color='gray')
    ax.set_xlabel("Slip Rate")
    ax.set_ylabel("Coef. of Friction, $\mu_f$")
    ax.set_xlim((1.0e-14, 1.0e-7))
    ax.set_ylim((0.35,0.45))

pyplot.show()
pyplot.savefig('friction_%s' % model)
