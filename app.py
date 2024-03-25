import streamlit as st

from Extract_folder_data import *
from Extinction_coef import *
from spectra import *
from Spectral_peak_method import *
from Johnson_method import *
from Single_peak_method import *
from Plot_bar import *
from Plot_comparison import *
from Plot_comparison_real_data import *

# Define Streamlit app
def main():
    st.title("LED emission approximation app")

    # Add UI elements for parameters
    is_simulation = st.sidebar.checkbox("Simulate data", value=True)

    folder_path = None
    separator = None
    if not is_simulation:
        folder_path = st.sidebar.text_input("Data folder path")
        separator = st.sidebar.text_input("Separator for data", value=":")

    starting_wavelength = st.sidebar.number_input("Starting wavelength", value=600)
    ending_wavelength = st.sidebar.number_input("Ending wavelength", value=1200)
    title = st.sidebar.text_input("Title", value="LED emission approximation")
    save_the_plots = st.sidebar.checkbox("Save the plots", value=False)
    
    plot_path = None
    if save_the_plots:
        plot_path = st.sidebar.text_input("Plot path")

    run_toggle = st.sidebar.checkbox("Run", value = False)

    # Display parameters
    st.write("Simulation:", is_simulation)
    if not is_simulation:
        st.write("Data folder path:", folder_path)
        st.write("Separator for data:", separator)
    st.write("Starting wavelength:", starting_wavelength)
    st.write("Ending wavelength:", ending_wavelength)
    st.write("Title:", title)
    st.write("Save the plots:", save_the_plots)
    if save_the_plots:
        st.write("Plot path:", plot_path)

    # Add code to load and process data, using the parameters as inputs
    if run_toggle:
        johnson = Johnson_method(simulation=is_simulation, folder_path=folder_path, separator=separator, starting_wavelength=starting_wavelength, ending_wavelength=ending_wavelength)
        diff, diff_perc = johnson.get_extinction_coef()
        lib_spectral_data_p15 = johnson.get_lib_spectral_data()
        lib_central_wavelengths_p15 = johnson.get_lib_central_wavelengths()

        Plot_bar_extinction(diff, diff_perc, save_the_plots, plot_path).plot(title)

        if not is_simulation:
            Plot_comparison_real_data(lib_spectral_data_p15, save_the_plots, plot_path).plot_spectra(title)

            Plot_comparison_real_data(lib_spectral_data_p15, save_the_plots, plot_path).plot_cumulative_spectra(title)

        elif is_simulation == True:
            Plot_comparison(lib_spectral_data_p15, save_the_plots, plot_path).plot_spectra(title)

            Plot_comparison(lib_spectral_data_p15, save_the_plots, plot_path).plot_cumulative_spectra(title)


if __name__ == "__main__":
    main()