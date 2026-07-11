# spack-deployer

An opinionated structure around deploying Spack 1.2.1 (and possibly other
versions) on OpenHPC 3.

# Overall file structure

## Before deployment

- `deploy` contains a deployment shell script, currently set for Spack 1.2.1, GCC 14, and cuda_arch=80
- `site-settings/` contains settings to be copied into `$spack/etc/spack/site/`

## After deployment

- `packages_develop/` will contain a clone of https://github.com/spack/spack-packages.git , develop branch
- `$tag/` will contain an extracted archive of a tag of https://github.com/spack/spack.git -- usually this is a `v[0-9]*` folder

# Usage

As root: `dnf -q -y install git gcc-gfortran gcc-c++ patch unzip`

As a normal user:
- clone this repository to a folder where you want to deploy Spack into
- change directories to that folder
- `./deploy`