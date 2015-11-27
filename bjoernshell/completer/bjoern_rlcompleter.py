import readline


class BjoernCompleter(object):
    def __init__(self, bjoern_client):
        self.bjoern_client = bjoern_client
        self.context = None
        self.matches = None
        readline.set_completer_delims(".)(}{")

    def complete(self, text, state):
        if state == 0:
            self.set_context(text)
            if self.context == 'groovy':
                self.matches = self._get_groovy_matches(text)
            elif self.context == 'gremlin':
                self.matches = self._get_gremlin_matches(text)
            else:
                self.matches = []

        try:
            return self.matches[state]
        except IndexError:
            return None

    def set_context(self, text):
        line = readline.get_line_buffer()

        for c in reversed(line):
            if c in '.':
                self.context = "gremlin"
                return
            if c in ')}':
                self.context = "complete"
                return
            elif c in '({':
                self.context = "groovy"
                return

        self.context = "groovy"

    def _get_groovy_matches(self, text):
        variables = self._get_groovy_variables_matches(text)
        return variables

    def _get_gremlin_matches(self, text):
        steps = self._get_gremlin_step_matches(text)
        return steps

    def _get_groovy_variables_matches(self, text):
        total = self.bjoern_client.get_variables()
        return [match for match in total if match.startswith(text)]

    def _get_gremlin_step_matches(self, text):
        total = self.bjoern_client.get_stepnames()
        return [match for match in total if match.startswith(text)]
