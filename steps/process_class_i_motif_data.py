from typing import Dict
import requests

from helpers.files import write_file



alleles = {}
peptides = {}
amino_acid_distributions = {}
peptide_length_distributions = {}


def slugify_mhc_motif_atlas_allele(allele:str) -> str:
    """
    This function converts the allele name from the MHC Motif Atlas into a slugified version including the species stem and correct placements of '_
    
    Args:
        allele (str): The allele name from the MHC Motif Atlas

    Returns:
        str: The slugified allele name
    """
    return f"hla_{allele[0]}_{allele[1:3]}_{allele[3:]}".lower()


def add_allele_and_peptide(allele_number:str, peptide:str, peptide_length:str) -> bool:
    """
    This function adds the allele number, peptide and peptide length to the relevant dictionary

    Args:
        allele_number (str): The slugified allele number
        peptide (str): The peptide sequence
        peptide_length (str): The peptide length

    Returns:
        bool: Whether the peptide was added to the dictionary
    """                    
    # if the allele number is not in the dictionary, add it
    if allele_number not in alleles:
        alleles[allele_number] = {}
    # if the peptide length is not in the part of the dictionary for this allele, add it
    if peptide_length not in alleles[allele_number]:
        alleles[allele_number][peptide_length] = []
    # add the peptide to the list of peptides for this allele and peptide length
    if peptide not in alleles[allele_number][peptide_length]:
        alleles[allele_number][peptide_length].append(peptide)
        return True
    else:
        return False


def add_peptide(peptide:str, allele_number:str):
    """
    This function adds the peptide to the relevant dictionary
    
    Args:
        peptide (str): The peptide sequence
        allele_number (str): The slugified allele number
    """
    # if the peptide sequence is not in the dictionary, add it 
    if peptide not in peptides:
        peptides[peptide] = []
    # add the allele number to the list of alleles for this peptide
    if allele_number not in peptides[peptide]:
        peptides[peptide].append(allele_number) 
    pass


def add_to_amino_acid_distribution(allele_number:str, peptide:str, peptide_length:str):
    """
    This function adds the amino acid distribution for the peptide to the relevant dictionary

    Args:
        allele_number (str): The slugified allele number
        peptide (str): The peptide sequence
        peptide_length (str): The peptide length
    """
    if not allele_number in amino_acid_distributions:
        amino_acid_distributions[allele_number] = {}
    if not peptide_length in amino_acid_distributions[allele_number]:
        amino_acid_distributions[allele_number][peptide_length] = {}

    j = 1
    for amino_acid in peptide:
        position = str(j)
        if not position in amino_acid_distributions[allele_number][peptide_length]:
            amino_acid_distributions[allele_number][peptide_length][position] = {}
        if not amino_acid in amino_acid_distributions[allele_number][peptide_length][position]:
            amino_acid_distributions[allele_number][peptide_length][position][amino_acid] = {'count':0, 'percentage':None}
        amino_acid_distributions[allele_number][peptide_length][position][amino_acid]['count'] += 1
        j+=1     
    pass


def process_peptide_length_distribution(allele_number:str):
    """
    This function processes the peptide length distribution for the allele
    
    Args:
        allele_number (str): The slugified allele number
    """
    # set a counter for the total number of peptides for this allele to 0
    allele_peptide_count = 0
    # create a dictionary for the peptide length distribution for this allele
    peptide_length_distributions[allele_number] = {'total':0,'lengths':{}}
    # iterate through the peptide lengths for this allele
    for peptide_length in alleles[allele_number]:
        # add the peptide length to the dictionary
        peptide_length_distributions[allele_number]['lengths'][peptide_length] = {
            'count':len(alleles[allele_number][peptide_length]),
            'percentage':None
        }
        # add the number of peptides for this length to the total number of peptides for this allele
        allele_peptide_count += len(alleles[allele_number][peptide_length])
    # set the total number of peptides for this allele in the dictionary   
    peptide_length_distributions[allele_number]['total'] = allele_peptide_count
    # iterate through the peptide lengths for this allele
    for peptide_length in peptide_length_distributions[allele_number]['lengths']:
        this_length = peptide_length_distributions[allele_number]['lengths'][peptide_length]
        # set the percentage of peptides for this length
        this_length['percentage'] = this_length['count'] / allele_peptide_count * 100
    pass


def process_amino_acid_distribution(allele_number:str):
    """
    This function processes the amino acid distribution for the peptides bound by the allele

    Args:
        allele_number (str): The slugified allele number
    """
    for peptide_length in amino_acid_distributions[allele_number]:
        for position in amino_acid_distributions[allele_number][peptide_length]:
            for amino_acid in amino_acid_distributions[allele_number][peptide_length][position]:
                this_amino_acid = amino_acid_distributions[allele_number][peptide_length][position][amino_acid]
                this_amino_acid['percentage'] = this_amino_acid['count'] / peptide_length_distributions[allele_number]['lengths'][peptide_length]['count'] * 100
    pass


def process_class_i_motif_data(**kwargs) -> Dict[str,str]:
    """
    This function processes the downloaded data from the MHC Motif Atlas

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

    # open the cached dataset
    filename = config['CONSTANTS']['MHC_MOTIF_ATLAS_CLASS_I_FILENAME']    
    filepath = f"{config['PATHS']['TMP_PATH']}/{filename}"
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    

    # iterate through the lines and process the data
    i = 0
    for line in lines:
        if i != 0:
            data = line.strip().split('\t')
            allele = data[0]
            peptide = data[1]
            peptide_length = str(len(peptide))

            # currently only capturing the human alleles and their peptides
            if not 'H2' in allele:
                allele_number = slugify_mhc_motif_atlas_allele(allele)
                peptide_added = add_allele_and_peptide(allele_number, peptide, peptide_length)
                if peptide_added:
                    add_to_amino_acid_distribution(allele_number, peptide, peptide_length)

                add_peptide(peptide, allele_number)

                
        i+=1 

    j = 0
    for allele in alleles:
        if j == 0:
            console.print (allele)
            process_peptide_length_distribution(allele)
            process_amino_acid_distribution(allele)

            console.print (peptide_length_distributions[allele])  

            console.print (amino_acid_distributions[allele])
        j+=1      
    

    print (f"Number of peptides in dataset: {len(lines) -1}")
    print (f"Number of HLA alleles for which there is motif data: {len(alleles)}")
    print (f"Number of unique peptides: {len(peptides)}")

    console.print ('HLA-A*02:01 / P2')
    console.print (amino_acid_distributions['hla_a_02_01']['9']['P2'])
    console.print ('HLA-A*02:01 / P2')
    console.print (amino_acid_distributions['hla_a_02_01']['9']['P9'])

    action_log = {}
    
    return action_log