from typing import Union, Any
from velopix.ReconstructionAlgorithms import TrackFollowing, GraphDFS, SearchByTripletTrie

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

MetricsDict: TypeAlias = dict[str, Union[int, float, bool]]
pMapType: TypeAlias = dict[str, tuple[Union[type[int], type[float], type[bool]], Any]]
pMap: TypeAlias = dict[str, Union[int, float, bool]]
EventType: TypeAlias = list[dict[str, Any]]
ReconstructionAlgorithmsType: TypeAlias = Union[TrackFollowing, GraphDFS, SearchByTripletTrie]
ValidationResults: TypeAlias = dict[str, dict[str, list[dict[str, Union[int, float, str]]]]]
ValidationResultsNested: TypeAlias = dict[str, dict[str, Union[list[dict[str, Union[int, float, str]]], dict[str, list[Union[int, float, str]]]]]]
ConfigType: TypeAlias = dict[str, tuple[Union[type[float], type[bool], type[int]], Any]]
boundType: TypeAlias = dict[str, Union[tuple[Union[int, float], Union[int, float]], Any]]
