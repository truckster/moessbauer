from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math


def two_lorentz(x, *p):
    A0, gamma0, x00, A1, gamma1, x01, offset = p
    return offset + A0 * gamma0**2 / ((x - x00)**2 + gamma0**2)\
           + A1 * gamma1**2 / ((x - x01)**2 + gamma1**2)\



def fit_it_two(p, x, y, yerr=None):
    if not yerr:
        return curve_fit(two_lorentz, x, y, p0=p)
    if yerr:
        return curve_fit(two_lorentz, x, y, p0=p, sigma=yerr)


def draw_two_lorentz(x, p):
    A0, gamma0, x00, A1, gamma1, x01, offset = p
    return offset + A0 * gamma0 ** 2 / ((x - x00) ** 2 + gamma0 ** 2) \
           + A1 * gamma1 ** 2 / ((x - x01) ** 2 + gamma1 ** 2) \



def read_manual_file(path, filename):
    steel_file = path + filename
    lines = loadtxt(steel_file, delimiter="\t")

    channel = []
    counts = []
    for event in lines:
        if event[1] > 400:
            channel.append(event[0])
            counts.append(event[1])

    yerrors = []
    for value in counts:
        yerrors.append(math.sqrt(value))
        # yerrors.append(0.1)

    plt.figure(figsize=(30, 15))
    plt.errorbar(channel, counts, yerr=yerrors, fmt='b.')

    p_two = [-3000, 2.75, 119,
             -4000, 2.75, 172, 2700]

    fit_params, rest = fit_it_two(p_two, channel, counts, yerrors)

    print(fit_params)

    para = (fit_params[0], fit_params[1], fit_params[2],
            fit_params[3], fit_params[4], fit_params[5], fit_params[6])

    print(para)

    plt.plot(channel, draw_two_lorentz(channel, para), 'r')

    perr = np.sqrt(np.diag(rest))

    print(perr)

    for dip in range(2):
        plt.figtext(0.2+0.1*dip, 0.13, ("Center: %.1f +/- %.1f \nWidth %.1f +/- %.1f" %
                                        (para[2+dip*3], perr[2+dip*3], 2*para[1+dip*3], 2*perr[1+dip*3])))

    plt.savefig(path + "eisensulfat_lines.png")

    plt.close()


def read_cassy_file(path, filename):
    file = open(path + filename, 'r')

    channel = []
    counts = []
    data = file.readlines()
    for line in range(261):
        if line > 4:
            line_data = data[line].split('\t')
            if float(line_data[1]) > 400:
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

    plt.figure(figsize=(30, 15))
    plt.errorbar(channel, counts, yerr=yerrors, fmt='b.')

    p_two = [-3000, 2.75, 119,
             -4000, 2.75, 172, 2700]

    fit_params, rest = fit_it_two(p_two, channel, counts, yerrors)

    print(fit_params)

    para = (fit_params[0], fit_params[1], fit_params[2],
            fit_params[3], fit_params[4], fit_params[5], fit_params[6])

    print(para)

    plt.plot(channel, draw_two_lorentz(channel, para), 'r')

    perr = np.sqrt(np.diag(rest))

    print(perr)

    for dip in range(2):
        plt.figtext(0.2+0.1*dip, 0.13, ("Center: %.1f +/- %.1f \nWidth %.1f +/- %.1f" %
                                        (para[2+dip*3], perr[2+dip*3], 2*para[1+dip*3], 2*perr[1+dip*3])))

    plt.savefig(path + "eisensulfat_lines.png")

    plt.close()