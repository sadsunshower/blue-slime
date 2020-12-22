import subprocess, typing

class Profile():
    def __init__(self, command: typing.List[str], console: bool) -> None:
        self._command = command
        self._console = console
        self._underlying = None

    def __str__(self) -> str:
        return f'Profile for {self._command}; console access: {self._console}'

    def run(self) -> None:
        self._underlying = subprocess.Popen(self._command, stdin=subprocess.PIPE, text=True)
    
    def console_allowed(self) -> bool:
        return self._console
    
    def running(self) -> bool:
        if self._underlying is None:
            return False

        ret = self._underlying.poll()
        if ret is not None:
            self._underlying = None
            return False

        return True

    def console(self, line: str) -> None:
        self._underlying.stdin.write(line + '\n')
        self._underlying.stdin.flush()

    def kill(self) -> None:
        self._underlying.send_signal(subprocess.signal.SIGKILL)