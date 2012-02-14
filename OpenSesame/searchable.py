from collections import defaultdict

MAX_LEN = 13

class Searchable(object):
    def __init__(self, searchables):
        self.searchables = searchables # sorted dict {id:'searchable'}
        self.candidates = [[x for x in self.searchables.keys()]]
        self.string = "" # user search string

    @property
    def candidate_keys(self):
        return self.candidates[len(self.candidates)-1]

    def push(self, char):
        if len(self.string) + 1 < MAX_LEN:
            self.string += char
            self._instant_search()

    def pop(self):
        if len(self.string) > 0:
            self.string = self.string[:len(self.string)-1]
            self.candidates.pop()

    def _instant_search(self):
        """Determine possible keys after a push or pop
        """
        _keys = []
        for k,v in self.searchables.iteritems():
            if self.string in v:
                _keys.append(k)
        self.candidates.append(_keys)

    def best_guess(self):
        """Return the gnomekeyring position of the closest matching
        """
        best_guess_ever = (0, 0) # (key, string)
        points = defaultdict(float)
        points[0] = 0
        if len(self.string) > 0:
            for key in self.candidate_keys:
                guess = self.searchables[key]
                if guess == self.string:
                    points[key] += 100
                    break
                # skip, entry longer then guess
                if len(self.string) > len(guess):
                    continue
                # begins with
                if guess.startswith(self.string):
                    points[key] += 1
                # contained in
                if self.string in guess:
                    points[key] += 1
                # percentage of user search string in best guess
                if points[key] > 0:
                    points[key] += float(len(self.string))/len(guess)
        for k,v in points.iteritems():
            if points[best_guess_ever[0]] < points[k]:
                best_guess_ever = (k, self.searchables[k])
        return best_guess_ever
