from typing import Dict

from pipeline import create_folder

from helpers.files import write_json, read_json


def get_percentage(amino_acid: Dict[str, str]) -> int:
    """
    This function returns the percentage of an amino acid in a motif or zero if the percentage key does not exist

    Args:
        amino_acid (Dict[str, str]): The amino acid to get the percentage of

    Returns:
        int: The percentage of the amino acid in the motif or zero if the percentage key does not exist
    """
    return amino_acid.get('percentage', 0)


def assign_grade(percentage: float) -> str:
    """
    This function assigns a grade to an amino acid based on the percentage of the amino acid in the motif

    Args:
        percentage (float): The percentage of the amino acid in the motif
    
    Returns:
        str: The grade of the amino acid in the motif (used for styling in the HTML output)
    """
    if percentage > 60:
        return "dominant"
    elif percentage > 30:
        return "high"
    elif percentage > 20:
        return "medium"
    elif percentage > 10:
        return "low"
    else:
        return "very-low"


def manipulate_data(motif_data: Dict[str, Dict[str, Dict[str, str]]]) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    This function processes the output of the processed class I data downloaded from the MHC Motif Atlas

    It sorts the amino acids by percentage and assigns a grade to each amino acid based on the percentage and creates a rounded down percentage value for display

    Args:
        motif_data (Dict[str, Dict[str, Dict[str, str]]]): The motif data to process

    Returns:
        Dict[str, Dict[str, Dict[str, str]]]: The processed motif data
    """
    for key, sub_dict in motif_data.items():

        # Ensure the percentage key exists and set to zero if not
        for amino_acid, amino_acid_data in sub_dict.items():
            amino_acid_data.setdefault('percentage', 0)

        
        # Set the 'grade' field based on the 'percentage' field
        for amino_acid, amino_acid_data in sub_dict.items():
            amino_acid_data['grade'] = assign_grade(amino_acid_data['percentage'])
            amino_acid_data['rounded_percentage'] = round(amino_acid_data['percentage'], 1)
        
        # Order the sub-dictionary by the percentage value
        sorted_sub_dict = dict(sorted(sub_dict.items(), key=lambda item: get_percentage(item[1]), reverse=True))
        motif_data[key] = sorted_sub_dict

    return motif_data


def build_sorted_amino_acid_distributions(**kwargs) -> Dict[str,str]:
    """
    This function processes the output of the processed class I data downloaded from the MHC Motif Atlas

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
    input_filename = f"{output_path}/motifs/amino_acid_distributions.json"
    output_filename = f"{output_path}/motifs/sorted_amino_acid_distributions.json"

    # Read the input file
    raw_amino_acid_distributions = read_json(input_filename)

    # Create a new dictionary to store the sorted amino acid distributions
    sorted_amino_acid_distributions = {}

    # Initialise counters for numbers of alleles and motifs processed
    i = 0
    j = 0

    # Process the raw amino acid distributions
    for allele in raw_amino_acid_distributions:

        # Create a new sub-dictionary for the allele
        sorted_amino_acid_distributions[allele] = {}
        
        # Increment the allele counter
        i += 1

        # Process the raw amino acid distributions for each length
        for length in raw_amino_acid_distributions[allele]:

            # Create a new sub-dictionary for the length and add the sorted, graded and rounded amino acid distribution
            sorted_amino_acid_distributions[allele][length] = manipulate_data(raw_amino_acid_distributions[allele][length])
            
            # Increment the motif counter
            j += 1

            if verbose:
                print (f"Sorted, graded and rounded amino acid distribution for {allele} and length {length}")

    # Output the sorted amino acid distributions to a JSON file
    write_json(output_filename, sorted_amino_acid_distributions)


    # create the action log which will be included in the log file for this run of the pipeline
    action_log = {
        'alleles_processed': i,
        'motifs_processed': j
    }
    
    return action_log