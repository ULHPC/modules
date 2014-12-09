#######################################################################################################################
# Author: Maxime Schmitt
# Mail: maxime.schmitt@telecom-bretagne.eu
# Overview: Module that take care of bootstraping EasyBuild.
#######################################################################################################################

import os
import re
import sys
import shutil
import subprocess
from git import Repo

sys.path.append('.')
from configManager import getEasyBuildVersion

#######################################################################################################################
# Function that do the bootstrap using the other functions of this module and return the associated modulePath.
def bootstrap(hashTable):

	# We install all the necessary files of EasyBuild.
	easybuildFilesInstaller(hashTable)

	# We create the modulefile of EasyBuild.
	eb_version = getEasyBuildVersion(hashTable['rootinstall'])
	modulefileCreator(hashTable, "install-" + eb_version)

	# We create some files to source to rapidly start using the bootstrap module and the associated softwares.
	modulePath = sourcefileCreator(hashTable)

	return modulePath

#######################################################################################################################


#######################################################################################################################
# Functions that do the different important tasks of the bootstrap.

# Get and put at the right place all the EasyBuild files.
def easybuildFilesInstaller(hashTable):
	# We create the directory that we need to install the EasyBuild sources
	easyBuildDir = os.path.join(hashTable['rootinstall'], '.installRef')
	if not os.path.exists(easyBuildDir):
		os.makedirs(easyBuildDir)

	altSources = {}
	# If we were provided alternative sources for the EasyBuild files, we create the useful variables
	if any(True for x in ['gh_ebuser', 'git_ebframework', 'git_ebblocks', 'git_ebconfigs'] if x in hashTable):
		if 'gh_ebuser' in hashTable:
			altSources['easybuild-framework'] = ('https://github.com/' + hashTable['gh_ebuser'] + '/easybuild-framework.git', \
				hashTable['branch_ebframework'] if 'branch_ebframework' in hashTable else None)

			altSources['easybuild-easyblocks'] = ('https://github.com/' + hashTable['gh_ebuser'] + '/easybuild-easyblocks.git', \
				hashTable['branch_ebblocks'] if 'branch_ebblocks' in hashTable else None)

			altSources['easybuild-easyconfigs'] = ('https://github.com/' + hashTable['gh_ebuser'] + '/easybuild-easyconfigs.git', \
				hashTable['branch_ebconfigs'] if 'branch_ebconfigs' in hashTable else None)

		if 'git_ebframework' in hashTable:
			altSources['easybuild-framework'] = (hashTable['git_ebframework'], hashTable['branch_ebframework'] if 'branch_ebframework' in hashTable else None)
	
		for v in ['blocks', 'configs']:
			if 'git_eb'+v in hashTable:
				altSources['easybuild-easy'+v] = (hashTable['git_eb'+v], hashTable['branch_eb'+v] if 'branch_eb'+v in hashTable else None)

	# Import any alternative EasyBuild files from given sources
	pwd = os.getcwd()
	os.chdir(os.path.join(hashTable['rootinstall'], '.installRef'))
	subprocess.check_call(['git', 'init'])
	subprocess.check_call(['touch', 'temp'])
	subprocess.check_call(['git', 'add', 'temp'])
	subprocess.check_call(['git', 'commit', '-m', 'initial commit'])
	tmp = os.getcwd()
	for k,v in altSources.iteritems():
		# Crash if the directory is not empty, not critical, but what would we do in this case ?
		# Throw a error message of our own ? Overwrite ? (seems a bad idea) Consider it is ok ("already installed")
		# and proceed just throwing a Warning ?

		# We get the remote
		subprocess.check_call(['git', 'remote', 'add', '-f', 'install-'+k, v[0]])
		# If a branch is provided we use it, otherwise we clone the one pointed by HEAD.
		if v[1] == None:
			subprocess.check_call(['git', 'checkout', 'FETCH_HEAD', '-b', k+'-FETCH_HEAD'])
			subprocess.check_call(['git', 'filter-branch', '-f', k+'-FETCH_HEAD'])
			subprocess.check_call(['git', 'checkout', 'master'])
			subprocess.check_call(['git', 'submodule', 'add', '-b', k+'-FETCH_HEAD', './', k])
			subprocess.check_call(['git', 'branch', '-D', k+'-FETCH_HEAD'])
		else:
			subprocess.check_call(['git', 'checkout', 'install-'+k+'/'+v[1], '-b', k+'-'+v[1]])
			subprocess.checkout(['git', 'filter-branch', '-f', k+'-'+v[1]])
			subprocess.check_call(['git', 'checkout', 'master'])
			subprocess.check_call(['git', 'submodule', 'add', '-b', k+'-'+v[1], './', k])
			subprocess.check_call(['git', 'branch', '-D', k+'-'+v[1]])
		# We remove the remotes when finished
		os.chdir(os.path.join(tmp, k))
		subprocess.check_call(['git', 'remote', 'remove', 'origin'])
		os.chdir(tmp)
		subprocess.check_call(['git', 'commit', '-m', "'Adding "+k+"'"])

	if any(True for x in ['easybuild-framework', 'easybuild-easyblocks', 'easybuild-easyconfigs'] if not x in altSources):
		# We complete the EasyBuild files with the ones from the subtree if necessary
		subprocess.check_call(['git', 'remote', 'add', '-f', 'install-resif', hashTable['srcpath']])
	
		for k in ['easybuild-framework', 'easybuild-easyblocks', 'easybuild-easyconfigs']:
			if not k in altSources:
				ebPart = re.search("[^-]*$", k).group(0)
				if hashTable['release'] != 'HEAD':
					subprocess.check_call(['git', 'checkout', 'install-resif/'+hashTable['branch'], '-b', k])
				elif 'branch' in hashTable:
					subprocess.check_call(['git', 'checkout', hashTable['release'], '-b', k])
				else:
					subprocess.check_call(['git', 'checkout', 'FETCH_HEAD', '-b', k])
				subprocess.check_call(['git', 'filter-branch', '-f', '--subdirectory-filter', 'easybuild/'+ebPart , k])
				subprocess.check_call(['git', 'checkout', 'master'])
				subprocess.check_call(['git', 'submodule', 'add', '-b', k, './', k])
				subprocess.check_call(['git', 'branch', '-D', k])
				# We remove the local remote
				os.chdir(os.path.join(tmp, k))
				subprocess.check_call(['git', 'remote', 'remove', 'origin'])
				os.chdir(tmp)
				subprocess.check_call(['git', 'commit', '-m' , "'Adding "+k+"'"])

	# We remove the remote when finished, clean the repository and commit the final state.
	subprocess.check_call(['git', 'rm', 'temp'])
	subprocess.check_call(['git', 'commit', '-m', "'EasyBuild installed'"])
	os.chdir(pwd)


# Create the EasyBuild module file and the associated symlink and put them at the right places.
# If the ThematicMNS module naming scheme is used, it is also installed.
def modulefileCreator(hashTable, moduleName):
	modulesDirPath = os.path.join(os.path.join(hashTable['rootinstall'], 'core'), 'modules')
	# Adapt the location of the modulfile to the chosen MNS
	if hashTable['mns'] == "ThematicMNS":
		# We create the directories we need to install EasyBuild
		EBmoduleDir = os.path.join('base', 'EasyBuild')
		easybuildPath = os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir)
		if not os.path.exists(easybuildPath):
			os.makedirs(easybuildPath)
		easybuildPath = os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir)
		if not os.path.exists(easybuildPath):
			os.makedirs(easybuildPath)
		# We install the ThematicMNS
		setThematicMNS(hashTable)

	else:
		# We create the directories we need to install EasyBuild
		EBmoduleDir = 'EasyBuild'
		easybuildPath = os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir)
		if not os.path.exists(easybuildPath):
			os.makedirs(easybuildPath)
		easybuildPath = os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir)
		if not os.path.exists(easybuildPath):
			os.makedirs(easybuildPath)

	# Path to the actual module file
	moduleFilePath = os.path.join(os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir), moduleName)

	with open(moduleFilePath, "w") as f:
		f.write("\
#%Module\n\
\n\
proc ModulesHelp { } {\n\
	puts stderr {   EasyBuild is a software build and installation framework\n\
written in Python that allows you to install software in a structured,\n\
repeatable and robust way. - Homepage: http://hpcugent.github.com/easybuild/\n\
This module provides the development version of EasyBuild.\n\
}\n\
}\n\
module-whatis {EasyBuild is a software build and installation framework\n\
written in Python that allows you to install software in a structured,\n\
repeatable and robust way. - Homepage: http://hpcugent.github.com/easybuild/\n\
This module provides the development version of EasyBuild.\n\
}\n\
set root    " + os.path.join(hashTable['rootinstall'], '.installRef') + "\n\
conflict    EasyBuild\n\
prepend-path    PATH            \"$root/easybuild-framework\"\n" \
+ ("\nprepend-path    PYTHONPATH      \"$root/MNS\"\n" if hashTable['mns'] == 'ThematicMNS' else "\n") + \
"prepend-path    PYTHONPATH      \"$root/easybuild-framework\"\n\
prepend-path    PYTHONPATH      \"$root/easybuild-easyblocks\"\n\
prepend-path    PYTHONPATH      \"$root/easybuild-easyconfigs\"\n\
")
	
	# Path to the symlink to the module file.
	symlinkPath = os.path.join(os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir), moduleName)
	os.symlink(moduleFilePath, symlinkPath)


# TODO: Go to using repo instead of direct file access from the directory
# Install the ThematicMNS module naming scheme.
def setThematicMNS(hashTable):
	mnsroot = os.path.join(os.path.join('.installRef', 'MNS'), 'easybuild')
	
	# Extends the Python path in such a way that we included this architecture in the easybuild namespace.
	mnsPath = os.path.join(hashTable['rootinstall'], os.path.join(os.path.join(mnsroot, 'tools'), 'module_naming_scheme'))
	if not os.path.exists(mnsPath):
		os.makedirs(mnsPath)
	with open(os.path.join(mnsPath, '__init__.py'), "w") as f:
		f.write("\
from pkgutil import extend_path\n\
__path__ = extend_path(__path__, __name__)\n\
")
	shutil.copyfile(os.path.join(mnsPath, '__init__.py'), \
		os.path.join(os.path.join(os.path.join(hashTable['rootinstall'] ,mnsroot), 'tools'), '__init__.py'))
	shutil.copyfile(os.path.join(mnsPath, '__init__.py'), \
		os.path.join(os.path.join(hashTable['rootinstall'], mnsroot), '__init__.py'))

	# Import the module naming scheme
	#repo shutil.copyfile(os.path.join(os.path.join(hashTable['srcpath'], 'bin'), 'ThematicMNS.py'), \
	#repo	os.path.join(mnsPath, 'ThematicMNS.py'))
	thematicStr = hashTable['git_tree']['bin/ThematicMNS.py'].data_stream.read()
	with open(os.path.join(mnsPath, 'ThematicMNS.py'), 'w') as f:
		f.write(thematicStr)


# Create some files to source to easily start using the EasyBuild module and the associated softwares.
# These files are put in the <rootinstall> directory.
def sourcefileCreator(hashTable):
	trueVersion = os.path.basename(hashTable['rootinstall'])
	# Variable containing all the required path for the MODULEPATH
	modulePath = ""
	moduleClasses = ['bio', 'cae', 'chem', 'compiler', 'data', 'debugger', 'devel', 'geo', 'lang', 'lib', 'math', \
	'mpi', 'numlib', 'perf', 'phys', 'system', 'toolchain', 'tools', 'vis', 'base']
	for swset in hashTable['swsets']:
		for moduleclass in moduleClasses:
			modulePath += os.path.join(os.path.join(os.path.join(hashTable['rootinstall'], swset), 'modules'), moduleclass) + ":"
	# If the core software set is not in the software sets to be installed, we still have to add the EasyBuild module location
	if not 'core' in hashTable['swsets']:
		modulePath += os.path.join(os.path.join(os.path.join(hashTable['rootinstall'], 'core'), 'modules'), 'base') + ":"

	# If we have the admin role, we create two files to source, one for the admin and another one for the cluster users.
	if hashTable['role'] == "admin":
		# By default, we don't install in core but in ulhpc
		sourcepathAdmin = os.path.join(os.path.join(hashTable['rootinstall'], ".ebdirs"), 'sources') # "<rootinstall>/.ebdirs/sources"
		buildpathAdmin = os.path.join(os.path.join(hashTable['rootinstall'], ".ebdirs"), 'build') # "<rootinstall>/.ebdirs/build"
		installpathAdmin = os.path.join(hashTable['rootinstall'], 'ulhpc')
		repositorypathAdmin = os.path.join(os.path.join(hashTable['rootinstall'], ".ebdirs"), 'eb_repo') # "<rootinstall>/.ebdirs/eb_repo"

		sourcepathUser = os.path.join(os.path.join(os.path.join("$HOME", ".resif"), trueVersion), 'sources') # "$HOME/.resif/vx.y-YYYYMMDD/sources"
		buildpathUser = os.path.join(os.path.join(os.path.join("$HOME", ".resif"), trueVersion), 'build') # "$HOME/.resif/vx.y-YYYYMMDD/build"
		installpathUser = os.path.join(os.path.join("$HOME", ".resif"), trueVersion) # "$HOME/.resif/vx.y-YYYYMMDD"
		repositorypathUser = os.path.join(os.path.join(os.path.join("$HOME", ".resif"), trueVersion), 'eb_repo') # "$HOME/.resif/vx.y-YYYYMMDD/eb_repo"
		# The admin file is there to easily add software in the ulhpc swset without any manual changes to the config.
		with open(os.path.join(hashTable['rootinstall'], "LOADME-" + trueVersion + "-admin.sh"), "w") as f:
			f.write("\
export EASYBUILD_SOURCEPATH=" + sourcepathAdmin + "\n\
export EASYBUILD_BUILDPATH=" + buildpathAdmin + "\n\
export EASYBUILD_INSTALLPATH=" + installpathAdmin + "\n\
export MODULEPATH=" + modulePath + "\n\
export EASYBUILD_REPOSITORY=FileRepository\n\
export EASYBUILD_REPOSITORYPATH=" + repositorypathAdmin + "\n\
export EASYBUILD_LOGFILE_FORMAT=(\"easybuild\", \"easybuild-%(name)s-%(version)s-%(date)s.%(time)s.log\")\n\
# Currently, we continue to use environment-modules. We'll switch to Lmod later\n\
#export EASYBUILD_MODULES_TOOL=Lmod\n\
export EASYBUILD_MODULE_NAMING_SCHEME=" + hashTable['mns'] + "\n\
export RESIF_ROOTINSTALL=" + hashTable['rootinstall'] + "\n\
")
		# The user file is there to easily add software locally without any manual change to the config.
		with open(os.path.join(hashTable['rootinstall'], "LOADME-" + trueVersion + "-user.sh"), "w") as f:
			f.write("\
export EASYBUILD_SOURCEPATH=" + sourcepathUser + "\n\
export EASYBUILD_BUILDPATH=" + buildpathUser + "\n\
export EASYBUILD_INSTALLPATH=" + installpathUser + "\n\
export MODULEPATH=" + modulePath + "\n\
export EASYBUILD_REPOSITORY=FileRepository\n\
export EASYBUILD_REPOSITORYPATH=" + repositorypathUser + "\n\
export EASYBUILD_LOGFILE_FORMAT=(\"easybuild\", \"easybuild-%(name)s-%(version)s-%(date)s.%(time)s.log\")\n\
# Currently, we continue to use environment-modules. We'll switch to Lmod later\n\
#export EASYBUILD_MODULES_TOOL=Lmod\n\
export EASYBUILD_MODULE_NAMING_SCHEME=" + hashTable['mns'] + "\n\
export RESIF_ROOTINSTALL=" + hashTable['rootinstall'] + "\n\
")

	# If we have the user role, we only create one file to source, this configuration being meant for only one user.
	else:
		sourcepathUser = os.path.join(os.path.join(hashTable['rootinstall'], '.ebdirs'), 'sources') # "<rootinstall>/.ebdirs/sources"
		buildpathUser = os.path.join(os.path.join(hashTable['rootinstall'], '.ebdirs'), 'build') # "<rootinstall>/.ebdirs/build"
		installpathUser = os.path.join(hashTable['rootinstall'], 'core') # "<rootinstall>/.ebdirs"
		repositorypathUser = os.path.join(os.path.join(hashTable['rootinstall'], '.ebdirs'), 'eb_repo') # "<rootinstall>/.ebdirs/eb_repo"
		with open(os.path.join(hashTable['rootinstall'], "LOADME-" + trueVersion + ".sh"), "w") as f:
			f.write("\
export EASYBUILD_SOURCEPATH=" + sourcepathUser + "\n\
export EASYBUILD_BUILDPATH=" + buildpathUser + "\n\
export EASYBUILD_INSTALLPATH=" + installpathUser + "\n\
export MODULEPATH=" + modulePath + "\n\
export EASYBUILD_REPOSITORY=FileRepository\n\
export EASYBUILD_REPOSITORYPATH=" + repositorypathUser + "\n\
export EASYBUILD_LOGFILE_FORMAT=(\"easybuild\", \"easybuild-%(name)s-%(version)s-%(date)s.%(time)s.log\")\n\
# Currently, we continue to use environment-modules. We'll switch to Lmod later\n\
#export EASYBUILD_MODULES_TOOL=Lmod\n\
export EASYBUILD_MODULE_NAMING_SCHEME=" + hashTable['mns'] + "\n\
export RESIF_ROOTINSTALL=" + hashTable['rootinstall'] + "\n\
")
	return modulePath

#######################################################################################################################