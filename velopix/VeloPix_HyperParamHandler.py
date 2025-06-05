import os
import json
import logging
from typing import Any
import argparse

from solvers.velopix_pipeline import TrackFollowingPipeline, GraphDFSPipeline, SearchByTripletTriePipeline, PipelineBase
import solvers

"""     
Unknowns for atm:
- How do we save the data?
    - how do we get this run data?
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_events(num_events: int, directory: str = "./data/raw") -> list[dict[str, Any]]:
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        logger.error(
            "Cannot load events: directory does not exist -> %s", directory
        )
        return []
    logger.info("Looking for JSON files in directory: %s", directory)

    events: list[dict[str, Any]] = []
    for i in range(num_events):
        if i == 51:
            logger.warning("Skipping problematic file: velo_event_%d.json", i)
            continue

        filename = f"velo_event_{i}.json"
        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, "r") as f:
                events.append(json.load(f))
            logger.info("Loaded file: %s", filename)
        except FileNotFoundError:
            logger.error("File not found: %s", filepath)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in %s: %s", filepath, e)

    return events


def get_pipeline(algo: str, events: list[dict[str, Any]], intra_node: bool) -> PipelineBase:
    mapping: dict[str, PipelineBase] = {
        "TF": TrackFollowingPipeline,
        "GDFS": GraphDFSPipeline,
        "ST": SearchByTripletTriePipeline,
    } # type: ignore
    try:
        pipeline = mapping[algo]
    except KeyError:
        raise ValueError(f"Invalid reconstruction_algo: {algo!r}")

    return pipeline(events=events, intra_node=intra_node) # type: ignore


def main(config: dict[str, Any], root_dir: str):
    try:
        Solver = getattr(solvers, config.get("solverName")) # solverName CANNOT be None!
    except AttributeError:
        raise ValueError(f"No class named {config.get('solverName')} found")
    
    logging.info(f"Root Dir: {root_dir}")
    events = load_events(config["num_events"], os.path.join(root_dir, "data/raw"))
    if not events:
        logger.error("No events were loaded. Exiting.")
        return
    pipeline = get_pipeline(config["reconstruction_algo"], events, config["intra_node"])

    optimiser = Solver(**CONFIG["optimizer"])

    logger.info("Starting pipeline...")
    optimal_parameters = pipeline.optimise_parameters(
        optimiser,
        max_runs=config["max_runs"],
    )
    logger.info("Optimal parameters found: %s", optimal_parameters)

    with open(os.path.join(root_dir, "result.json"), "w") as f:
        json.dump(optimiser.history, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to the configuration file")
    args = parser.parse_args()

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = args.config

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            CONFIG = json.load(f)
            main(CONFIG, base_path)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"Unable to load config from '{config_path}': {e}")
    
