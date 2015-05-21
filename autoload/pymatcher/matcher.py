import vim, re
from datetime import datetime

def py_matcher():

    items = vim.eval('a:items')
    astr = vim.eval('a:str')
    lowAstr = astr.lower()
    limit = int(vim.eval('a:limit'))
    mmode = vim.eval('a:mmode')
    aregex = int(vim.eval('a:regex'))

    rez = vim.bindeval('s:rez')

    specialChars = ['^','$','.','{','}','(',')','[',']','\\','/','+']

    regex = ''
    if aregex == 1:
        regex = astr
    else:
        if len(lowAstr) == 1:
            c = lowAstr
            if c in specialChars:
                c = '\\' + c
            regex += c
        else:
            for c in lowAstr[:-1]:
                if c in specialChars:
                    c = '\\' + c
                regex += c + '[^' + c + ']*'
            else:
                c = lowAstr[-1]
                if c in specialChars:
                    c = '\\' + c
                regex += c

    res = []
    prog = re.compile(regex)

    if mmode == 'filename-only':
        for line in items:
            lineLower = line

            # get filename via reverse find to improve performance
            slashPos = lineLower.rfind('/')
            if slashPos != -1:
                lineLower = lineLower[slashPos + 1:]

            lineLower = lineLower.lower()
            result = prog.search(lineLower)
            if result:
                scores = []
                scores.append(result.end() - result.start() + 1)
                # scores.append((1 + result.start()) * (result.end() - result.start() + 1))
                scores.append(( len(lineLower) + 1 ) / 100.0)
                scores.append(( len(line) + 1 ) / 1000.0)
                score = 1000.0 / sum(scores)
                res.append((score, line))
    else:
        for line in items:
            lineLower = line.lower()
            result = prog.search(lineLower)
            if result:
                scores = []
                scores.append(result.end() - result.start() + 1)
                scores.append(( len(lineLower) + 1 ) / 100.0)
                score = 1000.0 / sum(scores)
                res.append((score, line))

    sortedlist = sorted(res, key=lambda x: x[0], reverse=True)[:limit]
    sortedlist = [x[1] for x in sortedlist]

    rez.extend(sortedlist)

    vim.command("let s:regex = '%s'" % regex)
