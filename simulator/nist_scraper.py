"""
build_component_db.py

Pulls component data from the `thermo` library and writes component_db.py.

Units we need:
  MW        kg/kmol
  Tb, Tc    K
  Pc        bar
  Cp_liq    kJ/kmol/K
  Cp_vap    kJ/kmol/K
  Hvap      kJ/kmol
  antoine   (A, B, C) for log10(P_bar) = A - B / (T_K + C)

Run:
  pip install thermo
  python build_component_db.py
"""

from thermo import Chemical

COMPONENTS_TO_SCRAPE = [
    "water", "hydrogen", "oxygen", "nitrogen", "carbon dioxide", "carbon monoxide", "hydrogen chloride", "hydrogen fluoride", "hydrogen cyanide", "phosgene", "sulfur trioxide", "silicon tetrachloride", "trichlorosilane", "trimethylsilane", "hexamethyldisiloxane", "tetraethyl orthosilicate",
    "methane", "ethane", "propane", "n-butane", "n-pentane",
    "n-hexane", "n-heptane", "n-octane", "n-nonane", "n-decane",
    "benzene", "toluene", "p-xylene", "o-xylene", "m-xylene",
    "ethylene", "propylene", "1-butene", "2-butene", "isobutylene",
    "1-pentene", "1-hexene", "1-octene", "styrene", "ethylbenzene",
    "cumene", "naphthalene", "tetralin", "decalin", "indane",
    "isobutane", "isopentane", "neopentane", "isohexane", "2-methylpentane",
    "3-methylpentane", "2-methylhexane", "3-methylhexane", "isooctane", "cyclohexane",
    "methylcyclohexane", "cyclopentane", "methylcyclopentane", "ethylcyclohexane", "decahydronaphthalene",
    "methanol", "ethanol", "1-propanol", "2-propanol", "1-butanol",
    "2-butanol", "isobutanol", "tert-butanol", "1-pentanol", "1-hexanol",
    "ethylene glycol", "propylene glycol", "glycerol", "benzyl alcohol", "cyclohexanol",
    "acetone", "methyl ethyl ketone", "methyl isobutyl ketone", "cyclohexanone", "acetophenone",
    "diethyl ketone", "methyl propyl ketone", "diisobutyl ketone", "isophorone", "benzophenone",
    "acetic acid", "formic acid", "propionic acid", "butyric acid", "valeric acid",
    "acrylic acid", "benzoic acid", "oxalic acid", "adipic acid", "lactic acid",
    "methyl acetate", "ethyl acetate", "n-propyl acetate", "n-butyl acetate", "isobutyl acetate",
    "ethyl formate", "vinyl acetate", "ethyl acrylate", "methyl acrylate", "dimethyl phthalate",
    "formaldehyde", "acetaldehyde", "propionaldehyde", "butyraldehyde", "benzaldehyde",
    "furfural", "acrolein", "crotonaldehyde", "glyoxal", "glutaraldehyde",
    "diethyl ether", "diisopropyl ether", "tetrahydrofuran", "1,4-dioxane", "methyl tert-butyl ether",
    "ethylene oxide", "propylene oxide", "furan", "anisole", "diphenyl ether",
    "chloromethane", "dichloromethane", "chloroform", "carbon tetrachloride", "1,2-dichloroethane",
    "1,1,1-trichloroethane", "trichloroethylene", "tetrachloroethylene", "chlorobenzene", "o-dichlorobenzene",
    "bromethane", "bromoform", "carbon tetrabromide", "bromobenzene", "iodobenzene",
    "methylamine", "dimethylamine", "trimethylamine", "ethylamine", "diethylamine",
    "triethylamine", "aniline", "pyridine", "piperidine", "morpholine",
    "acetonitrile", "propionitrile", "acrylonitrile", "benzonitrile", "caprolactam",
    "nitromethane", "nitrobenzene", "nitroethane", "n-nitropropane", "o-nitrotoluene",
    "water", "hydrogen peroxide", "ammonia", "hydrazine", "hydroxylamine",
    "sulfuric acid", "nitric acid", "hydrochloric acid", "phosphoric acid", "acetic anhydride",
    "carbon disulfide", "dimethyl sulfoxide", "dimethyl sulfide", "diethyl sulfide", "thiophene",
    "hydrogen sulfide", "sulfur dioxide", "carbon monoxide", "carbon dioxide", "nitrogen",
    "oxygen", "hydrogen", "argon", "helium", "chlorine",
    "hydrogen chloride", "hydrogen fluoride", "hydrogen cyanide", "phosgene", "sulfur trioxide",
    "silicon tetrachloride", "trichlorosilane", "trimethylsilane", "hexamethyldisiloxane", "tetraethyl orthosilicate",
    "methyl chloride", "ethyl chloride", "allyl chloride", "epichlorohydrin", "vinylidene chloride",
    "dimethylformamide", "dimethylacetamide", "n-methyl-2-pyrrolidone", "acetamide", "urea",
    "ethylene diamine", "hexamethylenediamine", "monoethanolamine", "diethanolamine", "triethanolamine",
    "maleic anhydride", "phthalic anhydride", "succinic anhydride", "propionic anhydride", "butyric anhydride",
    "phenol", "cresol", "resorcinol", "catechol", "bisphenol a",
    "aniline", "diphenylamine", "n-methylaniline", "toluidine", "naphthylamine",
    "methyl methacrylate", "ethyl methacrylate", "butyl methacrylate", "methyl acrylate", "hydroxyethyl methacrylate",
    "isoprene", "butadiene", "chloroprene", "cyclopentadiene", "dicyclopentadiene",
]


def get_antoine(chem: Chemical) -> tuple | None:
    """
    Pull Antoine coefficients with base=10.
    Prefers ANTOINE_POLING, falls back to others converted to base 10.
    Returns (A, B, C) for log10(P_bar) = A - B / (T_K + C)
    """
    params = chem.VaporPressure.Antoine_parameters

    # Prefer base-10 source
    for source in ["ANTOINE_POLING", "ANTOINE_WEBBOOK", "LANDOLT"]:
        if source not in params:
            continue
        p = params[source]
        A, B, C = p["A"], p["B"], p["C"]
        base = p["base"]

        # Convert to base 10 if needed
        import math
        if abs(base - 10.0) > 0.01:
            A = A / math.log(10)
            B = B / math.log(10)
            # C is a temperature shift — no conversion needed

        # NIST Antoine is often in Pa or mmHg — figure out pressure units
        # Test at Tb: log10(P_sat) should ≈ log10(1.01325) ≈ 0.0055 for bar
        # or log10(101325) ≈ 5.0 for Pa, or log10(760) ≈ 2.88 for mmHg
        Tb = chem.Tb
        if Tb is None:
            return (round(A, 5), round(B, 4), round(C, 4))

        log_p_test = A - B / (Tb + C)

        # Detect units and convert A to give bar
        if log_p_test > 4.0:           # likely Pa: subtract log10(1e5)
            A = A - 5.0
        elif log_p_test > 2.0:         # likely mmHg: subtract log10(750.06)
            A = A - 2.8751

        return (round(A, 5), round(B, 4), round(C, 4))

    return None


def scrape(name: str) -> dict | None:
    print(f"  {name}...", end=" ", flush=True)
    try:
        c = Chemical(name)

        # thermo returns J/kg/K for Cp and J/kg for Hvap
        # Convert to kJ/kmol/K and kJ/kmol: value * MW / 1000
        MW = c.MW
        Cp_liq = round(c.Cpl * MW / 1000, 2) if c.Cpl else None
        Cp_vap = round(c.Cpg * MW / 1000, 2) if c.Cpg else None

        # Light gases may not have Hvap at 298K — evaluate at Tb instead
        if c.Hvap:
            Hvap = round(c.Hvap * MW / 1000, 1)
        elif c.Tb:
            hvap_at_Tb = c.EnthalpyVaporization(c.Tb)
            Hvap = round(hvap_at_Tb * MW / 1000, 1) if hvap_at_Tb else None
        else:
            Hvap = None

        # Pc: thermo gives Pa → bar
        Pc = round(c.Pc / 1e5, 4) if c.Pc else None

        antoine = get_antoine(c)

        data = {
            "mw":      round(c.MW, 4),
            "Tb":      round(c.Tb, 3) if c.Tb else None,
            "Tc":      round(c.Tc, 3) if c.Tc else None,
            "Pc":      Pc,
            "omega":   round(c.omega, 4) if c.omega else None,
            "Cp_liq":  Cp_liq,
            "Cp_vap":  Cp_vap,
            "Hvap":    Hvap,
            "antoine": antoine,
        }

        missing = [k for k, v in data.items() if v is None]
        if missing:
            print(f"⚠️  missing: {missing}")
        else:
            print("✅")

        return data

    except Exception as e:
        print(f"❌  {e}")
        return None


def write_db(results: dict):
    lines = [
        '"""',
        'component_db.py — auto-generated by build_component_db.py',
        'Source: thermo library (Caleb Bell), DIPPR / NIST data',
        '',
        'Antoine:  log10(P_sat [bar]) = A - B / (T [K] + C)',
        'Cp:       kJ/kmol/K',
        'Hvap:     kJ/kmol',
        'Pc:       bar',
        'Tb, Tc:   K',
        '"""',
        '',
        'from simulator import Component',
        '',
        'component_db = {',
    ]

    for name, d in results.items():
        if d is None:
            lines.append(f'    # "{name}": scrape failed')
            continue
        lines.append(f'    "{name}": Component(')
        lines.append(f'        name="{name}",')
        for key in ["mw", "Tb", "Tc", "Pc", "omega", "Cp_liq", "Cp_vap", "Hvap", "antoine"]:
            lines.append(f'        {key}={d[key]},')
        lines.append('    ),')

    lines.append('}')
    lines.append('')

    with open("component_db.py", "w") as f:
        f.write("\n".join(lines))

    print("\n✅  Written to component_db.py")


if __name__ == "__main__":
    print("Building component database from thermo library")
    print("=" * 50)

    results = {}
    for name in COMPONENTS_TO_SCRAPE:
        results[name] = scrape(name)

    write_db(results)

    success = sum(1 for v in results.values() if v is not None)
    print(f"Done: {success}/{len(COMPONENTS_TO_SCRAPE)} components scraped successfully.")