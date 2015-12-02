import code
import os
import readline
import sys

from bjoernshell.completer.bjoern_rlcompleter import BjoernCompleter

HISTORY_FILE = "~/.bjoern_history"


class BjoernInteractiveConsole(code.InteractiveConsole):
    def __init__(self, bjoern, locals=None, filename="<console>"):
        super().__init__(locals=locals, filename=filename)
        self.bjoern = bjoern
        self.history_file = os.path.expanduser(HISTORY_FILE)

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            response = self.bjoern.run(source)
        except Exception as e:
            response = str(e)
        if "[MultipleCompilationErrorsException]" in response:
            return True
        self.write(response)
        self.write('\n')
        return False

    def interact(self, host="localhost", port=6000):
        self._load_prompt()
        self._load_banner()
        self._init_readline()
        self._load_history()
        super().interact(self.banner)
        self._save_history()

    def _init_readline(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(BjoernCompleter(self.bjoern).complete)

    def _load_history(self):
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass

    def _save_history(self):
        readline.write_history_file(self.history_file)

    def _load_banner(self):
        base = os.path.dirname(__file__)
        path = "data/banner.txt"
        fname = os.path.join(base, path)
        try:
            with open(fname, 'r') as f:
                self.banner = f.read()
        except:
            self.banner = "bjosh --- bjoern shell\n"
        return self.banner

    def _load_prompt(self):
        prompt = os.getenv("BJOERNPROMPT", "bjoern> ")
        prompt = bytes(prompt, "utf-8").decode("unicode_escape")
        sys.ps1 = prompt
