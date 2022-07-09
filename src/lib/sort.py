# Sort library
from operator import itemgetter

qolang_export = {
    "sortonelist": "sort",
    "sortonelistr": "sortr",
    "sorttwolists": "sortbyval",
    "sorttwolistsr": "sortbyvalr",
}

def sortonelist(Variables, args):
    """
    Sort a list.
    """
    return (Variables, args[0].sort())

def sortonelistr(Variables, args):
    """
    Sort a list, reversed.
    """
    return (Variables, args[0].sort(reverse=True))

def sorttwolists(Variables, args):
    """
    Sort two lists by the values of the second list.
    """
    i = 0
    ddict = dict()
    for var in args[1]:
        ddict[var] = args[0][i]
        i += 1
    ddict = {k: v for k, v in sorted(ddict.items(), key=lambda item: item[0])}
    return (Variables, [ddict.keys(), ddict.values()])

def sorttwolistsr(Variables, args):
    """
    Sort two lists by the values of the second list, reversed.
    """
    i = 0
    ddict = dict()
    for var in args[1]:
        ddict[var] = args[0][i]
        i += 1
    ddict = {k: v for k, v in sorted(ddict.items(), key=lambda item: item[0], reverse=True)}
    return (Variables, [list(ddict.values()), list(ddict.keys())])
