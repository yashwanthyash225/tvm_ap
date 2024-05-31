# Installing and Running TVM
#### Install LLVM (Pre-requisite) ( from source )
```
git clone --depth 1 https://github.com/llvm/llvm-project.git
```
```
cd llvm-project
```

```
cmake -S llvm -B build -G "Unix Makefiles" -DLLVM_ENABLE_PROJECTS="clang;lld" -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=on
```

```
cd build
```

```
cmake --build . -j8
```

After this, you can see llvm executables in ```llvm-project/build/bin/``` folder.

While installing TVM, provide the ```/path/to/llvm-project/build/bin/llvm-config```

#### Other requirements
Could create new conda environment.
 ```
 sudo apt-get update
  ```
  
 ```
sudo apt-get install -y python3 python3-dev python3-setuptools gcc libtinfo-dev zlib1g-dev build-essential cmake libedit-dev libxml2-dev
```

Install python dependencies which are present at the end of the document.
 ```
 pip3 install numpy decorator attrs
  ```

 ```
pip3 install typing-extensions psutil scipy
 ```

```
pip3 install tornado
 ```
 
 ```
pip3 install 'xgboost>=1.1.0' cloudpickle
```

#### Install TVM ( from source )
We will be following the document https://tvm.apache.org/docs/install/from_source.html for installing TVM from source

```
git  clone  --recursive  https://github.com/apache/tvm  tvm
```

```
cd tvm
```

```
mkdir build
```

```
cp cmake/config.cmake build/
```

```
cd build/
```

Do changes in config.cmake in build folder
```
Provide llvm-config path installed in USE_LLVM
USE_RELAY_DEBUG ON
```

```
make -j8
```

### Set enviornment variable PYTHONPATH to use tvm
1. Edit the file ```vi ~/.bashrc```
2. Add the following in the file
```
export TVM_HOME=/path/to/tvm
export PYTHONPATH=$TVM_HOME/python:${PYTHONPATH}
```
3. ```$ source ~/.bashrc```


### Running TVM
A very simple model of a FC layer is used in ```test.py``` file
```
python3 test.py
```
Added few logs in the source code to get the flow of TVM, run this to print the logs added.
```
TVM_LOG_DEBUG="relay/backend/te_compiler.cc=1,relay/backend/build_module.cc=1,relay/backend/graph_executor_codegen.cc=1,driver/driver_api.cc=1,target/codegen.cc=1,target/llvm/llvm_module.cc=1,target/llvm/codegen_llvm.cc=1,target/llvm/codegen_llvm.h=1,tir/ir/stmt_functor.cc=1,tir/stmt_functor.h=1" python3 lower.py
```
