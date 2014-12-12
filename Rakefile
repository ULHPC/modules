##############################################################################
# Rakefile - Configuration file for rake (http://rake.rubyforge.org/)
# Time-stamp: <Ven 2014-12-12 18:03 svarrette>
#
# Copyright (c) 2014 Sebastien Varrette <Sebastien.Varrette@uni.lu>
# .             http://varrette.gforge.uni.lu
#                       ____       _         __ _ _
#                      |  _ \ __ _| | _____ / _(_) | ___
#                      | |_) / _` | |/ / _ \ |_| | |/ _ \
#                      |  _ < (_| |   <  __/  _| | |  __/
#                      |_| \_\__,_|_|\_\___|_| |_|_|\___|
#
# Use 'rake -T' to list the available actions
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Resources:
# * http://www.stuartellis.eu/articles/rake/
# * Pascal Morillon's Capfile for the Grid5000 puppet repository
##############################################################################

require 'falkorlib'

# Adapt the Git flow aspects
FalkorLib.config.gitflow do |c|
  c[:branches] = {
    :master  => 'prod',
    :develop => 'develop'
  }
end

# Configure the git submodules
FalkorLib.config.git do |c|
    c[:submodules] = {
        'Makefiles' => {
            :url    => 'https://github.com/Falkor/Makefiles'
        }
  }
  c[:subtrees] = {
    'easybuild/framework' => {
      :url    => 'https://github.com/ULHPC/easybuild-framework.git',
      :branch => 'develop'
    },
    'easybuild/easyblocks' => {
      :url    => 'https://github.com/ULHPC/easybuild-easyblocks.git',
      :branch => 'develop'
    },
    'easybuild/easyconfigs' => {
      :url    => 'https://github.com/ULHPC/easybuild-easyconfigs.git',
      :branch => 'uni.lu'
    },
    'easybuild/wiki' => {
      :url    => 'https://github.com/hpcugent/easybuild-wiki.git',
    },
                  end



    # Git[Flow] and Versioning management
    require "falkorlib/tasks/git"    # OR require "falkorlib/git_tasks"





    #=======================================================================
    # eof
    #
    # Local Variables:
    # mode: ruby
    # End:
