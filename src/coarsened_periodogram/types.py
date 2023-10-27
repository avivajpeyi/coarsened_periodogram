from dataclasses import dataclass
from typing import Literal
import numpy as np
from xarray_dataclasses import (
    AsDataArray,
    Attr,
    Coord,
    Coordof,
    Data,
    DataOptions,
    Name,
)

TIME = Literal["time"]
FREQ = Literal["freq"]




@dataclass
class TimeAxis:
    data: Data[TIME, int]
    long_name: Attr[str] = "Time"
    units: Attr[str] = "s"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]


@dataclass
class FreqAxis:
    data: Data[FREQ, int]
    long_name: Attr[str] = "Frequency"
    units: Attr[str] = "Hz"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]


@dataclass
class TimeSeries(AsDataArray):
    data: Data[TIME, float]
    time: Coordof[TimeAxis] = 0
    name: Name[str] = "Time Series"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    @property
    def sample_rate(self):
        return 1 / self.dt

    @property
    def duration(self):
        return self.time[-1] - self.time[0]

    @property
    def dt(self):
        return self.time[1] - self.time[0]

    @property
    def nyquist_frequency(self):
        return 1 / (2 * self.dt)


@dataclass
class FrequencySeries(AsDataArray):
    data: Data[FREQ, float]
    freq: Coordof[FreqAxis] = 0
    name: Name[str] = "Frequency Series"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    @classmethod
    def from_time_series(cls, time_series: TimeSeries):
        freq = np.fft.rfftfreq(len(time_series), d=time_series.dt)
        data = np.fft.rfft(time_series)
        return cls(
            data=data,
            freq=FreqAxis(freq),
        )

    @property
    def df(self):
        return self.freq[1] - self.freq[0]

    @property
    def sample_rate(self):
        return self.df * len(self.freq)

