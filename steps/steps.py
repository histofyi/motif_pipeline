from download_class_i_motif_data import download_class_i_motif_data
from process_class_i_motif_data import process_class_i_motif_data

steps = {
    '1':{
        'function':download_class_i_motif_data,
        'title_template':'Downloading a local copy of Class I data from the MHC Motif Atlas.',
        'list_item':'Downloads a local copy of Class I data from the MHC Motif Atlas.',
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '2':{
        'function':process_class_i_motif_data,
        'title_template':'Processing the local copy of Class I data from the MHC Motif Atlas.',
        'list_item':'Processes the local copy of Class I data from the MHC Motif Atlas.',
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    }
}