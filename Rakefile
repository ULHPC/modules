#
# Rakefile - Configuration file for rake (http://rake.rubyforge.org/)
#
require 'falkorlib'

# Adapt the Git flow aspects
FalkorLib.config.gitflow do |c|
    c[:branches] = {
        :master  => 'production',
        :develop => 'develop'
    }
end

require 'falkorlib/tasks/git'
