# my_app/history_patch.py

import json
import gzip
import atexit
from uuid import uuid4
from copy import deepcopy
from typing import Any

from velopix.hyperParameterFramework._optimizers import BaseOptimizer

class HistoryFileWriter:
    def __init__(self, path="history.jsonl", compress=False):
        opener = gzip.open if compress else open
        mode = "at" if compress else "a"
        self.f = opener(path, mode=mode, encoding="utf-8", buffering=1)

    def record(self, validation_result, score):
        entry: dict[str, Any] = {
            str(uuid4()): {
            "params": validation_result["parameters"],
            "score": score,
            "total_tracks": validation_result["total_tracks"],
            "overall_ghost_rate": validation_result["overall_ghost_rate"]
            "avg_event_ghost_rate": validation_result["event_avg_ghost_rate"]
            "meta": validation_result,
            }
        }
        self.f.write(json.dumps(entry) + "\n")

    def close(self):
        self.f.close()

_writer = HistoryFileWriter(path="history.jsonl", compress=False)
atexit.register(_writer.close)

def _file_backed_evaluate_run(self, validationResult, weight, nested):  
    score = self.objective_func(weight, nested)
    _writer.record(validationResult, score)
    if score is None:  # type:ignore
        return
    self.score_history.append(score)
    compare = (score < self.best_score) if (self.objective == "min") else (score > self.best_score)
    if compare:
        self.best_score = score
        self.best_config = deepcopy(self.prev_config)

BaseOptimizer._evaluate_run = _file_backed_evaluate_run