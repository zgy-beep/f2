"""
输出重定向工具：用于捕获日志输出并重定向到GUI界面
"""

from PyQt5.QtCore import QObject, pyqtSignal


class OutputRedirector(QObject):
    """
    自定义输出重定向器，将日志输出到GUI界面
    """
    outputWritten = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buffer = ""

    def write(self, text):
        if text.strip():  # 忽略空行
            self._buffer += text
            if self._buffer.endswith("\n"):
                self.outputWritten.emit(self._buffer.rstrip())
                self._buffer = ""
        
    def flush(self):
        if self._buffer:
            self.outputWritten.emit(self._buffer)
            self._buffer = ""