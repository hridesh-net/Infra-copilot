from abc import ABC, abstractmethod
from typing import Optional, Any

# from src.backend.core.context import context
class Agent(ABC):
    """
    Abstract base class for all Agents in an agentic workflow.
    Defines the canonical lifecycle: initialize, observe, decide, act, cleanup.
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Common initialization hook.
        Subclasses should call super().__init__() if they override this.
        :param config: Optional dict of parameters (e.g. API keys, model weights, thresholds)
        """

        self.config = config or {}
        self.internal_state: dict[str, Any] = {}
        self._initialized = False
        # self.context = context

    def initialize(self) -> None:
        """
        Set up any external connections, load models, etc.
        Called once before any observe/decide/act cycle begins.
        """
        self._initialized = True

    @abstractmethod
    def observe(self, inputs: Any) -> Any:
        """
        Pull data from environment or pre-process raw inputs.
        :param inputs: raw data or context
        :return: processed observation
        """
        ...

    @abstractmethod
    def decide(self, observation: Any) -> Any:
        """
        Core planning or decision-making logic.
        :param observation: output from observe()
        :return: a plan or action descriptor
        """
        ...

    @abstractmethod
    def act(self, plan: Any) -> Any:
        """
        Execute the chosen action (e.g., API call, database update, physical actuator).
        :param plan: output from decide()
        :return: result or feedback
        """
        ...

    def run_one_cycle(self, inputs: Any) -> Any:
        """
        Orchestrates a single observe→decide→act cycle.
        Automatically initializes on first run.
        """
        if not self._initialized:
            self.initialize()
        obs = self.observe(inputs)
        plan = self.decide(obs)
        result = self.act(plan)
        return result

    def cleanup(self) -> None:
        """
        Graceful shutdown: close connections, flush logs, etc.
        """
        self._initialized = False
        # override in subclass if needed

    def __enter__(self):
        """Support for `with Agent() as a:` patterns."""
        if not self._initialized:
            self.initialize()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.cleanup()
