from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math


def six_lorentz(x, *p):
    A0, gamma0, x00, A1, gamma1, x01, A2, gamma2, x02, A3, gamma3, x03, A4, gamma4, x04, A5, gamma5, x05, offset = p
    return offset + A0 * gamma0**2 / ((x - x00)**2 + gamma0**2)\
           + A1 * gamma1**2 / ((x - x01)**2 + gamma1**2)\
           + A2 * gamma2**2 / ((x - x02)**2 + gamma2**2)\
           + A3 * gamma3**2 / ((x - x03)**2 + gamma3**2)\
           + A4 * gamma4**2 / ((x - x04)**2 + gamma4**2)\
           + A5 * gamma5**2 / ((x - x05)**2 + gamma5**2)


def fit_it_six(p, x, y, yerr=None):
    if not yerr:
        return curve_fit(six_lorentz, x, y, p0=p)
    if yerr:
        return curve_fit(six_lorentz, x, y, p0=p, sigma=yerr)


def draw_six_lorentz(x, p):
    A0, gamma0, x00, A1, gamma1, x01, A2, gamma2, x02, A3, gamma3, x03, A4, gamma4, x04, A5, gamma5, x05, offset = p
    return offset + A0 * gamma0 ** 2 / ((x - x00) ** 2 + gamma0 ** 2) \
           + A1 * gamma1 ** 2 / ((x - x01) ** 2 + gamma1 ** 2) \
           + A2 * gamma2 ** 2 / ((x - x02) ** 2 + gamma2 ** 2) \
           + A3 * gamma3 ** 2 / ((x - x03) ** 2 + gamma3 ** 2) \
           + A4 * gamma4 ** 2 / ((x - x04) ** 2 + gamma4 ** 2) \
           + A5 * gamma5 ** 2 / ((x - x05) ** 2 + gamma5 ** 2)


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

    p_six = [-20000, 5.75, 37,
             -20000, 5.75, 74,
             -10000, 4.75, 111,
             -10000, 4.35, 137,
             -20000, 5.0, 175,
             -20000, 5.75, 212, 2700]

    fit_params, rest = fit_it_six(p_six, channel, counts, yerrors)

    print(fit_params)

    para = (fit_params[0], fit_params[1], fit_params[2],
            fit_params[3], fit_params[4], fit_params[5],
            fit_params[6], fit_params[7], fit_params[8],
            fit_params[9], fit_params[10], fit_params[11],
            fit_params[12], fit_params[13], fit_params[14],
            fit_params[15], fit_params[16], fit_params[17], fit_params[18])

    print(para)

    plt.plot(channel, draw_six_lorentz(channel, para), 'r')

    perr = np.sqrt(np.diag(rest))

    print(perr)

    for dip in range(6):
        plt.figtext(0.2+0.1*dip, 0.13, ("Center: %.1f +/- %.1f \nWidth %.1f +/- %.1f" %
                                        (para[2+dip*3], perr[2+dip*3], 2*para[1+dip*3], 2*perr[1+dip*3])))

    plt.savefig(path + "weicheisen_lines.png")

    plt.close()


def fit_it(channel, counts, path):
    yerrors = []
    for value in counts:
        yerrors.append(math.sqrt(value))
        # yerrors.append(0.1)

    plt.figure(figsize=(30, 15))
    plt.errorbar(channel, counts, yerr=yerrors, fmt='b.')

    p_six = [-20000, 5.75, 37,
             -20000, 5.75, 74,
             -10000, 4.75, 111,
             -10000, 4.35, 137,
             -20000, 5.0, 175,
             -20000, 5.75, 212, 2700]

    fit_params, rest = fit_it_six(p_six, channel, counts, yerrors)

    print(fit_params)

    para = (fit_params[0], fit_params[1], fit_params[2],
            fit_params[3], fit_params[4], fit_params[5],
            fit_params[6], fit_params[7], fit_params[8],
            fit_params[9], fit_params[10], fit_params[11],
            fit_params[12], fit_params[13], fit_params[14],
            fit_params[15], fit_params[16], fit_params[17], fit_params[18])

    print(para)

    plt.plot(channel, draw_six_lorentz(channel, para), 'r')

    perr = np.sqrt(np.diag(rest))

    print(perr)

    for dip in range(6):
        plt.figtext(0.2+0.1*dip, 0.13, ("Center: %.1f +/- %.1f \nWidth %.1f +/- %.1f" %
                                        (para[2+dip*3], perr[2+dip*3], 2*para[1+dip*3], 2*perr[1+dip*3])))

    plt.savefig(path + "weicheisen_lines.png")

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
