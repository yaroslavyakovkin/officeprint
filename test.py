from win32 import win32print
import time


printer_name = win32print.GetDefaultPrinter()
default = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
handle = win32print.OpenPrinter(printer_name, default)
while True:
    status = win32print.GetPrinter(handle, 6)['Status']
    job = win32print.EnumJobs(handle, 0, 1, 2)
    if job:
        job = job[0]['Status']
    print("status:", status, '|| job:', job)
    time.sleep(1)
