from typing import Dict, List

from helpers.files import write_json, read_json

import hdbscan

def cluster_motifs(**kwargs) -> Dict[str,str]:
    config = kwargs['config']
    verbose = kwargs['verbose']
    force = kwargs['force']
    output_path = kwargs['output_path']
    console = kwargs['console']
    function_name = kwargs['function_name']

    # we take the sorted amino acid distributions as input
    input_filename = f"{output_path}/motifs/sorted_amino_acid_distributions.json"

    sorted_amino_acid_distributions = read_json(input_filename)
    
    # load the list of amino acids from the constants
    amino_acid_list = config['CONSTANTS']['AMINO_ACIDS']

    # initialise the position_amino_acid_labels list
    position_amino_acid_labels = []

    # and populate it with the composite labels for the position and amino acid
    for position in range(1,10):
        for amino_acid in amino_acid_list:
            position_amino_acid_labels.append(f"{position}_{amino_acid}")
    
    # initialise the allele_labels list
    allele_labels = []

    # initialise the flattened_motifs list
    flattened_motifs = []

    # loop through the alleles
    for allele_slug in sorted_amino_acid_distributions:
        # add the allele to the allele_labels list
        allele_labels.append(allele_slug)
        # initialise the flattened_motif list for this allele
        flattened_motif = []

        # loop through the positions in the nonamer motif
        for position in sorted_amino_acid_distributions[allele_slug]['9']:
            # initialise the position_amino_acids dictionary, we set the percentage for each amino acid to 0 as a default
            position_amino_acids = {amino_acid:0 for amino_acid in amino_acid_list}
            # loop through the amino acids at this position and add the percentages to the position_amino_acids dictionary
            for motif_amino_acid in sorted_amino_acid_distributions[allele_slug]['9'][position]:
                position_amino_acids[motif_amino_acid['amino_acid']] = motif_amino_acid['percentage'] 
            # add the amino acid percentages to the flattened motif
            for position_amino_acid in position_amino_acids:
                flattened_motif.append(position_amino_acids[position_amino_acid])
        # add the flattened motif to the flattened_motifs list
        flattened_motifs.append(flattened_motif)


    # cluster the motifs using HDBSCAN
    # we set the minimum cluster size to 2 as we want the maximum number of precise clusters
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2)

    # generate the cluster labels for the motifs
    cluster_labels = clusterer.fit_predict(flattened_motifs)

    # create a dictionary to store the clusters
    clusters = {}

    # loop through the alleles and add them to the appropriate cluster
    for i in range(len(allele_labels)):
        # if the cluster label is -1 then the motif is an outlier
        if cluster_labels[i] == -1:
            cluster_label = 'outliers'
        else:
            cluster_label = f"cluster_{cluster_labels[i] + 1}"
        # if the cluster label is not already in the clusters dictionary then add it
        if cluster_label not in clusters:
            clusters[cluster_label] = []
        # add the allele to the appropriate cluster
        clusters[cluster_label].append(allele_labels[i])
    
    # generate an ordered list of the clusters
    ordered_clusters = sorted(clusters.keys())
    # iterate through the ordered clusters and print the alleles in each cluster
    for cluster in ordered_clusters:
        print (f"Cluster {cluster}: {clusters[cluster]}")   


    # create the action log which will be included in the log file for this run of the pipeline
    action_log = {
        'alleles_processed':len(flattened_motifs),
        'motifs_processed':len(flattened_motifs),
        'clusters_found':len(ordered_clusters) - 1,
        'outlier_count':len(clusters['outliers'])
    }
    
    return action_log