#!/usr/bin/env python3

def extract_bgen_region(bgen_file, region):
  from subprocess import Popen, PIPE
  import sys

  # This could be modified to select individual variants instead of a region with one of: 
  # -incl-positions, -incl-rsids, -incl-snpids, or -incl-variants
  p = Popen(f"qctool -g {bgen_file} -incl-range {region} -ofiletype gen -og -", shell=True, stdout=PIPE, stderr=PIPE, close_fds=True, universal_newlines=True)

  # For qctool, it is important to attempt to read stdout first. If we wait for stderr first,
  # the process will block waiting for stdout to be read.
  # This block loops over .gen formatted lines, yielding each one. 
  for line in p.stdout:
    yield line

  # Check if there was any output on stderr.
  # qctool unfortunately uses stderr to print console output, so we need to check stderr for error messages.
  stderr = p.stderr.read()
  stderr_lower = stderr.lower()
  if 'error' in stderr_lower or 'fail' in stderr_lower:
    sys.stderr.write(stderr)
    raise Exception(f"An error occurred while reading from qctool. The error message is printed above.")

if __name__ == "__main__":
  # This loops over each line in the bgen file within a region and prints the first few elements.
  # Note the chromosome is "01" (this is apparently what is used in the bgen file). 
  for line in extract_bgen_region("example.v11.bgen", "01:1-15000"):
    print(line.split()[0:9])
