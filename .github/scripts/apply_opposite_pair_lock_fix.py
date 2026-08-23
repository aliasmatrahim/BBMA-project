from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/P3_INPUT_PARAMETER_UI_MAPPING_AUDIT.md')

s = SOURCE.read_text(encoding='utf-8')

old_header = 'Version 4.5.1 - P3-M2-11.1 Mode2 Diagnostic Closure'
new_header = 'Version 4.5.1 - P3-UI-01 Input Panel Cleanup'
if s.count(old_header) != 1:
    raise SystemExit(f'build header anchor count={s.count(old_header)}')
s = s.replace(old_header, new_header, 1)

# Move the two existing enum types ahead of the input declarations so MT4 can
# render true dropdowns without duplicating enum definitions later in Module 02.
old_trade_enum = 'enum ENUM_TRADE_LOCK { LOCK_OFF, LOCK_SAME_DIRECTION, LOCK_ONE_POSITION };\n'
old_debug_enum = 'enum ENUM_DEBUG_LEVEL { DBG_OFF, DBG_ERROR, DBG_SIGNAL, DBG_TRADE, DBG_FULL };\n'
if s.count(old_trade_enum) != 1 or s.count(old_debug_enum) != 1:
    raise SystemExit('existing TradeLock/Debug enum anchors missing or duplicated')
s = s.replace(old_trade_enum, '', 1)
s = s.replace(old_debug_enum, '', 1)

old_inputs = '''//--- INPUTS
input int      EntryMode                          = 2;          // EntryMode: 1=RE_ENTRY_ONLY, 2=ALL_VALIDATED_BBMA_ENTRIES
input int      TradeLockMode                      = 0;          // TradeLockMode: 0=OFF, 1=SAME_DIRECTION_ONLY, 2=ONE_POSITION
input int      MaxWaitBars_Extreme                = 5;          // MaxWaitBars_Extreme
input int      MaxWaitBars_MLV                    = 5;          // Legacy compatibility only; canonical MHV/MLV has no strategy TTL
input int      MaxWaitBars_CSD                    = 5;          // MaxWaitBars_CSD
input int      MaxWaitBars_ReEntry                = 5;          // MaxWaitBars_ReEntry
input int      MaxWaitBars_Combined               = 5;          // MaxWaitBars_Combined
input int      MaxWaitBars_Global                 = 10;         // MaxWaitBars_Global
input int      MMMode                             = 1;          // MMMode: 1=AutoLot, 2=FixedLot
input double   AutoLotPercent                     = 1.0;        // AutoLotPercent
input double   FixedLot                           = 0.01;       // FixedLot
input double   MaxAutoLot                         = 1.0;        // MaxAutoLot
input double   MaxSpreadPips                      = 10.0;       // MaxSpreadPips
input double   MaxDrawdownPercent                 = 20.0;       // MaxDrawdownPercent
input double   BasketLossPercent                  = 10.0;       // BasketLossPercent
input double   MaxTotalRiskPercent                = 5.0;        // MaxTotalRiskPercent
input double   MinRRRatio                         = 1.5;        // MinRRRatio
input double   MaxSLPips                          = 100.0;      // MaxSLPips
input int      SignalMode                         = 1;          // Deprecated for M15 entry authority; retained for compatibility/display only
input int      ScoreDisplayThresholdManual        = 60;         // Deprecated trading threshold; display compatibility only
input bool     EnableBBShapeEngine                = true;       // EnableBBShapeEngine
input bool     EnableExtremeClassifier            = true;       // EnableExtremeClassifier
input bool     EnableMLVStateEngine               = true;       // EnableMLVStateEngine
input bool     EnableReEntryEngine                = true;       // EnableReEntryEngine
input bool     EnableSignalScoring                = true;       // Optional M18 label metadata only; never gates trading
input bool     EnableRE_Type1                     = true;       // EnableRE_Type1
input bool     EnableRE_Type2                     = true;       // EnableRE_Type2
input bool     EnableRE_Type3                     = true;       // EnableRE_Type3
input bool     EnableRE_Type4                     = true;       // EnableRE_Type4
input string   PairList                           = "EURUSD,USDJPY,GBPUSD,AUDUSD,USDCAD,USDCHF,NZDUSD"; // PairList
input int      MaxActivePair                      = 7;          // MaxActivePair
input int      MaxTradePerPair                    = 2;          // MaxTradePerPair
input int      MaxTotalTrade                      = 10;         // MaxTotalTrade
input double   BasketProfitPercent                = 5.0;        // Display compatibility only; not an execution TP
input bool     ShowDashboard                      = true;       // ShowDashboard
input int      Slippage                           = 3;          // Slippage (points)
input int      MaxRetry                           = 3;          // MaxRetry
input int      BERetryInterval                    = 60;         // BERetryInterval (seconds)
input int      DebugLevel                         = 0;          // DebugLevel: 0=OFF, 1=ERROR, 2=SIGNAL, 3=TRADE, 4=FULL
input int      StrategyID                         = 1;          // StrategyID (1-99)
input int      InstanceID                         = 0;          // InstanceID (0-99)
input int      AllowedExecutionDeviation_MinPoints= 5;          // AllowedExecutionDeviation_MinPoints
'''

new_inputs = '''//--- USER INPUT ENUMS (numeric values preserved for compatibility)
enum ENUM_ENTRY_MODE_INPUT
{
   MODE_1_RE_ENTRY_ONLY          = 1, // Re-Entry only | selective
   MODE_2_ALL_VALIDATED_BBMA     = 2  // RE + REM/RRE/REE | more opportunities
};

enum ENUM_MM_MODE_INPUT
{
   MM_AUTO_LOT                   = 1, // Lot derived from risk %
   MM_FIXED_LOT                  = 2  // Use FixedLot
};

enum ENUM_TRADE_LOCK
{
   LOCK_OFF                      = 0, // No optional live-position lock
   LOCK_SAME_DIRECTION           = 1, // Existing pair trades constrain new direction
   LOCK_ONE_POSITION             = 2  // Max 1 live EA trade / pair
};

enum ENUM_DEBUG_LEVEL
{
   DBG_OFF                       = 0,
   DBG_ERROR                     = 1,
   DBG_SIGNAL                    = 2,
   DBG_TRADE                     = 3,
   DBG_FULL                      = 4
};

//--- 01 TRADING SETUP
input ENUM_ENTRY_MODE_INPUT EntryMode             = MODE_2_ALL_VALIDATED_BBMA; // 01 Trading | Mode 1=RE only, Mode 2=RE+REM/RRE/REE

//--- 02 PAIR SELECTION
input string   PairList                           = "EURUSD,USDJPY,GBPUSD,AUDUSD,USDCAD,USDCHF,NZDUSD"; // 02 Pairs | comma-separated symbols

//--- 03 TRADE LIMITS
input int      MaxTradePerPair                    = 2;          // 03 Limits | max live trades per pair
input int      MaxTotalTrade                      = 10;         // 03 Limits | max total live EA trades
input int      MaxActivePair                      = 7;          // 03 Limits | max pairs active at once

//--- 04 MONEY MANAGEMENT
input ENUM_MM_MODE_INPUT MMMode                   = MM_AUTO_LOT; // 04 Money | AUTO=risk %, FIXED=FixedLot
input double   AutoLotPercent                     = 1.0;        // 04 Money | risk % used by Auto Lot
input double   FixedLot                           = 0.01;       // 04 Money | used only in Fixed Lot mode
input double   MaxAutoLot                         = 1.0;        // 04 Money | hard cap for Auto Lot

//--- 05 TRADE CONTROL
input ENUM_TRADE_LOCK TradeLockMode               = LOCK_OFF;   // 05 Control | OFF / SAME_DIRECTION / ONE_POSITION

//--- 06 RISK PROTECTION
input double   MaxSpreadPips                      = 10.0;       // 06 Risk | reject entry above this spread
input double   MaxDrawdownPercent                 = 20.0;       // 06 Risk | maximum EA drawdown %
input double   BasketLossPercent                  = 10.0;       // 06 Risk | emergency basket-loss %
input double   MaxTotalRiskPercent                = 5.0;        // 06 Risk | maximum total EA risk %

//--- 07 DISPLAY
input bool     ShowDashboard                      = true;       // 07 Display | show chart dashboard

//--- 08 ADVANCED SAFETY / EXECUTION
input double   MinRRRatio                         = 1.5;        // 08 Advanced | minimum accepted Risk:Reward
input double   MaxSLPips                          = 100.0;      // 08 Advanced | maximum accepted SL distance
input int      Slippage                           = 3;          // 08 Advanced | broker slippage in points
input ENUM_DEBUG_LEVEL DebugLevel                 = DBG_OFF;    // 08 Advanced | OFF / ERROR / SIGNAL / TRADE / FULL
input int      StrategyID                         = 1;          // 08 Advanced | strategy identity 1-99
input int      InstanceID                         = 0;          // 08 Advanced | instance identity 0-99

//--- INTERNAL / LOCKED (not shown in MT4 Inputs; defaults preserved)
int            MaxWaitBars_Extreme                = 5;
int            MaxWaitBars_MLV                    = 5;          // Legacy compatibility only; canonical MHV/MLV has no strategy TTL
int            MaxWaitBars_CSD                    = 5;
int            MaxWaitBars_ReEntry                = 5;
int            MaxWaitBars_Combined               = 5;
int            MaxWaitBars_Global                 = 10;
int            SignalMode                         = 1;          // Deprecated compatibility/display only
int            ScoreDisplayThresholdManual        = 60;         // Deprecated display compatibility only
bool           EnableBBShapeEngine                = true;
bool           EnableExtremeClassifier            = true;
bool           EnableMLVStateEngine               = true;
bool           EnableReEntryEngine                = true;
bool           EnableSignalScoring                = true;       // M18 label metadata only; never gates trading
bool           EnableRE_Type1                     = true;
bool           EnableRE_Type2                     = true;
bool           EnableRE_Type3                     = true;
bool           EnableRE_Type4                     = true;
double         BasketProfitPercent                = 5.0;        // Display compatibility only; not execution TP
int            MaxRetry                           = 3;
int            BERetryInterval                    = 60;
int            AllowedExecutionDeviation_MinPoints= 5;
'''

if s.count(old_inputs) != 1:
    raise SystemExit(f'input block anchor count={s.count(old_inputs)}')
s = s.replace(old_inputs, new_inputs, 1)

# Static UI/compatibility invariants.
required = [
    'input ENUM_ENTRY_MODE_INPUT EntryMode',
    'MODE_1_RE_ENTRY_ONLY          = 1',
    'MODE_2_ALL_VALIDATED_BBMA     = 2',
    'input ENUM_MM_MODE_INPUT MMMode',
    'MM_AUTO_LOT                   = 1',
    'MM_FIXED_LOT                  = 2',
    'input ENUM_TRADE_LOCK TradeLockMode',
    'input ENUM_DEBUG_LEVEL DebugLevel',
    'input string   PairList',
    'input int      MaxTradePerPair',
    'input int      MaxTotalTrade',
    'input int      MaxActivePair',
    'int            MaxWaitBars_Extreme                = 5;',
    'bool           EnableReEntryEngine                = true;',
    'int            AllowedExecutionDeviation_MinPoints= 5;'
]
for token in required:
    if token not in s:
        raise SystemExit('missing UI invariant: ' + token)

for hidden in [
    'input int      MaxWaitBars_Extreme',
    'input bool     EnableBBShapeEngine',
    'input bool     EnableReEntryEngine',
    'input int      SignalMode',
    'input double   BasketProfitPercent',
    'input int      MaxRetry',
    'input int      AllowedExecutionDeviation_MinPoints'
]:
    if hidden in s:
        raise SystemExit('internal control still exposed: ' + hidden)

if s.count('enum ENUM_TRADE_LOCK') != 1:
    raise SystemExit('ENUM_TRADE_LOCK duplicate/missing after move')
if s.count('enum ENUM_DEBUG_LEVEL') != 1:
    raise SystemExit('ENUM_DEBUG_LEVEL duplicate/missing after move')
if s.count('{') != s.count('}'):
    raise SystemExit('brace imbalance after UI patch')

SOURCE.write_text(s, encoding='utf-8')

# Append materialization status to the existing audit without changing its
# approved mapping decisions.
a = AUDIT.read_text(encoding='utf-8')
marker = '\n## Patch materialization — P3-UI-01\n'
if marker not in a:
    a += marker + '''\n- Source patch: `P3-UI-01 Input Panel Cleanup`.\n- 15 normal-user inputs retained and ordered by use frequency.\n- 6 Advanced inputs retained at the bottom.\n- fixed-choice EntryMode/MMMode/TradeLockMode/DebugLevel converted to enum dropdown inputs with numeric values preserved.\n- Strategy-Core/lifecycle/deprecated/execution-internal controls removed from the MT4 Inputs window but kept at the same internal defaults.\n- No detector, entry, exit, risk formula, magic generation or BBMA source rule changed.\n- Fresh native MetaEditor `0E0W` is mandatory before this UI build is accepted.\n'''
    AUDIT.write_text(a, encoding='utf-8')
