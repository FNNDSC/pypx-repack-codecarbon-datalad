# High Performance _Green_ DICOM Retrival Using Rust

Reproducible benchmarking of [`px-repack`](https://github.com/FNNDSC/pypx)'s energy consumption and carbon emissions,
compared to that of [`rx-repack`](https://github.com/FNNDSC/pypx-listener).

**README WIP**

## The Benchmark

The data are a collection of [phantom data from the _Dartmouth Brain Imaging Center_](https://datasets.datalad.org/?dir=/dicoms/dartmouth-phantoms).
In this experiment, we are going to process 76GB of DICOM data.

`px-repack` and `rx-repack` are each called per DICOM instance as subprocesses.
When `px-repack` is called by `storescp`, there is no upper limit to the number of subproecesses created.
This is a source of CPU and memory inefficiency. However, in this experiment the number of threads
is limited to (a realistic value of) 512 so that the machine does not run out-of-memory. I suggest that
30GB of memory be available to run this benchmark.

## Running

```shell
export TMPDIR=/var/tmp/somewhere/with/space...  # optional
just bench
```

## Notes About CodeCarbon

- https://github.com/mlco2/codecarbon/issues/244
- `tracking_mode="machine"` is necessary: when CodeCarbon is tracking `process` instead of `machine`,
  it tries to track the memory usage of individual subprocesses, but that doesn't work here because
  each subprocess is short-lived.
