import inspect
import asyncio
from contextlib import contextmanager
from typing import Any, Iterator


class CallRecorder:
    """Records calls and returns or raises a configured value."""

    def __init__(
        self,
        return_value: Any = None,
        side_effect: Any = None,
    ) -> None:
        self.return_value = return_value
        self.side_effect = side_effect
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        side_effect = self.side_effect
        if side_effect is not None:
            if isinstance(side_effect, BaseException):
                raise side_effect
            if isinstance(side_effect, type) and issubclass(side_effect, BaseException):
                raise side_effect()
            if callable(side_effect):
                result = side_effect(*args, **kwargs)
                if inspect.iscoroutine(result):
                    return result
                return result
        return self.return_value

    @property
    def call_count(self) -> int:
        return len(self.calls)

    def assert_called_once(self) -> None:
        if self.call_count != 1:
            raise AssertionError(
                f"Expected exactly one call, got {self.call_count}"
            )


class FakeRepo:
    """Fake repository with get/create call recorders."""

    def __init__(self) -> None:
        self.get = CallRecorder()
        self.get_by_username = CallRecorder()
        self.get_by_email = CallRecorder()
        self.get_all = CallRecorder()
        self.create = CallRecorder()
        self.update = CallRecorder()
        self.delete = CallRecorder()


class FakeSession:
    """Stand-in for an SQLAlchemy Session."""

    def __init__(self) -> None:
        self.commit_calls = 0
        self.rollback_calls = 0

    def commit(self) -> None:
        self.commit_calls += 1

    def rollback(self) -> None:
        self.rollback_calls += 1


class FakeDatabase:
    """Provides a context-manager .session() yielding the given FakeSession."""

    def __init__(self, session: FakeSession) -> None:
        self._session = session

    @contextmanager
    def session(self) -> Iterator[FakeSession]:
        yield self._session


class FakeRow:
    """Simple attribute container."""

    def __init__(self, **attrs: Any) -> None:
        for key, value in attrs.items():
            setattr(self, key, value)