from typing import Dict

from pipeline import create_folder

from helpers.files import write_json, read_json


def build_simplified_motifs(**kwargs) -> Dict[str,str]:
    """
    This function processes the output of the processed class I data downloaded from the MHC Motif Atlas into simplified motifs for each allele for the allele group view

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


    # Create the filenames for the input file (the output of the previous step) and the output file (the input for the next step)
    input_filename = f"{output_path}/motifs/sorted_amino_acid_distributions.json"
    output_filename = f"{output_path}/motifs/simplified_motifs.json"


    # Read the input file
    sorted_amino_acid_distributions = read_json(input_filename)

    # Create a new dictionary to store the simplified motifs
    simplified_motifs = {}

    """
    # Rules for simplification

    1. If the amino acid distribution is dominant for a single amino acid, then that is in row 1 of the motif and is shown in bold
    2. If the amino acid distribution is high for a single amino acid, then that is in row 1 of the motif if there is nothing at that position in row 1 
    but is not shown in bold
    3. If the amino acid distribution is high then that is shown in row 2 of the motif
    4. Only 2 rows are shown

    """

    # Initialise counters for numbers of alleles and motifs processed
    i = 0

    # Loop through the alleles
    for allele in sorted_amino_acid_distributions:

        # Select the nonamer motif
        motif = sorted_amino_acid_distributions[allele]['9']

        # Create a new dictionary to store the simplified motif
        simplified_motif = {}

        # Loop through the positions in the motif
        for position in motif:
            simplified_motif[position] = []
            # Loop through the amino acids at each position
            for amino_acid in motif[position]:
                # If the amino acid is dominant or high, add it to the simplified motif
                if amino_acid['grade'] in ['dominant', 'high']:
                    simplified_motif[position].append({'amino_acid':amino_acid['amino_acid'], 'grade':amino_acid['grade']}) 
        # If the verbosity is true, print the allele and the simplified motif
        if verbose:
            print (f"{allele} processed: {simplified_motif}")
        # Add the simplified motif to the dictionary of simplified motifs
        simplified_motifs[allele] = simplified_motif
        i += 1

    # Output the simplified motifs to a JSON file
    write_json(output_filename, simplified_motifs, pretty=True)

    # create the action log which will be included in the log file for this run of the pipeline
    action_log = {
        'alleles_processed':i,
    }
    
    return action_log