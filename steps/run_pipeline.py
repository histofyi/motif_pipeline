from typing import Dict

from pipeline import Pipeline

from steps import steps


def run_pipeline(**kwargs) -> Dict:
    pipeline = Pipeline()

    pipeline.load_steps(steps)

    pipeline.run_step('1')
    pipeline.run_step('2')

    action_logs = pipeline.finalise()

    return action_logs

def main():

    output = run_pipeline()

if __name__ == '__main__':
    main()