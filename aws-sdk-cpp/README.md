### Read Me

AWS SDK is not fully compiled, only core library, s3, and s3 transfer are provided. The static libraries can be downloaded at https://github.com/haoxi911/ports_v141_xp/releases/download/v0.1/aws-sdk-cpp.zip

### Modifications

#### 1) aws-c-common

  - Remove the Vista-only library bcrypt.lib, review source file "device_random.c" and remove all the BCrypt API references.

  - Copy "condition_variable.c", "mutex.c", and "rw_lock.c" from the "posix" folder and overwrite the same files in "windows" folder. Add depedency library pthreads4w, this will replace the Vista-only thread saftey implementations (defined in Synchapi.h) with pthreads.
  
  - Revise "clock.c" and "thread.c", remove the use of Vista-only API "InitOnceExecuteOnce".
   
#### 2) aws-cpp-sdk-core

   - Find cmake / external_dependencies.cmake and set ENABLE_OPENSSL_ENCRYPTION to ON while PLATFORM_WINDOWS is set. By default, CMake will use BCrypt on Windows, which is not compatible with Windows XP, this change will tell CMake to use OpenSSL instead.

   - Remove "SimpleUDP.cpp" and its references from the aws-cpp-sdk-core project (the related APIs like "inet_ntop" are not existed on Windows XP).