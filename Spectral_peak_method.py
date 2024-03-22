from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.ndimage import gaussian_filter1d
from scipy.stats import johnsonsu
from scipy import signal

class Spectral_peak_method:
    def __init__(self, data, rolling_average = False, gaussian_smoothing = False, 
                 filtfilt = True,sigma = 150, method = "spectral"):
        
        if method == "spectral":
            self.wavelength = [item[0] for item in data]
            self.intensity = [item[1] for item in data]
        elif method == "gaussian" or method == "johnson":
            self.means = [item[0] for item in data]
            self.std_devs = [item[1] for item in data]
        self.rolling_average = rolling_average
        self.gaussian_smoothing = gaussian_smoothing
        self.filtfilt = filtfilt
        self.sigma = sigma
        self.method = method
        
    def get_peaks(self):
        
        # Generate x values and merged distribution if spectral method is used

        if self.method == "spectral":
            self.x = self.wavelength
            x = self.x
            self.merged_distribution = self.intensity

        # Generate x values and merged distribution if gaussian method is used

        if self.method == "gaussian":

            min_mean = min(self.means)
            idx_min_mean = self.means.index(min_mean)
            max_mean = max(self.means)
            idx_max_mean = self.means.index(max_mean)

            self.x = np.linspace(min_mean - 4 * self.std_devs[idx_min_mean], max_mean + 4 * self.std_devs[idx_max_mean], 10000)
            x = self.x

            self.merged_distribution = np.zeros(len(x))
            for i in range(len(self.means)):
                self.merged_distribution = [a + b for a,b in zip(self.merged_distribution, norm.pdf(x, self.means[i], scale=self.std_devs[i]))]

        # Generate x values and merged distribution if johnson method is used
                
        elif self.method == "johnson":

            self.list_of_as = self.means
            self.list_of_bs = self.std_devs

            self.x = np.linspace(johnsonsu.ppf(0.01, max(self.list_of_as), max(self.list_of_bs)),
                            johnsonsu.ppf(0.99, max(self.list_of_as),  max(self.list_of_as)), 10000)
            
            x = self.x

            means = []
            vars = []
            skews = []
            kurts = []

            for idx in range(len(self.list_of_as)):

                a = self.list_of_as[idx]
                b = self.list_of_bs[idx]

                mean, var, skew, kurt = johnsonsu.stats(a, b, moments='mvsk')
            
                means.append(mean)
                vars.append(var)
                skews.append(skew)
                kurts.append(kurt)
                
                self.merged_distribution = np.zeros(len(x))
                self.merged_distribution = [i + j for i,j in zip(self.merged_distribution, johnsonsu.pdf(x, a, b))]

        # get peaks of the clean distribution
            
        self.clean_peaks, _ = find_peaks(self.merged_distribution, height=0)
        self.clean_lambdas = [round(x[i],2) for i in self.clean_peaks]
        self.clean_merged_distribution = self.merged_distribution

        # add some noise to the distribution for testing purposes

        if self.method == "gaussian" or self.method == "johnson":
            
            self.merged_distribution = self.merged_distribution + np.random.normal(0, 0.01, len(self.merged_distribution))
            self.noisy_merged_distribution = self.merged_distribution

        # add some peak noise to the distribution for testing purposes
            self.peak_noise_index_list = []
            for _ in range(5):
                peak_noise_index = int(np.random.uniform(0, len(self.merged_distribution)))
                self.peak_noise_index_list.append(round(x[peak_noise_index],2))
                peak_noise_amp = np.random.uniform(0.1, 0.3)
                for shift in range(5):
                    if peak_noise_index + shift < len(self.merged_distribution):
                        self.merged_distribution[peak_noise_index + shift] += peak_noise_amp
                    else:
                        continue
        
        # use filtfilt to smoothen the distribution
        if self.filtfilt:
            b, a = signal.butter(4, 0.05)
            self.merged_distribution = signal.filtfilt(b, a, self.merged_distribution, padlen=150)


        # smoothen the distribution (simple kernel division by 1000)
        if self.rolling_average:
            self.merged_distribution = np.convolve(self.merged_distribution, np.ones(10)/10, mode='same')

        # smoothen using a gaussian filter
        if self.gaussian_smoothing:
            self.merged_distribution = gaussian_filter1d(self.merged_distribution, sigma=self.sigma)

        # get the peaks

        self.peaks, _ = find_peaks(self.merged_distribution)
        self.troughs_idx, _ = find_peaks(-np.array(self.merged_distribution))

        # get the lambdas of the peaks 

        self.lambdas = []

        for idx in self.peaks:
            peak_intensity = self.merged_distribution[idx]
            if peak_intensity > 0.05:
                self.lambdas.append(round(x[idx],3))

        peak_intensities = [self.merged_distribution[idx] for idx in self.peaks]
        idx_max_intensity = peak_intensities.index(max(peak_intensities))
        self.idx_max_intensity_for_x = self.peaks[idx_max_intensity]
        # self.lambdas = [round(x[self.peaks[idx_max_intensity]],3)]


        # get the FWHM of the peak with the highest intensity

        half_max = max(peak_intensities) / 2
        for intensity in self.merged_distribution:
            if intensity >= half_max:
                left_half_max_index = list(self.merged_distribution).index(intensity)
                break

        for intensity in self.merged_distribution[::-1]:
            if intensity >= half_max:
                right_half_max_index = list(self.merged_distribution).index(intensity)
                break

        self.lambdas_widths = (x[left_half_max_index], x[right_half_max_index])
        

        # find the troughs
        self.troughs = []

        for idx in self.troughs_idx:
            trough_intensity = self.merged_distribution[idx]
            # if trough_intensity != 0:
            self.troughs.append(round(x[idx],3))

        # add 2 custom troughs at the edges of the spectrum 

        self.troughs.append(round(x[0],3))
        self.troughs.append(round(x[-1],3))
        self.troughs = sorted(self.troughs)

        # Get the limits of the troughs

        self.lib_trough_limits = {}        
        
        for peak in self.lambdas:
            for trough_idx in range(len(self.troughs) - 1):
                if peak > self.troughs[trough_idx] and peak < self.troughs[trough_idx + 1]:
                    self.lib_trough_limits[peak] = (self.troughs[trough_idx], self.troughs[trough_idx + 1])
                    break


    def get_central_wavelength(self):
        wavelengths = np.array(self.wavelength[self.idx_max_intensity_for_x - 101:self.idx_max_intensity_for_x + 101])
        intensities = np.array(self.intensity[self.idx_max_intensity_for_x - 101:self.idx_max_intensity_for_x + 101])
        return round(np.sum(wavelengths * intensities) / np.sum(intensities),3)


    def run_accuracy_test(self, test_mean = (-10,10), test_std = (1,3) , num_of_distributions = 3, num_tests = 100):
        correct_guesses = 0
        for i in range(num_tests):
            test_data = [(np.random.uniform(test_mean[0], test_mean[1]), np.random.uniform(test_std[0], test_std[1])) for j in range(num_of_distributions)]
            self.means = [item[0] for item in test_data]
            self.std_devs = [item[1] for item in test_data]
            self.get_peaks()
            num_peaks = self.get_peaks_count()
            num_clean_peaks = self.get_clean_peaks_count()
            if num_peaks == num_clean_peaks:
                correct_guesses += 1
        self.accuracy = correct_guesses/num_tests

    def cumulitive_quantile(self, distribution):
        # createa a cdf of the distribution and calculate the 0.2, 0,4, 0,6 and 0.8 quantiles
        # quantiles = {0.067:0, 0.309:0, 0.691:0, 0.933:0}

        n = len(self.intensity)
        pn = (n-0.5)/n
        zn = 0.5
        
        quantiles = {round(norm.cdf(-3*zn),4):0,
                     round(norm.cdf(-zn),4):0,
                     round(norm.cdf(zn),4):0,
                     round(norm.cdf(3*zn),4):0}

        # idx_600 = self.wavelength.index(min(idx for idx in self.wavelength if idx > 600))
        # idx_1000 = self.wavelength.index(min(idx for idx in self.wavelength if idx > 1000))

        # self.shorter_wavelength = self.wavelength[idx_600 - 1:idx_1000 + 1]
        # intensity = self.intensity[idx_600 - 1:idx_1000 + 1]

        cumsum = np.cumsum(distribution)
        cumsum = cumsum / cumsum[-1]
        idx_quantiles = [np.argmin(np.abs(cumsum - quantile)) for quantile in list(quantiles.keys())]
        for idx in range (len(idx_quantiles)):
            quantiles[list(quantiles.keys())[idx]] = self.wavelength[idx_quantiles[idx]]
        return quantiles
    
    def reduce_by_1_peak(self):
        limits = list(self.lib_trough_limits.values())[0]
        for idx in range(len(self.intensity )):
            if self.wavelength[idx] > limits[0] and self.wavelength[idx] < limits[1]:
                self.intensity[idx] = 0

    def deconstruct_into_peaks(self):
        lib_deconstructed_peaks = {}

        for idx in range(len(self.lib_trough_limits.values())):
            limits = list(self.lib_trough_limits.values())[idx]
            peak = list(self.lib_trough_limits.keys())[idx]
            lib_deconstructed_peaks[peak] = self.intensity.copy()

            for idx2 in range(len(lib_deconstructed_peaks[peak])):
                if self.wavelength[idx2] < limits[0] or self.wavelength[idx2] > limits[1]:
                    lib_deconstructed_peaks[peak][idx2] = int(0)

        return lib_deconstructed_peaks


    def get_shorter_wavelength(self):
        return self.shorter_wavelength

    def get_cumsum(self): 
        return self.cumsum

    def get_accuracy(self):
        return self.accuracy
                
    def get_peaks_count(self):
        return len(self.peaks)
    
    def get_clean_peaks_count(self):
        return len(self.clean_peaks)

    def get_lambdas(self):
        return self.lambdas
    
    def get_clean_lambdas(self):
        return self.clean_lambdas
    
    def get_lambdas_widths(self):
        return self.lambdas_widths
    
    def get_troughs(self):
        return self.troughs
    
    def get_lib_troughs_limits(self):
        return self.lib_trough_limits
    
    def plot(self):
        self.get_peaks()
        num_peaks = self.get_peaks_count()

        # import x values

        x = self.x

        fig = plt.figure(figsize=(6, 5))
        
        # Plot distributions
        if self.method == "gaussian" or self.method == "johnson":
            plt.plot(x, self.noisy_merged_distribution, color = "cyan", linestyle = '--', label = 'Noisy merged distribution')
        plt.plot(x, self.merged_distribution, color = "g" , label = 'Smoothed spectrum')
        plt.plot(x, self.clean_merged_distribution, color = "r" , label = 'Original spectrum')

        # Set xlim 

        if len(self.lambdas) == 1:
            plt.xlim(self.lambdas[0] - 50,self.lambdas[0] + 51)

        # Plot lambdas

        auxillary_clean_peaks = [round(item,0) for item in self.clean_lambdas]
        auxillary_clean_peaks_copy= [round(item,0) for item in self.clean_lambdas]
        peak_tolerance = 2
        for i in auxillary_clean_peaks_copy:
            for j in range(1,peak_tolerance + 1):
                auxillary_clean_peaks.append(i - j)
                auxillary_clean_peaks.append(i + j)
        
        for item in self.lambdas:
            if round(item,0) not in auxillary_clean_peaks:
                plt.axvline(item, color = 'black', label = f"Peak misfound at {item}")
            else:
                plt.axvline(item, color = 'g', label = f"Peak found at {item}")

        auxillary_smoothed_peaks = [round(item,0) for item in self.lambdas]
        auxillary_smoothed_peaks_copy= [round(item,0) for item in self.lambdas]
        peak_tolerance = 2
        for i in auxillary_smoothed_peaks_copy:
            for j in range(1,peak_tolerance + 1):
                auxillary_smoothed_peaks.append(i - j)
                auxillary_smoothed_peaks.append(i + j)
        
        if self.method == "gaussian" or self.method == "johnson":
            for item in self.clean_lambdas:
                if round(item,0) not in auxillary_smoothed_peaks:
                    plt.axvline(item, color = 'r', label = f"Peak NOT found at {item}")
            
        # Create a single shared legend
        if self.method == "gaussian" or self.method == "johnson":
            plt.title('simulated distributions with peaks')
        else:
            plt.title('Spectal data with peaks')
        fig.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

        print(f"Number of smoothed peaks: {num_peaks}")
        print(f"Number of original peaks: {self.get_clean_peaks_count()}")
        if self.method == "gaussian" or self.method == "johnson":
            print(f"Location of peak noise: {sorted(self.peak_noise_index_list)}")
        plt.tight_layout()
        plt.show()

    
    def plot_data(self):
        plt.plot(self.wavelength, self.intensity, color = "royalblue", label = "Spectral data")
        plt.legend()
        plt.show()