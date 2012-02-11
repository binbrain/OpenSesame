from OpenSesame.searchable import Searchable

def test_searchable():
    items = {1:'a', 2:'ab', 3:'abc', 4:'abcefg', 5:'abcexyz', 6:'abcxyz', 7:'xyz'}
    search = Searchable(items)
    assert(len(search.candidate_keys) == 7)
    search.push('a')
    assert(len(search.candidate_keys) == 6 and 7 not in search.candidate_keys)
    search.pop()
    assert(len(search.candidate_keys) == 7)
    search.push('abce')
    assert(len(search.candidate_keys) == 2)
    search.pop()
    search.push('x')
    assert(search.candidate_keys[0] == 6 and len(search.candidate_keys) == 1)

def test_best_guess():
    items = {1:'a', 2:'ab', 3:'abc', 4:'abcefg', 5:'abcexyz', 6:'abcxyz', 7:'xyz'}
    search = Searchable(items)
    search.string = 'abc'
    assert(search.best_guess()[0] == 3)
    search.string = 'yz'
    assert(search.best_guess()[0] == 7)
    search.string = 'cex'
    assert(search.best_guess()[0] == 5)

    items = {1:'twitter', 2:'witter', 3:'twit', 4:'witt', 5:'ftwitter'}
    search = Searchable(items)
    search.string = 'witte'
    assert(search.best_guess()[0] == 2)
