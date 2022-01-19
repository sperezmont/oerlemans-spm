import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def Plot1D(data, name, units, time_units, shades=[],  labels=['ABUC', 'ABUK', 'ABUM'], color=['blue', 'red', 'orange'], linestyles=['solid', 'solid', 'solid'], linewidths=[2, 2, 2], file_name='plot1D.png', plotpath=plotpath):
    ''' Plots the time series of one 1D variable '''
    ''' data.shape = nexps, ntimes '''
    nexps, ntimes = np.shape(data)
    fig, ax = plt.subplots(figsize=(10, 8))
    alpha = [1, 0.7, 0.5]
    shadecolor = ['lightblue', 'lightcoral', 'yellow']

    if shades != []:
        for j in range(3):
            ax.fill_between(np.arange(0, ntimes, round(ntimes/51)), shades[j, 0, 0, :],
                            shades[j, 1, i, :], alpha=alpha[j], color=shadecolor[j], edgecolor=shadecolor[j])
    for j in range(nexps):
        ax.plot(data[j, :], color=color[j], linestyle=linestyles[j],
                linewidth=linewidths[j], label=labels[j])
        ax.text(450, 0.98*data[j, -1], str(round(data[j, -1], 1)) + ' ' + units,
                color=color[j], fontsize=20, horizontalalignment='center')
        ax.set_xlim([0, 500])
        ax.grid(linestyle='--', alpha=0.5)
        ax.set_xlabel(r'Time (' + time_units + ')', fontsize=20)
        ax.set_ylabel(name + ' (' + units + ')', fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)
    ax.legend(fontsize=20)
    plt.savefig(plotpath + file_name)
