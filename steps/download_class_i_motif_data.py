from typing import Dict
import requests

from helpers.files import write_file

def download_class_i_motif_data(**kwargs) -> Dict[str,str]:
    """
    This function downloads the class I motif data from the MHC Motif Atlas

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

    url = config['CONSTANTS']['MHC_MOTIF_ATLAS_CLASS_I']

    filename = config['CONSTANTS']['MHC_MOTIF_ATLAS_CLASS_I_FILENAME']
    
    action_log = {}

    r = requests.get(url)
    action_log['http_status_code'] = r.status_code
    if r.status_code == 200:
        text = r.text
        filepath = f"{config['PATHS']['TMP_PATH']}/{filename}"
        write_file(filepath, text)
        action_log['file_length'] = len(text)
        action_log['file_path'] = filepath
        action_log['error'] = None
    else:
        action_log['error'] = 'file_not_found'
        if verbose:
            print (f"Error with {r.status_code} when downloading {url}")
        text = None
    return action_log