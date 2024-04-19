from typing import Dict

from pipeline import create_folder

from helpers.files import write_json, read_json

import os 

from io import BytesIO
import base64

import logomaker
import matplotlib.pyplot as plt
import numpy as np


colors = {
        'F': [.9, .87, .31],
        'Y': [.9, .87, .31],
        'L': [.9, .87, .31],
        'V': [.9, .87, .31],
        'I': [.9, .87, .31],
        'H': [.78, .78, .78],
        'W': [.9, .87, .31],
        'A': [.78, .78, .78],
        'S': [.78, .78, .78],
        'T': [.78, .78, .78],
        'M': [.9, .87, .31],
        'N': [.78, .78, .78],
        'Q': [.78, .78, .78],
        'R': [.26, .43, .67],
        'K': [.26, .43, .67],
        'E': [.76, .31, .36],
        'G': [.78, .78, .78],
        'D': [.76, .31, .36],
        'P': [.78, .78, .78],
        'C': [.78, .78, .78]
    }



def build_logoplots(**kwargs) -> Dict[str,str]:
    """
    This function processes the output of the processed class I data downloaded from the MHC Motif Atlas into logoplots for each allele/length

    Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
        Dict[str,str]: A dictionary containing the action log for this step.

    Keyword Args:
        config (dict): The configuration dictionary.
        verbose (bool): Whether to print verbose output.
        force (bool): Whether to force the step to run ignoring any previous results.
        output_path (str): The path to the output directory.
        console (Console): A Rich console object for printing Rich output.
    """
    config = kwargs['config']
    verbose = kwargs['verbose']
    force = kwargs['force']
    output_path = kwargs['output_path']
    console = kwargs['console']
    function_name = kwargs['function_name']

    # Create the filenames for the input file (the output of the previous step)
    input_filename = f"{output_path}/motifs/alleles.json"

    # Read the input file
    alleles = read_json(input_filename)

    # Create the logoplots folders
    create_folder(f"{output_path}/motifs/logoplots/png", verbose)
    create_folder(f"{output_path}/motifs/logoplots/svg", verbose)

    # Create counters for number of alleles and motifs processed
    i = 0
    j = 0

    # Iterate throught the alleles
    for allele in alleles:

        # set the length to 9, at the moment we're only creating logoplots for nonamers
        length = '9'
        
        # create a file stem for the png of the logoplot
        # TODO check if we're using the text representation of the png
        logoplot_png_stem = f"{output_path}/motifs/logoplots/png/{allele}_{length}"

        # set a boolean for whether the plot already exists or not
        logoplot_exists = False

        # check if the logoplot already exists
        if os.path.exists(f"{logoplot_png_stem}.png") and os.path.exists(f"{logoplot_png_stem}.txt"):
            logoplot_exists = True

        # if the force flag is set or the logoplot doesn't exist, create the logoplot
        if force or not logoplot_exists:

            # generate a set of peptides for the allele and length
            peptides = alleles[allele][length]

            # create a matrix of the peptides
            counts_mat = logomaker.alignment_to_matrix(peptides)
            counts_mat.index = range(1, int(length) + 1)
            
            # transform the matrix to information content
            info_mat = logomaker.transform_matrix(counts_mat, from_type='counts', to_type='information')
            
            # initialise a set of variables for the logoplot, the png, and the png data
            logoplot = None
            logo_png = None
            logo_png_data = None

            # create the logoplot
            logoplot = logomaker.Logo(info_mat, vpad=0.1, color_scheme=colors, show_spines=False, figsize=(25,20))
            logoplot.ax.tick_params(axis='both', which='major', labelsize=40)

            logoplot.ax.set_xlabel('Peptide position', fontsize=60, labelpad=10)
            logoplot.ax.set_ylabel('Bits', fontsize=60, labelpad=40)

            logoplot.style_spines(visible=False)
            logoplot.style_spines(spines=['left', 'bottom'], visible=True)

            # save the logoplot as a png, and generate the base64 encoded data
            logo_png = BytesIO()

            plt.savefig(f"{logoplot_png_stem}.png", format='png')

            logo_png_data = base64.b64encode(logo_png.getbuffer()).decode("ascii")

            with open(f"{logoplot_png_stem}.txt", "w") as logo_png_datafile:
                logo_png_datafile.write(logo_png_data)
            
            # close the plot object, and clear the figure, if we don't do this we'll get a memory leak
            plt.close()
            
            if verbose:
                print (f"Logoplot for {allele} {length}mer motif created")
        else:
            if verbose:
                print (f"Logoplot for {allele} {length}mer motif already exists")

        j += 1
        i += 1

    # create the action log which will be included in the log file for this run of the pipeline
    action_log = {
        'alleles_processed':i,
        'motifs_processed':j
    }
    
    return action_log