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
