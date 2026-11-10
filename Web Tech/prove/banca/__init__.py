"""La banca delle domande: un modulo per capitolo della dispensa.

Ogni modulo `cNN_*.py` definisce la lista `DOMANDE`. Per aggiungere domande
basta scriverle in uno di questi file (o in un file nuovo con lo stesso
schema di nome): vengono raccolte da sole.
"""

import importlib
import pkgutil

DOMANDE = []
for _modulo in sorted(m.name for m in pkgutil.iter_modules(__path__) if m.name[:1] == "c"):
    DOMANDE.extend(importlib.import_module(__name__ + "." + _modulo).DOMANDE)

_visti = {}
for _d in DOMANDE:
    if _d.id in _visti:
        raise ValueError("identificatore di domanda ripetuto: %r" % _d.id)
    _visti[_d.id] = _d
