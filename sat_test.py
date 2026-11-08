import sys
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

# src: https://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments
if len(sys.argv) < 2:
    # src: https://pysathq.github.io/docs/html/api/examples/rc2.html
    wcnf = WCNF(from_file='formula.wcnf.xz')
else:
    # src: https://pysathq.github.io/docs/html/api/examples/rc2.html
    wcnf = WCNF(from_file=sys.argv[1])

# code from PySAT example
with RC2(wcnf) as rc2:
    for m in rc2.enumerate():
        print('model {0} has cost {1}'.format(m, rc2.cost))
