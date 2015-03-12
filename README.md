-*- mode: markdown; mode: auto-fill; fill-column: 100 -*-
Time-stamp: <Ven 2014-11-14 00:42 svarrette>

       _   _ _       _   _ ____   ____   __  __           _       _
      | | | | |     | | | |  _ \ / ___| |  \/  | ___   __| |_   _| | ___  ___
      | | | | |     | |_| | |_) | |     | |\/| |/ _ \ / _` | | | | |/ _ \/ __|
      | |_| | |___  |  _  |  __/| |___  | |  | | (_) | (_| | |_| | |  __/\__ \
       \___/|_____| |_| |_|_|    \____| |_|  |_|\___/ \__,_|\__,_|_|\___||___/

> Copyright (c) 2014 [UL HPC Management Team](mailto:<hpc-sysadmins@uni.lu>) 

[Environment Modules](http://modules.sourceforge.net/) /
[LMod](https://www.tacc.utexas.edu/tacc-projects/lmod) /
[Easybuild](http://hpcugent.github.io/easybuild/) configuration available on the
[UL HPC](http://hpc.uni.lu) platform.  

* [MIT Licence](Licence.md) 
* [GitHub Homepage](https://github.com/ULHPC/modules) 

-------------------

## Synopsis

This repository host all elements required to manage the
[Modules](http://modules.sourceforge.net/) environment available on the
[UL HPC](http://hpc.uni.lu) platform.  

Mostly, our workflow relies on [Easybuild](http://hpcugent.github.io/easybuild/). 

## Pre-requisites & related tools/frameworks

### Git

You should become familiar (if not yet) with [Git](http://git-scm.com/).
Consider these resources:

* [Git book](http://book.git-scm.com/index.html)
* [Github:help](http://help.github.com/mac-set-up-git/)
* [Git reference](http://gitref.org/)

At least, you shall configure the following exported variables within your favorite shell (adapt accordingly):

    # Bash configuration
    # Set your git user info
    export GIT_AUTHOR_NAME='<firstname> <name>'
    export GIT_AUTHOR_EMAIL='<email>'
    export GIT_COMMITTER_NAME="${GIT_AUTHOR_NAME}"
    export GIT_COMMITTER_EMAIL="${GIT_AUTHOR_EMAIL}"

You can also use the following commands:

    $> git config --global user.name "Your Name Comes Here"
    $> git config --global user.email you@yourdomain.example.com
    # configure colors
    $> git config --global color.diff auto
    $> git config --global color.status auto
    $> git config --global color.branch auto
    
### git-flow

The Git branching model for this repository follows the guidelines of
[gitflow](http://nvie.com/posts/a-successful-git-branching-model/).
In particular, the central repository holds two main branches with an infinite lifetime:

* `production`:    the *production-ready* branch
* `devel`: the main branch where the latest developments intervene. This is
  the *default* branch you get when you clone the repo

### Ruby, Bundle and Rakefile

The various operations that can be conducted from this repository are piloted
from a `Rakefile` and assumes you have a running Ruby installation.

#### bootstrapping without RVM 

If you hate [RVM](https://rvm.io/) and run [Debian](https://www.debian.org/), you can bootstrap this repository as follows: 

	$> sudo apt-get install build-essential  ruby1.9.3	$> sudo gem install bundler
	$> bundle 


You should now be able to access the list of available tasks by running:

	$> rake -T

#### bootstrapping with RVM 

The bootstrapping of your repository is normally based on [RVM](https://rvm.io/), thus
ensure this tools are installed on your system -- see
[installation notes](https://rvm.io/rvm/install).

The ruby stuff part of this repository corresponds to the following files: 

* `.ruby-{version,gemset}`: [RVM](https://rvm.io/) configuration, use the name of the
  project as [gemset](https://rvm.io/gemsets) name
* `Gemfile[.lock]`: used by `[bundle](http://bundler.io/)`
  







You should now be able to access the list of available tasks by running:

	$> rake -T

You probably wants to activate the bash-completion for rake tasks.
I personnaly use the one provided [here](https://github.com/ai/rake-completion)



## Installation

This repository is hosted on out [GitHub](https://github.com/ULHPC/modules).
Once cloned, initiate your local copy of the repository by running:

    $> cd modules
    $> rake setup



----  

# Advanced information

## Releasing mechanism

The operation consisting of releasing a new version of this repository is automated by a set of tasks within the `Rakefile`.

In this context, a version number have the following format:

      <major>.<minor>.<patch>-b<build>

where:

* `< major >` corresponds to the major version number
* `< minor >` corresponds to the minor version number
* `< patch >` corresponds to the patching version number
* `< build >` states the build number _i.e._ the total number of commits within the `develop` branch.

Example: `1.0.0-b28`

The current version number is stored in the file `VERSION`. __/!\ NEVER MAKE ANY MANUAL CHANGES TO THIS FILE__

For more information on the version, run:

     $> rake version:info

If a new  version number such be bumped, you simply have to run:

      $> rake version:bump:{major,minor,patch}

This will start the release process for you using `git-flow`.
Probably after that, the first things to do is to change within the main LaTeX document the version number and commit this change.
Then, to make the release effective, just run:

      $> rake version:release

it will finish the release using `git-flow`, create the appropriate tag in the `prod` branch and merge all things the way they should be.

