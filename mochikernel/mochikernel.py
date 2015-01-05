from IPython.kernel.zmq.kernelbase import Kernel
import mochi.mochi as mochi
import sys
import io


from io import StringIO
class FifoBuffer(io.TextIOBase):
    def __init__(self):
        self.buf = StringIO()
        self.len = 0

    def read(self):
        """Reads data from buffer"""
        self.buf.seek(0)
        l = self.len
        self.len=0
        res = self.buf.read(l)
        
        self.buf.seek(0)
        return res
        
        

    def write(self, arg):
        self.len = self.len + self.buf.write(arg)

    def peek(self):
        x = self.buf.tell()
        self.buf.seek(0)
        res =  self.buf.read(x)
        self.buf.seek(x)
        return res


class MochiKernel(Kernel):
    implementation = 'Mochi'
    implementation_version = '0.1'
    language = 'python'
    language_version = '0.1'
    language_info = {'mimetype': 'text/x-python','name':'python'}
    banner = "the mochi kernel"

    def __init__(self, *args, **kwargs):
        self.output = FifoBuffer()
        self.error = FifoBuffer()
        # sys.std* are zmqstreams
        # not perfect yet though to use fifo.
        # Shoudl find a way to use zmq stream directly
        self.orig_stdout = sys.stdout
        self.orig_stderr = sys.stderr
        sys.stdout = self.output;
        sys.stderr = self.error;
        mochi.current_output_port = mochi.OutputPort(sys.stdout)
        mochi.current_error_port = mochi.OutputPort(sys.stderr)
        mochi.init()

        super().__init__(*args, **kwargs)

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        mochi.eval_code_block(code)
        if not silent:
            stream_content = {'name': 'stdout', 'text': self.output.read()}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        else:
            pass
            #self.output.read()
        if self.error.peek():
            stream_content = {'name': 'stderr', 'text': self.error.read()}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        else:
            pass
            #self.error.read()


        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MochiKernel)
