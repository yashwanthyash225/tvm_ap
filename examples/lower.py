import torch.nn as nn
import torch
import tvm
from tvm import relay
from tvm.relay import transform
from tvm.contrib import graph_executor
from tvm.relay.backend import Runtime
from tvm.relay.backend import Executor
import logging

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.k1 = nn.Linear(4, 1)
    def forward(self, input1):
        return self.k1(input1)

logging.basicConfig(level=logging.INFO)
model = MyModel()
input_shape = [1, 4]
# input_shape = [4]
input_data = torch.tensor([[1.0, 2.0, 3.0, 4.0]])
input_name = "input0"
shape_list = [(input_name, input_shape)]
# b = torch.tensor([3.0, 4.0])

### Converting the pytorch model to TorchScript
scripted_model = torch.jit.trace(model, input_data).eval()

@tvm.tir.transform.prim_func_pass(opt_level=3)
def print_tir(f, mod, ctx):
    print("Hello------")
    print(f)

### Converting TorchScript to Relay Graph/IR
mod, params = relay.frontend.from_pytorch(scripted_model, input_infos=[(input_name, input_shape)])
# print(mod["main"])		# Prints the Relay IR of the model
print(mod.astext())

# mod = transform.AnnotateTarget(["ccompiler"])(mod)
# mod = transform.MergeCompilerRegions()(mod)
# mod = transform.PartitionGraph()(mod)
# print(mod.astext())
### Compiling the Relay Graph/IR for specified target riscv64
target = tvm.target.Target("llvm")
# target = tvm.target.Target("ccompiler")
with tvm.transform.PassContext(opt_level=3):
# with tvm.transform.PassContext(opt_level=3, config={"tir.add_lower_pass": [(1, print_tir)]}):
    lib = relay.build(mod, target=target, params=params)
	# lib = relay.build(mod, target="c", params=params, runtime=Runtime("crt", {"system-lib": True}), executor=Executor("aot", {"link-params": True}))
# print(lib.get_lib().get_source())		# Prints the LLVM IR of the model


# tvm.micro.export_model_library_format(lib, "lower.tar")
# ### Running the model
device = tvm.cpu(0)
m = graph_executor.GraphModule(lib["default"](device))
m.set_input(input_name, input_data)
m.run()
tvm_output = m.get_output(0)
print(tvm_output)