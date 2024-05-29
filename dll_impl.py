import ctypes
from ctypes import *
import time

class RECT(Structure):
			_fields_ = [('left', c_int), ('top', c_int), ('right', c_int), ('bottom', c_int)]
                     
class LogonPara(Structure):
    LEN_16 = 16
    LEN_32 = 32
    LEN_64 = 64
    _fields_ = [
        ("iSize", c_int),
        ("cProxy", c_char * LEN_32),
        ("cNvsIP", c_char * LEN_32),
        ("cNvsName", c_char * LEN_32),
        ("cUserName", c_char * LEN_16),
        ("cUserPwd", c_char * LEN_16),
        ("cProductID", c_char * LEN_32),
        ("iNvsPort", c_int),
        ("cCharSet", c_char * LEN_32),
        ("cAccontName", c_char * LEN_16),
        ("cAccontPasswd", c_char * LEN_16),
        ("cNvsIPV6", c_char * LEN_64),
        ("iClientType", c_int),
        ("cPlatFeature", c_char * LEN_32)
    ]
class SetPtz(Structure):
    _fields_ = [
        ("iSize", c_int),
        ("iType", c_int),
        ("iPan", c_int),
        ("iTilt", c_int),
        ("iZoom", c_int)
    ]
class DLL:
    def __init__(self):
        self.dll_path=r"C:\Users\hp\Documents\algorithm_its\dll\NVSSDK.dll"
        self.dll = ctypes.windll.LoadLibrary(self.dll_path)
        dll_startup = self.dll.NetClient_Startup_V4
        self.ip = b'192.168.1.2'
        self.cIP = ctypes.c_char_p(self.ip)
        self.cUserName =ctypes.c_char_p(b'admin')
        self.cPassword = ctypes.c_char_p(b'vinayan@123')
        self.port=ctypes.c_int(3000)
        dll_startup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        nSet = dll_startup(3000, 6000, 0)
        print(nSet)
        
    def logon(self, charset="UTF-8"):
        ip=b'192.168.1.2'
        username=b'admin'
        password=b'vinayan@123'
        port=3000
        # Define the SERVER_NORMAL constant
        SERVER_NORMAL = 0  # Replace with the actual value if different

        # Create and initialize the LogonPara structure
        logon_para = LogonPara()
        logon_para.iSize = sizeof(LogonPara)
        logon_para.cNvsIP = ip
        logon_para.cUserName = username
        logon_para.cUserPwd = password
        logon_para.iNvsPort = port
        logon_para.cCharSet = charset.encode('utf-8')

        # Define the prototype of the NetClient_Logon_V4 function
        self.dll.NetClient_Logon_V4.argtypes = [c_int, POINTER(LogonPara), c_int]
        self.dll.NetClient_Logon_V4.restype = c_int

        # Call the function
        iBufLen = sizeof(LogonPara)
        self.dllLogOnSet = self.dll.NetClient_Logon_V4(SERVER_NORMAL, byref(logon_para), iBufLen)

        print('Logon id is: ', self.dllLogOnSet)    # if logon id < 0 connection failed otherwise success.
        print(type(self.dllLogOnSet))

        time.sleep(2)

        dllGetLogonStatus = self.dll.NetClient_GetLogonStatus
        dllGetLogonStatus.argtypes = [c_int]
        dllGetSet = dllGetLogonStatus(self.dllLogOnSet)

        print('Logon Status is: ', dllGetSet, '(0 and 1 are both normal)')   # (Both 0 and 1 are normal)
        if dllGetSet in [0, 1]:  # Add condition for both normal statuses
            return self.dllLogOnSet
        else:
            return None
    def send_ptz_command(self):
        logon_id=self.dllLogOnSet
        ptz_type=1
        pan=1200
        tilt=150
        zoom=23000

        # max 2300, its 100x of dashboard zoom



        tSetPtz = SetPtz()
        tSetPtz.iSize = sizeof(SetPtz)
        tSetPtz.iType = ptz_type
        tSetPtz.iPan = pan
        tSetPtz.iTilt = tilt
        tSetPtz.iZoom = zoom

        COMMAND_ID_SET_PTZ = 73  # Replace with the actual command ID

        self.dll.NetClient_SendCommand.argtypes = [c_int, c_int, c_int, POINTER(SetPtz), c_int]
        self.dll.NetClient_SendCommand.restype = c_int

        iRet = self.dll.NetClient_SendCommand(logon_id, COMMAND_ID_SET_PTZ, 0, byref(tSetPtz), sizeof(SetPtz))
        print(iRet)

dll=DLL()
dll.logon()
dll.send_ptz_command()