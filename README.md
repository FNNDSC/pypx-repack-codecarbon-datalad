# High Performance _Green_ DICOM Retrival Using Rust

Benchmarking of [`px-repack`](https://github.com/FNNDSC/pypx)'s energy consumption and carbon emissions,
compared to that of [`rx-repack`](https://github.com/FNNDSC/pypx-listener).

This is a [Datalad](https://www.datalad.org/) repository.

## Background

[pypx](https://github.com/FNNDSC/pypx) is a suite of Python tools which provide a Python and command-line
API to a PACS server for DICOM query and retrieval. `px-repack`, is a tool from `pypx` which is called by
[`storescp`](https://support.dcmtk.org/docs/storescp.html) on each DICOM instance received from the PACS.
The job of `px-repack` is to copy incoming DICOM files to another path named by DICOM tag data.
Recently, we re-implemented `px-repack` in [Rust](https://www.rust-lang.org/) for better performance.
This reimplementation is known as `rx-repack` and is housed under a new project called
[`pypx-listener`](https://github.com/FNNDSC/pypx-listener).

## The Benchmark

In this experiment, we will compare the elapsed duration, energy consumption, and estimated carbon emissions
of `rx-repack` versus `px-repack`.

### The Data

The data are a collection of [phantom data from the _Dartmouth Brain Imaging Center_](https://datasets.datalad.org/?dir=/dicoms/dartmouth-phantoms).

> Yaroslav Halchenko. (2023). dbic/QA: 0.20230710.0 (0.20230710.0). Zenodo. https://doi.org/10.5281/zenodo.8180219

For this experiment we are using 76GB of DICOM data.

### Technical Details

`px-repack` and `rx-repack` are each called per DICOM instance as subprocesses.
Concurrency is limited to 512 instances.

While there is no upper limit nor buffering on the number of subprocess callbacks made by `storescp`,
which is a source of CPU and memory inefficiency, in this experiment the number of threads is limited to
(a realistic value of) 512 so that the machine does not run out-of-memory. I suggest that 30GB of memory
be available to run this benchmark.

### Setup Data and Benchmarks

First, install [`just`](https://github.com/casey/just#installation)
and [`micromamba`](https://mamba.readthedocs.io/en/latest/installation.html#micromamba-standalone-executable).
Then run

```shell
# get the data
just untar

# install dependencies
just install
```

You also need to compile `rx-repack` from [FNNDSC/pypx-listener](https://github.com/FNNDSC/pypx-listener)
(`cargo build --release`) and add the binary to `$PATH`.

Lastly, see https://github.com/mlco2/codecarbon/issues/244 for how to set up CPU power consumption tracking.

### Run the Benchmark

200GB of free space is required on `/tmp` to run the benchmark. Alternatively, set the `TMPDIR`
variable to somewhere where sufficient scratch space is mounted:

```shell
export TMPDIR=/var/tmp/somewhere/with/space...  # optional
```

To run the benchmark:

```shell
just bench
```

### Visualization

`carbonboard` is used to visualize `emissions.csv` (produced by [CodeCarbon](https://codecarbon.io),
ran by `just bench`). However, it is currently broken. See https://github.com/mlco2/codecarbon/issues/423

You can install the fixed `carbonboard` by running

```shell
pip install 'codecarbon[viz] @ git+https://github.com/mlco2/codecarbon.git@refs/pull/424/merge'
```

## Results

To process 76GB of data, `px-repack` takes 4.8 hours, costing 1.74 kWh of power and emitting 0.6 kg CO2.
`rx-repack` does the same in 9 minutes and has a negligible energy cost of 4 watt-hours.

## Conclusion

Rust is _blazingly fast!_
