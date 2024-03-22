import matplotlib.pyplot as plt
import numpy as np

class Plot_bar_extinction():
    def __init__(self, diff, diff_perc, save_plots, plot_path = None):
        self.diff = diff
        self.diff_perc = diff_perc
        self.save_plots = save_plots
        self.plot_path = plot_path

    def plot(self, title):

        def addlabels_O2Hb(x,y,s):
            for i in range(len(x)):
                plt.text(i, y[i]*1.01, f"{s[i]}%", ha = 'center', fontsize = 6)

        def addlabels_HHb(x,y,s):
            for i in range(len(x)):
                plt.text(i + 0.4, y[i]*1.01, f"{s[i]}%", ha = 'center', fontsize = 6)

        peak_types = self.diff.keys()
        copy = self.diff_perc.copy()
        for key, value in copy.items():
            if self.diff[key] == {}:
                self.diff.pop(key)
                self.diff_perc.pop(key)

        O2Hb_percentage = [self.diff_perc[peak_type]["O2Hb"] for peak_type in peak_types]
        HHb_percentage = [self.diff_perc[peak_type]["HHb"] for peak_type in peak_types]

        O2Hb = [self.diff[peak_type]["O2Hb"] for peak_type in peak_types]
        HHb = [self.diff[peak_type]["HHb"] for peak_type in peak_types]

        plt.figure(figsize=(15,5))

        bar_width = 0.40

        plt.bar(np.arange(len(peak_types)), O2Hb_percentage, width = bar_width,label="O2Hb", color='tomato')
        plt.bar(np.arange(len(peak_types)) + bar_width, HHb_percentage, width = bar_width,label="HHb", color='steelblue')

        plt.grid(True, linestyle='--', alpha=0.5, axis='y')

        addlabels_O2Hb(np.arange(len(peak_types)), O2Hb_percentage, O2Hb_percentage)
        addlabels_HHb(np.arange(len(peak_types)), HHb_percentage, HHb_percentage)

        plt.axhline(0, color='black', lw=0.5)
        plt.xticks(np.arange(len(peak_types)) + bar_width / 2, peak_types, rotation=0)
        plt.xlabel("LEDs")
        plt.ylabel("Percentage difference of the extinction coefficients (%)")
        plt.title(f"{title} - mean error; O2Hb: {round(np.mean(O2Hb_percentage),2)}%, HHb: {round(np.mean(HHb_percentage),2)}%")

        plt.legend(loc = "upper right", bbox_to_anchor=(1.15, 1))

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Bar plot " + title + ".png")
        plt.show()

class Plot_bar_central_wavelength():
    def __init__(self, dominant_wavelengths_diff, fwhm_diff, central_wavelengths_diff, save_plots, plot_path = None):
        self.dominant_wavelengths_diff = dominant_wavelengths_diff
        self.fwhm_diff = fwhm_diff
        self.central_wavelengths_diff = central_wavelengths_diff
        self.save_plots = save_plots
        self.plot_path = plot_path


    def plot(self, title):

        def addlabels_dominant_wavelength_diff(x,y,s):
            for i in range(len(x)):
                if y[i] >= 0:
                    plt.text(i, y[i]*1.01, f"{s[i]}", ha = 'center', fontsize = 6)
                else:
                    plt.text(i, y[i] - 0.15, f"{s[i]}", ha = 'center', fontsize = 6)

        def addlabels_fwhm_diff(x,y,s):
            for i in range(len(x)):
                if y[i] >= 0:
                    plt.text(i + 0.3 * 2, y[i]*1.01, f"{s[i]}", ha = 'center', fontsize = 6)
                else:
                    plt.text(i + 0.3 * 2, y[i] - 0.15, f"{s[i]}", ha = 'center', fontsize = 6)

        def addlabels_central_wavelength(x,y,s):
            for i in range(len(x)):
                if y[i] >= 0:
                    plt.text(i + 0.3, y[i]*1.01, f"{s[i]}", ha = 'center', fontsize = 6)
                else:
                    plt.text(i + 0.3, y[i] - 0.15, f"{s[i]}", ha = 'center', fontsize = 6)

        LEDs = self.dominant_wavelengths_diff.keys()

        plt.figure(figsize=(20,5))

        bar_width = 0.30

        plt.bar(np.arange(len(LEDs)), list(self.dominant_wavelengths_diff.values()), width = bar_width,label="Dominant wavelength difference", color='mediumvioletred')
        plt.bar(np.arange(len(LEDs)) + bar_width, list(self.central_wavelengths_diff.values()), width = bar_width,label="Central wavelength difference", color='indigo')
        plt.bar(np.arange(len(LEDs)) + bar_width*2, list(self.fwhm_diff.values()), width = bar_width,label="FWHM difference", color='thistle')

        plt.grid(True, linestyle='--', alpha=0.5, axis='y')

        addlabels_dominant_wavelength_diff(np.arange(len(LEDs)), list(self.dominant_wavelengths_diff.values()), list(self.dominant_wavelengths_diff.values()))
        addlabels_central_wavelength(np.arange(len(LEDs)), list(self.central_wavelengths_diff.values()), list(self.central_wavelengths_diff.values()))
        addlabels_fwhm_diff(np.arange(len(LEDs)), list(self.fwhm_diff.values()), list(self.fwhm_diff.values()))

        plt.text(15.8, 0.25, 'P20 is higher', rotation=90, va='bottom', ha='right', fontsize=10)
        plt.text(15.8, -3.75, 'P15 is higher', rotation=90, va='bottom', ha='right', fontsize=10)

        plt.axhline(0, color='black', lw=0.5)
        plt.xticks(np.arange(len(LEDs)) + bar_width * 2 / 3, LEDs, rotation=0)
        plt.xlabel("LEDs")
        plt.ylabel("Difference (nm)")
        plt.title(f"{title} - mean error; Dominant wavelength: {round(np.mean(list(self.dominant_wavelengths_diff.values())),2)} nm, FWHM: {round(np.mean(list(self.fwhm_diff.values())),2)} nm, Central wavelength: {round(np.mean(list(self.central_wavelengths_diff.values())),2)} nm")

        plt.legend(loc = "upper right", bbox_to_anchor=(1.22, 1))

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Bar plot " + title + ".png")
        plt.show()
