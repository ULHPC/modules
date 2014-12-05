#
# Rakefile - Configuration file for rake (http://rake.rubyforge.org/)
#
require 'falkorlib'

# Adapt the Git flow aspects
FalkorLib.config.gitflow do |c|
  c[:branches] = {
    :master  => 'production',
    :develop => 'devel'
  }
end

# Git customization
FalkorLib.config.git do |c|
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
  }
end


require 'falkorlib/tasks/git'
