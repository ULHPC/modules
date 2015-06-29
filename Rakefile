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
    'easybuild/easybuild-framework' => {
      :url    => 'https://github.com/ULHPC/easybuild-framework.git',
      :branch => 'uni.lu-develop'
    },
    'easybuild/easybuild-easyblocks' => {
      :url    => 'https://github.com/ULHPC/easybuild-easyblocks.git',
      :branch => 'uni.lu-develop'
    },
    'easybuild/easybuild-easyconfigs' => {
      :url    => 'https://github.com/ULHPC/easybuild-easyconfigs.git',
      :branch => 'uni.lu-develop'
    },
  }
end


require 'falkorlib/tasks/git'
