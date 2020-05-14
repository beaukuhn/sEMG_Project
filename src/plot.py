"""
plot.py

This file contains code pertaining to plotting data.
TODO: Refine code to parameterize functions for generalization
"""
def plot1(sensor2coefs, sensor_num):
    s2d = sensor2coefs[sensor_num]
    plt.stem(s2d['cD4'])
    plt.show()

def plot_data(sensor2data, sensor2dwt, sensor_num):
    plt.subplot(121)
    plt.stem(sensor2data[sensor_num])
    plt.subplot(122)
    rec_sig = waverec(sensor2dwt[sensor_num], 'db2')
    plt.stem(rec_sig)
    plt.show()

def plot_dwt_data(sensor2coefs, sensor_num):
    coefs = sensor2coefs[sensor_num]
    y_bounds = [-1, 1]

    plt.subplot(421)
    plt.stem(coefs['cA1'])
    axes = plt.gca()
    axes.set_title('cA1', fontsize=10)

    plt.subplot(422)
    plt.stem(coefs['cD1'])
    axes = plt.gca()
    axes.set_title('cD1', fontsize=10)
    axes.set_ylim(y_bounds)

    plt.subplot(423)
    axes = plt.gca()
    plt.stem(coefs['cA2'])
    axes.set_title('cA2', fontsize=10)

    plt.subplot(424)
    plt.stem(coefs['cD2'])
    axes = plt.gca()
    axes.set_title('cD2', fontsize=10)
    axes.set_ylim(y_bounds)

    plt.subplot(425)
    axes = plt.gca()
    axes.set_title('cA3', fontsize=10)
    plt.stem(coefs['cA3'])

    plt.subplot(426)
    plt.stem(coefs['cD3'])
    axes = plt.gca()
    axes.set_title('cD3', fontsize=10)
    axes.set_ylim(y_bounds)

    plt.subplot(427)
    plt.stem(coefs['cA4'])
    axes = plt.gca()
    axes.set_title('cA4', fontsize=10)

    plt.subplot(428)
    plt.stem(coefs['cD4'])
    axes = plt.gca()
    axes.set_ylim(y_bounds)
    axes.set_title('cD4', fontsize=10)

    plt.tight_layout()
    plt.show()
