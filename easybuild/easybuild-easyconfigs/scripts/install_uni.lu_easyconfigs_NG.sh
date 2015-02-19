#!/bin/bash --posix
#
# FG, 20131226 - See INSTRUCTIONS below
#
# Description:
#
# Bootstrapping for automated building of HPC software stacks & modules,
# permitting customization on per site (or system) basis; includes:
# * IntelMPI stacks; MUST be customized, eg. for oarsh
# * OpenMPI  stacks; MUST be customized, eg. for oarsh
# * INTEL toolchains (compiler & mpi stack)
# * GNU   toolchains (compiler & mpi stack)
# * HPL suites
# * few more that help to bootstrap this business


# INSTRUCTIONS
#
# 1) ensure ~sw/.bashrc properly references the correct new directory, eg. `export EASYBUILD_PREFIX=/opt/apps/HPCBIOS.20131224`
# 2) copy Intel compilers and other sourcefiles or download as needed: ln -s ../sources $EASYBUILD_PREFIX # pick from parent dir
# 3) Follow the procedure for EB as described at: https://github.com/hpcugent/easybuild/wiki/Bootstrapping-EasyBuild
# 4) Assuming you installed EB under /tmp: module load /tmp/modules/all/EasyBuild/*
# 5) eb --version # This is CRITICAL CHECK; it should report the expected version of EasyBuild without ANY problem
# 6) EBROOTEASYBUILD= time eb --try-software-name=EasyBuild --try-software-version=1.10.0
# 7) if all went fine, exit completely and log-in again and do the very final check, similar to steps 4, 5:
# 8) eb --version # This SHOULD match the step 5) and is a very strong check of reproducibility
# 9) Fix ~/easyconfig symlink as needed, so that it points to latest easyconfigs, for convenience!


export CFGS="$HOME/easybuild-easyconfigs/easybuild/easyconfigs" # where to find the easyconfigs sources
ls -als $CFGS # a human-based visual check will not hurt
module load EasyBuild
eb --version || exit 1 # Just a reality check, this step should NEVER fail
sleep 1

## First things first, this allows fast verification checks of the priority builds, at early stage
time eb $CFGS/i/impi/impi-4.1.0.030.eb -r # for ictce/5.3.0
time eb $CFGS/o/OpenMPI/OpenMPI-1.6.4-GCC-4.7.2.eb -r # for goolf/1.4.10

## Build all biodeps, to ensure enough common dependencies get started early on, good for first checks
time eb $CFGS/b/biodeps/biodeps-1.6-*-extended.eb --ignore-osdeps -r # this covers goolf/1.4.10 & ictce/5.3.0

## ==== OpenMPI stacks; MUST be customized, eg. for oarsh
## ==== Intel MPI stacks; MUST be customized, eg. for oarsh
## ==== MVAPICH stacks; MUST be customized, eg. for oarsh
## ==== MPICH stack; MUST be customized, eg. for oarsh
time eb $CFGS/o/OpenMPI/OpenMPI-*.eb -r
time eb $CFGS/i/impi/impi-*.eb -r
time eb `ls $CFGS/m/MVAPICH2/MVAPICH2-*.eb |egrep -v '(rc1|a2|b)-'` --ignore-osdeps -r # filter out Release Candidates, Alphas, Betas
time eb $CFGS/m/MPICH/MPICH*.eb -r
time eb $CFGS/m/MPICH2/MPICH2*.eb -r

## ==== custom packages (fi. TotalView, MATLAB, needs local license)
time eb $CFGS/t/TotalView/TotalView*.eb

### "Foundation" builds are over at this point; the following serve more as regression tests ###

## ==== zlib, HPL, PETSc & petsc4py
##time eb $CFGS/z/zlib/zlib*go*eb $CFGS/z/zlib/zlib*cg*eb $CFGS/z/zlib/zlib*ictce*eb -r	# Builds many many toolchains
time eb `ls $CFGS/z/zlib/zlib*{go,cg,ictce}*eb |egrep -v rc1` -r	# Build many more toolchains, but no RCs please
time eb `ls $CFGS/h/HPL/HPL-2.0-*eb            |egrep -v rc1` -r	# Widen the complexity of the builds to HPL
time eb $CFGS/p/petsc4py/petsc4py*eb --ignore-osdeps -r		# 4 complex builds with 4 major toolchains

# Desired properties of an ideal future tool for further automating the bootstrap build procedure:
# - ability to automate job submission and node task allocation for builds, on a cluster
# - block running of >2 GCC builds on the same node			# why? size limit on /dev/shm
# - block running of >1 Intel builds on the same node			# why? collission under /tmp
# - block running of >5 Intel builds in total				# why? uni.lu license limit
# - force running of ATLAS (auto-tuning) builds on a single node	# why? needed for optimization
# - understand/handle variability of nodes (eg. AVX vs non-AVX builds)	# why? differing builds

echo == Hello EasyBuild World ==
echo Substrate work of toolchains and basicing building blocks should be ready at this point.
echo Now it is time to start using HPCBIOS policies as targets for addressing specific user needs!

eb -S hpcbios_
echo "Or, you may wish to type things like: 'eb -D WRF-3.5-ictce-5.3.0-dmpar.eb -r' or:"
echo "    time eb -S goolf |cut -d/ -f4-|grep eb$|sort -R|xargs -n1 -P 12 --replace eb {} -r"
echo "    time eb -S ictce-5.3.0 |cut -d/ -f4-|grep eb$|sort -R|xargs -n1 -P 12 --replace eb {} -r"

#exit 0 # EOF
