"""Evidence dispositions for R04-HQ03-DEP003. Generated from a reviewed mapping, kept as literal data."""
DISPOSITIONS = [
{
"candidate": "K0",
"path": ".claude/scripts/check-dependencies.cjs",
"start_line": 166,
"end_line": 170,
"disposition": "REWORDED",
"new_quote": "ManagePackageVersionsCentrally must be true",
"note": "Function signature gained the exception list; the CPM check text is unchanged at this rule",
"n_records": 4,
"keys": [
"FG-K0-36395ffe06",
"FG-K0-641844cc06",
"FG-K0-8aea50ed37",
"FG-K0-b59fc319ae"
]
},
{
"candidate": "K0",
"path": ".claude/scripts/check-dependencies.cjs",
"start_line": 171,
"end_line": 183,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 2,
"keys": [
"FG-K0-6d818b0488",
"FG-K0-a07875dec8"
]
},
{
"candidate": "K0",
"path": ".claude/scripts/check-dependencies.cjs",
"start_line": 193,
"end_line": 197,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 3,
"keys": [
"FG-K0-6d818b0488",
"FG-K0-a07875dec8",
"FG-K0-6eb6f9d717"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/check-manifests.cjs",
"start_line": 99,
"end_line": 104,
"disposition": "REWORDED",
"new_quote": "ManagePackageVersionsCentrally is not enabled",
"note": "Findings seed gained exception problems; CPM check unchanged",
"n_records": 3,
"keys": [
"FG-K1-25602ccfaf",
"FG-K1-5db7bc1f73",
"FG-K1-ad9966e3b7"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/check-manifests.cjs",
"start_line": 105,
"end_line": 115,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 2,
"keys": [
"FG-K1-877ef8d914",
"FG-K1-91cade62f4"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/check-manifests.cjs",
"start_line": 125,
"end_line": 150,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-K1-5fd760807d"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/check-manifests.cjs",
"start_line": 137,
"end_line": 146,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-K1-4a6d4edee1"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/classify-command.cjs",
"start_line": 237,
"end_line": 249,
"disposition": "REWORDED",
"new_quote": "npmSpecIsRecorded",
"note": "npm version gate honors a recorded explicit request; peer-bypass finding unchanged",
"n_records": 1,
"keys": [
"FG-K1-891a447fdc"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/classify-command.cjs",
"start_line": 242,
"end_line": 251,
"disposition": "REWORDED",
"new_quote": "npmSpecIsRecorded",
"note": "npm version gate honors a recorded explicit request; peer-bypass finding unchanged",
"n_records": 5,
"keys": [
"FG-K1-70713e9a0a",
"FG-K1-23a2f5e23c",
"FG-K1-b0cc0892a5",
"FG-K1-b8551d715e",
"FG-K1-e32ee646e0"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/classify-command.cjs",
"start_line": 245,
"end_line": 249,
"disposition": "REWORDED",
"new_quote": "npmSpecIsRecorded",
"note": "npm version gate honors a recorded explicit request; peer-bypass finding unchanged",
"n_records": 2,
"keys": [
"FG-K1-b8551d715e",
"FG-K1-e32ee646e0"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/classify-command.cjs",
"start_line": 263,
"end_line": 314,
"disposition": "REWORDED",
"new_quote": "recordedVersion",
"note": "NuGet floating branch honors a recorded explicit request; other logic unchanged",
"n_records": 1,
"keys": [
"FG-K1-c626df3b1f"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/classify-command.cjs",
"start_line": 308,
"end_line": 313,
"disposition": "REWORDED",
"new_quote": "recordedVersion",
"note": "NuGet floating branch honors a recorded explicit request; other logic unchanged",
"n_records": 2,
"keys": [
"FG-K1-b8551d715e",
"FG-K1-e32ee646e0"
]
},
{
"candidate": "K1",
"path": ".claude/scripts/classify-command.cjs",
"start_line": 308,
"end_line": 315,
"disposition": "REWORDED",
"new_quote": "recordedVersion",
"note": "NuGet floating branch honors a recorded explicit request; other logic unchanged",
"n_records": 2,
"keys": [
"FG-K1-b8551d715e",
"FG-K1-e32ee646e0"
]
},
{
"candidate": "L0",
"path": ".claude/hooks/manifest-checks.mjs",
"start_line": 309,
"end_line": 316,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Version check honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-L0-f02a237ee7"
]
},
{
"candidate": "L0",
"path": ".claude/hooks/manifest-checks.mjs",
"start_line": 326,
"end_line": 330,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-L0-4b6db2676f"
]
},
{
"candidate": "L0",
"path": ".claude/hooks/manifest-checks.mjs",
"start_line": 326,
"end_line": 344,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-L0-3708d5cfe2"
]
},
{
"candidate": "L0",
"path": ".claude/hooks/manifest-checks.mjs",
"start_line": 328,
"end_line": 330,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-L0-bd31e51536"
]
},
{
"candidate": "L1",
"path": ".claude/hooks/post-change-checks.mjs",
"start_line": 68,
"end_line": 78,
"disposition": "REWORDED",
"new_quote": "ManagePackageVersionsCentrally must stay true",
"note": "Signature gained the exception list; CPM check unchanged",
"n_records": 3,
"keys": [
"FG-L1-461eaf8b76",
"FG-L1-759ea3374d",
"FG-L1-f2ee786a8d"
]
},
{
"candidate": "L1",
"path": ".claude/hooks/post-change-checks.mjs",
"start_line": 80,
"end_line": 92,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 2,
"keys": [
"FG-L1-24f8e5d111",
"FG-L1-461eaf8b76"
]
},
{
"candidate": "M",
"path": ".claude/scripts/check-manifests.mjs",
"start_line": 225,
"end_line": 236,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-M-531f4679db"
]
},
{
"candidate": "M",
"path": ".claude/scripts/check-manifests.mjs",
"start_line": 230,
"end_line": 236,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 2,
"keys": [
"FG-M-8494a3058e",
"FG-M-9cfaa31700"
]
},
{
"candidate": "M",
"path": ".claude/scripts/check-manifests.mjs",
"start_line": 329,
"end_line": 342,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-M-531f4679db"
]
},
{
"candidate": "M1",
"path": ".claude/scripts/check-manifests.js",
"start_line": 115,
"end_line": 133,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-M1-29f43fdad5"
]
},
{
"candidate": "M1",
"path": ".claude/scripts/check-manifests.js",
"start_line": 124,
"end_line": 131,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 2,
"keys": [
"FG-M1-6b989baa85",
"FG-M1-a740c4fdf7"
]
},
{
"candidate": "M1",
"path": ".claude/scripts/check-manifests.js",
"start_line": 144,
"end_line": 165,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-M1-68952da4f0"
]
},
{
"candidate": "M1",
"path": ".claude/scripts/check-manifests.js",
"start_line": 149,
"end_line": 151,
"disposition": "REWORDED",
"new_quote": "approvedVersionException",
"note": "Floating branch honors a recorded explicit request, default rejection unchanged",
"n_records": 1,
"keys": [
"FG-M1-6b989baa85"
]
},
{
"candidate": "M1",
"path": ".claude/skills/add-dependency/SKILL.md",
"start_line": 41,
"end_line": 49,
"disposition": "REWORDED",
"new_quote": "names the package and the version or range",
"note": "M1 text aligned: floating versions now share the explicit exception, as in the other five",
"n_records": 2,
"keys": [
"FG-M1-a740c4fdf7",
"FG-M1-61e68465cf"
]
},
{
"candidate": "M1",
"path": ".claude/skills/add-dependency/SKILL.md",
"start_line": 43,
"end_line": 49,
"disposition": "REWORDED",
"new_quote": "names the package and the version or range",
"note": "M1 text aligned: floating versions now share the explicit exception, as in the other five",
"n_records": 1,
"keys": [
"FG-M1-6b989baa85"
]
},
{
"candidate": "M1",
"path": ".claude/skills/add-dependency/SKILL.md",
"start_line": 49,
"end_line": 49,
"disposition": "REWORDED",
"new_quote": "names the package and the version or range",
"note": "M1 text aligned: floating versions now share the explicit exception, as in the other five",
"n_records": 1,
"keys": [
"FG-M1-3eef13fe55"
]
}
]
