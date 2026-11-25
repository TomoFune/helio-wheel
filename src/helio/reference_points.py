"""Unified lookup across the three kinds of "rotate the chart to put
this at 0 deg Aries" reference point this app supports: an individual
catalog star (`stars.STARS`), a GCS group center (`stars.STAR_GROUPS`,
e.g. Orion's belt or the Big Dipper as a single averaged point), or a
deep-sky object (`deep_sky.DEEP_SKY_OBJECTS`, e.g. the Andromeda
Galaxy). Each namespace is small and hand-curated, so keys are assumed
not to collide across them; callers that previously only knew about
`STARS` (cli.py, chart.py, comparison.py) can swap in
`resolve_reference_longitude`/`all_reference_keys` to accept any of
the three without otherwise changing shape.
"""
from __future__ import annotations

from astropy.time import Time

from .deep_sky import DEEP_SKY_OBJECTS, deep_sky_heliocentric_longitude
from .stars import STAR_GROUPS, STARS, group_center_longitude, star_heliocentric_longitude


def all_reference_keys() -> list[str]:
    return sorted(set(STARS) | set(STAR_GROUPS) | set(DEEP_SKY_OBJECTS))


# 「恒星・銀河との合」の表示先を絞り込むための3分類のうち、GCS以外の2つ
# (2026-09-10、「恒星リスト選択はGCS/主要な恒星・銀河/その他の3分類」
# より) -- GCS(8つの起点候補)はJS側で既に別管理(GCS_STAR_KEYS)のため
# ここでは定義しない。「主要」はユーザー提供の恒星の一覧(polock.s223.xrea.comの
# 285星のうち太文字85星などの、星の名前)と既存カタログを突き合わせ、
# 既存カタログに無かった分を追加した上でのキー一覧。
# 「その他」は元の一覧の残り約203星に相当するが、今回はスコープ外
# (JS側で「工事中」表示のプレースホルダーのみ)。
MAJOR_REFERENCE_KEYS: set[str] = {
    # 恒星
    "alderamin", "alpheratz", "alrescha", "mirach", "hamal", "schedar", "tsih",
    "menkar", "algol", "alcyone", "mirfak", "aldebaran", "rigel", "bellatrix",
    "capella", "phact", "mintaka", "elnath", "alnilam", "alnitak", "polaris",
    "betelgeuse", "menkalinan", "mirzam", "alhena", "sirius", "canopus", "castor",
    "pollux", "procyon", "acubens", "dubhe", "merak", "alphard", "regulus",
    "phecda", "megrez", "sex_principal", "thuban", "zosma", "denebola", "alkes",
    "diadem", "vindemiatrix", "gienah", "alchiba", "spica", "arcturus",
    "miaplacidus", "gacrux", "acrux", "alphecca", "zubenelgenubi",
    "zubeneschamali", "lup_principal", "hadar", "rigil_kentaurus", "antares",
    "rasalgethi", "sabik", "rasalhague", "nunki", "vega", "rukbat", "peacock",
    "albireo", "altair", "fawaris", "sualocin", "sadalsuud", "deneb_algedi",
    "sadr", "sadalmelik", "fomalhaut", "deneb", "achernar", "ankaa", "markab",
    "scheat", "quadrans",
    # 銀河・星団
    "andromeda_galaxy", "sunflower_galaxy", "galactic_center",
    "aculeus", "acumen", "facies", "capulus",
}



# 起点の「恒星一覧」に出す星・星団・銀河(2026-11-26、「ないものはいらない」より)。
# polockさん(メルさん)の285星の一覧と同じ内容 -- エンジンには「〜座の主星」など
# 一覧にない星も入っているが(恒星の合の検索などで使う)、起点としては出さない。
ORIGIN_LIST_KEYS: frozenset[str] = frozenset({
    "achernar", "acrux", "acubens", "aculeus", "acumen", "albireo", "alchiba", "alcyone",
    "aldebaran", "alderamin", "alf01_cap", "algedi", "algol", "alhena", "alioth", "alkaid", "alkes",
    "alnair", "alnilam", "alnitak", "alphard", "alphecca", "alpheratz", "alrescha", "altair",
    "andromeda_galaxy", "ankaa", "antares", "ara_principal", "arcturus", "arneb", "atria",
    "beehive_cluster", "bellatrix", "bet01_sgr", "bet02_sgr", "bet_aql", "bet_ara", "bet_ari",
    "bet_boo", "bet_cap", "bet_cas", "bet_cep", "bet_cet", "bet_cmi", "bet_cnc", "bet_col",
    "bet_com", "bet_crb", "bet_crt", "bet_cru", "bet_crv", "bet_cvn", "bet_del", "bet_dra",
    "bet_eri", "bet_her", "bet_lep", "bet_lup", "bet_lyr", "bet_oph", "bet_psc", "bet_sco",
    "bet_tri", "bet_umi", "bet_vir", "betelgeuse", "canopus", "capella", "capulus", "castor",
    "chi_dra", "chi_uma", "cor_caroli", "del_aqr", "del_ari", "del_cas", "del_cen", "del_cma",
    "del_cnc", "del_cru", "del_crv", "del_dra", "del_gem", "del_her", "del_oph", "del_sco",
    "del_sgr", "del_tau", "del_umi", "del_vir", "deneb", "deneb_algedi", "denebola", "diadem",
    "dubhe", "elnath", "eps_aqr", "eps_aur", "eps_boo", "eps_car", "eps_cas", "eps_cma", "eps_cru",
    "eps_crv", "eps_cyg", "eps_del", "eps_gem", "eps_hya", "eps_oph", "eps_peg", "eps_sco",
    "eps_sgr", "eps_tau", "eta_aur", "eta_boo", "eta_cma", "eta_dra", "eta_gem", "eta_lyr",
    "eta_peg", "eta_per", "eta_vir", "f16_tau", "f17_tau", "f19_tau", "f20_tau", "f23_tau",
    "f27_tau", "f28_tau", "f53_eri", "f80_uma", "facies", "fawaris", "fomalhaut", "gacrux",
    "galactic_center", "gam_and", "gam_aql", "gam_aqr", "gam_ari", "gam_boo", "gam_cap", "gam_cep",
    "gam_cma", "gam_cnc", "gam_dra", "gam_eri", "gam_leo", "gam_lib", "gam_lup", "gam_lyr",
    "gam_peg", "gam_sgr", "gam_tau", "gam_umi", "gam_vir", "gienah", "hadar", "hamal", "iot_aur",
    "iot_boo", "iot_car", "iot_dra", "iot_ori", "iot_uma", "iot_vir", "kap02_boo", "kap_ori",
    "kap_per", "kap_sco", "kap_vel", "ksi_and", "ksi_aqr", "ksi_cep", "ksi_cnc", "ksi_dra",
    "ksi_gem", "ksi_per", "ksi_pup", "ksi_uma", "lam_her", "lam_leo", "lam_oph", "lam_ori",
    "lam_sco", "lam_sgr", "lam_uma", "lam_vel", "lam_vir", "lup_principal", "m8_m20_m21", "markab",
    "megrez", "menkalinan", "menkar", "merak", "miaplacidus", "mintaka", "mirach", "mirfak",
    "mirzam", "mizar", "mothallah", "mu_boo", "mu_cep", "mu_dra", "mu_gem", "mu_leo", "mu_peg",
    "mu_sgr", "mu_uma", "naos", "nu01_sgr", "nu_cap", "nu_oph", "nu_sco", "nunki", "ome_her",
    "ome_sgr", "omi01_eri", "omi02_eri", "omi_leo", "peacock", "phact", "phecda", "pi01_cyg",
    "pi03_ori", "pi_sgr", "polaris", "pollux", "praecipua", "procyon", "psi_dra", "pyx_principal",
    "rasalgethi", "rasalhague", "regor", "regulus", "rho_pup", "rigel", "rigil_kentaurus", "rukbat",
    "sabik", "sadalmelik", "sadalsuud", "sadr", "scheat", "schedar", "sex_principal", "sham",
    "sig_dra", "sig_hya", "sig_sco", "sirius", "spica", "sualocin", "tau_sco", "tet01_ser",
    "tet_aqr", "tet_aur", "tet_cen", "tet_leo", "tet_peg", "tet_sco", "thuban", "tsih", "unukalhai",
    "ups02_eri", "vega", "vindemiatrix", "whirlpool_galaxy", "zet_aql", "zet_aur", "zet_cma",
    "zet_dra", "zet_gem", "zet_leo", "zet_peg", "zet_sgr", "zet_tau", "zet_vir", "zosma",
    "zubenelgenubi", "zubeneschamali"
})


def reference_info(key: str) -> dict:
    """The underlying dict for `key`, whichever namespace it's from --
    all three carry at least `label_ja`/`name_en`/`source`."""
    if key in STARS:
        return STARS[key]
    if key in STAR_GROUPS:
        return STAR_GROUPS[key]
    if key in DEEP_SKY_OBJECTS:
        return DEEP_SKY_OBJECTS[key]
    raise KeyError(key)


def resolve_reference_longitude(key: str, t: Time) -> float:
    if key in STARS:
        return star_heliocentric_longitude(key, t)
    if key in STAR_GROUPS:
        return group_center_longitude(key, t)
    if key in DEEP_SKY_OBJECTS:
        return deep_sky_heliocentric_longitude(key, t)
    raise KeyError(key)
