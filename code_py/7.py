import warnings


class NDFrame:
    pass


class Index:
    pass


class DatetimeIndex(Index):
    pass


class PeriodIndex(Index):
    pass


class TimedeltaIndex(Index):
    pass


class Resampler:
    def __init__(self, obj, timegrouper, group_keys, gpr_index):
        pass


class DatetimeIndexResampler(Resampler):
    pass


class PeriodIndexResampler(Resampler):
    pass


class TimedeltaIndexResampler(Resampler):
    pass


def find_stack_level():
    return 1


class TimeGrouper:
    def __init__(self):
        self.group_keys = True

    def _set_grouper(self, obj, gpr_index=None):
        return None, PeriodIndex(), None

    def _get_resampler(self, obj: NDFrame) -> Resampler:
        """
        Return my resampler or raise if we have an invalid axis.

        Parameters
        ----------
        obj : Series or DataFrame

        Returns
        -------
        Resampler

        Raises
        ------
        TypeError if incompatible axis

        """
        _, ax, _ = self._set_grouper(obj, gpr_index=None)
        if isinstance(ax, DatetimeIndex):
            return DatetimeIndexResampler(
                obj,
                timegrouper=self,
                group_keys=self.group_keys,
                gpr_index=ax,
            )
        elif isinstance(ax, PeriodIndex):
            if isinstance(ax, PeriodIndex):
                # GH#53481
                warnings.warn(
                    "Resampling with a PeriodIndex is deprecated. "
                    "Cast index to DatetimeIndex before resampling instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            return PeriodIndexResampler(
                obj,
                timegrouper=self,
                group_keys=self.group_keys,
                gpr_index=ax,
            )
        elif isinstance(ax, TimedeltaIndex):
            return TimedeltaIndexResampler(
                obj,
                timegrouper=self,
                group_keys=self.group_keys,
                gpr_index=ax,
            )

        raise TypeError(
            "Only valid with DatetimeIndex, "
            "TimedeltaIndex or PeriodIndex, "
            f"but got an instance of '{type(ax).__name__}'"
        )


if __name__ == "__main__":
    tg = TimeGrouper()
    obj = NDFrame()
    tg._get_resampler(obj)