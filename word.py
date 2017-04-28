class Word(object):
    """
    Format the word data into adequate format for hashing process.
    """
    def __init__(self, word):
        self.word = word
        self.formats = set()  # Set to avoid equal values
        self.formats.add(self._to_lower())
        self.formats.add(self._to_upper())
        self.formats.add(self._to_alpha())

    def _to_lower(self):
        return self.word.lower()

    def _to_upper(self):
        return self.word.upper()

    def _to_alpha(self):
        return self.word[0:1].upper() + self.word[1:].lower()
