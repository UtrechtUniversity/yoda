# YodaDrive Development Environment
This document describes setting up a development environment for YodaDrive. [YodaDrive](https://github.com/UtrechtUniversity/YodaDrive) is a WebDAV driver for Windows, written in C#. Development of YodaDrive requires a Windows development environment with Visual Studio Community 2017 or better.

## Virtual Machine
A Windows development environment, if not already available, can be installed on a virtual machine in Azure (`Standard B2ms`, 2 CPUs, 8 GB memory) or another cloud provider. If creating a VM in the cloud, make sure to restrict RDP access by IP address, or the machine will be hacked in short order even when kept fully up-to-date.

## Visual Studio
[Visual Studio Community 2019](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) is sufficient for development of YodaDrive, since YodaDrive is open source.
Make sure that the following components are included for installation:
* .NET Desktop Development
* .NET Framework 4.6.1 development tools

## WinFsp
[WinFsp](https://github.com/billziss-gh/winfsp/releases) is a FUSE-like driver for Windows, which is required by YodaDrive.  The version to install is `2019.3 B2` or later, and must match the version used by YodaDrive.
WinFsp must be installed manually. Installing it as part of YodaDrive is not sufficient, since the `Developer` option must be selected during installation.

## YodaDrive
Within VS2019, clone from [https://github.com/UtrechtUniversity/YodaDrive.git](https://github.com/UtrechtUniversity/YodaDrive).  Then open the `KS2Drive.sln` solution.

## Development
YodaDrive is an open source project, which inherits from (KS2.Drive)[https://github.com/FrKaram/KS2.Drive).  Main development takes part on the `development` branch. Everything specific to YodaDrive is on the `feature/yoda-rebranding' branch.
When buiding a YodaDrive release, switch to the `feature/yoda-rebranding` branch, merge the latest changes from the `development` branch if needed, and update the version number in `About/About.xaml`.

## WinFsp dependency files for YodaDrive distributable
The distributable for YodaDrive can be made to automatically install the proper version of WinFsp as part of the installation process. In order to build the distributable properly, the following has to be done first.
* checkout branch `feature/yoda-rebranding`
* copy the `Reference/WinFsp*_*` folder to
```
C:\Program Files (x86)\Microsoft SDKs\ClickOnce Bootstrapper\Packages
```
* reboot the machine
* start Visual Studio
* verify that WinFsp is listed among the requirements for publication

## Developer code signing
The YodaDrive distributable should be signed with the appropriate code signing key. The person in charge of this can install the key within Visual Studio, so that it can automatically sign releases thereafter.

## Publication
Publication will generate `Application Files`, `KS2Drive.application` and `setup.exe` in the output directory `C:\OutputKS2Drive`.  These can then be archived in a ZIP file for distribution.
