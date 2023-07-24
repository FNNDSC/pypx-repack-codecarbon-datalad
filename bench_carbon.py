#!/usr/bin/env python
"""
Use codecarbon to compare energy efficiency improvement of rx-repack over px-repack.
"""
import subprocess as sp
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePath
from tempfile import TemporaryDirectory

from codecarbon import track_emissions
from tqdm import tqdm


def main():
    parser = ArgumentParser(description='benchmark carbon emissions of rx-repack and px-repack')
    parser.add_argument('-p', '--program', action='append', help='program to benchmark')
    parser.add_argument('dicom_dir', type=Path, help='directory containing input DICOMs')
    parser.add_argument('-J', '--jobs', type=int, help='number of threads')
    options = parser.parse_args()
    dicom_dir: Path = options.dicom_dir
    programs: list[str] = options.program if options.program else ['rx-repack', 'px-repack']

    for exe in programs:
        print(flush=True)
        print('--------------------------------------------------------------------------------')
        print(f'                         BENCHMARKING: {exe}')
        print('--------------------------------------------------------------------------------')
        print(flush=True)

        with TemporaryDirectory() as temp_dir:
            benchmark(dicom_dir, temp_dir, exe, options.jobs)


def find_dicoms(path: Path) -> list[Path]:
    if path.name.startswith('.'):
        return []
    if path.suffix == '.dcm':
        return [path]
    if path.is_dir():
        return [
            dcm for subpath in path.iterdir()
            for dcm in find_dicoms(subpath)
            if not subpath.name.startswith('.')
        ]
    return []


def curry_cmd(exe: str, temp_dir: str, pbar: tqdm):
    temp_path = Path(temp_dir)
    data_dir = temp_path / 'data'
    log_dir = temp_path / 'log'

    def repack(dicom_instance: PurePath):
        cmd = [
            exe,
            '--xcrdir', dicom_instance.parent,
            '--xcrfile', dicom_instance.name,
            '--datadir', data_dir,
            '--logdir', log_dir,
            '--verbosity', '0'
        ]
        sp.run(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL, check=True)
        pbar.update()

    return repack


@track_emissions(log_level='warning')
def benchmark(dicom_dir: Path, temp_dir: str, exe: str, max_workers: int):
    dicoms = find_dicoms(dicom_dir)
    with tqdm(total=len(dicoms)) as pbar:
        repack_dicom = curry_cmd(exe, temp_dir, pbar)
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for dcm in dicoms:
                pool.submit(repack_dicom, dcm)


if __name__ == '__main__':
    main()
