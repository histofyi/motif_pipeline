from typing import Dict

from pipeline import Pipeline

from steps import steps


def run_pipeline(**kwargs) -> Dict:
    pipeline = Pipeline()

    pipeline.load_steps(steps)

    #pipeline.run_step('1') # Download Class I data from the MHC Motif Atlas
    #pipeline.run_step('2') # Process Class I data from the MHC Motif Atlas
    #pipeline.run_step('3') # Create sorted amino acid distribution tables for each allele
    #pipeline.run_step('4') # Create simplified motifs for each allele
    #pipeline.run_step('5') # Create logoplots for each allele (for each length)
    #pipeline.run_step('6') # Create peptide length distribution plots for each allele
    pipeline.run_step('7') # Cluster motifs
    #pipeline.run_step('8') # Create a table representation of the data for use in datasette

    #pipeline.run_step('9') # Create text descriptions for each allele - not yet developed
    
    action_logs = pipeline.finalise()

    return action_logs

def main():

    output = run_pipeline()

if __name__ == '__main__':
    main()