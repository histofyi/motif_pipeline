from typing import Dict, List

from helpers.files import write_json, read_json
import csv
import os


def build_table_representation(**kwargs) -> Dict[str,str]:
    config = kwargs['config']
    verbose = kwargs['verbose']
    force = kwargs['force']
    output_path = kwargs['output_path']
    console = kwargs['console']
    function_name = kwargs['function_name']

    input_filename = f"{output_path}/motifs/sorted_amino_acid_distributions.json"
    csv_output_filename = f"{output_path}/motifs/motifs.csv"

    sorted_amino_acid_distributions = read_json(input_filename)

    ## table format ##

    # allele_slug   position    amino_acid  grade       percentage  peptide_length
    # hla_a_01_01   3           D           very-high   67.933      9

    peptide_length = 9

    table = []

    labels = ['allele_slug', 'position', 'amino_acid', 'grade', 'percentage', 'peptide_length']

    table.append(labels)

    for allele_slug in sorted_amino_acid_distributions:
        for position in sorted_amino_acid_distributions[allele_slug][str(peptide_length)]:
            for motif_amino_acid in sorted_amino_acid_distributions[allele_slug]['9'][position]:
                row = [allele_slug, position, motif_amino_acid['amino_acid'], motif_amino_acid['grade'], motif_amino_acid['percentage'], peptide_length]
                table.append(row)

    print (labels)
    print (len(table))

    with open(csv_output_filename, 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    db_output_filename = f"{output_path}/motifs/motifs.db"

    if os.path.exists(db_output_filename):
        os.remove(db_output_filename)

    csvs_to_sqllite_command = f"csvs-to-sqlite {csv_output_filename} {db_output_filename}"

    print (csvs_to_sqllite_command)
    os.system(csvs_to_sqllite_command)