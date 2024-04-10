from typing import Dict

from pipeline import create_folder

from helpers.files import write_json, read_json

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

    logoplots = {}

    i = 0
    j = 0
    for allele in alleles:
        length = '9'
        peptides = alleles[allele][length]

        counts_mat = logomaker.alignment_to_matrix(peptides)
        counts_mat.index = range(1, int(length) + 1)
        
        info_mat = logomaker.transform_matrix(counts_mat, from_type='counts', to_type='information')
        
        logoplot = None

        logoplot = logomaker.Logo(info_mat, vpad=0.1, color_scheme=colors, show_spines=False, figsize=(25,20))
        logoplot.ax.tick_params(axis='both', which='major', labelsize=40)

        logoplot.ax.set_xlabel('Peptide position', fontsize=60, labelpad=10)
        logoplot.ax.set_ylabel('Bits', fontsize=60, labelpad=40)

        logoplot.style_spines(visible=False)
        logoplot.style_spines(spines=['left', 'bottom'], visible=True)

        logoplot_svg_stem = f"{output_path}/motifs/logoplots/svg/{allele}_{length}"
        logoplot_png_stem = f"{output_path}/motifs/logoplots/png/{allele}_{length}"

        #logo_svg = BytesIO()
        logo_png = BytesIO()

        #plt.savefig(logo_svg, format='svg')
        plt.savefig(logo_png, format='png')
        
        #plt.savefig(f"{logoplot_svg_stem}.svg", format='svg')
        plt.savefig(f"{logoplot_png_stem}.png", format='png')


        #logo_svg_data = base64.b64encode(logo_svg.getbuffer()).decode("ascii")
        logo_png_data = base64.b64encode(logo_png.getbuffer()).decode("ascii")

        #with open(f"{logoplot_svg_stem}.txt", "w") as logo_svg_datafile:
        #    logo_svg_datafile.write(logo_svg_data)
        
        with open(f"{logoplot_png_stem}.txt", "w") as logo_png_datafile:
            logo_png_datafile.write(logo_png_data)
        
        plt.close()
        
        print (f"Logoplot for {allele} {length}mer motif created")

        j += 1
        i += 1

    # create the action log which will be included in the log file for this run of the pipeline
    action_log = {
        'alleles_processed':i,
        'motifs_processed':j
    }
    
    return action_log