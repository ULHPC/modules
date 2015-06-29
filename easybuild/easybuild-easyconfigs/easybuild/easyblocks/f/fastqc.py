##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
General EasyBuild support for installing FastQC

@author: Emilio Palumbo
"""
import os
import stat

from easybuild.tools.filetools import run_cmd
from easybuild.easyblocks.generic.packedbinary import PackedBinary


class EB_FastQC(PackedBinary):
    """Easyblock implementing the build step for FastQC,
    this is just give execution permission to the `fastqc` binary before installing.
    """

    def install_step(self):
        """Overwrite install_step from PackedBinary"""
        os.chdir(self.builddir)
        os.chmod("FastQC/fastqc", os.stat("FastQC/fastqc").st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        super(EB_FastQC, self).install_step()


