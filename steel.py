'''Script to analyze moessbauer experiment'''

from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math


def lorentz(x, *p):
    A, gamma, x0, offset = p
    return offset + A * gamma**2 / ((x - x0)**2 + gamma**2)


def fit_it_one(p, x, y, yerr=None):
    if not yerr:
        return curve_fit(lorentz, x, y, p0=p)
    if yerr:
        return curve_fit(lorentz, x, y, p0=p, sigma=yerr)


def draw_lorentz(x, p):
    A, gamma, x0, offset = p
    return offset + A * gamma**2 / ((x - x0) ** 2 + gamma ** 2)


def read_manual_file(path, filename):
    steel_file = path + filename
    lines = loadtxt(steel_file, delimiter="\t")

    channel = []
    counts = []
    for event in lines:
        if event[1] > 50 and event[0]:
            channel.append(event[0])
            counts.append(event[1])

    yerrors = []
    for value in counts:
        yerrors.append(math.sqrt(value))
        # yerrors.append(0.1)

    p1 = [-2500, 3.75, 122, 500]
    fit_params, rest = fit_it_one(p1, channel, counts, yerrors)

    para = (fit_params[0], fit_params[1], fit_params[2], fit_params[3])

    # plt.plot(counts, 'b.')
    plt.errorbar(channel, counts, yerr=yerrors, fmt='b.')
    plt.plot(channel, draw_lorentz(channel, para), 'r')

    perr = np.sqrt(np.diag(rest))

    plt.figtext(0.55, 0.2, ("Center: %.1f +/- %.1f \nWidth %.1f +/- %.1f" % (para[2], perr[2], 2*para[1], 2*perr[1])))

    plt.savefig(path + "steel_line.png")

    plt.close()


def read_cassy_file(path, filename):
    file = open(path + filename, 'r')

    channel = []
    counts = []
    data = file.readlines()
    for line in range(261):
        if line > 4:
            line_data = data[line].split('\t')
            if float(line_data[1]) > 50:
                channel.append(float(line_data[2]))
                counts.append(float(line_data[1]))
    print(channel)
    print(counts)
    return channel, counts


def fit_it(channel, counts, path):
    yerrors = []
    for value in counts:
        yerrors.append(math.sqrt(value))
        # yerrors.append(0.1)

    p1 = [-2500, 3.75, 122, 500]
    fit_params, rest = fit_it_one(p1, channel, counts, yerrors)

    para = (fit_params[0], fit_params[1], fit_params[2], fit_params[3])

    # plt.plot(counts, 'b.')
    plt.errorbar(channel, counts, yerr=yerrors, fmt='b.')
    plt.plot(channel, draw_lorentz(channel, para), 'r')

    perr = np.sqrt(np.diag(rest))

    plt.figtext(0.55, 0.2, ("Center: %.1f +/- %.1f \nWidth %.1f +/- %.1f" % (para[2], perr[2], 2*para[1], 2*perr[1])))

    plt.savefig(path + "steel_line.png")

    plt.close()
