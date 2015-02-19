There are a couple of ways to install EasyBuild, depending on your use case. This page describes the various installation methods.

 * [Bootstrapping](#bootstrapping)
 * [Standard installation of latest release](#standard_install)
 * [Installation from downloaded sources](#source_install)
 * [Installation of latest release from GitHub](#github_install)
 * [Installation of latest development version](#github_devel_install)

***

<a name="wiki-bootstrapping">
## Bootstrapping

The easiest way (by far) to installing EasyBuild is by bootstrapping, i.e. installing EasyBuild with EasyBuild. By following the bootstrap procedure, you'll obtain an `EasyBuild` module you can load to start using EasyBuild.

```bash
wget https://raw.github.com/hpcugent/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py
python bootstrap_eb.py $HOME/.local/easybuild
```

Only when that fails to work for you for some reason, you should resort to one of the approaches below, which are more involved (but also give more control).

See [[Bootstrapping EasyBuild]] for more detailed information.

<a name="wiki-standard_install">
## Standard installation of latest release

Usually, you just want to install the latest (stable) version of each of the EasyBuild packages (framework, easyblocks, easyconfigs).

Python provides a couple of tools for that, which rely on the Python Package Index (PyPi).
Every version of the EasyBuild packages is released via PyPi.


### Installing EasyBuild without admin rights

If you do not have EasyBuild installed yet, or if you just want to install the most recent version of each of the EasyBuild packages,
you can use one of the following simple commands:

 * using ```easy_install``` (old tool, but still works):
```bash
easy_install --user easybuild
```

 * using ```pip``` (more recent and better installation tool for Python software):
```base
pip install --user easybuild 
```

The ```--user``` part in these commands allows you to install EasyBuild without admin rights.
It will just install EasyBuild in your home directory (the exact location depends on the OS).

If you don't have `pip` or `easy_install` available, see [here](#source_install).

### Adjusting ```PATH``` environment variable

After installing EasyBuild with either ```easy_install``` or ```pip``` like this, you will need to
update the ```PATH``` environment variable to make sure the system can find the main EasyBuild command ```eb```.
On (most) Linux distributions, the command for doing this is:

```bash
export PATH=$HOME/.local/bin:$PATH
```

On Mac OS X systems, the user-site install location is different, so the command would look something like:

```bash
export PATH=$HOME/Library/Python/2.7/bin:$PATH
```

Depending on the OS X version and the Python version that comes with it, you may need to adjust the Python version used in the path.


### Install with admin rights

If you do have admin rights on the system where you want to install EasyBuild, you can simply omit the ```--user``` flag
to have EasyBuild installed system-wide. In that case, you do not need to touch the ```PATH``` environment variable since
the ```eb``` command will be installed in one of the default paths.


<a name="wiki-user_alternatives">
### Alternatives to ```--user```

One problem is that the ```--user``` option is relatively new, and thus only available in recent Python installations.
As an alternative when you do not have admin rights, you can control where EasyBuild is installed using the ```--prefix``` option.
However, that does require that you also adjust the ```PYTHONPATH``` environment variable that specifies the Python search path.
With the ```--user``` option, Python takes care of that itself.

The full list of commands to install EasyBuild in the installation prefix ```/tmp``` using ```pip``` would be:

```bash
pip install --prefix=/tmp easybuild
export PATH=/tmp/bin:$PATH
export PYTHONPATH=/tmp/lib/python2.7/site-packages:$PYTHONPATH
```
Or alternatively (with an old pip) 
```bash
pip install --install-option="--prefix=/tmp" easybuild
```

To determine the path that should be added to the ```PYTHONPATH``` environment variable for a given installation prefix, you can use the following command:

```bash
python -c "import distutils.sysconfig; print distutils.sysconfig.get_python_lib(prefix='/tmp');"
```


### Installing the EasyBuild packages separately

Each of the EasyBuild packages can also be installed separetely:

```bash
pip install --user easybuild-framework
pip install --user easybuild-easyblocks
pip install --user easybuild-easyconfigs
```

This is basically the exact same sequence of steps as they will be performed when running ```pip install --user easybuild```.



<a name="wiki-source_install">
## Installation from downloaded sources

To install one of the EasyBuild packages from a downloaded source tarball, use the following steps:

```bash
tar xfvz easybuild-framework-1.0.tar.gz
cd easybuild-framework-1.0
pip install --user .
```

Do note that when an EasyBuild package is being installed without having the EasyBuild packages that it depends upon available,
both ```easy_install``` and ```pip``` will try and pull in the latest available version of those packages from PyPi.

Thus, to have full control over the EasyBuild installation, you need to respect the following installation order:
easybuild-framework, easybuild-easyblocks, easybuild-easyconfigs. The easyblocks package depends on the framework package;
the easyconfigs package depends on both the framework and easyblocks packages.

If you do not have `pip` or `easy_install` available, you can also fall back to using the `setup.py` script directly:

```bash
python setup.py --user install
```

or, using `--prefix` (see also [here](#user_alternatives))

```bash
python setup.py install --prefix $HOME/.local
```

<a name="wiki-github_install">
## Installation of the latest release from GitHub

To install the latest (stable) release of an EasyBuild package directly from GitHub, use the following command:

```bash
pip install --user http://github.com/hpcugent/easybuild-framework/archive/master.tar.gz
```

Again, the order in which the EasyBuild packages are installed is important to have full control over the installation process, see previous section.



<a name="wiki-github_devel_install">
## Installation of latest development version

To install the latest development version of an EasyBuild package from GitHub, you can simply adjust the command
from the previous section to install from the ```develop``` branch (or any of the available feature branches in any
EasyBuild repository for that matter).

```bash
pip install --user http://github.com/hpcugent/easybuild-framework/archive/develop.tar.gz
```

'''Note''': you should only use this if you are interested in developing for EasyBuild. Although it is well tested,
the development version of EasyBuild may be unstable at a given point in time.