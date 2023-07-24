# High Performance _Green_ DICOM Retrival Using Rust


## Notes About CodeCarbon

- https://github.com/mlco2/codecarbon/issues/244
- `tracking_mode="machine"` is necessary: when CodeCarbon is tracking `process` instead of `machine`,
  it tries to track the memory usage of individual subprocesses, but that doesn't work here because
  each subprocess is short-lived.

