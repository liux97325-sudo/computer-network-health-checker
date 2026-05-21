import ctypes
import socket
import threading
import time
from ctypes import wintypes


APP_TITLE = "电脑网络健康情况检测"
HEADER_TEXT = "电脑网络连接检测"
READY_TEXT = "准备就绪"
BUTTON_TEXT = "点击开始检测"
DETECTING_TEXT = "AI大模型智能检测中"
ONLINE_TEXT = "这不是有网么笨蛋"
OFFLINE_TEXT = "没网你检测个毛线"
DETECTION_SECONDS = 15


user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
comctl32 = ctypes.windll.comctl32
kernel32 = ctypes.windll.kernel32

kernel32.GetModuleHandleW.restype = wintypes.HMODULE
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HWND,
    wintypes.HANDLE,
    wintypes.HINSTANCE,
    wintypes.LPVOID,
]
user32.CreateWindowExW.restype = wintypes.HWND
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = ctypes.c_longlong
user32.LoadIconW.argtypes = [wintypes.HINSTANCE, wintypes.LPVOID]
user32.LoadIconW.restype = wintypes.HANDLE
user32.LoadCursorW.argtypes = [wintypes.HINSTANCE, wintypes.LPVOID]
user32.LoadCursorW.restype = wintypes.HANDLE
user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.SendMessageW.restype = ctypes.c_longlong
user32.SetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
user32.SetWindowTextW.restype = wintypes.BOOL
user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL
user32.UpdateWindow.argtypes = [wintypes.HWND]
user32.UpdateWindow.restype = wintypes.BOOL
user32.GetMessageW.argtypes = [wintypes.LPVOID, wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = [wintypes.LPVOID]
user32.TranslateMessage.restype = wintypes.BOOL
user32.DispatchMessageW.argtypes = [wintypes.LPVOID]
user32.DispatchMessageW.restype = ctypes.c_longlong
user32.RegisterClassExW.argtypes = [wintypes.LPVOID]
user32.RegisterClassExW.restype = wintypes.ATOM
user32.EnableWindow.argtypes = [wintypes.HWND, wintypes.BOOL]
user32.EnableWindow.restype = wintypes.BOOL
user32.SetTimer.argtypes = [wintypes.HWND, ctypes.c_size_t, wintypes.UINT, wintypes.LPVOID]
user32.SetTimer.restype = ctypes.c_size_t
user32.KillTimer.argtypes = [wintypes.HWND, ctypes.c_size_t]
user32.KillTimer.restype = wintypes.BOOL
user32.PostQuitMessage.argtypes = [ctypes.c_int]
user32.PostQuitMessage.restype = None
gdi32.CreateSolidBrush.restype = wintypes.HBRUSH
gdi32.CreateFontW.restype = wintypes.HANDLE
gdi32.SetBkMode.argtypes = [wintypes.HDC, ctypes.c_int]
gdi32.SetBkMode.restype = ctypes.c_int


WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)


WM_CREATE = 0x0001
WM_DESTROY = 0x0002
WM_COMMAND = 0x0111
WM_TIMER = 0x0113
WM_SETFONT = 0x0030
WM_SETTEXT = 0x000C
WM_CTLCOLORSTATIC = 0x0138
WM_CTLCOLORBTN = 0x0135

WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000
WS_CHILD = 0x40000000
WS_TABSTOP = 0x00010000
WS_CLIPCHILDREN = 0x02000000
BS_PUSHBUTTON = 0x00000000
SS_CENTER = 0x00000001
SS_CENTERIMAGE = 0x00000200
SS_LEFT = 0x00000000
PBS_SMOOTH = 0x01

CW_USEDEFAULT = -2147483648
SW_SHOW = 5
COLOR_WINDOW = 5
DEFAULT_GUI_FONT = 17
IDI_APPLICATION = 32512
IDC_HAND = 32649
IDC_ARROW = 32512

PBM_SETRANGE32 = 0x0400 + 6
PBM_SETPOS = 0x0400 + 2

BUTTON_ID = 1001
TIMER_ID = 2001


class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HANDLE),
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", wintypes.POINT),
    ]


class NativeNetworkHealthApp:
    def __init__(self) -> None:
        self.hinstance = kernel32.GetModuleHandleW(None)
        self.class_name = "NetworkHealthCheckWindow"
        self.hwnd = None
        self.controls = {}
        self.is_running = False
        self.started_at = 0.0
        self.network_ok = False
        self.tick_count = 0
        self.brush_white = gdi32.CreateSolidBrush(0x00FFFFFF)
        self.brush_page = gdi32.CreateSolidBrush(0x00FBF7F5)
        self.font_title = self._create_font(28, 700)
        self.font_body = self._create_font(17, 400)
        self.font_button = self._create_font(20, 700)
        self.font_result = self._create_font(28, 700)
        self.wndproc = WNDPROC(self._wndproc)

    def run(self) -> None:
        self._register_window_class()
        self.hwnd = user32.CreateWindowExW(
            0,
            self.class_name,
            APP_TITLE,
            WS_OVERLAPPEDWINDOW | WS_VISIBLE | WS_CLIPCHILDREN,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            760,
            480,
            None,
            None,
            self.hinstance,
            None,
        )
        user32.ShowWindow(self.hwnd, SW_SHOW)
        user32.UpdateWindow(self.hwnd)

        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def _register_window_class(self) -> None:
        icon = user32.LoadIconW(None, IDI_APPLICATION)
        cursor = user32.LoadCursorW(None, IDC_ARROW)
        wc = WNDCLASSEXW()
        wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
        wc.lpfnWndProc = self.wndproc
        wc.hInstance = self.hinstance
        wc.hIcon = icon
        wc.hCursor = cursor
        wc.hbrBackground = self.brush_page
        wc.lpszClassName = self.class_name
        wc.hIconSm = icon
        user32.RegisterClassExW(ctypes.byref(wc))

    def _build_ui(self, hwnd: wintypes.HWND) -> None:
        comctl32.InitCommonControls()
        self._label("title", HEADER_TEXT, 40, 38, 660, 48, self.font_title, SS_LEFT)
        self._label("subtitle", "点击按钮后将进行 15 秒“严肃”的网络健康分析", 43, 92, 660, 28, self.font_body, SS_LEFT)
        self._label("status", READY_TEXT, 40, 146, 660, 30, self.font_body, SS_CENTER)
        self._button("start", BUTTON_TEXT, 260, 194, 220, 48)
        self._progress("progress", 92, 278, 576, 26)
        self._label("progress_text", "", 40, 314, 660, 28, self.font_body, SS_CENTER)
        self._label("result", "", 40, 362, 660, 48, self.font_result, SS_CENTER | SS_CENTERIMAGE)

    def _label(self, key, text, x, y, w, h, font_handle, style) -> None:
        hwnd = user32.CreateWindowExW(0, "STATIC", text, WS_CHILD | WS_VISIBLE | style, x, y, w, h, self.hwnd, None, self.hinstance, None)
        user32.SendMessageW(hwnd, WM_SETFONT, font_handle, True)
        self.controls[key] = hwnd

    def _button(self, key, text, x, y, w, h) -> None:
        hwnd = user32.CreateWindowExW(
            0,
            "BUTTON",
            text,
            WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_PUSHBUTTON,
            x,
            y,
            w,
            h,
            self.hwnd,
            BUTTON_ID,
            self.hinstance,
            None,
        )
        user32.SendMessageW(hwnd, WM_SETFONT, self.font_button, True)
        self.controls[key] = hwnd

    def _progress(self, key, x, y, w, h) -> None:
        hwnd = user32.CreateWindowExW(0, "msctls_progress32", "", WS_CHILD | WS_VISIBLE | PBS_SMOOTH, x, y, w, h, self.hwnd, None, self.hinstance, None)
        user32.SendMessageW(hwnd, PBM_SETRANGE32, 0, 100)
        user32.SendMessageW(hwnd, PBM_SETPOS, 0, 0)
        self.controls[key] = hwnd

    def _create_font(self, size, weight):
        return gdi32.CreateFontW(
            -size,
            0,
            0,
            0,
            weight,
            False,
            False,
            False,
            1,
            0,
            0,
            5,
            0,
            "Microsoft YaHei UI",
        )

    def _set_text(self, key, text) -> None:
        user32.SetWindowTextW(self.controls[key], text)

    def _start_detection(self) -> None:
        if self.is_running:
            return
        self.is_running = True
        self.started_at = time.monotonic()
        self.network_ok = False
        self.tick_count = 0
        self._set_text("status", "正在连接云端脑补引擎...")
        self._set_text("result", "")
        self._set_text("progress_text", DETECTING_TEXT)
        user32.EnableWindow(self.controls["start"], False)
        user32.SendMessageW(self.controls["progress"], PBM_SETPOS, 0, 0)
        threading.Thread(target=self._check_network, daemon=True).start()
        user32.SetTimer(self.hwnd, TIMER_ID, 45, None)

    def _check_network(self) -> None:
        self.network_ok = has_network_connection()

    def _on_timer(self) -> None:
        elapsed = time.monotonic() - self.started_at
        ratio = min(elapsed / DETECTION_SECONDS, 1.0)
        progress = int(ratio * 100)
        user32.SendMessageW(self.controls["progress"], PBM_SETPOS, progress, 0)

        if ratio < 1.0:
            self.tick_count += 1
            dots = "." * ((self.tick_count // 8) % 4)
            pulse = "▰" * ((self.tick_count // 5) % 4)
            self._set_text("progress_text", f"{DETECTING_TEXT}{dots} {pulse}")
            return

        user32.KillTimer(self.hwnd, TIMER_ID)
        self.is_running = False
        self._set_text("progress_text", "检测完成")
        self._set_text("status", "分析报告已生成")
        self._set_text("result", ONLINE_TEXT if self.network_ok else OFFLINE_TEXT)
        user32.EnableWindow(self.controls["start"], True)

    def _wndproc(self, hwnd, message, wparam, lparam):
        if message == WM_CREATE:
            self.hwnd = hwnd
            self._build_ui(hwnd)
            return 0
        if message == WM_COMMAND and (wparam & 0xFFFF) == BUTTON_ID:
            self._start_detection()
            return 0
        if message == WM_TIMER and wparam == TIMER_ID:
            self._on_timer()
            return 0
        if message in (WM_CTLCOLORSTATIC, WM_CTLCOLORBTN):
            gdi32.SetBkMode(wparam, 1)
            return self.brush_page
        if message == WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0
        return user32.DefWindowProcW(hwnd, message, wparam, lparam)


def has_network_connection() -> bool:
    targets = [
        ("223.5.5.5", 53),
        ("114.114.114.114", 53),
        ("1.1.1.1", 53),
        ("8.8.8.8", 53),
        ("www.baidu.com", 80),
        ("www.microsoft.com", 80),
    ]
    for host, port in targets:
        try:
            with socket.create_connection((host, port), timeout=2.0):
                return True
        except OSError:
            continue
    return False


def main() -> None:
    NativeNetworkHealthApp().run()


if __name__ == "__main__":
    main()
