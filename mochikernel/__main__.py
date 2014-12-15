from IPython.kernel.zmq.kernelapp import IPKernelApp
from .mochikernel import MochiKernel
IPKernelApp.launch_instance(kernel_class=MochiKernel)
