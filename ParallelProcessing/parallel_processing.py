"""Example on how to trigger Spark actions in parallel from Python.
The core idea of this app is to use ThreadPoolExecutor to trigger Spark actions from different threads.
HOW TO RUN
    To run, download/copy-paste this gist and run it from your terminal:
    python parallel_processing.py
    Prerequisites:
    - Python 3.8+
    - Java installed and enabled via JAVA_HOME env var
    - PySpark installed
HOW TO CONFIGURE
    Use `Config` object to tweak the output directory and number of tasks to generate.
HOW TO UNDERSTAND IT BETTER
    Try to adjust the `execute_one()` function to:
    1. Use named arguments instead of `TriggerParams`. How do you adjust `pool.map()` call?
    2. Try to raise exceptions. How would you refactor the code to fail gracefully?
       How to gather exceptions from all failing threads?
"""

import random
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pyspark.sql import SparkSession


class Config:
    """Contains config parameterizing this app."""

    output_data_root_dir: Path = Path(__file__).parent.joinpath("output_data")
    number_of_runs: int = 20
    do_shuffle: bool = True


@dataclass(frozen=True)
class TriggerParams:
    """This is a parameters' wrapper for every action trigger.
    The processing function should be fed with a SINGLE argument, and dataclass is a good way to prevent
    arbitrary arguments passing into that function.
    Together with mypy, it allows better type safety, especially important in parallel execution
    (when it's not clear on which step exactly an error occurred).
    BUT it is also possible to use other data types such as tuples, dicts etc.
    In this case, you'd need to adjust the execution function accordingly.
    """

    run_id: int
    query: str
    output_path: str


def main():
    spark = SparkSession.builder.getOrCreate()
    trigger_params = build_trigger_params(Config())

    # We need to trigger Spark actions in different THREADS, not processes, to overcome Python GIL
    # Learn more here: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
    pool = ThreadPoolExecutor(max_workers=4)
    # `.map()` method returns the futures (and results) in the SAME ORDER as elements of the iterator passed there
    futures = pool.map(lambda tp: execute_one(spark, tp), trigger_params)

    # Wait until each future is done
    # If we care about the actual outputs, e.g. to handle exceptions, assign them to a variable:
    # results = [f for f in futures is f is not None]
    _ = [f for f in futures]

    print("Processing is done.")


def build_trigger_params(cfg: Config) -> List[TriggerParams]:
    """Builds parameters for each execution that will be passed to an execution function."""
    trigger_configs = [
        TriggerParams(run_id, f"SELECT {run_id} AS x", cfg.output_data_root_dir.joinpath(f"run_id={run_id}").as_posix())
        for run_id in range(cfg.number_of_runs)
    ]
    if cfg.do_shuffle:
        return random.sample(trigger_configs, len(trigger_configs))
    return trigger_configs


def execute_one(spark: SparkSession, trigger_params: TriggerParams) -> None:
    """This function does the actual job."""
    print(f"[{trigger_params.run_id:02}] Trigger parameters: {trigger_params}.")
    spark.sql(trigger_params.query).repartition(1).write.mode("overwrite").csv(trigger_params.output_path)
    print(f"[{trigger_params.run_id:02}] Data is written into `{trigger_params.output_path}`")


if __name__ == "__main__":
    main()