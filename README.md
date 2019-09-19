## Summary

This repo contains a few widely-used open source libraries, they're all compiled with Visual Studio 2017 and v141_xp platform toolset and tested on Windows XP.

## Motivations

We are maintaining some Windows programs which still need XP support, and we used quite a few C and C++ libraries in the program. We've also been searching for a suitable C or C++ package manager to help us easying obtaining these libraries, but the tools like vcpkg or NuGet don't provide an option to compile the source with the XP platform toolset (maybe they will, just not yet). 

Microsoft has dropped XP support since 2014, and also Visual Studio 2017 is the last Visual Studio that can build a Windows XP program. It seems to be a perfect time to recompile all these open-source libraries using v141_xp (the latest XP platform toolset), and then we'll be all done with XP support (hopefully).

## Compile Options

All of these libraries were statically linked to the C runtime libraries, it means your programs won't need to additionally distribute the vc_redist.exe to customer's computer, of course, there is a trade-off of this approach (unable to obtain secure updates, etc.).

For LGPL licensed libraries, we've built them as DLL files (still statically linked to CRT). The reason for distributing LGPL libraries as dynamic libraries can be found here: https://www.gnu.org/licenses/gpl-faq.html#LGPLStaticVsDynamic

## Libraries

### VMime

VMime is a special one, it is licensed under GPL but also provides a commercial license. We built VMime as static libraries since we purchased a commercial license from the developer. If you want to use VMime in your closed-source project, please consider purchasing a license from http://www.kisli.com/solutions/vmime/licenses.html 

### AWS SDK

AWS SDK is not fully compiled, only core library, s3, and s3 transfer are provided. AWS core library requires aws-c-common which uses quite a few Vista APIs for thread safety, as a workaround, we rebuilt aws-c-common with pthreads4win and used its POSIX wrappers, it works so far. There are also a few other changes we made to the SDK, I'll explain these changes in a separate place.

## Source Code

Eventually, we will upload all the source code into this repo, probably a separate branch.
