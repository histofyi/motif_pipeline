from download_class_i_motif_data import download_class_i_motif_data
from process_class_i_motif_data import process_class_i_motif_data
from build_sorted_amino_acid_distributions import build_sorted_amino_acid_distributions
from build_simplified_motifs import build_simplified_motifs
from build_logoplots import build_logoplots
from build_peptide_length_distribution_plots import build_peptide_length_distribution_plots
from build_text_descriptions import build_text_descriptions
from cluster_motifs import cluster_motifs
from build_table_representation import build_table_representation



steps = {
    '1':{
        'function':download_class_i_motif_data,
        'title_template':'a local copy of Class I data from the MHC Motif Atlas.',
        'title_verb':['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '2':{
        'function':process_class_i_motif_data,
        'title_template':'the local copy of Class I data from the MHC Motif Atlas.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '3':{
        'function':build_sorted_amino_acid_distributions,
        'title_template':'the output to build sorted amino acid distribution tables.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '4':{
        'function':build_simplified_motifs,
        'title_template':'the output to build simplified motifs for each allele.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '5':{
        'function':build_logoplots,
        'title_template':'the output to build motif logoplots for each allele.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '6':{
        'function':build_peptide_length_distribution_plots,
        'title_template':'the output to build motif length distribution plots for each allele.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '7':{
        'function':build_text_descriptions,
        'title_template':'the output to build a text description for each allele.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '8':{
        'function':cluster_motifs,
        'title_template':'the output to cluster similar motifs - coming soon.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '9':{
        'function':build_table_representation,
        'title_template':'the output to build a table representation for use in datasette - coming soon.',
        'title_verb':['Processing', 'Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    }
}