
dicom_tgz_dir := "./QA/sourcedata/sub-qa64/"
dicom_dir := "./dicom_dir/"
condaenv := "./.condaenv/"

bench:
    false

untar: get
    mkdir -v {{dicom_dir}}
    find {{dicom_tgz_dir}} -name '*.dicom.tgz' \
      | parallel --bar tar xf '{}' --directory {{dicom_dir}}

get:
    micromamba -p {{condaenv}} run datalad get {{dicom_tgz_dir}}

install: install-pypx

install-pypx: install-conda-deps
    micromamba -p {{condaenv}} run pip install pypx==3.10.16

install-conda-deps:
    micromamba create -p {{condaenv}} -f env.yaml
