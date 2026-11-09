"""Rule order at two history levels. ORDER is v1's frozen 27 rules: their suites and data replay here as regressions, and their checkpoints stay in v1.
V2_ORDER is this run's atomic changes; a change is added only when it is declared. ALL is the replay order for suites, reviews and dispositions."""
ORDER = ['R01-HQ06-PI012', 'R02-HQ01-GOV015', 'R03-HQ02-RUN021', 'R04-HQ03-DEP003', 'R05-HQ04-GOV017', 'R06-HQ05-DEP025', 'R07-81-SWAGGER', 'R08-82-K0CPM', 'R09-83-K1PERF', 'R10-84-L0MIGR',
         'R11-87-CUSTOMSETTINGS', 'R12-87-K1LOCALDB', 'R13-87-TESTPRIORITY', 'R14-87-LANGVERSION', 'R15-85-HTTPTIMEOUT', 'R16-86-L1LIVENESS', 'R17-87-SECSCAN', 'R18-87-FASTSLOW', 'R19-87-CIUPDATES',
         'R20-92-K0DESER', 'R21-10-NEWCLAUSES', 'R22-111-TRIGGER', 'R23-112-MIXED', 'R24-113-LIMITS', 'R25-COR103', 'R26-DATASET', 'R27-FINAL']

# Candidates whose template a v1 rule touched. Kept for reference.
TEMPLATE_SCOPE = {'R02-HQ01-GOV015': ['M', 'M1', 'L0', 'L1', 'K0', 'K1'], 'R03-HQ02-RUN021': ['M', 'M1', 'L0', 'L1', 'K0', 'K1'], 'R04-HQ03-DEP003': ['M', 'M1', 'L0', 'L1', 'K0', 'K1'],
                  'R05-HQ04-GOV017': ['M', 'M1', 'L0', 'L1', 'K0', 'K1'], 'R06-HQ05-DEP025': ['M', 'M1', 'L0', 'L1', 'K0', 'K1'], 'R07-81-SWAGGER': ['M', 'M1', 'L0', 'L1', 'K0', 'K1'],
                  'R08-82-K0CPM': ['K0'], 'R09-83-K1PERF': ['K1'], 'R10-84-L0MIGR': ['L0'], 'R11-87-CUSTOMSETTINGS': ['L0', 'K0', 'K1'], 'R12-87-K1LOCALDB': ['K1']}

V2_ORDER = ['V0-BASELINE-REPLAY', 'C01-CPM-EFFECTIVE', 'C02-RUN008-EVIDENCE', 'C03-WF019-EXCEPTION', 'C04-GIT-CONDITIONAL', 'C05-PI012-RESIDUAL', 'C06-REVIEW-SETS', 'C06B-R22-APPLICABILITY', 'C07-PARITY-CLOSE']

ALL = ORDER + V2_ORDER
