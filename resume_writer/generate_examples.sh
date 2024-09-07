#!/bin/bash

pushd resume_writer

# Usage: main.py [OPTIONS] INPUT_FILE
# 
#   Convert a text resume to a .docx file.
#
# Options:
#   --output-file PATH
#   --settings-file PATH
#   --resume-type [ats|basic|plain]
#   --help                          Show this message and exit.

# plain format, summary only
echo
echo "Plain format, summary only"
echo
python main.py \
--output-file data/plain_summary_resume.docx \
--resume-type plain \
--settings-file settings_summary_resume.toml \
../tests/test_resume.md

echo '#########################'
echo
echo "Plain format, job history only"
echo
python main.py \
--output-file data/plain_no_summary_resume.docx \
--resume-type plain \
--settings-file settings_nosummary_resume.toml \
../tests/test_resume.md

echo '#########################'
echo
echo "Plain format, full resume"
echo
python main.py \
--output-file data/plain_full_resume.docx \
--resume-type plain \
--settings-file settings_full_resume.toml \
../tests/test_resume.md

echo '#########################'
echo
echo "ATS format"
echo
python main.py \
--output-file data/ats_resume.docx \
--resume-type plain \
--settings-file settings_ats_resume.toml \
../tests/test_resume.md

echo '#########################'
echo
echo "Basic formatting, for debugging"
echo
python main.py \
--output-file data/basic_test_resume.docx \
--resume-type plain \
--settings-file settings_debug.toml \
../tests/test_resume.md