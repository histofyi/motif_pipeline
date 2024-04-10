from typing import Dict

from pipeline import create_folder

from helpers.files import write_json, read_json

from io import BytesIO
import base64

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np



def build_peptide_length_distribution_plots(**kwargs) -> Dict[str,str]:
    """
    This function processes the output of the processed class I data downloaded from the MHC Motif Atlas into length distribution plots for each allele

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
    input_filename = f"{output_path}/motifs/peptide_length_distributions.json"

    peptide_length_distributions = read_json(input_filename)

    i = 0
    for allele in peptide_length_distributions:
        motif_lengths = peptide_length_distributions[allele]

        reworked_motif_lengths = {int(key):motif_lengths['lengths'][key] for key in motif_lengths['lengths']}

        labels = sorted(reworked_motif_lengths.keys())
        values = [reworked_motif_lengths[label]['percentage'] for label in labels]

        fig = Figure()
        fig.set_figwidth(25)
        fig.set_figheight(20)
        ax = fig.subplots()
        ax.bar(labels, values, color='#0a0039')
        ax.tick_params(axis='both', which='major', labelsize=55)

        ax.set_xlabel('Peptide length', fontsize=70, labelpad=10)
        ax.set_ylabel('Percentage of peptides', fontsize=70, labelpad=40)
        ax.spines[['right', 'top']].set_visible(False)

        lengthplot_png_stem = f"{output_path}/motifs/lengthplots/png/{allele}"

        png = BytesIO()

        fig.savefig(png, format="png")
        fig.savefig(f"{lengthplot_png_stem}.png", format="png")

        png_data = base64.b64encode(png.getbuffer()).decode("ascii")

        with open(f"{lengthplot_png_stem}.txt", 'w') as f:
            f.write(png_data)

        print (f"Length distribution plot for {allele} created")

        i += 1

    # create the action log which will be included in the log file for this run of the pipeline
    action_log = {
        'alleles_processed':i,
    }
    
    return action_log
