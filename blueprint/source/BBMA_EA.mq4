//+------------------------------------------------------------------+
//|                                           BBMA_EA.mq4 |
//| Version 5.2.0 - M06 Complete Indicator Data Validation       |
//|                                           CODE-READY              |
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//|                    CODING COMPLEXITY LIMITER                       |
//|                    =========================                       |
//|                                                                   |
//|  PURPOSE:                                                         |
//|  Prevent unnecessary over-engineering during MQL4 implementation. |
//|                                                                   |
//|  GENERAL RULE:                                                    |
//|  Use the SIMPLEST implementation that fully satisfies this        |
//|  Master Blueprint.                                                |
//|                                                                   |
//|  COMPLEXITY LEVELS:                                               |
//|  BEGINNER        - Direct code. Basic conditions, loops, calc.   |
//|  INTERMEDIATE    - Modular functions. Structs/state only where    |
//|                    required. Normal production-grade EA coding.   |
//|  INTERMEDIATE+   - Stateful, lifecycle or sequence-based logic    |
//|                    allowed. Limited to actual Blueprint req.      |
//|  EXPERT-RESTRICTED- Only where state/risk/execution integrity,    |
//|                    persistence, recovery, lifecycle or orchest-   |
//|                    ration correctness requires it.                |
//|  EXPERT          - Critical execution and recovery infrastructure.|
//|                    Every complex mechanism must have a clear      |
//|                    technical reason.                              |
//|                                                                   |
//|  IMPORTANT: "EXPERT" DOES NOT MEAN "MAXIMUM COMPLEXITY".         |
//+------------------------------------------------------------------+
#property copyright "BBMA EA"
#property link      ""
#property version   "5.20"
#property strict

#define BBMA_BUILD_TAG      "V520_M06_COMPLETE_DATA_20261022"
#define BBMA_SOURCE_REV_TAG "CORE_FIDELITY_292_M06_001_20261022"

//+------------------------------------------------------------------+
//| MODULE 01: HEADER & INPUTS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

//--- USER INPUT ENUMS (numeric values preserved for compatibility)
enum ENUM_ENTRY_MODE_INPUT
{
   MODE_1_RE_ENTRY_ONLY          = 1, // Re-Entry only | selective
   MODE_2_ALL_VALIDATED_BBMA     = 2  // Retest-ready Extreme + RE + REM/RRE/REE
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
input ENUM_ENTRY_MODE_INPUT EntryMode             = MODE_2_ALL_VALIDATED_BBMA; // 01 Trading | Mode 1=RE only, Mode 2=Extreme+RE+REM/RRE/REE

//--- 02 PAIR SELECTION
input string   PairList                           = "EURUSD,GBPUSD,USDJPY,USDCHF,USDCAD,AUDUSD,NZDUSD,EURJPY,GBPJPY,EURGBP,AUDJPY,CADJPY,CHFJPY,NZDJPY,EURAUD,EURCAD,EURCHF,GBPAUD,GBPCAD,AUDCAD"; // 02 Pairs | default 20-pair FX universe

//--- 03 TRADE LIMITS
input int      MaxTradePerPair                    = 2;          // 03 Limits | max live trades per pair
input int      MaxTotalTrade                      = 10;         // 03 Limits | max total live EA trades
input int      MaxActivePair                      = 7;          // 03 Limits | requested max active pairs; runtime caps safely

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
input double   MinRRRatio                         = 0.0;        // 08 Advanced | optional global Min RR filter; 0=disabled
input bool     BlockNMJEConflict                  = true;       // 08 Legacy compatibility | INACTIVE: NMJE is observation-only
input bool     BlockNMJEBuilding                  = true;       // 08 Legacy compatibility | INACTIVE: NMJE is observation-only
input double   MaxSLPips                          = 100.0;      // 08 Advanced | maximum accepted SL distance
input int      Slippage                           = 3;          // 08 Advanced | broker slippage in points
input ENUM_DEBUG_LEVEL DebugLevel                 = DBG_OFF;    // 08 Advanced | OFF / ERROR / SIGNAL / TRADE / FULL
input int      StrategyID                         = 1;          // 08 Advanced | strategy identity 1-99
input int      InstanceID                         = 0;          // 08 Advanced | instance identity 0-99

//--- INTERNAL / LOCKED (not shown in MT4 Inputs; defaults preserved)
int            MaxWaitBars_Extreme                = 5;          // Legacy diagnostic metadata only; no Strategy-Core expiry
int            MaxWaitBars_MLV                    = 5;          // Legacy compatibility only; canonical MHV/MLV has no strategy TTL
int            MaxWaitBars_CSD                    = 5;
int            MaxWaitBars_ReEntry                = 5;          // Legacy diagnostic metadata only; no Strategy-Core expiry
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
// F7/C044 Re-Entry lifecycle reopened by explicit strategy decision 2026-09-04.
// M23/M24 close, checkpoint and restart reconstruction are active for source-backed owners.
bool           EnableC044Lifecycle                = true;
// D1 EXTREME_TPW staged lifecycle. Keep OFF until native/static gates and
// broker/demo restart + close-idempotency validation are complete.
bool           EnableD1TPWLifecycle               = false;
double         BasketProfitPercent                = 5.0;        // Display compatibility only; not execution TP
int            MaxRetry                           = 3;
int            BERetryInterval                    = 60;
int            AllowedExecutionDeviation_MinPoints= 5;

//--- CONSTANTS
#define TIMEFRAME_TREND         1440
#define TIMEFRAME_HIGHER        240
#define TIMEFRAME_MAIN          60
#define TIMEFRAME_LOWER         15
#define BB_PERIOD               20
#define BB_DEVIATION            2
#define MA5_HIGH_PERIOD         5
#define MA10_HIGH_PERIOD        10
#define MA5_LOW_PERIOD          5
#define MA10_LOW_PERIOD         10
#define EMA50_PERIOD            50
#define EXTREME_WICK_BUFFER_PIPS 3.0
#define MAX_PAIRS               40
#define MAX_TRADES_PER_PAIR     20
#define MAX_MONITORED           400
#define NMJE_CF_MAX_CANDIDATES   16
#define NMJE_CF_MAX_ACTIVE_SETS  64
#define RETRY_SLEEP_MS          100
#define TRADE_TIMEOUT           2000
#define MAGIC_BASE              100000
#define SIGNAL_HISTORY_MAX      2000
#define SIGNAL_HISTORY_CLEANUP_SIZE 200
#define PAIR_ID_MIN             1
#define PAIR_ID_MAX             99
#define INSTANCE_ID_MIN         0
#define INSTANCE_ID_MAX         99
#define STRATEGY_ID_MIN         1
#define STRATEGY_ID_MAX         99

//+------------------------------------------------------------------+
//| MODULE 02: ENUMS & STRUCTS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

//--- ENUMS
enum ENUM_SIGNAL_TYPE
{
   SIGNAL_NONE,
   SIGNAL_EXTREME,
   SIGNAL_MHV,
   SIGNAL_MLV,
   SIGNAL_CSD,
   SIGNAL_ECSD,
   SIGNAL_CSM,
   SIGNAL_RE_ENTRY,
   SIGNAL_REM,
   SIGNAL_RRE,
   SIGNAL_REE,
};

enum ENUM_DIRECTION { DIR_NONE, DIR_BUY, DIR_SELL };

enum ENUM_BB_STATE { BB_NONE, BB_SQUEEZE, BB_EXPANDING, BB_CONTRACTING, BB_FLAT };

enum ENUM_MLV_STATE
{
   MLV_NONE,
   MLV_PARENT_READY,
   MLV_TP_COMPLETE,
   MLV_LOSS_DEVELOPING,
   MLV_FORMATION_ESTABLISHED,
   MLV_RETEST_COMPLETE,
   MLV_DIRECTION_TAKEN,
   MLV_VOID,
   MLV_SUPERSEDED
};

enum ENUM_RE_TYPE { RE_NONE, RE_TYPE_1, RE_TYPE_2, RE_TYPE_3_CSM, RE_TYPE_4_CSD };

enum ENUM_RE_STATE { RE_STATE_NONE, RE_STATE_CANDIDATE, RE_STATE_CONFIRMED, RE_STATE_EXPIRED };

enum ENUM_TYPE1_CONTEXT_STATE
{
   TYPE1_CTX_NONE,
   TYPE1_CTX_DIRECTION_OWNER,
   TYPE1_CTX_RANGING
};

enum ENUM_H4_OWNER_STATE
{
   H4_OWNER_RECOVERY_UNRESOLVED,
   H4_OWNER_NONE,
   H4_OWNER_ACTIVE
};

enum ENUM_D1_OWNER_STATE
{
   D1_OWNER_UNRESOLVED,
   D1_OWNER_BUY_CONFIRMED,
   D1_OWNER_SELL_CONFIRMED,
   D1_TRANSITION
};

// D1O-02: user-approved D1 BBMA opportunity execution extension.
enum ENUM_D1_OPPORTUNITY_FAMILY
{
   D1_OPP_NONE,
   D1_OPP_EXTREME_TPW,
   D1_OPP_CSD,
   D1_OPP_RE_ENTRY,
   D1_OPP_MOMENTUM_RETRACE
};

enum ENUM_D1_AUTHORITY_MODE
{
   D1_AUTH_NONE,
   D1_AUTH_STRATEGIC_OWNER,
   D1_AUTH_OPPORTUNITY
};

// N1-03: observation-only nested MTF relationship states.
enum ENUM_NESTED_RELATION
{
   NESTED_NOT_APPLICABLE,
   NESTED_BUILDING,
   NESTED_SUPPORTING,
   NESTED_ALIGNED,
   NESTED_CONFLICT,
   NESTED_UNRESOLVED
};

enum ENUM_NESTED_PARENT_KIND
{
   NESTED_PARENT_NONE,
   NESTED_PARENT_H4_RE,
   NESTED_PARENT_H4_OWNER,
   NESTED_PARENT_D1_RE,
   NESTED_PARENT_D1_OWNER
};

// Q9 NMJE V2 P4+ categorical observer metadata. Enum ordinals are storage only.
enum ENUM_NMJE_JOURNEY_MATURITY
{
   NMJE_MATURITY_NONE,
   NMJE_MATURITY_OWNER_ONLY,
   NMJE_MATURITY_EXTREME_DEVELOPING,
   NMJE_MATURITY_EXTREME_MATURE,
   NMJE_MATURITY_MHV_DEVELOPING,
   NMJE_MATURITY_MHV_MATURE,
   NMJE_MATURITY_DIRECTION_STAGE,
   NMJE_MATURITY_REENTRY_CANDIDATE,
   NMJE_MATURITY_REENTRY_CONFIRMED,
   NMJE_MATURITY_MOMENTUM_CONTINUATION,
   NMJE_MATURITY_OWNER_TRANSITION,
   NMJE_MATURITY_UNRESOLVED
};

enum ENUM_NMJE_STRUCTURE_STAGE_BIT
{
   NMJE_STRUCTURE_EXTREME   = 1,
   NMJE_STRUCTURE_TPW       = 2,
   NMJE_STRUCTURE_MHV       = 4,
   NMJE_STRUCTURE_DIRECTION = 8,
   NMJE_STRUCTURE_REENTRY   = 16,
   NMJE_STRUCTURE_MOMENTUM  = 32
};

enum ENUM_NMJE_LINEAGE_EVENT_CLASS
{
   NMJE_LINEAGE_NONE,
   NMJE_LINEAGE_FIRST,
   NMJE_LINEAGE_CONTINUATION,
   NMJE_LINEAGE_NEW_JOURNEY,
   NMJE_LINEAGE_UNRESOLVED
};

enum ENUM_EXTREME_TYPE { EXT_NONE, EXT_SIDEWAYS, EXT_WITH_MOMENTUM, EXT_WITHOUT_MOMENTUM };

enum ENUM_EXTREME_MATURITY
{
   EXT_MAT_NONE,
   EXT_MAT_RAW,
   EXT_MAT_REVERSAL_CONFIRMED,
   EXT_MAT_RETEST_PHASE,
   EXT_MAT_RETEST_READY,
   EXT_MAT_VOID,
   EXT_MAT_SUPERSEDED
};

enum ENUM_SIGNAL_LEVEL { LEVEL_NONE, LEVEL_D, LEVEL_C, LEVEL_B, LEVEL_A, LEVEL_A_PLUS };

enum ENUM_PRIORITY_TIER { TIER_NONE, TIER_C, TIER_B, TIER_A, TIER_A_PLUS };


enum ENUM_SIGNAL_REQUIREMENT { REQ_STANDALONE, REQ_COMBINATION, REQ_SEQUENCE };

enum ENUM_DECISION_STATE { DEC_CREATED, DEC_VALIDATED, DEC_INVALIDATED, 
                           DEC_REJECTED, DEC_EXECUTED, DEC_EXPIRED };

enum ENUM_REJECTION_REASON
{
   REJ_NONE,
   REJ_NO_DATA,
   REJ_INSUFFICIENT_HISTORY,
   REJ_BROKER_SPEC_INVALID,
   REJ_EXPIRED,
   REJ_OPPOSITE_SIGNAL,
   REJ_SEQUENCE_BREAK,
   REJ_SPREAD_HIGH,
   REJ_DD_LIMIT,
   REJ_BASKET_LOSS,
   REJ_TOTAL_RISK,
   REJ_PORTFOLIO_LIMIT,
   REJ_INVALID_SL,
   REJ_INVALID_TP,
   REJ_INVALID_RR,
   REJ_SLTP_UNRESOLVED,
   REJ_INVALID_LOT,
   REJ_DUPLICATE,
   REJ_TRADE_LOCK,
   REJ_BROKER_ERROR,
   REJ_MARKET_PRICE_INVALID,
   REJ_INVALID_DECISION_STATE,
   REJ_MAGIC_COLLISION,
   REJ_CORRUPTED_RECOVERY_STATE,
   REJ_PORTFOLIO_LIMIT_ATOMIC,
   REJ_TEMPORARY_BROKER_DATA_FAILURE,
   REJ_AMBIGUOUS_RESULT,
   REJ_RECOVERY_INVALID,
   REJ_EXECUTION_DEVIATION_EXCEEDED,
   REJ_MANUAL_TIERS_EMPTY
};

enum ENUM_OPPOSITE_CONFLICT_TYPE
{
   CONFLICT_NONE,
   CONFLICT_TEMPORAL_VIOLATION,
   CONFLICT_DIRECTION_VIOLATION,
   CONFLICT_HIGHER_PRIORITY_BREAK
};


enum ENUM_RECOVERY_STATE { REC_NORMAL, REC_CORRUPTED, REC_RECOVERY_INVALID, REC_PARTIAL_INFERRED,
                           REC_IDENTITY_HASH_ONLY, REC_IDENTITY_MISSING_FROZEN,
                           REC_AMBIGUOUS_EXECUTION_FROZEN };

enum ENUM_PORTFOLIO_OWNERSHIP_STATE
{
   PORT_OWNERSHIP_UNKNOWN = -1,
   PORT_OWNERSHIP_EXCLUDED = 0,
   PORT_OWNERSHIP_LIVE_OWNED = 1
};

// C044 staged targetless lifecycle state. Execution remains gated OFF until
// owner-event evaluation and recovery activation pass their final gate.
enum ENUM_C044_LIFECYCLE_STATE
{
   C044_LIFE_NONE,
   C044_LIFE_MOMENTUM_PENDING,
   C044_LIFE_WAIT_NEXT_REENTRY,
   C044_LIFE_EXIT_LATCHED,
   C044_LIFE_FROZEN
};

enum ENUM_C044_EXIT_REASON
{
   C044_EXIT_NONE,
   C044_EXIT_FAILED_MOMENTUM,
   C044_EXIT_CYCLE_SUPERSEDED,
   C044_EXIT_OPPOSITE_CSM
};

//--- STRUCTS
struct ComponentIdentity
{
   ENUM_SIGNAL_TYPE   ComponentType;
   ENUM_DIRECTION     Direction;
   int                Timeframe;
   datetime           CandleTime;
   string             DecisionID;
};

struct ComponentSet
{
   ENUM_SIGNAL_TYPE   CombinationType;
   int                ComponentCount;
   ComponentIdentity  Comp1;
   ComponentIdentity  Comp2;
   ComponentIdentity  Comp3;
   datetime           SequenceStartTime;
   string             SequenceHash;
   ENUM_SIGNAL_TYPE   SLTPSource;
};

struct Candle
{
   double   Open;
   double   High;
   double   Low;
   double   Close;
   datetime Time;
   int      Index;
   int      Type;
};

struct BollingerBand
{
   double   TOP_BB;
   double   MID_BB;
   double   LOW_BB;
   double   Width;
   ENUM_BB_STATE State;
};

struct MovingAverage
{
   double   MA5_High;
   double   MA10_High;
   double   MA5_Low;
   double   MA10_Low;
   double   EMA50;
};

struct Signal
{
   ENUM_SIGNAL_TYPE     Type;
   ENUM_DIRECTION       Direction;
   bool                 Valid;
   int                  Timeframe;
   ENUM_SIGNAL_TYPE     SubType;
   double               Strength;
   string               Reason;
   int                  BarIndex;
   int                  ExpiryBar;
   int                  Score;
   ENUM_SIGNAL_LEVEL    Level;
   ENUM_PRIORITY_TIER   PriorityTier;
   double               EntryPrice;
   double               StopLoss;
   double               TakeProfit;
   double               StopLossPoints;
   double               MA5_Level;
   double               MA10_Level;
   double               MA50_Level;
   double               MID_BB;
   datetime             Timestamp;
   datetime             CandleTime;
   double               Close;
};

struct ExtremeLifecycleData
{
   ENUM_EXTREME_MATURITY Maturity;
   ENUM_DIRECTION        Direction;
   int                   Timeframe;
   int                   RawBar;
   datetime              RawCandleTime;
   int                   ConfirmationBar;
   datetime              ConfirmationCandleTime;
   double                ConfirmationClose;
   int                   LastUpdateBar;
   datetime              LastUpdateCandleTime;
   double                PreviousClose;
   double                ProvisionalBodyAnchor;
   double                FrozenBodyAnchor;
   double                RelevantMA5;
   int                   RetestStartBar;
   datetime              RetestStartCandleTime;
   int                   RetestCompletionBar;
   datetime              RetestCompletionCandleTime;
   bool                  IsValid;
   string                Reason;
};

struct MLVData
{
   ENUM_MLV_STATE       State;
   ENUM_DIRECTION       Direction;
   ENUM_DIRECTION       ParentExtremeDirection;
   int                  Timeframe;
   string               Reason;

   datetime             ParentRawCandleTime;
   datetime             ParentConfirmationCandleTime;
   datetime             TPWajibCandleTime;

   double               ProvisionalBodyAnchor;
   double               FrozenMarkedBody;
   double               PreviousClose;

   int                  StartBar;
   datetime             StartCandleTime;
   int                  LastUpdateBar;
   datetime             LastUpdateCandleTime;

   int                  ConfirmationBar;
   datetime             ConfirmationCandleTime;
   double               ConfirmationClose;

   int                  RetestBar;
   datetime             RetestCandleTime;
   int                  DirectionTakeoverBar;
   datetime             DirectionTakeoverCandleTime;

   int                  VoidBar;
   datetime             VoidCandleTime;
   int                  SupersededBar;
   datetime             SupersededCandleTime;

   bool                 InvalidationWindowOpen;
   bool                 IsValid;

   bool                 SupersessionCandidateActive;
   int                  SupersessionRawBar;
   datetime             SupersessionRawCandleTime;
};

struct ReEntryData
{
   ENUM_RE_TYPE         Type;
   ENUM_RE_STATE        State;
   ENUM_DIRECTION       Direction;
   int                  Timeframe;
   double               EntryPrice;
   double               StopLoss;
   double               TakeProfit;
   double               StopLossPoints;
   double               MA5_Level;
   double               MA10_Level;
   double               MA50_Level;
   double               MID_BB;
   datetime             EntryCandle;
   datetime             ConfirmationCandle;
   int                  StartBar;
   datetime             StartCandleTime;
   int                  LastUpdateBar;
   datetime             LastUpdateCandleTime;
   int                  ConfirmationBar;
   int                  ExpiryBar;
   datetime             ExpiryCandleTime;
   int                  MinCandlesRequired;
   int                  QualifyingCandles;

   ENUM_TYPE1_CONTEXT_STATE Type1ContextState;
   ENUM_SIGNAL_TYPE     Type1OwnerSignal;
   datetime             Type1OwnerCandleTime;
   datetime             Type1RangingStartCandleTime;
   double               Type1PreviousClose;

   bool                 IsValid;
   double               StrengthScore;
   string               Reason;
};

struct H4DirectionalOwner
{
   ENUM_H4_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   ENUM_SIGNAL_TYPE     SourceSignal;
   datetime             SourceCandleTime;
   ENUM_SIGNAL_TYPE     LastAdvanceSignal;
   datetime             LastAdvanceCandleTime;
   datetime             LastProcessedH4CandleTime;
   bool                 IsValid;
   bool                 RecoveryComplete;
   bool                 RecoveredFromCheckpoint;
   string               Reason;
};

struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   // N1 P1 provenance-only contiguous D1 owner epoch.
   datetime             EpochStartCandleTime;
   datetime             LastProcessedD1CandleTime;
   double               Close1;
   double               MA50_1;
   double               MA50_2;
   bool                 IsValid;
   string               Reason;
};

struct D1OpportunityJourney
{
   ENUM_D1_OPPORTUNITY_FAMILY Family;
   ENUM_DIRECTION             Direction;
   ENUM_SIGNAL_TYPE           SourceSignal;
   datetime                   SourceCandleTime;
   datetime                   ActivationTime;
   datetime                   LastProcessedD1CandleTime;
   string                     CycleID;
   bool                       Active;
   bool                       Tactical;
   bool                       TPWCompleted;
   string                     Reason;
};

// N1-03: read-only observation node. It never owns BBMA strategy state.
struct NestedTFNode
{
   int                  Timeframe;
   ENUM_SIGNAL_TYPE     StageType;
   ENUM_DIRECTION       Direction;
   int                  StateCode;
   datetime             CandleTime;
   bool                 Valid;
   bool                 Resolved;
   string               Label;
   string               CanonicalEventID;

   // N1.1 coverage-only secondary overlays. These never own strategy state.
   ENUM_RE_STATE        ReEntryBuyState;
   ENUM_RE_STATE        ReEntrySellState;
   bool                 ReEntryBuyValid;
   bool                 ReEntrySellValid;
   datetime             ReEntryBuyCandleTime;
   datetime             ReEntrySellCandleTime;
   ENUM_EXTREME_MATURITY ExtremeBuyMaturity;
   ENUM_EXTREME_MATURITY ExtremeSellMaturity;
   bool                 ExtremeBuyValid;
   bool                 ExtremeSellValid;
   datetime             ExtremeBuyCandleTime;
   datetime             ExtremeSellCandleTime;
   ENUM_MLV_STATE       MLVBuyState;
   ENUM_MLV_STATE       MLVSellState;
   bool                 MLVBuyValid;
   bool                 MLVSellValid;
   datetime             MLVBuyCandleTime;
   datetime             MLVSellCandleTime;
   string               OverlayLabel;
};

// Q9 P7 shadow-only canonical-cycle fingerprint. Never score/rank/gate.
struct NMJEStructuralDensityState
{
   bool                 Present;
   bool                 Valid;
   int                  StageMask;
   int                  PrefixMask;
   int                  StageCount;
   string               Reason;
};

// Q9 P10 post-fill research telemetry only.
struct NMJEEntryDisplacementState
{
   bool                 Present;
   ENUM_SIGNAL_TYPE     SourceSignal;
   int                  SourceTimeframe;
   datetime             SourceCandleTime;
   double               SourceReferencePrice;
   double               PreflightReferencePrice;
   double               BrokerOpenPrice;
   double               SourceToPreflightPips;
   double               PreflightToOpenPips;
   double               SourceToOpenPips;
};

// Q9 P4 durable observer attribution. Missing/corrupt state is diagnostic only.
struct NMJEShadowAttributionState
{
   bool                 Present;
   bool                 Durable;
   string               JourneyHash;
   string               ParentEventHash;
   ENUM_NESTED_RELATION Relation;
   ENUM_NESTED_RELATION StableRelation;
   ENUM_NMJE_JOURNEY_MATURITY Maturity;
   ENUM_NMJE_LINEAGE_EVENT_CLASS LineageClass;
   string               LineageRootHash;
   string               PreviousLineageRootHash;
   NMJEStructuralDensityState StructureDensity;
   NMJEEntryDisplacementState EntryDisplacement;
   bool                 M5SnapshotPresent;
   string               M5EventHash;
   datetime             M5ClosedCandleTime;
   bool                 M5SemanticResolved;
   ENUM_NESTED_RELATION M5DiagnosticRelation;
   string               M5ReasonHash;
};

// N1-03: one pair-level nested journey observation per closed-M15 cycle.
struct NestedJourneyState
{
   string                  Pair;
   string                  JourneyID;
   ENUM_NESTED_PARENT_KIND ParentKind;
   int                     ParentTimeframe;
   ENUM_SIGNAL_TYPE        ParentSignal;
   ENUM_DIRECTION          ParentDirection;
   datetime                ParentCandleTime;
   string                  ParentEventID;
   ENUM_DIRECTION          StrategicDirection;
   ENUM_NESTED_RELATION    Relation;
   bool                    Resolved;
   bool                    Valid;
   datetime                UpdateCandleTime;
   string                  Reason;
   // NMJE V2 P2/P3 shadow metadata; never candidate/risk/execution authority.
   bool                    P2CoherencePresent;
   int                     P2EligibleCount;
   datetime                P2CandleTime;
   bool                    M5ShadowPresent;
   datetime                M5ShadowClosedCandleTime;
   string                  M5ShadowEventID;
   ENUM_DIRECTION          M5ShadowDirection;
   string                  M5ShadowReason;
   // P5 current-owner boundary: P3 has closed-M5 data only, no M5 signal semantics.
   bool                    M5SemanticResolved;
   ENUM_NESTED_RELATION    M5DiagnosticRelation;
   string                  M5DiagnosticReason;
   // P6/P8/P11 observer-only metadata.
   ENUM_NESTED_RELATION    StableRelation;
   string                  RelationEvidenceID;
   string                  StableRelationEvidenceID;
   bool                    ParentTransitioned;
   string                  PreviousParentEventID;
   ENUM_NMJE_LINEAGE_EVENT_CLASS LineageClass;
   string                  LineageRootEventID;
   string                  PreviousLineageRootEventID;
   string                  LineageReason;
   string                  StabilityReason;
   ENUM_NMJE_JOURNEY_MATURITY Maturity;
   NestedTFNode            D1Node;
   NestedTFNode            H4Node;
   NestedTFNode            H1Node;
   NestedTFNode            M15Node;

   // N1.1 read-only D1 Opportunity overlay; not parent or execution authority.
   bool                       D1OpportunityActive;
   ENUM_D1_OPPORTUNITY_FAMILY D1OpportunityFamily;
   ENUM_DIRECTION             D1OpportunityDirection;
   ENUM_SIGNAL_TYPE           D1OpportunitySourceSignal;
   datetime                   D1OpportunitySourceCandleTime;
   datetime                   D1OpportunityActivationTime;
   bool                       D1OpportunityTactical;
   bool                       D1OpportunityTPWCompleted;
   string                     D1OpportunityCycleID;
};

struct TimeframeSnapshot
{
   datetime ProcessingServerTime;
   datetime M15_ClosedCandleTime;
   datetime D1_CandleTime;
   bool     D1_IsClosed;
   datetime H4_CandleTime;
   bool     H4_IsClosed;
   datetime H1_CandleTime;
   bool     H1_IsClosed;
   datetime M15_CandleTime;
   bool     M15_IsClosed;
};

struct TimeframeData
{
   double   ma[10];
   double   bollinger[3];
   double   trend;
   double   open;
   double   close;
   double   high;
   double   low;
   double   point;
   int      digits;
   int      barIndex;
   int      data_count;
   datetime candle_time;
   bool     is_valid;
   bool     is_closed;
   int      timeframe;
};

struct BBMA_Decision
{
   // IMMUTABLE PAYLOAD
   bool                 Valid;
   ENUM_DIRECTION       Direction;
   ENUM_SIGNAL_TYPE     SignalType;
   ENUM_PRIORITY_TIER   PriorityTier;
   int                  ComponentCount;
   ComponentIdentity    Components[3];
   datetime             CandidateExpiry;
   bool                 HasSLTPSourceComponent;
   ComponentIdentity    SLTPSourceComponent;
   bool                 PatternValid;
   bool                 SequenceValid;
   int                  ExpiryBar;
   datetime             CandleTime;
   double               EntryPrice;
   double               StopLoss;
   double               TakeProfit;
   double               StopLossPoints;
   string               Reason;
   string               SourceSequence;
   string               DecisionID;
   string               SequenceHash;
   datetime             CycleStartTime;
   ENUM_SIGNAL_TYPE     SLTPSource;
   string               Pair;

   // D1-02 frozen M11 strategic-owner identity for downstream M16 verification.
   ENUM_D1_OWNER_STATE  D1OwnerState;
   ENUM_DIRECTION       D1OwnerDirection;
   datetime             D1OwnerCandleTime;
   double               D1OwnerClose;
   double               D1OwnerMA50Current;
   double               D1OwnerMA50Previous;
   bool                 D1OwnerSnapshotValid;

   // D1O-02 selected D1 authority identity. Legacy candidates stay strategic;
   // only Mode-2 opportunity candidates use D1_AUTH_OPPORTUNITY.
   ENUM_D1_AUTHORITY_MODE       D1AuthorityMode;
   ENUM_D1_OPPORTUNITY_FAMILY   D1OpportunityFamily;
   ENUM_DIRECTION               D1OpportunityDirection;
   ENUM_SIGNAL_TYPE             D1OpportunitySourceSignal;
   datetime                     D1OpportunitySourceCandleTime;
   datetime                     D1OpportunityActivationTime;
   string                       D1OpportunityCycleID;
   bool                         D1OpportunitySnapshotValid;

   // Q9 P4+ frozen observer metadata. Never candidate/risk/execution authority.
   bool                         NMJESnapshotPresent;
   string                       NMJEJourneyID;
   string                       NMJEParentEventID;
   ENUM_NESTED_RELATION         NMJERelation;
   ENUM_NESTED_RELATION         NMJEStableRelation;
   string                       NMJEStableRelationEvidenceID;
   bool                         NMJEParentTransitioned;
   string                       NMJEPreviousParentEventID;
   ENUM_NMJE_LINEAGE_EVENT_CLASS NMJELineageClass;
   string                       NMJELineageRootEventID;
   string                       NMJEPreviousLineageRootEventID;
   ENUM_NMJE_JOURNEY_MATURITY   NMJEMaturity;
   NMJEStructuralDensityState   NMJEStructureDensity;
   datetime                     NMJEUpdateCandleTime;
   bool                         NMJEM5SnapshotPresent;
   string                       NMJEM5ShadowEventID;
   datetime                     NMJEM5ShadowClosedCandleTime;
   bool                         NMJEM5SemanticResolved;
   ENUM_NESTED_RELATION         NMJEM5DiagnosticRelation;
   string                       NMJEM5DiagnosticReason;
   
   // MUTABLE LIFECYCLE
   bool                 C044LifecycleManaged;
   bool                 D1TPWLifecycleManaged;
   ENUM_DECISION_STATE  DecisionState;
   ENUM_REJECTION_REASON RejectionReason;
};

struct OppositeConflictPackage
{
   bool                 Exists;
   ENUM_OPPOSITE_CONFLICT_TYPE ConflictType;
   string               ConflictReason;
   bool                 BreaksSequence;
   ENUM_DIRECTION       LosingCandidateDirection;
   ENUM_PRIORITY_TIER   LosingCandidatePriorityTier;
   datetime             LosingCandidateCandleTime;
   ENUM_SIGNAL_TYPE     LosingCandidateSignalType;
   datetime             FrozenSnapshotTime;
};

struct SignalScoreResult
{
   int                  Score;
   ENUM_SIGNAL_LEVEL    Level;
   string               ScoreBreakdown;
};

struct RiskValidationSnapshot
{
   double               Bid;
   double               Ask;
   double               Equity;
   double               Balance;
   double               EntryPrice;
   double               StopLoss;
   double               TickValue;
   double               TickSize_Price;
   double               LotStep;
   double               MinLot;
   double               MaxLot;
   double               Point;
   double               StopLevel;
   double               FreezeLevel;
   int                  Digits;
   int                  LotDigits;
   double               CurrentSpreadPrice;
};

struct ValidatedSequenceCandidate
{
   ENUM_SIGNAL_TYPE     SequenceType;
   ENUM_DIRECTION       Direction;
   int                  ComponentCount;
   ComponentIdentity    Components[3];
   datetime             SequenceStartTime;
   string               SequenceHash;
   datetime             Expiry;
   ENUM_SIGNAL_TYPE     SLTPSource;
   bool                 Valid;
   ENUM_PRIORITY_TIER   PriorityTier;
   int                  RequirementCompleteness;
   int                  SequenceCompleteness;
   double               PatternStrength;

   // D1O-02 authority metadata; zero/false for all legacy candidates.
   bool                         UsesD1Opportunity;
   ENUM_D1_OPPORTUNITY_FAMILY   D1OpportunityFamily;
   ENUM_DIRECTION               D1OpportunityDirection;
   ENUM_SIGNAL_TYPE             D1OpportunitySourceSignal;
   datetime                     D1OpportunitySourceCandleTime;
   datetime                     D1OpportunityActivationTime;
   string                       D1OpportunityCycleID;
};

struct PairState
{
   string               base_symbol;
   string               actual_symbol;
   int                  pair_id;
   double               point;
   double               tick_value;
   double               tick_size_price;
   double               min_lot;
   double               max_lot;
   double               lot_step;
   int                  lot_digits;
   int                  cent_factor;
   int                  digits;
   int                  stop_level;
   int                  freeze_level;
   bool                 is_cent_account;
   bool                 pair_enabled;
   bool                 is_processing;
   TimeframeData        d1_data;
   TimeframeData        h4_data;
   TimeframeData        h1_data;
   TimeframeData        m15_data;
   // NMJE P3: closed-M5 shadow context only; never execution authority.
   TimeframeData        m5_data;
   Candle               last_3_candles[3];
   Candle               last_5_candles[5];
   Candle               last_20_candles[20];
   int                  last_3_count;
   int                  last_5_count;
   int                  last_20_count;
   BollingerBand        prev_bollinger;
   BollingerBand        current_bollinger;
   MLVData              mlv_buy_state;
   MLVData              mlv_sell_state;
   ReEntryData          re_h1_buy_state;
   ReEntryData          re_h1_sell_state;
   ReEntryData          re_h4_buy_state;
   ReEntryData          re_h4_sell_state;
   ReEntryData          re_d1_buy_state;
   ReEntryData          re_d1_sell_state;
   ReEntryData          re_m15_buy_state;
   ReEntryData          re_m15_sell_state;
   H4DirectionalOwner   h4_direction_owner;
   D1MajorTrendOwner    d1_major_trend_owner;
   D1OpportunityJourney d1_opportunity;
   double               prev_ema50;
   double               current_ema50;
   double               prev_daily_ema50;
   double               current_daily_ema50;
   // F2 source-aligned Extreme maturity lifecycle.
   ExtremeLifecycleData extreme_h1_buy_lifecycle;
   ExtremeLifecycleData extreme_h1_sell_lifecycle;
   ExtremeLifecycleData extreme_h4_buy_lifecycle;
   ExtremeLifecycleData extreme_h4_sell_lifecycle;
   ExtremeLifecycleData extreme_d1_buy_lifecycle;
   ExtremeLifecycleData extreme_d1_sell_lifecycle;
   // F1 uses the F2 Extreme maturity engine as same-TF M15 parent provenance.
   ExtremeLifecycleData extreme_m15_buy_lifecycle;
   ExtremeLifecycleData extreme_m15_sell_lifecycle;
   // M16 executable-component freshness/identity overlay for mature Extremes.
   // M08 owns RAW/reversal/retest maturity and strategy invalidation.
   Signal               extreme_h1_buy_state;
   Signal               extreme_h1_sell_state;
   Signal               extreme_h4_buy_state;
   Signal               extreme_h4_sell_state;
   Signal               last_signal;
   BBMA_Decision        last_decision;
   int                  last_trade_bar;
   int                  trade_tickets[MAX_TRADES_PER_PAIR];
   int                  trade_count;
   TimeframeSnapshot    tf_snapshot;
   int                  magic_number;
   int                  broker_retry_count;
   bool                 broker_spec_valid;
};

struct TradeInfo
{
   int                  ticket;
   int                  magic_number;
   string               pair;
   ENUM_DIRECTION       direction;
   ENUM_SIGNAL_TYPE     signal_type;
   double               initial_entry_price;
   double               initial_stop_loss;
   double               initial_take_profit;
   double               initial_lot;
   double               initial_risk_price_distance;
   double               entry_price;
   double               current_sl;
   double               current_tp;
   double               lot;
   double               remaining_lot;
   bool                 partial_closed;
   bool                 partial_available;
   bool                 partial_attempted;
   bool                 breakeven_set;
   bool                 be_attempted;
   datetime             be_last_attempt_time;
   datetime             partial_last_attempt_time;
   datetime             open_time;
   double               point;
   int                  digits;
   int                  stop_level;
   int                  freeze_level;
   string               decision_id;
   string               execution_hash;
   string               sequence_hash_short;
   // Q9 P4/P10 research-only attribution; never recovery/execution authority.
   NMJEEntryDisplacementState entry_displacement;
   NMJEShadowAttributionState nmje_attribution;

   // C044 immutable lifecycle owner + restart state. These fields are dormant
   // while EnableC044Lifecycle=false.
   bool                 c044_lifecycle_managed;
   int                  c044_owner_timeframe;
   datetime             c044_owner_reentry_candle;
   datetime             c044_epoch_anchor_candle;
   datetime             c044_last_processed_owner_candle;
   ENUM_C044_LIFECYCLE_STATE c044_state;
   ENUM_C044_EXIT_REASON c044_exit_reason;
   datetime             c044_exit_latched_candle;

   // C044 Step4 deterministic replay seed. These are canonical owner snapshots
   // captured at the runtime cursor and persisted with the lifecycle checkpoint.
   bool                 c044_replay_seed_valid;
   // Q9 P2 tester-only lifecycle replay. Live monitored trades keep false.
   bool                 c044_shadow_replay;
   ReEntryData          c044_replay_reentry;
   ExtremeLifecycleData c044_replay_extreme_buy;
   ExtremeLifecycleData c044_replay_extreme_sell;

   // D1 Extreme TP-Wajib lifecycle. Independent of C044.
   bool                 d1_tpw_lifecycle_managed;
   datetime             d1_tpw_extreme_candle;
   datetime             d1_tpw_last_processed_d1_candle;
   bool                 d1_tpw_exit_latched;
   datetime             d1_tpw_exit_latched_candle;
   bool                 d1_tpw_frozen;

   ENUM_RECOVERY_STATE  recovery_state;
};

struct PendingExecutionAmbiguity
{
   bool                 Active;
   bool                 PersistenceValid;
   string               DecisionID;
   string               ExecutionHash;
   string               Pair;
   ENUM_DIRECTION       Direction;
   int                  MagicNumber;
   datetime             LatchedTime;
};

struct RiskStatus
{
   bool                 allowed;
   string               reason;
   ENUM_REJECTION_REASON rejection_reason;
};

struct PortfolioStatus
{
   double               total_profit;
   double               total_risk;
   double               basket_profit_percent;
   double               basket_loss_percent;
   double               drawdown_percent;
   int                  active_pairs;
   int                  total_trades;
   int                  trades_per_pair[MAX_PAIRS];
   bool                 allowed;
   string               reason;
};

struct BrokerInfo
{
   bool                 is_cent_account;
   int                  cent_factor;
   string               account_currency;
   int                  account_leverage;
   double               contract_size;
   double               min_lot;
   double               max_lot;
   double               lot_step;
   int                  lot_digits;
   int                  digits;
   double               point;
   double               tick_value;
   double               tick_size_price;
   int                  stop_level;
   int                  freeze_level;
};

struct SignalHistoryEntry
{
   string               DecisionID;
   string               ExecutionHash;
   string               Pair;
   ENUM_DIRECTION       Direction;
   ENUM_SIGNAL_TYPE     SignalType;
   datetime             CandleTime;
   string               SequenceHash;
   datetime             Expiry;
   bool                 Executed;
   datetime             CreatedTime;
   int                  TicketNumber;
};

// Q9 P2 counterfactual research overlay.
// Tester-only, shadow-only: no candidate/risk/execution authority.
struct NMJECounterfactualPendingCandidate
{
   bool                       Present;
   ValidatedSequenceCandidate Candidate;
   bool                       ParentMatch;
   int                        StructureMask;
};

struct NMJECounterfactualPendingSet
{
   bool                       Present;
   string                     Pair;
   string                     SetID;
   datetime                   M15CandleTime;
   int                        EligibleCount;
   int                        Count;
   ENUM_NESTED_RELATION       Relation;
   ENUM_NESTED_RELATION       StableRelation;
   ENUM_NMJE_JOURNEY_MATURITY Maturity;
   bool                       M5SnapshotPresent;
   bool                       M5SemanticResolved;
   NMJECounterfactualPendingCandidate Candidates[NMJE_CF_MAX_CANDIDATES];
};

struct NMJECounterfactualC044ReplayState
{
   bool                       Present;
   int                        OwnerTimeframe;
   datetime                   OwnerReEntryCandle;
   datetime                   EpochAnchorCandle;
   datetime                   LastProcessedOwnerCandle;
   ENUM_C044_LIFECYCLE_STATE  State;
   ENUM_C044_EXIT_REASON      ExitReason;
   datetime                   ExitLatchedCandle;
   bool                       ReplaySeedValid;
   ReEntryData                ReplayReEntry;
   ExtremeLifecycleData       ReplayExtremeBuy;
   ExtremeLifecycleData       ReplayExtremeSell;
};

struct NMJECounterfactualOutcomeCandidate
{
   bool                 Present;
   string               CandidateID;
   bool                 Selected;
   ENUM_SIGNAL_TYPE     SignalType;
   ENUM_DIRECTION       Direction;
   string               SequenceHash;
   datetime             AnchorTime;
   datetime             SequenceStartTime;
   double               EntryProxy;
   double               StopLoss;
   double               TakeProfit;
   bool                 SLTPResolved;
   bool                 Targetless;
   bool                 BaseGeometryMatch;
   double               FrozenSpreadPrice;
   ENUM_SIGNAL_TYPE     SLTPSourceType;
   int                  SLTPSourceTimeframe;
   datetime             SLTPSourceCandleTime;
   bool                 ParentMatch;
   int                  StructureMask;
   bool                 C044SeedMatch;
   NMJECounterfactualC044ReplayState C044Replay;
};

struct NMJECounterfactualTradeSet
{
   bool                 Active;
   int                  Ticket;
   string               Pair;
   string               SetID;
   string               BaselineDecisionHash;
   datetime             OpenTime;
   int                  Count;
   NMJECounterfactualOutcomeCandidate Candidates[NMJE_CF_MAX_CANDIDATES];
};

//+------------------------------------------------------------------+
//| MODULE 03: GLOBAL VARIABLES                                      |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

//--- Pair management
string               g_pair_names[MAX_PAIRS];
PairState            g_pair_states[MAX_PAIRS];
NestedJourneyState   g_nested_journeys[MAX_PAIRS]; // N1 observation only; never entry authority
datetime             g_processed_candle_time[MAX_PAIRS];
int                  g_pair_count;
int                  g_effective_max_active_pair;
bool                 g_max_active_pair_sanitized;
bool                 g_pair_list_truncated;

//--- Broker info
BrokerInfo           g_broker_info;
bool                 g_broker_initialized;

//--- Trade monitoring
TradeInfo            g_monitored_trades[MAX_MONITORED];
int                  g_monitored_count;
PendingExecutionAmbiguity g_execution_ambiguity;
NMJECounterfactualPendingSet g_nmje_cf_pending[MAX_PAIRS];
NMJECounterfactualTradeSet   g_nmje_cf_active[NMJE_CF_MAX_ACTIVE_SETS];

//--- Signal history
SignalHistoryEntry   g_global_signal_history[];
int                  g_global_signal_count;

//--- Risk cache
datetime             g_last_risk_check_time;
bool                 g_cached_risk_allowed;
string               g_cached_risk_reason;
double               g_cached_balance;

//--- Profit tracking
double               g_cumulative_profit;
double               g_last_daily_profit;
datetime             g_last_reset_date;

//--- State flags
bool                 g_is_scanning;
bool                 g_is_managing_trade;
bool                 g_is_initialized;
bool                 g_terminal_connected;

//--- Manual mode
ENUM_PRIORITY_TIER   g_manual_priority_tiers[];

//--- Dashboard
string               g_dashboard_snapshot;
bool                 g_dashboard_needs_update;

//--- Observer diagnostics (presentation/telemetry only; never trading authority)
string               g_observer_keys[];
string               g_observer_last_messages[];
int                  g_observer_record_count;

//--- Protection
double               g_protection_reference_equity;
bool                 g_portfolio_emergency_close_requested;

//--- Processing time (frozen ONCE per scan cycle)
datetime             g_processing_time;

//+------------------------------------------------------------------+
//| MODULE 04: SYMBOL & MARKET DATA                                  |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

string RemoveSuffix(string symbol)
{
   int pos = StringFind(symbol, ".");
   if(pos > 0) return StringSubstr(symbol, 0, pos);
   return symbol;
}

string FindActualSymbol(string symbol)
{
   string requested = StringTrimLeft(StringTrimRight(symbol));
   if(requested == "") return "";

   // 1) Exact broker symbol wins when it exists and can be selected.
   int totalAll = SymbolsTotal(false);
   for(int i = 0; i < totalAll; i++)
   {
      string name = SymbolName(i, false);
      if(name != requested) continue;
      if(SymbolSelect(name, true)) return name;
      return "";
   }

   // 2) Otherwise accept a broker suffix/prefix variant only when unique.
   string base = RemoveSuffix(requested);
   string candidate = "";
   int matches = 0;
   for(int j = 0; j < totalAll; j++)
   {
      string name = SymbolName(j, false);
      if(RemoveSuffix(name) != base && StringFind(name, base) != 0) continue;
      candidate = name;
      matches++;
      if(matches > 1) return "";
   }

   if(matches != 1 || candidate == "") return "";
   if(!SymbolSelect(candidate, true)) return "";
   return candidate;
}

double GetPointSize(string pair)
{
   return MarketInfo(pair, MODE_POINT);
}

int GetDigits(string pair)
{
   return (int)MarketInfo(pair, MODE_DIGITS);
}

// FIX 2: Fixed GetPipValue for 4/2 digit brokers
double GetPipValue(string pair)
{
   int digits = GetDigits(pair);
   if(digits == 5 || digits == 3)
      return GetPointSize(pair) * 10;
   return GetPointSize(pair);
}

double GetTickValue(string pair)
{
   return MarketInfo(pair, MODE_TICKVALUE);
}

double GetTickSize_Price(string pair)
{
   return MarketInfo(pair, MODE_TICKSIZE);
}

double GetMinLot(string pair)
{
   return MarketInfo(pair, MODE_MINLOT);
}

double GetMaxLot(string pair)
{
   return MarketInfo(pair, MODE_MAXLOT);
}

double GetLotStep(string pair)
{
   return MarketInfo(pair, MODE_LOTSTEP);
}

int GetLotDigits(string pair)
{
   double step = GetLotStep(pair);
   if(step >= 0.01 && step < 0.1) return 2;
   if(step >= 0.001 && step < 0.01) return 3;
   if(step >= 1.0) return 0;
   return 2;
}

int GetStopLevel(string pair)
{
   return (int)MarketInfo(pair, MODE_STOPLEVEL);
}

int GetFreezeLevel(string pair)
{
   return (int)MarketInfo(pair, MODE_FREEZELEVEL);
}

double NormalizeLot(double lot, string pair)
{
   int digits = GetLotDigits(pair);
   return NormalizeDouble(RoundDownToLotStep(lot, pair), digits);
}

double RoundDownToLotStep(double lot, string pair)
{
   double step = GetLotStep(pair);
   if(step <= 0) return lot;
   return MathFloor(lot / step) * step;
}

bool IsTerminalConnected()
{
   return IsConnected();
}

bool ValidateBrokerSpecification(string pair)
{
   if(GetTickSize_Price(pair) <= 0) return false;
   if(GetTickValue(pair) <= 0) return false;
   if(GetLotStep(pair) <= 0) return false;
   if(GetMinLot(pair) <= 0) return false;
   if(GetMaxLot(pair) < GetMinLot(pair)) return false;
   if(GetDigits(pair) <= 0) return false;
   if(GetPointSize(pair) <= 0) return false;
   if(GetStopLevel(pair) < 0) return false;
   if(GetFreezeLevel(pair) < 0) return false;
   return true;
}

bool ValidateBrokerSpecificationWithRetry(string pair, PairState &state)
{
   int attempts = 0;
   while(attempts < 3)
   {
      if(ValidateBrokerSpecification(pair))
      {
         state.broker_spec_valid = true;
         return true;
      }
      attempts++;
      if(attempts < 3)
      {
         state.broker_retry_count = attempts;
         Sleep(5000);
      }
   }
   state.broker_spec_valid = false;
   state.broker_retry_count = 3;
   return false;
}

datetime GetProcessingTime()
{
   return TimeCurrent();
}

bool IsCandleClosed(datetime candleOpenTime, int timeframeSeconds)
{
   return (candleOpenTime + timeframeSeconds) <= g_processing_time;
}

datetime GetLatestClosedCandleTime(string pair, int timeframe)
{
   for(int shift = 1; shift < 50; shift++)
   {
      datetime candleTime = iTime(pair, timeframe, shift);
      if(candleTime == 0) continue;
      int seconds = GetTimeframeSeconds(timeframe);
      if(IsCandleClosed(candleTime, seconds))
         return candleTime;
   }
   return 0;
}

bool IsNear(double price1, double price2, string pair)
{
   double point = GetPointSize(pair);
   if(point <= 0) return false;
   return MathAbs(price1 - price2) < point * 2;
}

//+------------------------------------------------------------------+
//| MODULE 05: UTILITY FUNCTIONS                                     |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

int SplitString(string textValue, string separator, string &result[])
{
   ArrayResize(result, 0);
   if(separator == "")
   {
      ArrayResize(result, 1);
      result[0] = textValue;
      return 1;
   }

   int count = 0;
   int pos = 0;
   while(true)
   {
      int next = StringFind(textValue, separator, pos);
      ArrayResize(result, count + 1);
      if(next < 0)
      {
         result[count] = StringSubstr(textValue, pos);
         count++;
         break;
      }
      result[count] = StringSubstr(textValue, pos, next - pos);
      count++;
      pos = next + StringLen(separator);
   }
   return count;
}

int GeneratePairID(string symbol)
{
   string clean = RemoveSuffix(symbol);

   // P3 PairID registry hotfix:
   // PairID occupies the low two decimal digits of the magic number, so
   // 1..99 is the valid namespace. Common FX symbols use a fixed registry
   // to keep identity stable regardless of PairList order and to eliminate
   // hash collisions. Existing non-colliding legacy IDs are preserved.
   if(clean == "USDCAD") return 1;
   if(clean == "USDCHF") return 2;
   if(clean == "CHFJPY") return 3;
   if(clean == "EURGBP") return 4;
   if(clean == "AUDCHF") return 5;
   if(clean == "AUDNZD") return 6;
   if(clean == "CADCHF") return 7;
   if(clean == "USDJPY") return 8;
   if(clean == "EURNZD") return 9;
   if(clean == "EURJPY") return 10;
   if(clean == "GBPJPY") return 11;
   if(clean == "AUDJPY") return 12;
   if(clean == "EURUSD") return 13;
   if(clean == "GBPUSD") return 14;
   if(clean == "AUDUSD") return 15;
   if(clean == "NZDUSD") return 16;
   if(clean == "EURCAD") return 17;
   if(clean == "NZDJPY") return 18;
   if(clean == "AUDCAD") return 19;
   if(clean == "CADJPY") return 20;
   if(clean == "EURAUD") return 21;
   if(clean == "EURCHF") return 22;
   if(clean == "GBPAUD") return 23;
   if(clean == "GBPCAD") return 24;
   if(clean == "GBPCHF") return 25;
   if(clean == "GBPNZD") return 26;
   if(clean == "NZDCAD") return 27;
   if(clean == "NZDCHF") return 28;

   // Unsupported/non-standard symbols use a deterministic extension
   // namespace only. Collision validation remains fail-closed, but these
   // IDs can never collide with the fixed common-FX registry above.
   ulong hash = 0;
   for(int i = 0; i < StringLen(clean); i++)
      hash = hash * 1099511628211 + (ulong)StringGetChar(clean, i);

   int extensionMin = 29;
   int extensionSpan = PAIR_ID_MAX - extensionMin + 1;
   if(extensionSpan <= 0) return 0;
   return extensionMin + (int)(hash % (ulong)extensionSpan);
}

int GenerateMagicNumber(int strategyIdValue, int instanceIdValue, int pairIdValue)
{
   if(strategyIdValue < STRATEGY_ID_MIN || strategyIdValue > STRATEGY_ID_MAX) return 0;
   if(instanceIdValue < INSTANCE_ID_MIN || instanceIdValue > INSTANCE_ID_MAX) return 0;
   if(pairIdValue < PAIR_ID_MIN || pairIdValue > PAIR_ID_MAX) return 0;

   // Calculate in 64-bit space so the overflow guard is meaningful before narrowing to int.
   long magicValue = (long)MAGIC_BASE
                   + ((long)strategyIdValue * 10000)
                   + ((long)instanceIdValue * 100)
                   + (long)pairIdValue;

   if(magicValue < 0 || magicValue > 2147483647) return 0;
   return (int)magicValue;
}

datetime GetTodayStart()
{
   MqlDateTime dt;
   TimeCurrent(dt);
   dt.hour = 0;
   dt.min = 0;
   dt.sec = 0;
   return StructToTime(dt);
}

int FindPairStateIndex(string pair)
{
   for(int i = 0; i < g_pair_count; i++)
   {
      if(g_pair_names[i] == pair)
         return i;
   }
   return -1;
}

void InitPairState(PairState &state)
{
   ZeroMemory(state);
   state.lot_digits = 2;
   state.cent_factor = 1;
   state.digits = 5;

   InitTimeframeData(state.d1_data);
   InitTimeframeData(state.h4_data);
   InitTimeframeData(state.h1_data);
   InitTimeframeData(state.m15_data);

   state.mlv_buy_state.State = MLV_NONE;
   state.mlv_buy_state.Direction = DIR_BUY;
   state.mlv_buy_state.ParentExtremeDirection = DIR_SELL;
   state.mlv_buy_state.Timeframe = PERIOD_M15;
   state.mlv_sell_state.State = MLV_NONE;
   state.mlv_sell_state.Direction = DIR_SELL;
   state.mlv_sell_state.ParentExtremeDirection = DIR_BUY;
   state.mlv_sell_state.Timeframe = PERIOD_M15;

   state.extreme_m15_buy_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_m15_buy_lifecycle.Direction = DIR_BUY;
   state.extreme_m15_buy_lifecycle.Timeframe = PERIOD_M15;
   state.extreme_m15_sell_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_m15_sell_lifecycle.Direction = DIR_SELL;
   state.extreme_m15_sell_lifecycle.Timeframe = PERIOD_M15;

   state.extreme_d1_buy_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_d1_buy_lifecycle.Direction = DIR_BUY;
   state.extreme_d1_buy_lifecycle.Timeframe = PERIOD_D1;
   state.extreme_d1_sell_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_d1_sell_lifecycle.Direction = DIR_SELL;
   state.extreme_d1_sell_lifecycle.Timeframe = PERIOD_D1;

   state.re_h1_buy_state.State = RE_STATE_NONE;
   state.re_h1_buy_state.Direction = DIR_BUY;
   state.re_h1_buy_state.Timeframe = PERIOD_H1;
   state.re_h1_sell_state.State = RE_STATE_NONE;
   state.re_h1_sell_state.Direction = DIR_SELL;
   state.re_h1_sell_state.Timeframe = PERIOD_H1;
   state.re_h4_buy_state.State = RE_STATE_NONE;
   state.re_h4_buy_state.Direction = DIR_BUY;
   state.re_h4_buy_state.Timeframe = PERIOD_H4;
   state.re_h4_sell_state.State = RE_STATE_NONE;
   state.re_h4_sell_state.Direction = DIR_SELL;
   state.re_h4_sell_state.Timeframe = PERIOD_H4;
   state.re_d1_buy_state.State = RE_STATE_NONE;
   state.re_d1_buy_state.Direction = DIR_BUY;
   state.re_d1_buy_state.Timeframe = PERIOD_D1;
   state.re_d1_sell_state.State = RE_STATE_NONE;
   state.re_d1_sell_state.Direction = DIR_SELL;
   state.re_d1_sell_state.Timeframe = PERIOD_D1;
   state.re_m15_buy_state.State = RE_STATE_NONE;
   state.re_m15_buy_state.Direction = DIR_BUY;
   state.re_m15_buy_state.Timeframe = PERIOD_M15;
   state.re_m15_sell_state.State = RE_STATE_NONE;
   state.re_m15_sell_state.Direction = DIR_SELL;
   state.re_m15_sell_state.Timeframe = PERIOD_M15;

   state.h4_direction_owner.State = H4_OWNER_RECOVERY_UNRESOLVED;
   state.h4_direction_owner.Direction = DIR_NONE;
   state.h4_direction_owner.SourceSignal = SIGNAL_NONE;
   state.h4_direction_owner.LastAdvanceSignal = SIGNAL_NONE;
   state.h4_direction_owner.IsValid = false;
   state.h4_direction_owner.RecoveryComplete = false;
   state.h4_direction_owner.RecoveredFromCheckpoint = false;

   state.d1_major_trend_owner.State = D1_OWNER_UNRESOLVED;
   state.d1_major_trend_owner.Direction = DIR_NONE;
   state.d1_major_trend_owner.SourceCandleTime = 0;
   state.d1_major_trend_owner.EpochStartCandleTime = 0;
   state.d1_major_trend_owner.LastProcessedD1CandleTime = 0;
   state.d1_major_trend_owner.Close1 = 0.0;
   state.d1_major_trend_owner.MA50_1 = 0.0;
   state.d1_major_trend_owner.MA50_2 = 0.0;
   state.d1_major_trend_owner.IsValid = false;
   state.d1_major_trend_owner.Reason = "D1 owner not evaluated";

   state.d1_opportunity.Family = D1_OPP_NONE;
   state.d1_opportunity.Direction = DIR_NONE;
   state.d1_opportunity.SourceSignal = SIGNAL_NONE;
   state.d1_opportunity.Active = false;
   state.d1_opportunity.Tactical = false;
   state.d1_opportunity.TPWCompleted = false;
   state.d1_opportunity.Reason = "D1 opportunity not evaluated";
}

void InitTimeframeData(TimeframeData &data)
{
   ArrayInitialize(data.ma, 0);
   ArrayInitialize(data.bollinger, 0);
   data.trend = 0;
   data.open = 0;
   data.close = 0;
   data.high = 0;
   data.low = 0;
   data.point = 0;
   data.digits = 5;
   data.barIndex = 0;
   data.data_count = 0;
   data.candle_time = 0;
   data.is_valid = false;
   data.is_closed = false;
   data.timeframe = 0;
}

void InitBrokerInfo()
{
   g_broker_info.is_cent_account = DetectCentAccount();
   g_broker_info.cent_factor = GetCentFactor();
   g_broker_info.account_currency = AccountCurrency();
   g_broker_info.account_leverage = AccountLeverage();
   g_broker_info.contract_size = 100000;
   g_broker_info.min_lot = MarketInfo(Symbol(), MODE_MINLOT);
   g_broker_info.max_lot = MarketInfo(Symbol(), MODE_MAXLOT);
   g_broker_info.lot_step = MarketInfo(Symbol(), MODE_LOTSTEP);
   g_broker_info.lot_digits = GetLotDigits(Symbol());
   g_broker_info.digits = GetDigits(Symbol());
   g_broker_info.point = GetPointSize(Symbol());
   g_broker_info.tick_value = GetTickValue(Symbol());
   g_broker_info.tick_size_price = GetTickSize_Price(Symbol());
   g_broker_info.stop_level = GetStopLevel(Symbol());
   g_broker_info.freeze_level = GetFreezeLevel(Symbol());
   g_broker_initialized = true;
}

bool DetectCentAccount()
{
   double minLot = MarketInfo(Symbol(), MODE_MINLOT);
   if(minLot > 0 && minLot < 0.01) return true;
   return false;
}

int GetCentFactor()
{
   if(DetectCentAccount())
      return 100;
   return 1;
}

void CleanupGlobalSignalHistory()
{
   int count = ArraySize(g_global_signal_history);
   if(count <= SIGNAL_HISTORY_MAX)
   {
      g_global_signal_count = count;
      return;
   }

   int targetRemove = SIGNAL_HISTORY_CLEANUP_SIZE;
   int overflow = count - SIGNAL_HISTORY_MAX;
   if(targetRemove < overflow) targetRemove = overflow;

   int removed = 0;
   int write = 0;
   for(int i = 0; i < count; i++)
   {
      bool protectedTombstone = (g_global_signal_history[i].Executed &&
                                 g_global_signal_history[i].TicketNumber > 0);

      if(!protectedTombstone && removed < targetRemove)
      {
         removed++;
         continue;
      }

      if(write != i)
         g_global_signal_history[write] = g_global_signal_history[i];
      write++;
   }

   if(write < count)
      ArrayResize(g_global_signal_history, write);

   g_global_signal_count = write;
}

void CleanupSignalHistoryEntries()
{
   int count = ArraySize(g_global_signal_history);
   int write = 0;
   for(int i = 0; i < count; i++)
   {
      if(g_global_signal_history[i].Executed && g_global_signal_history[i].TicketNumber > 0)
      {
         g_global_signal_history[write++] = g_global_signal_history[i];
      }
      else if(g_global_signal_history[i].Expiry >= g_processing_time)
      {
         g_global_signal_history[write++] = g_global_signal_history[i];
      }
   }
   if(write < count)
      ArrayResize(g_global_signal_history, write);
   g_global_signal_count = write;
}

int GetTimeframeSeconds(int timeframe)
{
   switch(timeframe)
   {
      case 1: return 60;
      case 5: return 300;
      case 15: return 900;
      case 30: return 1800;
      case 60: return 3600;
      case 240: return 14400;
      case 1440: return 86400;
      case 10080: return 604800;
      case 43200: return 2592000;
      default: return 0;
   }
}

bool IsValidLotStep(double lot, string pair)
{
   double step = GetLotStep(pair);
   if(step <= 0) return false;
   double ratio = lot / step;
   double rounded = MathRound(ratio);
   return MathAbs(ratio - rounded) < 0.00001;
}

string GenerateSequenceHash(ComponentSet &componentSet)
{
   string hashText = IntegerToString(componentSet.CombinationType);
   hashText += IntegerToString(componentSet.ComponentCount);
   hashText += IntegerToString(componentSet.Comp1.ComponentType);
   hashText += IntegerToString(componentSet.Comp1.Direction);
   hashText += IntegerToString(componentSet.Comp1.Timeframe);
   hashText += TimeToString(componentSet.Comp1.CandleTime);
   hashText += IntegerToString(componentSet.Comp2.ComponentType);
   hashText += IntegerToString(componentSet.Comp2.Direction);
   hashText += IntegerToString(componentSet.Comp2.Timeframe);
   hashText += TimeToString(componentSet.Comp2.CandleTime);
   hashText += IntegerToString(componentSet.Comp3.ComponentType);
   hashText += IntegerToString(componentSet.Comp3.Direction);
   hashText += IntegerToString(componentSet.Comp3.Timeframe);
   hashText += TimeToString(componentSet.Comp3.CandleTime);
   return SHORT_HASH(hashText, 16);
}

string GenerateDecisionID(string pair, datetime candleTime, 
                          ENUM_DIRECTION direction, ENUM_SIGNAL_TYPE signalType,
                          string sequenceHash)
{
   return pair + "|" + TimeToString(candleTime) + "|" + 
          IntegerToString(direction) + "|" + IntegerToString(signalType) + "|" + sequenceHash;
}

string SHORT_HASH(string textValue, int chars=16)
{
   ulong hash = 0;
   for(int i = 0; i < StringLen(textValue); i++)
   {
      hash = hash * 1099511628211 + StringGetChar(textValue, i);
   }
   string result = "";
   string hexDigits = "0123456789ABCDEF";
   for(int i = 0; i < chars && i < 16; i++)
   {
      int digit = (int)(hash & 0xF);
      result += StringSubstr(hexDigits, digit, 1);
      hash >>= 4;
   }
   return result;
}

void Log(int level, string message)
{
   if(level <= DebugLevel)
   {
      Print(TimeToString(TimeCurrent()), " [", level, "] ", message);
   }
}

bool ObserverShouldEmit(string key, string message)
{
   if(key == "" || message == "") return false;

   for(int i = 0; i < g_observer_record_count; i++)
   {
      if(g_observer_keys[i] != key) continue;

      if(DebugLevel >= DBG_FULL || g_observer_last_messages[i] != message)
      {
         g_observer_last_messages[i] = message;
         return true;
      }
      return false;
   }

   int newCount = g_observer_record_count + 1;
   if(ArrayResize(g_observer_keys, newCount) != newCount ||
      ArrayResize(g_observer_last_messages, newCount) != newCount)
   {
      // Observability must fail open: never hide a diagnostic because its cache
      // could not grow. This path has no strategy/risk/execution authority.
      return true;
   }

   g_observer_keys[g_observer_record_count] = key;
   g_observer_last_messages[g_observer_record_count] = message;
   g_observer_record_count = newCount;
   return true;
}

void ObserverPrintChanged(string key, string message)
{
   if(ObserverShouldEmit(key, message))
      Print(message);
}

void MarkDecisionExecuted(string decisionID, int ticketNumber)
{
   if(decisionID == "" || ticketNumber <= 0) return;

   string executionHash = SHORT_HASH(decisionID);
   int count = ArraySize(g_global_signal_history);

   for(int i = 0; i < count; i++)
   {
      if(g_global_signal_history[i].DecisionID == decisionID ||
         (g_global_signal_history[i].ExecutionHash != "" &&
          g_global_signal_history[i].ExecutionHash == executionHash))
      {
         g_global_signal_history[i].DecisionID = decisionID;
         g_global_signal_history[i].ExecutionHash = executionHash;
         g_global_signal_history[i].Executed = true;
         g_global_signal_history[i].TicketNumber = ticketNumber;
         if(g_global_signal_history[i].CreatedTime <= 0)
            g_global_signal_history[i].CreatedTime = TimeCurrent();
         g_global_signal_count = ArraySize(g_global_signal_history);
         return;
      }
   }

   ArrayResize(g_global_signal_history, count + 1);
   ZeroMemory(g_global_signal_history[count]);
   g_global_signal_history[count].DecisionID = decisionID;
   g_global_signal_history[count].ExecutionHash = executionHash;
   g_global_signal_history[count].Executed = true;
   g_global_signal_history[count].TicketNumber = ticketNumber;
   g_global_signal_history[count].CreatedTime = TimeCurrent();
   g_global_signal_count = count + 1;
}

bool IsDecisionExecuted(string decisionID)
{
   if(decisionID == "") return false;
   string executionHash = SHORT_HASH(decisionID);
   int count = ArraySize(g_global_signal_history);
   for(int i = 0; i < count; i++)
   {
      if(g_global_signal_history[i].DecisionID == decisionID)
         return g_global_signal_history[i].Executed;
      if(g_global_signal_history[i].Executed &&
         g_global_signal_history[i].ExecutionHash != "" &&
         g_global_signal_history[i].ExecutionHash == executionHash)
         return true;
   }
   return false;
}

bool ExtractExecutionHash(string comment, string &executionHash)
{
   executionHash = "";
   string prefix = "BBMA|H:";
   if(StringFind(comment, prefix) != 0) return false;

   int start = StringLen(prefix);
   int end = StringFind(comment, "|", start);
   if(end < 0) end = StringLen(comment);
   if(end <= start) return false;

   executionHash = StringSubstr(comment, start, end - start);
   return (executionHash != "");
}


// P0 durable execution identity persistence.
// MT4 terminal GlobalVariables are authoritative; OrderComment is fallback only.
string ExecutionHashGVBase(string executionHash)
{
   return "BBXH|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|H" + executionHash + "|";
}

string ExecutionTicketGVBase(int ticket)
{
   return "BBXT|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(ticket) + "|";
}

int HexDigitValue(string digit)
{
   string hex = "0123456789ABCDEF";
   return StringFind(hex, digit);
}

double Hex4ToNumber(string chunk)
{
   if(StringLen(chunk) != 4) return -1.0;
   int value = 0;
   for(int i = 0; i < 4; i++)
   {
      int nibble = HexDigitValue(StringSubstr(chunk, i, 1));
      if(nibble < 0) return -1.0;
      value = value * 16 + nibble;
   }
   return (double)value;
}

string NumberToHex4(double encoded)
{
   int value = (int)MathRound(encoded);
   if(value < 0 || value > 65535) return "";
   string hex = "0123456789ABCDEF";
   string result = "";
   int divisor = 4096;
   for(int pos = 0; pos < 4; pos++)
   {
      int nibble = value / divisor;
      result += StringSubstr(hex, nibble, 1);
      value = value % divisor;
      if(divisor > 1) divisor /= 16;
   }
   return result;
}

bool LoadPersistedExecutionHashForTicket(int ticket, string pair,
                                         ENUM_DIRECTION direction, int magic,
                                         datetime openTime, string &executionHash)
{
   executionHash = "";
   if(ticket <= 0 || pair == "" || magic <= 0 || openTime <= 0 ||
      (direction != DIR_BUY && direction != DIR_SELL))
      return false;

   string base = ExecutionTicketGVBase(ticket);
   string keys[7] = {"H0","H1","H2","H3","M","O","D"};
   for(int i = 0; i < 7; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;

   int storedMagic = (int)GlobalVariableGet(base + "M");
   datetime storedOpen = (datetime)((int)GlobalVariableGet(base + "O"));
   ENUM_DIRECTION storedDirection =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   if(storedMagic != magic || storedOpen != openTime || storedDirection != direction)
      return false;

   string h0 = NumberToHex4(GlobalVariableGet(base + "H0"));
   string h1 = NumberToHex4(GlobalVariableGet(base + "H1"));
   string h2 = NumberToHex4(GlobalVariableGet(base + "H2"));
   string h3 = NumberToHex4(GlobalVariableGet(base + "H3"));
   if(h0 == "" || h1 == "" || h2 == "" || h3 == "") return false;
   executionHash = h0 + h1 + h2 + h3;

   string hashBase = ExecutionHashGVBase(executionHash);
   string hashKeys[4] = {"T","M","O","D"};
   for(int k = 0; k < 4; k++)
      if(!GlobalVariableCheck(hashBase + hashKeys[k]))
      {
         executionHash = "";
         return false;
      }

   if((int)GlobalVariableGet(hashBase + "T") != ticket ||
      (int)GlobalVariableGet(hashBase + "M") != magic ||
      (datetime)((int)GlobalVariableGet(hashBase + "O")) != openTime ||
      (ENUM_DIRECTION)((int)GlobalVariableGet(hashBase + "D")) != direction)
   {
      executionHash = "";
      return false;
   }
   return true;
}

bool SaveExecutionIdentityHash(string executionHash, int ticket, string pair,
                               ENUM_DIRECTION direction, int magic,
                               datetime openTime)
{
   if(StringLen(executionHash) != 16 || ticket <= 0 || pair == "" ||
      magic <= 0 || openTime <= 0 ||
      (direction != DIR_BUY && direction != DIR_SELL))
      return false;

   double h0 = Hex4ToNumber(StringSubstr(executionHash, 0, 4));
   double h1 = Hex4ToNumber(StringSubstr(executionHash, 4, 4));
   double h2 = Hex4ToNumber(StringSubstr(executionHash, 8, 4));
   double h3 = Hex4ToNumber(StringSubstr(executionHash, 12, 4));
   if(h0 < 0 || h1 < 0 || h2 < 0 || h3 < 0) return false;

   string hashBase = ExecutionHashGVBase(executionHash);
   string ticketBase = ExecutionTicketGVBase(ticket);

   if(GlobalVariableSet(hashBase + "T", (double)ticket) == 0) return false;
   if(GlobalVariableSet(hashBase + "M", (double)magic) == 0) return false;
   if(GlobalVariableSet(hashBase + "O", (double)openTime) == 0) return false;
   if(GlobalVariableSet(hashBase + "D", (double)direction) == 0) return false;

   if(GlobalVariableSet(ticketBase + "H0", h0) == 0) return false;
   if(GlobalVariableSet(ticketBase + "H1", h1) == 0) return false;
   if(GlobalVariableSet(ticketBase + "H2", h2) == 0) return false;
   if(GlobalVariableSet(ticketBase + "H3", h3) == 0) return false;
   if(GlobalVariableSet(ticketBase + "M", (double)magic) == 0) return false;
   if(GlobalVariableSet(ticketBase + "O", (double)openTime) == 0) return false;
   if(GlobalVariableSet(ticketBase + "D", (double)direction) == 0) return false;
   GlobalVariablesFlush();

   string verifyHash = "";
   return LoadPersistedExecutionHashForTicket(ticket, pair, direction, magic,
                                              openTime, verifyHash) &&
          verifyHash == executionHash;
}

int FindPersistedExecutionTicket(string decisionID, string pair, int orderType,
                                 int magicNumber)
{
   if(decisionID == "" || pair == "" || magicNumber <= 0 ||
      (orderType != OP_BUY && orderType != OP_SELL))
      return -1;

   string executionHash = SHORT_HASH(decisionID);
   string base = ExecutionHashGVBase(executionHash);
   string keys[4] = {"T","M","O","D"};
   for(int i = 0; i < 4; i++)
      if(!GlobalVariableCheck(base + keys[i])) return -1;

   int ticket = (int)GlobalVariableGet(base + "T");
   int storedMagic = (int)GlobalVariableGet(base + "M");
   datetime storedOpen = (datetime)((int)GlobalVariableGet(base + "O"));
   ENUM_DIRECTION storedDirection =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   ENUM_DIRECTION expectedDirection =
      (orderType == OP_BUY) ? DIR_BUY : DIR_SELL;

   if(ticket <= 0 || storedMagic != magicNumber || storedOpen <= 0 ||
      storedDirection != expectedDirection)
      return -1;
   if(!OrderSelect(ticket, SELECT_BY_TICKET)) return -1;
   if(OrderCloseTime() != 0 || OrderSymbol() != pair ||
      OrderMagicNumber() != magicNumber || OrderType() != orderType ||
      OrderOpenTime() != storedOpen)
      return -1;

   string ticketHash = "";
   if(!LoadPersistedExecutionHashForTicket(ticket, pair, expectedDirection,
                                           magicNumber, storedOpen, ticketHash))
      return -1;
   if(ticketHash != executionHash) return -1;
   return ticket;
}

bool IsExactEAOwnedSelectedOrder(int &pairIdx)
{
   pairIdx = -1;
   if(OrderCloseTime() != 0) return false;
   if(OrderType() != OP_BUY && OrderType() != OP_SELL) return false;

   int magic = OrderMagicNumber();
   string symbol = OrderSymbol();
   for(int p = 0; p < g_pair_count; p++)
   {
      if(g_pair_states[p].magic_number != magic) continue;
      if(g_pair_states[p].actual_symbol != symbol) continue;
      pairIdx = p;
      return true;
   }
   return false;
}

void UpsertExecutionHashTombstone(string executionHash, int ticket, string pair,
                                  ENUM_DIRECTION direction, datetime createdTime)
{
   if(executionHash == "" || ticket <= 0 || pair == "") return;

   int count = ArraySize(g_global_signal_history);
   for(int i = 0; i < count; i++)
   {
      if(g_global_signal_history[i].ExecutionHash == executionHash)
      {
         g_global_signal_history[i].Executed = true;
         g_global_signal_history[i].TicketNumber = ticket;
         return;
      }
   }

   ArrayResize(g_global_signal_history, count + 1);
   g_global_signal_history[count].DecisionID = "";
   g_global_signal_history[count].ExecutionHash = executionHash;
   g_global_signal_history[count].Pair = pair;
   g_global_signal_history[count].Direction = direction;
   g_global_signal_history[count].SignalType = SIGNAL_NONE;
   g_global_signal_history[count].CandleTime = 0;
   g_global_signal_history[count].SequenceHash = "";
   g_global_signal_history[count].Expiry = 0;
   g_global_signal_history[count].Executed = true;
   g_global_signal_history[count].CreatedTime = createdTime;
   g_global_signal_history[count].TicketNumber = ticket;
}

void RebuildExecutionHistory()
{
   for(int pass = 0; pass < 2; pass++)
   {
      int total = (pass == 0) ? OrdersTotal() : OrdersHistoryTotal();
      int pool = (pass == 0) ? MODE_TRADES : MODE_HISTORY;
      for(int i = 0; i < total; i++)
      {
         if(!OrderSelect(i, SELECT_BY_POS, pool)) continue;
         if(OrderType() != OP_BUY && OrderType() != OP_SELL) continue;

         int pairIdx = -1;
         int magic = OrderMagicNumber();
         string symbol = OrderSymbol();
         for(int p = 0; p < g_pair_count; p++)
         {
            if(g_pair_states[p].magic_number == magic &&
               g_pair_states[p].actual_symbol == symbol)
            {
               pairIdx = p;
               break;
            }
         }
         if(pairIdx < 0) continue;

         ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;
         string executionHash = "";
         bool localIdentity = LoadPersistedExecutionHashForTicket(
            OrderTicket(), symbol, liveDirection, magic, OrderOpenTime(), executionHash);
         if(!localIdentity)
         {
            if(!ExtractExecutionHash(OrderComment(), executionHash)) continue;
            // Migrate legacy/comment-backed identity into the durable terminal store.
            SaveExecutionIdentityHash(executionHash, OrderTicket(), symbol,
                                      liveDirection, magic, OrderOpenTime());
         }

         UpsertExecutionHashTombstone(executionHash, OrderTicket(), symbol,
                                      liveDirection, OrderOpenTime());
      }
   }
   g_global_signal_count = ArraySize(g_global_signal_history);
}

void SetDecisionLifecycleState(BBMA_Decision &decision, ENUM_DECISION_STATE state)
{
   decision.DecisionState = state;
}

void SetDecisionRejectionReason(BBMA_Decision &decision, ENUM_REJECTION_REASON reason)
{
   decision.RejectionReason = reason;
}

string CreateOrderComment(string decisionID, string pair, 
                          ENUM_DIRECTION direction, ENUM_SIGNAL_TYPE signalType,
                          double intendedEntry, double intendedSL, 
                          double intendedLot, double intendedRisk,
                          string sequenceHash, datetime candleTime)
{
   // P0: broker comments are not an authoritative persistence store.
   // Keep only the compact execution hash for secondary/fallback evidence.
   return "BBMA|H:" + SHORT_HASH(decisionID);
}

bool ParseOrderCommentFull(string comment, string &decisionHash, string &pair,
                           ENUM_DIRECTION &direction, ENUM_SIGNAL_TYPE &signalType,
                           double &intendedEntry, double &intendedSL,
                           double &intendedLot, double &intendedRisk,
                           string &sequenceHash, datetime &candleTime)
{
   if(StringFind(comment, "BBMA") != 0) return false;
   
   string fields[];
   int count = 0;
   int pos = 0;
   while(true)
   {
      int next = StringFind(comment, "|", pos);
      if(next < 0)
      {
         if(pos < StringLen(comment))
         {
            ArrayResize(fields, count + 1);
            fields[count] = StringSubstr(comment, pos);
            count++;
         }
         break;
      }
      if(next > pos)
      {
         ArrayResize(fields, count + 1);
         fields[count] = StringSubstr(comment, pos, next - pos);
         count++;
      }
      pos = next + 1;
   }
   
   candleTime = 0;
   for(int i = 0; i < count; i++)
   {
      string field = fields[i];
      int colon = StringFind(field, ":");
      if(colon < 0) continue;
      string key = StringSubstr(field, 0, colon);
      string value = StringSubstr(field, colon + 1);
      
      if(key == "H") decisionHash = value;
      else if(key == "C") candleTime = StringToTime(value);
      else if(key == "P") pair = value;
      else if(key == "D") direction = (ENUM_DIRECTION)StringToInteger(value);
      else if(key == "T") signalType = (ENUM_SIGNAL_TYPE)StringToInteger(value);
      else if(key == "E") intendedEntry = StringToDouble(value);
      else if(key == "S") intendedSL = StringToDouble(value);
      else if(key == "L") intendedLot = StringToDouble(value);
      else if(key == "R") intendedRisk = StringToDouble(value);
      else if(key == "Q") sequenceHash = value;
   }
   return (decisionHash != "" && pair != "" && candleTime > 0 &&
           direction != DIR_NONE && signalType != SIGNAL_NONE);
}

double CalculateTradeRiskMoney(string pair, double lot, double entryPrice, double stopLoss)
{
   double tickValue = GetTickValue(pair);
   double tickSizePrice = GetTickSize_Price(pair);
   if(tickValue <= 0 || tickSizePrice <= 0) return 0;
   double slDistance = MathAbs(entryPrice - stopLoss);
   if(slDistance <= 0) return 0;
   return lot * (slDistance * tickValue / tickSizePrice);
}

void BuildTimeframeSnapshot(string pair, TimeframeSnapshot &snapshot)
{
   snapshot.ProcessingServerTime = g_processing_time;
   
   snapshot.D1_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_D1);
   snapshot.D1_IsClosed = IsCandleClosed(snapshot.D1_CandleTime, 86400);
   
   snapshot.H4_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_H4);
   snapshot.H4_IsClosed = IsCandleClosed(snapshot.H4_CandleTime, 14400);
   
   snapshot.H1_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_H1);
   snapshot.H1_IsClosed = IsCandleClosed(snapshot.H1_CandleTime, 3600);
   
   snapshot.M15_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_M15);
   snapshot.M15_IsClosed = IsCandleClosed(snapshot.M15_CandleTime, 900);
}

void BuildRiskValidationSnapshot(string pair, BBMA_Decision &decision, RiskValidationSnapshot &snapshot)
{
   snapshot.Bid = MarketInfo(pair, MODE_BID);
   snapshot.Ask = MarketInfo(pair, MODE_ASK);
   snapshot.Equity = AccountEquity();
   snapshot.Balance = AccountBalance();
   snapshot.EntryPrice = decision.EntryPrice;
   snapshot.StopLoss = decision.StopLoss;
   snapshot.TickValue = GetTickValue(pair);
   snapshot.TickSize_Price = GetTickSize_Price(pair);
   snapshot.LotStep = GetLotStep(pair);
   snapshot.MinLot = GetMinLot(pair);
   snapshot.MaxLot = GetMaxLot(pair);
   snapshot.Point = GetPointSize(pair);
   snapshot.StopLevel = MarketInfo(pair, MODE_STOPLEVEL);
   snapshot.FreezeLevel = MarketInfo(pair, MODE_FREEZELEVEL);
   snapshot.Digits = GetDigits(pair);
   snapshot.LotDigits = GetLotDigits(pair);
   snapshot.CurrentSpreadPrice = MathAbs(snapshot.Ask - snapshot.Bid);
}

double GetAllowedExecutionDeviation(string pair, RiskValidationSnapshot &snapshot)
{
   double minDeviation = AllowedExecutionDeviation_MinPoints * snapshot.Point;
   double spreadDeviation = 2 * snapshot.CurrentSpreadPrice;
   return MathMax(spreadDeviation, minDeviation);
}

//+------------------------------------------------------------------+
//| MODULE 06: BBMA DATA ENGINE                                      |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool IsBBMAHistoryReady(string pair, int timeframe, int period, int shift,
                        int appliedPrice)
{
   if(period <= 0 || shift < 0 || iBars(pair, timeframe) - shift < period)
      return false;
   for(int i = 0; i < period; i++)
   {
      double price = iClose(pair, timeframe, shift + i);
      if(appliedPrice == PRICE_HIGH) price = iHigh(pair, timeframe, shift + i);
      else if(appliedPrice == PRICE_LOW) price = iLow(pair, timeframe, shift + i);
      if(!MathIsValidNumber(price) || price <= 0) return false;
   }
   return true;
}

double SMA(string pair, int timeframe, int period, int shift)
{
   if(!IsBBMAHistoryReady(pair, timeframe, period, shift, PRICE_CLOSE)) return 0;
   double sum = 0;
   for(int i = 0; i < period; i++)
   {
      double price = iClose(pair, timeframe, shift + i);
      if(!MathIsValidNumber(price) || price <= 0) return 0;
      sum += price;
   }
   return sum / period;
}

double BBMAHighMA(string pair, int timeframe, int period, int shift)
{
   if(!IsBBMAHistoryReady(pair, timeframe, period, shift, PRICE_HIGH)) return 0;
   return iMA(pair, timeframe, period, 0, MODE_LWMA, PRICE_HIGH, shift);
}

double BBMALowMA(string pair, int timeframe, int period, int shift)
{
   if(!IsBBMAHistoryReady(pair, timeframe, period, shift, PRICE_LOW)) return 0;
   return iMA(pair, timeframe, period, 0, MODE_LWMA, PRICE_LOW, shift);
}

double EMA(string pair, int timeframe, int period, int shift)
{
   if(!IsBBMAHistoryReady(pair, timeframe, period, shift, PRICE_CLOSE)) return 0;
   return iMA(pair, timeframe, period, 0, MODE_EMA, PRICE_CLOSE, shift);
}

double StandardDeviation(string pair, int timeframe, int period, int shift)
{
   double mean = SMA(pair, timeframe, period, shift);
   // Negative denotes unavailable history; zero is a valid flat-price deviation.
   if(!MathIsValidNumber(mean) || mean <= 0) return -1;
   double sum = 0;
   for(int i = 0; i < period; i++)
   {
      double price = iClose(pair, timeframe, shift + i);
      if(!MathIsValidNumber(price) || price <= 0) return -1;
      sum += MathPow(price - mean, 2);
   }
   return MathSqrt(sum / period);
}

void CalculateBollinger(string pair, int timeframe, int shift, BollingerBand &band)
{
   double middle = SMA(pair, timeframe, BB_PERIOD, shift);
   double stdDev = StandardDeviation(pair, timeframe, BB_PERIOD, shift);
   if(!MathIsValidNumber(middle) || middle <= 0 ||
      !MathIsValidNumber(stdDev) || stdDev < 0)
   {
      middle = 0;
      stdDev = 0;
   }
   band.MID_BB = middle;
   band.TOP_BB = middle + BB_DEVIATION * stdDev;
   band.LOW_BB = middle - BB_DEVIATION * stdDev;
   band.Width = band.TOP_BB - band.LOW_BB;
   band.State = BB_NONE;
}

void CalculateAllMA(string pair, int timeframe, int shift, MovingAverage &ma)
{
   ma.MA5_High = BBMAHighMA(pair, timeframe, MA5_HIGH_PERIOD, shift);
   ma.MA10_High = BBMAHighMA(pair, timeframe, MA10_HIGH_PERIOD, shift);
   ma.MA5_Low = BBMALowMA(pair, timeframe, MA5_LOW_PERIOD, shift);
   ma.MA10_Low = BBMALowMA(pair, timeframe, MA10_LOW_PERIOD, shift);
   ma.EMA50 = EMA(pair, timeframe, EMA50_PERIOD, shift);
}

void GetDataForTimeframe(string pair, int timeframe, datetime targetTime, TimeframeData &data)
{
   InitTimeframeData(data);
   data.timeframe = timeframe;
   if(targetTime == 0) return;
   int shift = iBarShift(pair, timeframe, targetTime);
   if(shift < 0) return;
   datetime candleTime = iTime(pair, timeframe, shift);
   if(candleTime != targetTime) return;
   
   data.open = iOpen(pair, timeframe, shift);
   data.high = iHigh(pair, timeframe, shift);
   data.low = iLow(pair, timeframe, shift);
   data.close = iClose(pair, timeframe, shift);
   data.candle_time = candleTime;
   data.barIndex = shift;
   data.point = GetPointSize(pair);
   data.digits = GetDigits(pair);
   data.is_closed = IsCandleClosed(candleTime, GetTimeframeSeconds(timeframe));
   data.data_count = iBars(pair, timeframe);

   if(!MathIsValidNumber(data.open) || !MathIsValidNumber(data.high) ||
      !MathIsValidNumber(data.low) || !MathIsValidNumber(data.close) ||
      data.open <= 0 || data.close <= 0 || data.low <= 0 ||
      data.high < MathMax(data.open, data.close) ||
      data.low > MathMin(data.open, data.close)) return;
   
   BollingerBand band;
   CalculateBollinger(pair, timeframe, shift, band);
   data.bollinger[0] = band.TOP_BB;
   data.bollinger[1] = band.MID_BB;
   data.bollinger[2] = band.LOW_BB;
   
   MovingAverage ma;
   CalculateAllMA(pair, timeframe, shift, ma);
   data.ma[0] = ma.MA5_High;
   data.ma[1] = ma.MA10_High;
   data.ma[2] = ma.MA5_Low;
   data.ma[3] = ma.MA10_Low;
   data.ma[4] = ma.EMA50;

   for(int b = 0; b < 3; b++)
      if(!MathIsValidNumber(data.bollinger[b]) || data.bollinger[b] <= 0) return;
   for(int m = 0; m < 5; m++)
      if(!MathIsValidNumber(data.ma[m]) || data.ma[m] <= 0) return;
   data.is_valid = true;
   
   double ema50 = ma.EMA50;
   if(data.close > ema50) data.trend = 1.0;
   else if(data.close < ema50) data.trend = -1.0;
   else data.trend = 0;
}

double GetHighestHigh(string pair, int timeframe, int count, int shift)
{
   double max = 0;
   for(int i = 0; i < count; i++)
   {
      double high = iHigh(pair, timeframe, shift + i);
      if(high > max) max = high;
   }
   return max;
}

double GetLowestLow(string pair, int timeframe, int count, int shift)
{
   double min = DBL_MAX;
   for(int i = 0; i < count; i++)
   {
      double low = iLow(pair, timeframe, shift + i);
      if(low < min) min = low;
   }
   return min;
}

//+------------------------------------------------------------------+
//| MODULE 07: BB SHAPE ENGINE                                       |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

ENUM_BB_STATE DetectBBState(BollingerBand &current, BollingerBand &previous,
                            double horizontalTolerance)
{
   if(current.Width <= 0 || previous.Width <= 0) return BB_NONE;
   if(current.TOP_BB <= 0 || current.MID_BB <= 0 || current.LOW_BB <= 0 ||
      previous.TOP_BB <= 0 || previous.MID_BB <= 0 || previous.LOW_BB <= 0)
      return BB_NONE;

   // CORE-V2-F5: flat/horizontal is a geometric BB-line state, not the
   // leftover branch of width-ratio classification.  Tolerance is exactly one
   // broker point supplied by BuildBBShapeState(), used only as numerical
   // equality tolerance rather than a trading/strategy threshold.
   if(horizontalTolerance > 0)
   {
      bool topHorizontal =
         (MathAbs(current.TOP_BB - previous.TOP_BB) <= horizontalTolerance);
      bool midHorizontal =
         (MathAbs(current.MID_BB - previous.MID_BB) <= horizontalTolerance);
      bool lowHorizontal =
         (MathAbs(current.LOW_BB - previous.LOW_BB) <= horizontalTolerance);

      if(topHorizontal && midHorizontal && lowHorizontal)
         return BB_FLAT;
   }

   double widthRatio = current.Width / previous.Width;

   // Preserve the pre-existing project shape thresholds outside the repaired
   // flat branch; F5 does not redefine squeeze/expansion strategy semantics.
   if(widthRatio < 0.9)
      return BB_SQUEEZE;
   if(widthRatio > 1.1)
      return BB_EXPANDING;

   return BB_CONTRACTING;
}

bool BuildBBShapeState(string pair, TimeframeData &data,
                       BollingerBand &current, BollingerBand &previous)
{
   ZeroMemory(current);
   ZeroMemory(previous);
   
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return false;
   
   current.TOP_BB = data.bollinger[0];
   current.MID_BB = data.bollinger[1];
   current.LOW_BB = data.bollinger[2];
   current.Width = current.TOP_BB - current.LOW_BB;
   
   CalculateBollinger(pair, data.timeframe, data.barIndex + 1, previous);
   
   if(current.MID_BB <= 0 || current.Width <= 0 ||
      previous.MID_BB <= 0 || previous.Width <= 0)
   {
      current.State = BB_NONE;
      return false;
   }
   
   double pointTolerance = GetPointSize(pair);
   if(pointTolerance <= 0)
   {
      current.State = BB_NONE;
      return false;
   }

   current.State = DetectBBState(current, previous, pointTolerance);
   return (current.State != BB_NONE);
}

//+------------------------------------------------------------------+
//| MODULE 08: EXTREME DETECTOR                                      |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool DetectExtreme(string pair, ENUM_DIRECTION direction, TimeframeData &data, BollingerBand &band)
{
   // F2 RAW detector only. Reversal confirmation and retest maturity are
   // handled by UpdateExtremeLifecycle(); RAW alone is never a combo component.
   if(!data.is_valid || !data.is_closed) return false;
   if(band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   if(direction == DIR_SELL)
   {
      double ma5High = data.ma[0];
      double ma10High = data.ma[1];
      if(ma5High <= 0 || ma10High <= 0) return false;
      return (ma5High > band.TOP_BB || ma10High > band.TOP_BB);
   }

   double ma5Low = data.ma[2];
   double ma10Low = data.ma[3];
   if(ma5Low <= 0 || ma10Low <= 0) return false;
   return (ma5Low < band.LOW_BB || ma10Low < band.LOW_BB);
}

void ResetExtremeLifecycle(ExtremeLifecycleData &extreme,
                           ENUM_DIRECTION direction, int timeframe)
{
   ZeroMemory(extreme);
   extreme.Maturity = EXT_MAT_NONE;
   extreme.Direction = direction;
   extreme.Timeframe = timeframe;
}

double GetExtremeRelevantMA5(TimeframeData &data, ENUM_DIRECTION direction)
{
   if(direction == DIR_SELL) return data.ma[0]; // MA5 High
   if(direction == DIR_BUY)  return data.ma[2]; // MA5 Low
   return 0.0;
}

double GetExtremeReversalBodyEdge(TimeframeData &data, ENUM_DIRECTION direction)
{
   if(direction == DIR_SELL) return MathMax(data.open, data.close);
   if(direction == DIR_BUY)  return MathMin(data.open, data.close);
   return 0.0;
}

bool IsExtremeReversalDirection(TimeframeData &data, ENUM_DIRECTION direction)
{
   if(data.open <= 0 || data.close <= 0) return false;
   if(direction == DIR_SELL) return (data.close < data.open);
   if(direction == DIR_BUY)  return (data.close > data.open);
   return false;
}

bool IsExtremeMomentumInvalidation(string pair, TimeframeData &data,
                                   BollingerBand &currentBand)
{
   if(data.barIndex < 1 || data.close <= 0 || currentBand.Width <= 0) return false;

   BollingerBand previousBand;
   ZeroMemory(previousBand);
   CalculateBollinger(pair, data.timeframe, data.barIndex + 1, previousBand);
   if(previousBand.Width <= 0 || previousBand.MID_BB <= 0 ||
      previousBand.TOP_BB <= 0 || previousBand.LOW_BB <= 0)
      return false;

   bool bbExpanding = (currentBand.Width > previousBand.Width);
   bool buyMomentum = bbExpanding &&
                      currentBand.MID_BB > previousBand.MID_BB &&
                      currentBand.TOP_BB > previousBand.TOP_BB &&
                      data.close > currentBand.TOP_BB;
   bool sellMomentum = bbExpanding &&
                       currentBand.MID_BB < previousBand.MID_BB &&
                       currentBand.LOW_BB < previousBand.LOW_BB &&
                       data.close < currentBand.LOW_BB;
   return (buyMomentum || sellMomentum);
}

bool IsExtremeLifecycleInvalidation(string pair, ENUM_DIRECTION direction,
                                    TimeframeData &data, BollingerBand &band)
{
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;

   // A continuation close through the original Extreme-side outer BB is void.
   // An opposite-side outside close is not made a universal hard failure here;
   // it is invalid only when it qualifies as accepted directional Momentum.
   bool relevantOuterBreak = (direction == DIR_SELL)
                             ? (data.close > band.TOP_BB)
                             : (data.close < band.LOW_BB);

   return (relevantOuterBreak || IsExtremeMomentumInvalidation(pair, data, band));
}

void MarkExtremeLifecycleVoid(ExtremeLifecycleData &extreme,
                              TimeframeData &data, string reason)
{
   extreme.Maturity = EXT_MAT_VOID;
   extreme.IsValid = false;
   extreme.LastUpdateBar = data.barIndex;
   extreme.LastUpdateCandleTime = data.candle_time;
   extreme.PreviousClose = data.close;
   extreme.Reason = reason;
}

bool IsExtremeCycleOwnerMature(ExtremeLifecycleData &extreme)
{
   if(!extreme.IsValid || extreme.ConfirmationCandleTime <= 0) return false;
   return (extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           extreme.Maturity == EXT_MAT_RETEST_PHASE ||
           extreme.Maturity == EXT_MAT_RETEST_READY);
}

void MarkExtremeLifecycleSuperseded(ExtremeLifecycleData &extreme,
                                    TimeframeData &data, string reason)
{
   extreme.Maturity = EXT_MAT_SUPERSEDED;
   extreme.IsValid = false;
   extreme.LastUpdateBar = data.barIndex;
   extreme.LastUpdateCandleTime = data.candle_time;
   extreme.PreviousClose = data.close;
   extreme.Reason = reason;
}

void ResolveOppositeExtremeSupersession(ExtremeLifecycleData &buyExtreme,
                                        ExtremeLifecycleData &sellExtreme,
                                        TimeframeData &data)
{
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return;
   if(buyExtreme.Timeframe != data.timeframe || sellExtreme.Timeframe != data.timeframe) return;

   bool buyMature = IsExtremeCycleOwnerMature(buyExtreme);
   bool sellMature = IsExtremeCycleOwnerMature(sellExtreme);
   if(!buyMature || !sellMature) return;

   if(buyExtreme.ConfirmationCandleTime > sellExtreme.ConfirmationCandleTime)
   {
      MarkExtremeLifecycleSuperseded(sellExtreme, data,
         "SELL Extreme superseded by newer reversal-confirmed opposite BUY Extreme");
      if(EntryMode == 2)
         Print("[P3M2][EXT_SUPERSEDE] TF=", data.timeframe,
               " Old=SELL New=BUY OldConfirm=", TimeToString(sellExtreme.ConfirmationCandleTime),
               " NewConfirm=", TimeToString(buyExtreme.ConfirmationCandleTime),
               " ProcessCandle=", TimeToString(data.candle_time));
   }
   else if(sellExtreme.ConfirmationCandleTime > buyExtreme.ConfirmationCandleTime)
   {
      MarkExtremeLifecycleSuperseded(buyExtreme, data,
         "BUY Extreme superseded by newer reversal-confirmed opposite SELL Extreme");
      if(EntryMode == 2)
         Print("[P3M2][EXT_SUPERSEDE] TF=", data.timeframe,
               " Old=BUY New=SELL OldConfirm=", TimeToString(buyExtreme.ConfirmationCandleTime),
               " NewConfirm=", TimeToString(sellExtreme.ConfirmationCandleTime),
               " ProcessCandle=", TimeToString(data.candle_time));
   }
   // Equal confirmation time remains ambiguous; downstream conflict stays fail-closed.
}

void UpdateExtremeProvisionalAnchor(ExtremeLifecycleData &extreme,
                                    TimeframeData &data)
{
   double edge = GetExtremeReversalBodyEdge(data, extreme.Direction);
   if(edge <= 0) return;

   if(extreme.ProvisionalBodyAnchor <= 0)
      extreme.ProvisionalBodyAnchor = edge;
   else if(extreme.Direction == DIR_SELL)
      extreme.ProvisionalBodyAnchor = MathMax(extreme.ProvisionalBodyAnchor, edge);
   else if(extreme.Direction == DIR_BUY)
      extreme.ProvisionalBodyAnchor = MathMin(extreme.ProvisionalBodyAnchor, edge);
}

bool IsExtremeRetestStart(ExtremeLifecycleData &extreme, TimeframeData &data)
{
   if(extreme.PreviousClose <= 0 || data.close <= 0) return false;
   if(extreme.Direction == DIR_SELL) return (data.close > extreme.PreviousClose);
   if(extreme.Direction == DIR_BUY)  return (data.close < extreme.PreviousClose);
   return false;
}

bool IsExtremeRetestInteraction(ExtremeLifecycleData &extreme,
                                TimeframeData &data)
{
   if(data.high <= 0 || data.low <= 0) return false;

   bool bodyTouch = false;
   if(extreme.FrozenBodyAnchor > 0)
   {
      if(extreme.Direction == DIR_SELL)
         bodyTouch = (data.high >= extreme.FrozenBodyAnchor);
      else if(extreme.Direction == DIR_BUY)
         bodyTouch = (data.low <= extreme.FrozenBodyAnchor);
   }

   double ma5 = GetExtremeRelevantMA5(data, extreme.Direction);
   extreme.RelevantMA5 = ma5;
   bool ma5Touch = (ma5 > 0 && data.low <= ma5 && data.high >= ma5);

   return (bodyTouch || ma5Touch);
}

ENUM_EXTREME_MATURITY UpdateExtremeLifecycle(ExtremeLifecycleData &extreme,
                                             string pair,
                                             ENUM_DIRECTION direction,
                                             TimeframeData &data,
                                             BollingerBand &band,
                                             bool rawDetected)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return extreme.Maturity;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return extreme.Maturity;

   if(extreme.Direction != direction || extreme.Timeframe != data.timeframe)
      ResetExtremeLifecycle(extreme, direction, data.timeframe);

   // F2 maturity has NO fixed candle/session expiry. MaxWaitBars_Extreme is
   // retained only as legacy diagnostic metadata and never invalidates owner state.

   if(extreme.Maturity == EXT_MAT_VOID || extreme.Maturity == EXT_MAT_SUPERSEDED)
   {
      ENUM_EXTREME_MATURITY terminalState = extreme.Maturity;
      if(!rawDetected || data.candle_time <= extreme.LastUpdateCandleTime)
         return terminalState;
      ResetExtremeLifecycle(extreme, direction, data.timeframe);
   }

   if(extreme.Maturity == EXT_MAT_NONE)
   {
      if(!rawDetected) return EXT_MAT_NONE;

      extreme.Maturity = EXT_MAT_RAW;
      extreme.Direction = direction;
      extreme.Timeframe = data.timeframe;
      extreme.RawBar = data.barIndex;
      extreme.RawCandleTime = data.candle_time;
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      extreme.IsValid = false;
      extreme.Reason = "RAW Extreme detected; awaiting reversal confirmation";

      if(IsExtremeLifecycleInvalidation(pair, direction, data, band))
         MarkExtremeLifecycleVoid(extreme, data,
                                  "RAW Extreme void: outside-BB/Momentum invalidation");
      return extreme.Maturity;
   }

   if(data.candle_time <= extreme.LastUpdateCandleTime)
      return extreme.Maturity;

   // Invalidation is evaluated before every pre-entry maturity promotion.
   if(IsExtremeLifecycleInvalidation(pair, direction, data, band))
   {
      MarkExtremeLifecycleVoid(extreme, data,
                               "Extreme void: outside-BB/Momentum invalidation");
      return EXT_MAT_VOID;
   }

   if(extreme.Maturity == EXT_MAT_RAW)
   {
      // RAW confirmation is necessarily a SUBSEQUENT closed source-TF candle:
      // the RAW candle was already stored as LastUpdateCandleTime above.
      if(IsExtremeReversalDirection(data, direction))
      {
         extreme.Maturity = EXT_MAT_REVERSAL_CONFIRMED;
         extreme.ConfirmationBar = data.barIndex;
         extreme.ConfirmationCandleTime = data.candle_time;
         extreme.ConfirmationClose = data.close;
         extreme.ProvisionalBodyAnchor = 0.0;
         UpdateExtremeProvisionalAnchor(extreme, data);
         extreme.IsValid = true;
         extreme.Reason = "Extreme reversal-confirmed; component maturity reached";
      }

      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      return extreme.Maturity;
   }

   if(extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED)
   {
      bool retestStarts = IsExtremeRetestStart(extreme, data);
      if(retestStarts)
      {
         // Trigger candle belongs to retest phase and is excluded from anchor.
         extreme.FrozenBodyAnchor = extreme.ProvisionalBodyAnchor;
         extreme.RetestStartBar = data.barIndex;
         extreme.RetestStartCandleTime = data.candle_time;
         extreme.Maturity = EXT_MAT_RETEST_PHASE;
         extreme.LastUpdateBar = data.barIndex;
         extreme.LastUpdateCandleTime = data.candle_time;
         extreme.PreviousClose = data.close;
         extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
         extreme.Reason = "Extreme retest phase started; body anchor frozen";

         // The retest-start candle is excluded from anchor construction but may
         // itself be the first valid revisit of the already-frozen reference.
         if(IsExtremeRetestInteraction(extreme, data))
         {
            extreme.Maturity = EXT_MAT_RETEST_READY;
            extreme.RetestCompletionBar = data.barIndex;
            extreme.RetestCompletionCandleTime = data.candle_time;
            extreme.Reason = "Extreme retest complete: body anchor or MA5 interaction";
         }
         return extreme.Maturity;
      }

      // No close progression back toward the original Extreme yet: the
      // structural reversal phase continues and its provisional body edge may
      // update. No fixed candle count is imposed.
      UpdateExtremeProvisionalAnchor(extreme, data);
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      return EXT_MAT_REVERSAL_CONFIRMED;
   }

   if(extreme.Maturity == EXT_MAT_RETEST_PHASE)
   {
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);

      if(IsExtremeRetestInteraction(extreme, data))
      {
         extreme.Maturity = EXT_MAT_RETEST_READY;
         extreme.RetestCompletionBar = data.barIndex;
         extreme.RetestCompletionCandleTime = data.candle_time;
         extreme.Reason = "Extreme retest complete: body anchor or MA5 interaction";
      }
      return extreme.Maturity;
   }

   if(extreme.Maturity == EXT_MAT_RETEST_READY)
   {
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      extreme.IsValid = true;
   }

   return extreme.Maturity;
}

bool ExportReversalConfirmedExtremeSignal(ExtremeLifecycleData &extreme,
                                          Signal &signal)
{
   ZeroMemory(signal);
   bool mature = (extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
                  extreme.Maturity == EXT_MAT_RETEST_PHASE ||
                  extreme.Maturity == EXT_MAT_RETEST_READY);
   if(!mature || !extreme.IsValid) return false;
   if(extreme.ConfirmationCandleTime <= 0 || extreme.Timeframe <= 0) return false;

   signal.Type = SIGNAL_EXTREME;
   signal.Direction = extreme.Direction;
   signal.Valid = true;
   signal.Timeframe = extreme.Timeframe;
   signal.BarIndex = extreme.ConfirmationBar;
   signal.ExpiryBar = MaxWaitBars_Extreme;
   signal.Timestamp = extreme.ConfirmationCandleTime;
   signal.CandleTime = extreme.ConfirmationCandleTime;
   signal.Close = extreme.ConfirmationClose;
   signal.MA5_Level = extreme.RelevantMA5;
   signal.Reason = extreme.Reason;
   return true;
}

//+------------------------------------------------------------------+
//| MODULE 09: MHV & MLV CANONICAL LIFECYCLE ENGINE                  |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

ENUM_DIRECTION GetMHVParentExtremeDirection(ENUM_DIRECTION mhvDirection)
{
   if(mhvDirection == DIR_BUY) return DIR_SELL;
   if(mhvDirection == DIR_SELL) return DIR_BUY;
   return DIR_NONE;
}

bool IsMHVParentExtremeMature(ExtremeLifecycleData &parent)
{
   if(!parent.IsValid) return false;
   if(parent.ConfirmationCandleTime <= 0 || parent.Timeframe != PERIOD_M15)
      return false;

   return (parent.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           parent.Maturity == EXT_MAT_RETEST_PHASE ||
           parent.Maturity == EXT_MAT_RETEST_READY);
}

bool IsCanonicalMLVMatureState(ENUM_MLV_STATE state)
{
   return (state == MLV_FORMATION_ESTABLISHED ||
           state == MLV_RETEST_COMPLETE ||
           state == MLV_DIRECTION_TAKEN);
}

void ResetMLVState(MLVData &mlv, ENUM_DIRECTION direction)
{
   ZeroMemory(mlv);
   mlv.State = MLV_NONE;
   mlv.Direction = direction;
   mlv.ParentExtremeDirection = GetMHVParentExtremeDirection(direction);
   mlv.Timeframe = PERIOD_M15;
}

void AttachCanonicalMHVParent(MLVData &mlv, ENUM_DIRECTION direction,
                              ExtremeLifecycleData &parent,
                              TimeframeData &data)
{
   ResetMLVState(mlv, direction);
   mlv.State = MLV_PARENT_READY;
   mlv.ParentRawCandleTime = parent.RawCandleTime;
   mlv.ParentConfirmationCandleTime = parent.ConfirmationCandleTime;
   mlv.LastUpdateBar = data.barIndex;
   mlv.LastUpdateCandleTime = data.candle_time;
   mlv.PreviousClose = data.close;
   mlv.IsValid = false;
   mlv.Reason = "Canonical MHV parent attached: reversal-confirmed M15 Extreme";
}

void MarkCanonicalMLVVoid(MLVData &mlv, TimeframeData &data, string reason)
{
   mlv.State = MLV_VOID;
   mlv.IsValid = false;
   mlv.InvalidationWindowOpen = false;
   mlv.VoidBar = data.barIndex;
   mlv.VoidCandleTime = data.candle_time;
   mlv.LastUpdateBar = data.barIndex;
   mlv.LastUpdateCandleTime = data.candle_time;
   mlv.PreviousClose = data.close;
   mlv.Reason = reason;
}

void MarkCanonicalMLVSuperseded(MLVData &mlv, TimeframeData &data, string reason)
{
   mlv.State = MLV_SUPERSEDED;
   mlv.IsValid = false;
   mlv.InvalidationWindowOpen = false;
   mlv.SupersededBar = data.barIndex;
   mlv.SupersededCandleTime = data.candle_time;
   mlv.LastUpdateBar = data.barIndex;
   mlv.LastUpdateCandleTime = data.candle_time;
   mlv.PreviousClose = data.close;
   mlv.Reason = reason;
}

bool IsMHVTPWajibCompleted(TimeframeData &data, ENUM_DIRECTION parentDirection)
{
   if(data.high <= 0 || data.low <= 0) return false;

   if(parentDirection == DIR_SELL)
   {
      double ma5Low = data.ma[2];
      double ma10Low = data.ma[3];
      if(ma5Low <= 0 || ma10Low <= 0) return false;
      return (data.low <= ma5Low || data.low <= ma10Low);
   }

   if(parentDirection == DIR_BUY)
   {
      double ma5High = data.ma[0];
      double ma10High = data.ma[1];
      if(ma5High <= 0 || ma10High <= 0) return false;
      return (data.high >= ma5High || data.high >= ma10High);
   }

   return false;
}

bool IsMHVContinuationInvalidation(string pair, ENUM_DIRECTION mhvDirection,
                                   TimeframeData &data, BollingerBand &band)
{
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;

   // Bottom-side BUY MHV follows a prior SELL Extreme/TP move: a fresh
   // downside outer-BB close / SELL CSM means prior momentum continued.
   if(mhvDirection == DIR_BUY)
   {
      if(data.close < band.LOW_BB) return true;
      return DetectCSM(pair, data.timeframe, DIR_SELL, data.barIndex);
   }

   // Top-side SELL MHV mirrors the rule after a prior BUY Extreme/TP move.
   if(mhvDirection == DIR_SELL)
   {
      if(data.close > band.TOP_BB) return true;
      return DetectCSM(pair, data.timeframe, DIR_BUY, data.barIndex);
   }

   return false;
}

bool IsMHVLossPhaseEligible(string pair, ENUM_DIRECTION mhvDirection,
                            TimeframeData &data, BollingerBand &band)
{
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;
   if(data.close < band.LOW_BB || data.close > band.TOP_BB) return false;

   ENUM_DIRECTION priorMoveDirection = GetMHVParentExtremeDirection(mhvDirection);
   if(priorMoveDirection == DIR_NONE) return false;
   if(DetectCSM(pair, data.timeframe, priorMoveDirection, data.barIndex)) return false;
   return true;
}

double GetMHVBodyEdge(TimeframeData &data, ENUM_DIRECTION mhvDirection)
{
   if(data.open <= 0 || data.close <= 0) return 0.0;
   if(mhvDirection == DIR_BUY)  return MathMin(data.open, data.close); // bottom body
   if(mhvDirection == DIR_SELL) return MathMax(data.open, data.close); // top body
   return 0.0;
}

void UpdateMHVProvisionalBody(MLVData &mlv, TimeframeData &data)
{
   double edge = GetMHVBodyEdge(data, mlv.Direction);
   if(edge <= 0) return;

   if(mlv.ProvisionalBodyAnchor <= 0)
      mlv.ProvisionalBodyAnchor = edge;
   else if(mlv.Direction == DIR_BUY)
      mlv.ProvisionalBodyAnchor = MathMin(mlv.ProvisionalBodyAnchor, edge);
   else if(mlv.Direction == DIR_SELL)
      mlv.ProvisionalBodyAnchor = MathMax(mlv.ProvisionalBodyAnchor, edge);
}

bool IsMHVFormationMoveAway(MLVData &mlv, TimeframeData &data)
{
   if(mlv.PreviousClose <= 0 || data.close <= 0) return false;
   if(mlv.Direction == DIR_BUY)  return (data.close > mlv.PreviousClose);
   if(mlv.Direction == DIR_SELL) return (data.close < mlv.PreviousClose);
   return false;
}

bool IsMHVRetestInteraction(MLVData &mlv, TimeframeData &data)
{
   if(mlv.FrozenMarkedBody <= 0 || data.high <= 0 || data.low <= 0) return false;
   if(mlv.Direction == DIR_BUY)  return (data.low <= mlv.FrozenMarkedBody);
   if(mlv.Direction == DIR_SELL) return (data.high >= mlv.FrozenMarkedBody);
   return false;
}

void InstallMHVSupersessionParent(MLVData &mlv,
                                  ExtremeLifecycleData &parent,
                                  TimeframeData &data)
{
   ENUM_DIRECTION parentDirection = GetMHVParentExtremeDirection(mlv.Direction);
   int rawBar = mlv.SupersessionRawBar;
   datetime rawTime = mlv.SupersessionRawCandleTime;

   ResetExtremeLifecycle(parent, parentDirection, data.timeframe);
   parent.Maturity = EXT_MAT_REVERSAL_CONFIRMED;
   parent.Direction = parentDirection;
   parent.Timeframe = data.timeframe;
   parent.RawBar = rawBar;
   parent.RawCandleTime = rawTime;
   parent.ConfirmationBar = data.barIndex;
   parent.ConfirmationCandleTime = data.candle_time;
   parent.ConfirmationClose = data.close;
   parent.LastUpdateBar = data.barIndex;
   parent.LastUpdateCandleTime = data.candle_time;
   parent.PreviousClose = data.close;
   parent.ProvisionalBodyAnchor = GetExtremeReversalBodyEdge(data, parentDirection);
   parent.RelevantMA5 = GetExtremeRelevantMA5(data, parentDirection);
   parent.IsValid = true;
   parent.Reason = "Reversal-confirmed M15 Extreme installed by F1 cycle supersession";
}

bool TryAdvanceMHVSupersessionCandidate(MLVData &mlv, string pair,
                                        TimeframeData &data, BollingerBand &band,
                                        ExtremeLifecycleData &parent)
{
   ENUM_DIRECTION parentDirection = GetMHVParentExtremeDirection(mlv.Direction);
   if(parentDirection == DIR_NONE) return false;

   if(mlv.SupersessionCandidateActive)
   {
      if(data.candle_time <= mlv.SupersessionRawCandleTime) return false;

      if(IsExtremeLifecycleInvalidation(pair, parentDirection, data, band))
      {
         mlv.SupersessionCandidateActive = false;
         mlv.SupersessionRawBar = 0;
         mlv.SupersessionRawCandleTime = 0;
         return false;
      }

      if(IsExtremeReversalDirection(data, parentDirection))
      {
         InstallMHVSupersessionParent(mlv, parent, data);
         MarkCanonicalMLVSuperseded(
            mlv, data,
            "Old MHV/MLV cycle superseded by opposite reversal-confirmed Extreme");
         if(EntryMode == 2)
            Print("[P3M2][MLV_SUPERSEDE] MLVDir=", EnumToString(mlv.Direction),
                  " NewExtremeDir=", EnumToString(parentDirection),
                  " Raw=", TimeToString(mlv.SupersessionRawCandleTime),
                  " Confirm=", TimeToString(data.candle_time));
         return true;
      }
      return false;
   }

   datetime boundary = mlv.ConfirmationCandleTime;
   if(boundary <= 0) boundary = mlv.VoidCandleTime;
   if(boundary <= 0 || data.candle_time <= boundary) return false;

   bool rawDetected = DetectExtreme(pair, parentDirection, data, band);
   if(!rawDetected) return false;

   // Opposite RAW Extreme is only a new-cycle candidate. It cannot erase the
   // old MHV provenance until the later reversal-confirmation candle arrives.
   if(IsExtremeLifecycleInvalidation(pair, parentDirection, data, band))
      return false;

   mlv.SupersessionCandidateActive = true;
   mlv.SupersessionRawBar = data.barIndex;
   mlv.SupersessionRawCandleTime = data.candle_time;
   if(EntryMode == 2)
      Print("[P3M2][MLV_SUPER_CAND] MLVDir=", EnumToString(mlv.Direction),
            " ExtremeDir=", EnumToString(parentDirection),
            " Raw=", TimeToString(data.candle_time));
   return false;
}

ENUM_MLV_STATE UpdateCanonicalMLVState(MLVData &mlv, string pair,
                                       ENUM_DIRECTION direction,
                                       TimeframeData &data,
                                       BollingerBand &band,
                                       ExtremeLifecycleData &parent,
                                       bool sameDirectionSignal)
{
   if(!EnableMLVStateEngine) return MLV_NONE;
   if(direction != DIR_BUY && direction != DIR_SELL) return MLV_NONE;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return mlv.State;

   if(mlv.Direction != direction || mlv.Timeframe != data.timeframe)
      ResetMLVState(mlv, direction);

   bool parentMature = IsMHVParentExtremeMature(parent);

   if(mlv.State == MLV_NONE)
   {
      if(!parentMature) return MLV_NONE;
      AttachCanonicalMHVParent(mlv, direction, parent, data);
      return mlv.State;
   }

   // A newly installed reversal-confirmed parent is a new cycle. Preserve the
   // atomic supersession transition for one processing step, then attach it.
   if(parentMature && parent.ConfirmationCandleTime > 0 &&
      parent.ConfirmationCandleTime != mlv.ParentConfirmationCandleTime)
   {
      if(mlv.State == MLV_SUPERSEDED || mlv.State == MLV_VOID)
      {
         AttachCanonicalMHVParent(mlv, direction, parent, data);
         return mlv.State;
      }

      MarkCanonicalMLVSuperseded(
         mlv, data,
         "MHV/MLV provenance superseded by a newer reversal-confirmed parent Extreme");
      return mlv.State;
   }

   if(data.candle_time <= mlv.LastUpdateCandleTime)
      return mlv.State;

   // Before formation, parent validity is mandatory. After formation, the
   // frozen parent identity is historical provenance and is not retroactively
   // erased by later same-cycle progression.
   if(!parentMature && !IsCanonicalMLVMatureState(mlv.State) &&
      mlv.State != MLV_VOID && mlv.State != MLV_SUPERSEDED)
   {
      MarkCanonicalMLVVoid(mlv, data,
                           "Canonical MHV void: parent Extreme lost validity before formation");
      return mlv.State;
   }

   if(mlv.State == MLV_PARENT_READY)
   {
      if(data.candle_time <= mlv.ParentConfirmationCandleTime) return mlv.State;

      if(IsMHVTPWajibCompleted(data, mlv.ParentExtremeDirection))
      {
         mlv.State = MLV_TP_COMPLETE;
         mlv.TPWajibCandleTime = data.candle_time;
         mlv.LastUpdateBar = data.barIndex;
         mlv.LastUpdateCandleTime = data.candle_time;
         mlv.PreviousClose = data.close;
         mlv.Reason = "Normal TP-Wajib structurally completed; awaiting loss of prior momentum";
      }
      else
      {
         mlv.LastUpdateBar = data.barIndex;
         mlv.LastUpdateCandleTime = data.candle_time;
         mlv.PreviousClose = data.close;
      }
      return mlv.State;
   }

   if(mlv.State == MLV_TP_COMPLETE)
   {
      // Continuing Momentum after TP means loss-of-momentum has not started.
      // No fixed candle count or timer is used; wait for an actual inside-BB,
      // non-CSM structural pause to begin the MHV formation phase.
      if(IsMHVLossPhaseEligible(pair, direction, data, band))
      {
         mlv.State = MLV_LOSS_DEVELOPING;
         mlv.StartBar = data.barIndex;
         mlv.StartCandleTime = data.candle_time;
         mlv.ProvisionalBodyAnchor = 0.0;
         UpdateMHVProvisionalBody(mlv, data);
         mlv.InvalidationWindowOpen = true;
         mlv.Reason = "Post-TP structural loss of prior momentum developing";
      }

      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_LOSS_DEVELOPING)
   {
      // Invalidation has priority over formation promotion.
      if(IsMHVContinuationInvalidation(pair, direction, data, band))
      {
         MarkCanonicalMLVVoid(
            mlv, data,
            "Canonical MHV void: prior Momentum/outer-BB continuation resumed before formation");
         return mlv.State;
      }

      bool moveAway = IsMHVFormationMoveAway(mlv, data);
      if(moveAway && mlv.ProvisionalBodyAnchor > 0)
      {
         // The move-away trigger candle confirms formation but is excluded from
         // the accumulated most-extreme body reference.
         mlv.FrozenMarkedBody = mlv.ProvisionalBodyAnchor;
         mlv.State = MLV_FORMATION_ESTABLISHED;
         mlv.ConfirmationBar = data.barIndex;
         mlv.ConfirmationCandleTime = data.candle_time;
         mlv.ConfirmationClose = data.close;
         mlv.IsValid = true;
         mlv.InvalidationWindowOpen = true;
         mlv.LastUpdateBar = data.barIndex;
         mlv.LastUpdateCandleTime = data.candle_time;
         mlv.PreviousClose = data.close;
         mlv.Reason = "Canonical MHV/MLV formation established; marked body frozen";
         return mlv.State;
      }

      UpdateMHVProvisionalBody(mlv, data);
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_FORMATION_ESTABLISHED ||
      mlv.State == MLV_RETEST_COMPLETE)
   {
      if(mlv.InvalidationWindowOpen &&
         IsMHVContinuationInvalidation(pair, direction, data, band))
      {
         MarkCanonicalMLVVoid(
            mlv, data,
            "Canonical MHV void: outer-BB/Momentum invalidation before direction takeover");
         return mlv.State;
      }

      if(TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent))
         return mlv.State;

      if(mlv.State == MLV_FORMATION_ESTABLISHED &&
         data.candle_time > mlv.ConfirmationCandleTime &&
         IsMHVRetestInteraction(mlv, data))
      {
         mlv.State = MLV_RETEST_COMPLETE;
         mlv.RetestBar = data.barIndex;
         mlv.RetestCandleTime = data.candle_time;
         mlv.Reason = "Canonical MHV/MLV retest complete at frozen marked body";
      }

      // eCSD/CSD is the normal next stage, not MHV invalidation. It may take
      // ownership only on a later closed candle after formation exists.
      if(sameDirectionSignal && data.candle_time > mlv.ConfirmationCandleTime)
      {
         mlv.State = MLV_DIRECTION_TAKEN;
         mlv.DirectionTakeoverBar = data.barIndex;
         mlv.DirectionTakeoverCandleTime = data.candle_time;
         mlv.InvalidationWindowOpen = false;
         mlv.IsValid = true;
         mlv.Reason = "Same-cycle eCSD/CSD direction takeover; MHV provenance retained";
      }

      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_DIRECTION_TAKEN)
   {
      // Later same-cycle RE/CSM/Momentum must not retroactively void MHV.
      mlv.InvalidationWindowOpen = false;
      mlv.IsValid = true;

      if(TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent))
         return mlv.State;

      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_VOID)
   {
      // VOID remains non-authoritative. A later RAW opposite-cycle Extreme is
      // only a candidate; a reversal-confirmed Extreme installs the new parent.
      TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent);
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_SUPERSEDED)
   {
      mlv.IsValid = false;
      mlv.InvalidationWindowOpen = false;
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
   }

   return mlv.State;
}

bool ExportCanonicalMHVSignal(MLVData &mlv, Signal &signal)
{
   ZeroMemory(signal);
   if(!IsCanonicalMLVMatureState(mlv.State) || !mlv.IsValid) return false;
   if(mlv.Direction != DIR_BUY && mlv.Direction != DIR_SELL) return false;
   if(mlv.Timeframe != PERIOD_M15 || mlv.ConfirmationCandleTime <= 0) return false;
   if(mlv.FrozenMarkedBody <= 0) return false;

   signal.Type = SIGNAL_MHV;
   signal.Direction = mlv.Direction;
   signal.Valid = true;
   signal.Timeframe = mlv.Timeframe;
   signal.BarIndex = mlv.ConfirmationBar;
   signal.Timestamp = mlv.ConfirmationCandleTime;
   signal.CandleTime = mlv.ConfirmationCandleTime;
   signal.Close = mlv.ConfirmationClose;
   signal.Reason = mlv.Reason;
   return true;
}

//+------------------------------------------------------------------+
//| MODULE 10: CSM, CSD, eCSD                                        |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool DetectCSM(string pair, int timeframe, ENUM_DIRECTION direction, int shift)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return false;
   if(shift < 1) return false;

   double close = iClose(pair, timeframe, shift);
   if(close <= 0) return false;

   BollingerBand currentBand, previousBand;
   ZeroMemory(currentBand);
   ZeroMemory(previousBand);
   CalculateBollinger(pair, timeframe, shift, currentBand);
   CalculateBollinger(pair, timeframe, shift + 1, previousBand);

   if(currentBand.TOP_BB <= 0 || currentBand.MID_BB <= 0 ||
      currentBand.LOW_BB <= 0 || currentBand.Width <= 0 ||
      previousBand.TOP_BB <= 0 || previousBand.MID_BB <= 0 ||
      previousBand.LOW_BB <= 0 || previousBand.Width <= 0)
      return false;

   bool bbExpanding = (currentBand.Width > previousBand.Width);

   if(direction == DIR_BUY)
   {
      bool bbDirectional = (currentBand.MID_BB > previousBand.MID_BB &&
                            currentBand.TOP_BB > previousBand.TOP_BB);
      return (bbExpanding && bbDirectional && close > currentBand.TOP_BB);
   }

   bool bbDirectional = (currentBand.MID_BB < previousBand.MID_BB &&
                         currentBand.LOW_BB < previousBand.LOW_BB);
   return (bbExpanding && bbDirectional && close < currentBand.LOW_BB);
}

bool CandleBodyCrossesLevel(double open, double close, double level,
                            ENUM_DIRECTION direction)
{
   if(open <= 0 || close <= 0 || level <= 0) return false;

   if(direction == DIR_BUY)
      return (open <= level && close > level);

   if(direction == DIR_SELL)
      return (open >= level && close < level);

   return false;
}

bool DetectCSD(string pair, int timeframe, ENUM_DIRECTION direction, int shift,
               MovingAverage &ma, BollingerBand &band)
{
   double open = iOpen(pair, timeframe, shift);
   double close = iClose(pair, timeframe, shift);
   if(open <= 0 || close <= 0 || band.MID_BB <= 0) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   if(direction == DIR_BUY)
   {
      if(ma.MA5_High <= 0 || ma.MA10_High <= 0) return false;
      return CandleBodyCrossesLevel(open, close, ma.MA5_High, direction) &&
             CandleBodyCrossesLevel(open, close, ma.MA10_High, direction) &&
             CandleBodyCrossesLevel(open, close, band.MID_BB, direction);
   }

   if(ma.MA5_Low <= 0 || ma.MA10_Low <= 0) return false;
   return CandleBodyCrossesLevel(open, close, ma.MA5_Low, direction) &&
          CandleBodyCrossesLevel(open, close, ma.MA10_Low, direction) &&
          CandleBodyCrossesLevel(open, close, band.MID_BB, direction);
}

bool DetectECSD(string pair, int timeframe, ENUM_DIRECTION direction, int shift,
                MovingAverage &ma)
{
   double open = iOpen(pair, timeframe, shift);
   double close = iClose(pair, timeframe, shift);
   if(open <= 0 || close <= 0) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   if(direction == DIR_BUY)
   {
      if(ma.MA5_High <= 0 || ma.MA10_High <= 0) return false;
      return CandleBodyCrossesLevel(open, close, ma.MA5_High, direction) &&
             CandleBodyCrossesLevel(open, close, ma.MA10_High, direction);
   }

   if(ma.MA5_Low <= 0 || ma.MA10_Low <= 0) return false;
   return CandleBodyCrossesLevel(open, close, ma.MA5_Low, direction) &&
          CandleBodyCrossesLevel(open, close, ma.MA10_Low, direction);
}

//+------------------------------------------------------------------+
//| MODULE 11: TREND FUNCTIONS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

bool M11_ClassifyD1OwnerValues(double close1, double ma50_1, double ma50_2,
                               ENUM_D1_OWNER_STATE &ownerState,
                               ENUM_DIRECTION &direction)
{
   ownerState = D1_OWNER_UNRESOLVED;
   direction = DIR_NONE;
   if(close1 <= 0.0 || ma50_1 <= 0.0 || ma50_2 <= 0.0)
      return false;

   if(close1 > ma50_1 && ma50_1 > ma50_2)
   {
      ownerState = D1_OWNER_BUY_CONFIRMED;
      direction = DIR_BUY;
   }
   else if(close1 < ma50_1 && ma50_1 < ma50_2)
   {
      ownerState = D1_OWNER_SELL_CONFIRMED;
      direction = DIR_SELL;
   }
   else
   {
      ownerState = D1_TRANSITION;
      direction = DIR_NONE;
   }
   return true;
}

// Q9 P1 provenance adapter: reads an older fully closed D1 snapshot and routes
// it through the same M11 classifier used by the live owner.
bool M11_ClassifyD1OwnerAtShift(string pair, int shift,
                                ENUM_D1_OWNER_STATE &ownerState,
                                ENUM_DIRECTION &direction,
                                datetime &candleTime)
{
   ownerState = D1_OWNER_UNRESOLVED;
   direction = DIR_NONE;
   candleTime = 0;
   if(pair == "" || shift < 1) return false;

   datetime t = iTime(pair, PERIOD_D1, shift);
   double close1 = iClose(pair, PERIOD_D1, shift);
   double ma50_1 = EMA(pair, PERIOD_D1, EMA50_PERIOD, shift);
   double ma50_2 = EMA(pair, PERIOD_D1, EMA50_PERIOD, shift + 1);
   if(t <= 0) return false;
   if(!M11_ClassifyD1OwnerValues(close1, ma50_1, ma50_2,
                                 ownerState, direction))
      return false;

   candleTime = t;
   return true;
}

// Reconstructs the exact contiguous owner epoch after restart/recovery.
// If history cannot prove the older boundary, provenance stays unresolved.
bool M11_ResolveD1OwnerEpochStart(string pair, D1MajorTrendOwner &owner,
                                  datetime &epochStart)
{
   epochStart = 0;
   if(pair == "" || owner.SourceCandleTime <= 0 || !owner.IsValid)
      return false;

   int shift = iBarShift(pair, PERIOD_D1, owner.SourceCandleTime, true);
   int bars = iBars(pair, PERIOD_D1);
   if(shift < 1 || bars <= shift + 1) return false;

   epochStart = owner.SourceCandleTime;
   for(int s = shift + 1; s < bars - 1; s++)
   {
      ENUM_D1_OWNER_STATE priorState;
      ENUM_DIRECTION priorDirection;
      datetime priorCandle = 0;
      if(!M11_ClassifyD1OwnerAtShift(pair, s, priorState,
                                     priorDirection, priorCandle))
      {
         epochStart = 0;
         return false;
      }

      if(priorState != owner.State || priorDirection != owner.Direction)
         return (epochStart > 0);

      epochStart = priorCandle;
   }

   epochStart = 0;
   return false;
}

void SetD1OwnerUnresolved(PairState &state, string reason)
{
   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   owner.State = D1_OWNER_UNRESOLVED;
   owner.Direction = DIR_NONE;
   owner.SourceCandleTime = state.d1_data.candle_time;
   // Fail closed for NMJE provenance; M11 execution semantics are unchanged.
   owner.EpochStartCandleTime = 0;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;
   owner.Close1 = (state.d1_data.close > 0.0) ? state.d1_data.close : 0.0;
   owner.MA50_1 = (state.d1_data.ma[4] > 0.0) ? state.d1_data.ma[4] : 0.0;
   owner.MA50_2 = 0.0;
   owner.IsValid = false;
   owner.Reason = reason;
   state.d1_major_trend_owner = owner;
}

void TraceD1MajorTrendOwner(string pair, PairState &state)
{
   if(DebugLevel < DBG_SIGNAL) return;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   Print("[D1-03][OWNER] Pair=", pair,
         " Candle=", TimeToString(owner.SourceCandleTime),
         " Epoch=", TimeToString(owner.EpochStartCandleTime),
         " State=", EnumToString(owner.State),
         " Dir=", EnumToString(owner.Direction),
         " Close=", DoubleToString(owner.Close1, state.d1_data.digits),
         " MA50=", DoubleToString(owner.MA50_1, state.d1_data.digits),
         " PrevMA50=", DoubleToString(owner.MA50_2, state.d1_data.digits));
}

void UpdateD1MajorTrendOwner(string pair, PairState &state)
{
   // D1-03: M11 produces one atomic closed-D1 owner snapshot consumed by M15/M16.
   // Re-evaluate on every M15 processing cycle so refreshed broker history cannot
   // create a hybrid identity from cached owner state plus newer raw D1 values.
   if(!state.d1_data.is_valid ||
      !state.d1_data.is_closed ||
      state.d1_data.timeframe != PERIOD_D1 ||
      state.d1_data.candle_time <= 0 ||
      state.d1_data.barIndex < 1)
   {
      SetD1OwnerUnresolved(state, "Invalid/incomplete closed D1 snapshot");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   double currentMA50 = state.d1_data.ma[4];
   double previousMA50 = EMA(pair, PERIOD_D1, EMA50_PERIOD,
                             state.d1_data.barIndex + 1);

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   ENUM_D1_OWNER_STATE previousState = owner.State;
   ENUM_DIRECTION previousDirection = owner.Direction;
   datetime previousEpoch = owner.EpochStartCandleTime;

   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;
   owner.Close1 = state.d1_data.close;
   owner.MA50_1 = currentMA50;
   owner.MA50_2 = previousMA50;

   // Compatibility mirrors only. Downstream D1 identity authority is owner.*.
   state.current_daily_ema50 = owner.MA50_1;
   state.prev_daily_ema50 = owner.MA50_2;

   if(owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
   {
      SetD1OwnerUnresolved(state, "Required closed D1 MA50 history unavailable");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   ENUM_D1_OWNER_STATE classifiedState;
   ENUM_DIRECTION classifiedDirection;
   if(!M11_ClassifyD1OwnerValues(owner.Close1, owner.MA50_1, owner.MA50_2,
                                 classifiedState, classifiedDirection))
   {
      SetD1OwnerUnresolved(state, "Required closed D1 MA50 history unavailable");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   owner.IsValid = true;
   owner.State = classifiedState;
   owner.Direction = classifiedDirection;

   if(owner.State == D1_OWNER_BUY_CONFIRMED)
      owner.Reason = "Closed D1 above MA50 with rising MA50";
   else if(owner.State == D1_OWNER_SELL_CONFIRMED)
      owner.Reason = "Closed D1 below MA50 with falling MA50";
   else
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";

   // Q9 P1 provenance only. Preserve a proven same-owner epoch in memory.
   // On startup/recovery or owner transition, rebuild the exact contiguous
   // epoch from closed D1 history; failure leaves NMJE identity unresolved.
   if(previousEpoch > 0 && owner.State == previousState &&
      owner.Direction == previousDirection)
      owner.EpochStartCandleTime = previousEpoch;
   else
   {
      datetime resolvedEpoch = 0;
      if(M11_ResolveD1OwnerEpochStart(pair, owner, resolvedEpoch))
         owner.EpochStartCandleTime = resolvedEpoch;
      else
         owner.EpochStartCandleTime = 0;
   }

   state.d1_major_trend_owner = owner;
   TraceD1MajorTrendOwner(pair, state);
}


//+------------------------------------------------------------------+
//| MODULE 11J: D1 BBMA OPPORTUNITY JOURNEY (EXECUTION CONTEXT)     |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

string D1OpportunityFamilyText(ENUM_D1_OPPORTUNITY_FAMILY family)
{
   if(family == D1_OPP_EXTREME_TPW) return "EXT_TPW";
   if(family == D1_OPP_CSD) return "CSD";
   if(family == D1_OPP_RE_ENTRY) return "RE";
   if(family == D1_OPP_MOMENTUM_RETRACE) return "MOM_RE";
   return "NONE";
}

string D1AuthorityModeText(ENUM_D1_AUTHORITY_MODE mode)
{
   if(mode == D1_AUTH_STRATEGIC_OWNER) return "STRAT";
   if(mode == D1_AUTH_OPPORTUNITY) return "OPP";
   return "NONE";
}

void ResetD1OpportunityJourney(D1OpportunityJourney &journey, string reason)
{
   ZeroMemory(journey);
   journey.Family = D1_OPP_NONE;
   journey.Direction = DIR_NONE;
   journey.SourceSignal = SIGNAL_NONE;
   journey.Active = false;
   journey.Tactical = false;
   journey.TPWCompleted = false;
   journey.Reason = reason;
}

bool D1OpportunityIsConfirmedRE(ReEntryData &reEntry)
{
   return (reEntry.State == RE_STATE_CONFIRMED && reEntry.IsValid &&
           (reEntry.Direction == DIR_BUY || reEntry.Direction == DIR_SELL) &&
           reEntry.Timeframe == PERIOD_D1 && reEntry.ConfirmationCandle > 0);
}

bool SelectConfirmedD1OpportunityRE(ReEntryData &buyState, ReEntryData &sellState,
                                    ReEntryData &selected, bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = D1OpportunityIsConfirmedRE(buyState);
   bool sellValid = D1OpportunityIsConfirmedRE(sellState);
   ambiguous = (buyValid && sellValid);
   if(ambiguous || (!buyValid && !sellValid)) return false;
   selected = buyValid ? buyState : sellState;
   return true;
}

bool D1OpportunityExtremeMature(ExtremeLifecycleData &extreme)
{
   if(!extreme.IsValid || extreme.Timeframe != PERIOD_D1 ||
      extreme.ConfirmationCandleTime <= 0) return false;
   return (extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           extreme.Maturity == EXT_MAT_RETEST_PHASE ||
           extreme.Maturity == EXT_MAT_RETEST_READY);
}

bool SelectMatureD1OpportunityExtreme(ExtremeLifecycleData &buyState,
                                      ExtremeLifecycleData &sellState,
                                      ExtremeLifecycleData &selected,
                                      bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = D1OpportunityExtremeMature(buyState);
   bool sellValid = D1OpportunityExtremeMature(sellState);
   ambiguous = false;
   if(!buyValid && !sellValid) return false;
   if(buyValid && sellValid)
   {
      if(buyState.ConfirmationCandleTime == sellState.ConfirmationCandleTime)
      {
         ambiguous = true;
         return false;
      }
      selected = (buyState.ConfirmationCandleTime > sellState.ConfirmationCandleTime)
                 ? buyState : sellState;
      return true;
   }
   selected = buyValid ? buyState : sellState;
   return true;
}

bool IsD1TPWCompletionAtShift(string pair, ENUM_DIRECTION direction, int shift)
{
   if(pair == "" || shift < 1) return false;
   double high = iHigh(pair, PERIOD_D1, shift);
   double low = iLow(pair, PERIOD_D1, shift);
   if(high <= 0.0 || low <= 0.0 || high < low) return false;

   if(direction == DIR_SELL)
   {
      double ma5Low = BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift);
      double ma10Low = BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift);
      if(ma5Low <= 0.0 || ma10Low <= 0.0) return false;
      return (low <= ma5Low || low <= ma10Low);
   }

   if(direction == DIR_BUY)
   {
      double ma5High = BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift);
      double ma10High = BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift);
      if(ma5High <= 0.0 || ma10High <= 0.0) return false;
      return (high >= ma5High || high >= ma10High);
   }

   return false;
}

bool D1OpportunityTPWCompletedSince(string pair, ExtremeLifecycleData &extreme,
                                    TimeframeData &latestClosedD1)
{
   if(!D1OpportunityExtremeMature(extreme)) return true;
   if(!latestClosedD1.is_valid || !latestClosedD1.is_closed ||
      latestClosedD1.timeframe != PERIOD_D1 || latestClosedD1.barIndex < 1)
      return true;

   int confirmationShift = iBarShift(pair, PERIOD_D1,
                                     extreme.ConfirmationCandleTime, true);
   int latestShift = latestClosedD1.barIndex;
   if(confirmationShift < 1 || latestShift < 1) return true;
   if(confirmationShift < latestShift) return true;
   if(confirmationShift == latestShift) return false;

   for(int shift = confirmationShift - 1; shift >= latestShift; shift--)
   {
      datetime barTime = iTime(pair, PERIOD_D1, shift);
      if(barTime <= 0) return true; // fail closed on incomplete history

      double high = iHigh(pair, PERIOD_D1, shift);
      double low = iLow(pair, PERIOD_D1, shift);
      if(high <= 0.0 || low <= 0.0 || high < low) return true;

      // Invalid MA history is fail-closed for opportunity activation.
      if(extreme.Direction == DIR_SELL)
      {
         double ma5Low = BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift);
         double ma10Low = BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift);
         if(ma5Low <= 0.0 || ma10Low <= 0.0) return true;
      }
      else if(extreme.Direction == DIR_BUY)
      {
         double ma5High = BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift);
         double ma10High = BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift);
         if(ma5High <= 0.0 || ma10High <= 0.0) return true;
      }
      else return true;

      if(IsD1TPWCompletionAtShift(pair, extreme.Direction, shift)) return true;
   }
   return false;
}

void InstallD1OpportunityJourney(D1OpportunityJourney &journey, string pair,
                                 ENUM_D1_OPPORTUNITY_FAMILY family,
                                 ENUM_DIRECTION direction,
                                 ENUM_SIGNAL_TYPE sourceSignal,
                                 datetime sourceCandleTime,
                                 datetime activationTime,
                                 bool tactical,
                                 string reason)
{
   ResetD1OpportunityJourney(journey, reason);
   journey.Family = family;
   journey.Direction = direction;
   journey.SourceSignal = sourceSignal;
   journey.SourceCandleTime = sourceCandleTime;
   journey.ActivationTime = activationTime;
   journey.Active = true;
   journey.Tactical = tactical;
   journey.TPWCompleted = false;
   journey.CycleID = SHORT_HASH(pair + "|D1OPP|" + IntegerToString((int)family) + "|" +
                                IntegerToString((int)direction) + "|" +
                                IntegerToString((int)sourceCandleTime), 16);
   journey.Reason = reason;
}

bool DetectD1OpportunityCSD(string pair, TimeframeData &data,
                            BollingerBand &band, ENUM_DIRECTION direction)
{
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return false;
   MovingAverage ma;
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];
   return DetectCSD(pair, PERIOD_D1, direction, data.barIndex, ma, band);
}

bool DetectD1OpportunityECSDWatch(string pair, TimeframeData &data,
                                  ENUM_DIRECTION direction)
{
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return false;
   MovingAverage ma;
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];
   return DetectECSD(pair, PERIOD_D1, direction, data.barIndex, ma);
}

void UpdateD1OpportunityJourney(int pairIndex, BollingerBand &d1Band)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   string pair = g_pair_states[pairIndex].actual_symbol;
   TimeframeData d1 = g_pair_states[pairIndex].d1_data;
   D1OpportunityJourney previous = g_pair_states[pairIndex].d1_opportunity;
   D1OpportunityJourney next = previous;

   if(!d1.is_valid || !d1.is_closed || d1.timeframe != PERIOD_D1 ||
      d1.candle_time <= 0 || d1.barIndex < 1)
   {
      ResetD1OpportunityJourney(next, "Invalid closed D1 opportunity snapshot");
      g_pair_states[pairIndex].d1_opportunity = next;
      return;
   }

   // Existing family remains structurally owned until invalidated or superseded.
   if(next.Active && next.Family == D1_OPP_RE_ENTRY)
   {
      ReEntryData owner = (next.Direction == DIR_BUY)
                          ? g_pair_states[pairIndex].re_d1_buy_state
                          : g_pair_states[pairIndex].re_d1_sell_state;
      if(!D1OpportunityIsConfirmedRE(owner) ||
         owner.ConfirmationCandle != next.SourceCandleTime)
      {
         next.Active = false;
         next.Reason = "D1 Re-Entry opportunity owner no longer valid";
      }
   }

   if(next.Active && next.Family == D1_OPP_EXTREME_TPW)
   {
      ExtremeLifecycleData owner = (next.Direction == DIR_BUY)
                                   ? g_pair_states[pairIndex].extreme_d1_buy_lifecycle
                                   : g_pair_states[pairIndex].extreme_d1_sell_lifecycle;
      if(!D1OpportunityExtremeMature(owner) ||
         owner.ConfirmationCandleTime != next.SourceCandleTime)
      {
         next.Active = false;
         next.Reason = "D1 Extreme opportunity owner no longer valid";
      }
      else if(D1OpportunityTPWCompletedSince(pair, owner, d1))
      {
         next.Active = false;
         next.TPWCompleted = true;
         next.Reason = "D1 Extreme normal TP-Wajib structurally completed";
      }
   }

   // A confirmed strategic reversal retires a stale normal directional family.
   if(next.Active && !next.Tactical &&
      (g_pair_states[pairIndex].d1_major_trend_owner.State == D1_OWNER_BUY_CONFIRMED ||
       g_pair_states[pairIndex].d1_major_trend_owner.State == D1_OWNER_SELL_CONFIRMED) &&
      g_pair_states[pairIndex].d1_major_trend_owner.IsValid &&
      g_pair_states[pairIndex].d1_major_trend_owner.Direction != next.Direction &&
      g_pair_states[pairIndex].d1_major_trend_owner.SourceCandleTime >= next.SourceCandleTime)
   {
      next.Active = false;
      next.Reason = "Strategic owner reversed against prior D1 opportunity";
   }

   datetime baselineSource = next.SourceCandleTime;
   bool installed = false;

   // Strongest active family: confirmed D1 Re-Entry.
   ReEntryData d1RE;
   bool reAmbiguous = false;
   if(SelectConfirmedD1OpportunityRE(g_pair_states[pairIndex].re_d1_buy_state,
                                     g_pair_states[pairIndex].re_d1_sell_state,
                                     d1RE, reAmbiguous))
   {
      if(d1RE.ConfirmationCandle >= baselineSource)
      {
         datetime activation = (d1RE.EntryCandle > 0)
                               ? d1RE.EntryCandle
                               : d1RE.ConfirmationCandle + GetTimeframeSeconds(PERIOD_D1);
         InstallD1OpportunityJourney(next, pair, D1_OPP_RE_ENTRY,
                                     d1RE.Direction, SIGNAL_RE_ENTRY,
                                     d1RE.ConfirmationCandle, activation, false,
                                     "Confirmed D1 Re-Entry opportunity");
         installed = true;
      }
   }
   else if(reAmbiguous)
   {
      next.Active = false;
      next.Reason = "Ambiguous opposite confirmed D1 Re-Entry owners";
   }

   // Momentum outranks CSD on the same D1 source candle. It opens a wait-for-RE window.
   if(!installed && !reAmbiguous)
   {
      bool csmBuy = DetectCSM(pair, PERIOD_D1, DIR_BUY, d1.barIndex);
      bool csmSell = DetectCSM(pair, PERIOD_D1, DIR_SELL, d1.barIndex);
      if(csmBuy != csmSell && d1.candle_time >= baselineSource)
      {
         ENUM_DIRECTION dir = csmBuy ? DIR_BUY : DIR_SELL;
         InstallD1OpportunityJourney(next, pair, D1_OPP_MOMENTUM_RETRACE,
                                     dir, SIGNAL_CSM, d1.candle_time,
                                     d1.candle_time + GetTimeframeSeconds(PERIOD_D1),
                                     false,
                                     "D1 Momentum/CSM continuation; wait for fresh LTF Re-Entry");
         installed = true;
      }
   }

   if(!installed && !reAmbiguous)
   {
      bool csdBuy = DetectD1OpportunityCSD(pair, d1, d1Band, DIR_BUY);
      bool csdSell = DetectD1OpportunityCSD(pair, d1, d1Band, DIR_SELL);
      if(csdBuy != csdSell && d1.candle_time >= baselineSource)
      {
         ENUM_DIRECTION dir = csdBuy ? DIR_BUY : DIR_SELL;
         InstallD1OpportunityJourney(next, pair, D1_OPP_CSD,
                                     dir, SIGNAL_CSD, d1.candle_time,
                                     d1.candle_time + GetTimeframeSeconds(PERIOD_D1),
                                     false, "Confirmed D1 CSD opportunity");
         installed = true;
      }
   }

   // eCSD is intentionally WATCH ONLY. It may be logged but never installs a family.
   bool ecsdWatchBuy = DetectD1OpportunityECSDWatch(pair, d1, DIR_BUY);
   bool ecsdWatchSell = DetectD1OpportunityECSDWatch(pair, d1, DIR_SELL);
   if(DebugLevel >= DBG_SIGNAL && ecsdWatchBuy != ecsdWatchSell)
      Print("[D1-OPP-WATCH] ", pair, " eCSD=", ecsdWatchBuy ? "B" : "S",
            " Action=WATCH_ONLY");

   if(!installed && !reAmbiguous)
   {
      ExtremeLifecycleData extreme;
      bool extremeAmbiguous = false;
      if(SelectMatureD1OpportunityExtreme(
            g_pair_states[pairIndex].extreme_d1_buy_lifecycle,
            g_pair_states[pairIndex].extreme_d1_sell_lifecycle,
            extreme, extremeAmbiguous))
      {
         if(extreme.ConfirmationCandleTime >= baselineSource &&
            !D1OpportunityTPWCompletedSince(pair, extreme, d1))
         {
            InstallD1OpportunityJourney(next, pair, D1_OPP_EXTREME_TPW,
                                        extreme.Direction, SIGNAL_EXTREME,
                                        extreme.ConfirmationCandleTime,
                                        extreme.ConfirmationCandleTime + GetTimeframeSeconds(PERIOD_D1),
                                        true,
                                        "Reversal-confirmed D1 Extreme with active TP-Wajib path");
            installed = true;
         }
      }
      else if(extremeAmbiguous)
      {
         next.Active = false;
         next.Reason = "Ambiguous opposite mature D1 Extremes";
      }
   }

   next.LastProcessedD1CandleTime = d1.candle_time;
   g_pair_states[pairIndex].d1_opportunity = next;

   bool changed = (previous.Family != next.Family ||
                   previous.Direction != next.Direction ||
                   previous.SourceCandleTime != next.SourceCandleTime ||
                   previous.Active != next.Active ||
                   previous.TPWCompleted != next.TPWCompleted);
   if(changed || DebugLevel >= DBG_SIGNAL)
   {
      Print("[D1-OPP] ", pair,
            " F=", D1OpportunityFamilyText(next.Family),
            " DIR=", (next.Direction == DIR_BUY ? "B" : (next.Direction == DIR_SELL ? "S" : "-")),
            " ACTIVE=", next.Active ? "Y" : "N",
            " TACT=", next.Tactical ? "Y" : "N",
            " SRC=", TimeToString(next.SourceCandleTime),
            " ACT=", TimeToString(next.ActivationTime),
            " CYCLE=", next.CycleID,
            " R=", next.Reason);
   }
}

//+------------------------------------------------------------------+
//| MODULE 12: RE-ENTRY ENGINE                                       |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

bool GetReEntryMACluster(TimeframeData &data, ENUM_DIRECTION direction,
                         double &ma5, double &ma10)
{
   ma5 = 0;
   ma10 = 0;

   if(direction == DIR_BUY)
   {
      ma5 = data.ma[2];
      ma10 = data.ma[3];
   }
   else if(direction == DIR_SELL)
   {
      ma5 = data.ma[0];
      ma10 = data.ma[1];
   }
   else return false;

   return (ma5 > 0 && ma10 > 0);
}

bool HasReEntryMAClusterTouch(TimeframeData &data, ENUM_DIRECTION direction)
{
   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;
   if(data.close <= 0 || data.high <= 0 || data.low <= 0) return false;

   if(direction == DIR_BUY)
   {
      return (data.low <= MathMax(ma5, ma10) &&
              data.close >= ma5 && data.close >= ma10);
   }

   return (data.high >= MathMin(ma5, ma10) &&
           data.close <= ma5 && data.close <= ma10);
}

bool HasReEntryMA5OrMA50Touch(TimeframeData &data, ENUM_DIRECTION direction)
{
   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;
   if(data.ma[4] <= 0 || data.close <= 0 || data.high <= 0 || data.low <= 0) return false;

   if(direction == DIR_BUY)
   {
      bool ma5Touch = (data.low <= ma5 && data.close >= ma5);
      bool ma50Touch = (data.low <= data.ma[4] && data.close >= data.ma[4]);
      return (ma5Touch || ma50Touch);
   }

   bool ma5Touch = (data.high >= ma5 && data.close <= ma5);
   bool ma50Touch = (data.high >= data.ma[4] && data.close <= data.ma[4]);
   return (ma5Touch || ma50Touch);
}

void BuildReEntryDirectionInputs(TimeframeData &data, MovingAverage &ma,
                                 BollingerBand &band)
{
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];

   ZeroMemory(band);
   band.TOP_BB = data.bollinger[0];
   band.MID_BB = data.bollinger[1];
   band.LOW_BB = data.bollinger[2];
   band.Width = band.TOP_BB - band.LOW_BB;
}

ENUM_SIGNAL_TYPE DetectReEntryDirectionOwnerSignal(string pair,
                                                    ENUM_DIRECTION direction,
                                                    TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return SIGNAL_NONE;
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return SIGNAL_NONE;

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);

   // Momentum is the strongest same-candle classification. CSD is checked
   // before eCSD because a CSD candle also contains the eCSD MA crossing.
   if(DetectCSM(pair, data.timeframe, direction, data.barIndex)) return SIGNAL_CSM;
   if(DetectCSD(pair, data.timeframe, direction, data.barIndex, ma, band)) return SIGNAL_CSD;
   if(DetectECSD(pair, data.timeframe, direction, data.barIndex, ma)) return SIGNAL_ECSD;
   return SIGNAL_NONE;
}

bool DetectReEntry_Type2(string pair, ENUM_DIRECTION direction, TimeframeData &data,
                         bool &mostPowerful)
{
   mostPowerful = false;
   if(!EnableRE_Type2) return false;
   if(!data.is_valid || !data.is_closed || data.bollinger[1] <= 0) return false;

   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;

   bool powerful = IsNear(ma5, data.bollinger[1], pair) &&
                   IsNear(ma10, data.bollinger[1], pair);
   if(!powerful) return false;

   mostPowerful = (data.ma[4] > 0 && IsNear(data.ma[4], data.bollinger[1], pair));
   return true;
}

bool DetectReEntry_Type3(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type3) return false;
   if(!data.is_valid || !data.is_closed) return false;
   return DetectCSM(pair, data.timeframe, direction, data.barIndex);
}

bool DetectReEntry_Type4(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type4) return false;
   if(!data.is_valid || !data.is_closed) return false;

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);
   return DetectCSD(pair, data.timeframe, direction, data.barIndex, ma, band);
}

void ResetReEntryState(ReEntryData &reEntry, ENUM_DIRECTION direction, int timeframe)
{
   ZeroMemory(reEntry);
   reEntry.Type = RE_NONE;
   reEntry.State = RE_STATE_NONE;
   reEntry.Direction = direction;
   reEntry.Timeframe = timeframe;
   reEntry.Type1ContextState = TYPE1_CTX_NONE;
   reEntry.Type1OwnerSignal = SIGNAL_NONE;
}

void SetReEntrySnapshotLevels(ReEntryData &reEntry, TimeframeData &data)
{
   double ma5, ma10;
   GetReEntryMACluster(data, reEntry.Direction, ma5, ma10);
   reEntry.MA5_Level = ma5;
   reEntry.MA10_Level = ma10;
   reEntry.MA50_Level = data.ma[4];
   reEntry.MID_BB = data.bollinger[1];
}

void ConfirmReEntryState(ReEntryData &reEntry, TimeframeData &data, string reason)
{
   reEntry.State = RE_STATE_CONFIRMED;
   reEntry.ConfirmationBar = data.barIndex;
   reEntry.ConfirmationCandle = data.candle_time;

   // CORE-V2-F6 metadata correction only: the closed source-TF candle is the
   // validation candle; execution is eligible in the immediately following
   // source-TF candle.  No extra candle delay is introduced.
   int sourceTfSeconds = GetTimeframeSeconds(data.timeframe);
   reEntry.EntryCandle = (sourceTfSeconds > 0)
                         ? data.candle_time + sourceTfSeconds
                         : 0;
   reEntry.EntryPrice = data.close;
   reEntry.IsValid = true;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   SetReEntrySnapshotLevels(reEntry, data);
   reEntry.Reason = reason;
}

string ReEntryOwnerSignalName(ENUM_SIGNAL_TYPE type)
{
   if(type == SIGNAL_ECSD) return "eCSD";
   if(type == SIGNAL_CSD) return "CSD";
   if(type == SIGNAL_CSM) return "CSM";
   return "NONE";
}

void AdoptType1DirectionOwner(ReEntryData &reEntry, ENUM_DIRECTION direction,
                              TimeframeData &data, ENUM_SIGNAL_TYPE ownerSignal)
{
   ResetReEntryState(reEntry, direction, data.timeframe);
   reEntry.Type1ContextState = TYPE1_CTX_DIRECTION_OWNER;
   reEntry.Type1OwnerSignal = ownerSignal;
   reEntry.Type1OwnerCandleTime = data.candle_time;
   reEntry.Type1PreviousClose = data.close;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   reEntry.Reason = "Type1 owner established by source-valid " +
                    ReEntryOwnerSignalName(ownerSignal) +
                    "; awaiting structural pause/retrace";
}

bool IsReEntryMAClusterCloseSideFailure(TimeframeData &data,
                                      ENUM_DIRECTION direction)
{
   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return true;
   if(data.close <= 0) return true;

   // Penetration of one MA is not automatically failure. The pending setup
   // fails only when price closes clear through the full MA5/MA10 cluster.
   if(direction == DIR_BUY)
      return (data.close < MathMin(ma5, ma10));
   if(direction == DIR_SELL)
      return (data.close > MathMax(ma5, ma10));
   return true;
}

bool IsType1StructuralRetraceEvidence(ReEntryData &reEntry,
                                      TimeframeData &data,
                                      ENUM_DIRECTION direction)
{
   if(reEntry.Type1PreviousClose <= 0 || data.close <= 0) return false;

   // A valid MA-cluster interaction is itself structural retrace evidence.
   // Otherwise use direction-only close progression toward the cluster; no
   // pip/ATR/EMA threshold or fixed candle count is introduced.
   if(HasReEntryMAClusterTouch(data, direction)) return true;
   if(direction == DIR_BUY)  return (data.close < reEntry.Type1PreviousClose);
   if(direction == DIR_SELL) return (data.close > reEntry.Type1PreviousClose);
   return false;
}

void BeginType1RangingCandidate(ReEntryData &reEntry,
                                ENUM_DIRECTION direction,
                                TimeframeData &data)
{
   reEntry.Type = RE_TYPE_1;
   reEntry.State = RE_STATE_CANDIDATE;
   reEntry.Direction = direction;
   reEntry.Timeframe = data.timeframe;
   reEntry.StartBar = data.barIndex;
   reEntry.StartCandleTime = data.candle_time;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   reEntry.EntryPrice = 0;
   reEntry.EntryCandle = 0;
   reEntry.ConfirmationBar = 0;
   reEntry.ConfirmationCandle = 0;
   reEntry.ExpiryBar = 0;
   reEntry.ExpiryCandleTime = 0;
   reEntry.MinCandlesRequired = 0;
   reEntry.QualifyingCandles = 0;
   reEntry.IsValid = false;
   reEntry.Type1ContextState = TYPE1_CTX_RANGING;
   reEntry.Type1RangingStartCandleTime = data.candle_time;
   reEntry.Type1PreviousClose = data.close;
   SetReEntrySnapshotLevels(reEntry, data);
   reEntry.Reason = "Type1 structural ranging/retrace established; awaiting MA5/10 validation";
}

void StartSpecificReEntryCandidate(ReEntryData &reEntry,
                                   ENUM_RE_TYPE type,
                                   ENUM_DIRECTION direction,
                                   TimeframeData &data,
                                   bool mostPowerful)
{
   ResetReEntryState(reEntry, direction, data.timeframe);
   reEntry.Type = type;
   reEntry.State = RE_STATE_CANDIDATE;
   reEntry.StartBar = data.barIndex;
   reEntry.StartCandleTime = data.candle_time;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   // Legacy expiry fields remain zero for compatibility/telemetry only.
   // Type 2/3/4 validity is structural and must not use a fixed candle TTL.
   reEntry.ExpiryBar = 0;
   reEntry.ExpiryCandleTime = 0;
   reEntry.QualifyingCandles = 1;
   SetReEntrySnapshotLevels(reEntry, data);

   if(type == RE_TYPE_2)
   {
      reEntry.MinCandlesRequired = 3;
      reEntry.Reason = mostPowerful
                       ? "Type2 candidate: MA5/10 + MID BB + MA50 collision (1/3)"
                       : "Type2 candidate: MA5/10 + MID BB collision (1/3)";
   }
   else if(type == RE_TYPE_3_CSM)
   {
      reEntry.MinCandlesRequired = 1;
      reEntry.Reason = "Type3 candidate: CSM formed; awaiting retrace to MA5 or MA50";
   }
   else if(type == RE_TYPE_4_CSD)
   {
      reEntry.MinCandlesRequired = 1;
      reEntry.Reason = "Type4 candidate: CSD formed; awaiting retrace to MA5/10";
   }
}

bool TryStartSpecificReEntry(ReEntryData &reEntry, string pair,
                             ENUM_DIRECTION direction, TimeframeData &data)
{
   // Exact Type 3/4 precursor families own their setup before generic Type 1.
   if(DetectReEntry_Type3(pair, direction, data))
   {
      StartSpecificReEntryCandidate(reEntry, RE_TYPE_3_CSM, direction, data, false);
      return true;
   }

   if(DetectReEntry_Type4(pair, direction, data))
   {
      StartSpecificReEntryCandidate(reEntry, RE_TYPE_4_CSD, direction, data, false);
      return true;
   }

   bool mostPowerful = false;
   if(DetectReEntry_Type2(pair, direction, data, mostPowerful))
   {
      StartSpecificReEntryCandidate(reEntry, RE_TYPE_2, direction, data, mostPowerful);
      return true;
   }

   return false;
}

void ResetType1AndAdoptCurrentOwner(ReEntryData &reEntry,
                                    ENUM_DIRECTION direction,
                                    TimeframeData &data,
                                    ENUM_SIGNAL_TYPE sameDirectionSignal)
{
   ResetReEntryState(reEntry, direction, data.timeframe);
   if(sameDirectionSignal != SIGNAL_NONE)
      AdoptType1DirectionOwner(reEntry, direction, data, sameDirectionSignal);
}

ENUM_RE_STATE UpdateReEntryState(ReEntryData &reEntry, string pair,
                                 ENUM_DIRECTION direction, TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return RE_STATE_NONE;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return reEntry.State;

   if(reEntry.Direction != direction || reEntry.Timeframe != data.timeframe)
      ResetReEntryState(reEntry, direction, data.timeframe);

   // Do not process the same closed source-TF candle twice.
   if(reEntry.LastUpdateCandleTime > 0 &&
      data.candle_time <= reEntry.LastUpdateCandleTime)
      return reEntry.State;

   ENUM_DIRECTION oppositeDirection =
      (direction == DIR_BUY) ? DIR_SELL : DIR_BUY;
   ENUM_SIGNAL_TYPE sameSignal =
      DetectReEntryDirectionOwnerSignal(pair, direction, data);
   ENUM_SIGNAL_TYPE oppositeSignal =
      DetectReEntryDirectionOwnerSignal(pair, oppositeDirection, data);

   // Opposite source-valid direction/momentum atomically removes the old
   // Type-1 directional context. The opposite-direction state is managed by
   // its own ReEntryData owner in the parallel direction pass.
   if(oppositeSignal != SIGNAL_NONE &&
      (reEntry.State == RE_STATE_CANDIDATE ||
       reEntry.State == RE_STATE_CONFIRMED ||
       reEntry.Type1ContextState != TYPE1_CTX_NONE))
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
      return RE_STATE_NONE;
   }

   // Any confirmed Re-Entry remains valid only while the common MA5/10
   // close-side structure survives. This is structural invalidation, not age.
   if(reEntry.State == RE_STATE_CONFIRMED &&
      IsReEntryMAClusterCloseSideFailure(data, direction))
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
      return RE_STATE_NONE;
   }

   // Type 1 additionally tracks same-direction owner transfer/progression.
   if(reEntry.State == RE_STATE_CONFIRMED && reEntry.Type == RE_TYPE_1)
   {
      if(sameSignal == SIGNAL_CSM || sameSignal == SIGNAL_CSD)
      {
         // Exact Type 3/4 may take ownership immediately on their precursor.
         if(TryStartSpecificReEntry(reEntry, pair, direction, data))
            return reEntry.State;
         ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
         return reEntry.State;
      }

      if(sameSignal == SIGNAL_ECSD)
      {
         ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
         return reEntry.State;
      }

      reEntry.IsValid = true;
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      reEntry.Type1PreviousClose = data.close;
      return RE_STATE_CONFIRMED;
   }

   if(reEntry.State == RE_STATE_EXPIRED)
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
      // Continue on the same candle so a fresh structural owner is not lost.
   }

   if(reEntry.State == RE_STATE_NONE)
   {
      // Specific source-defined Re-Entry families own before generic Type 1.
      if(TryStartSpecificReEntry(reEntry, pair, direction, data))
         return reEntry.State;

      if(!EnableRE_Type1)
      {
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         return RE_STATE_NONE;
      }

      if(sameSignal != SIGNAL_NONE)
      {
         // eCSD/CSD/CSM is prior-move evidence only for Type 1; it is never
         // itself a Type-1 entry. Type3/4 were already given exact ownership.
         AdoptType1DirectionOwner(reEntry, direction, data, sameSignal);
         return RE_STATE_NONE;
      }

      if(reEntry.Type1ContextState != TYPE1_CTX_DIRECTION_OWNER)
      {
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         return RE_STATE_NONE;
      }

      if(IsReEntryMAClusterCloseSideFailure(data, direction))
      {
         ResetReEntryState(reEntry, direction, data.timeframe);
         return RE_STATE_NONE;
      }

      if(!IsType1StructuralRetraceEvidence(reEntry, data, direction))
      {
         reEntry.Type1PreviousClose = data.close;
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         return RE_STATE_NONE;
      }

      BeginType1RangingCandidate(reEntry, direction, data);

      // No fixed minimum candle count: if this structurally proven retrace
      // candle also reaches MA5/MA10 and closes on the valid side, it may
      // complete Type 1 immediately. This is not an MA-touch-only shortcut
      // because an earlier source-valid direction owner was mandatory.
      if(HasReEntryMAClusterTouch(data, direction))
      {
         ConfirmReEntryState(
            reEntry, data,
            (direction == DIR_BUY)
            ? "Type1 confirmed: prior BBMA direction -> structural ranging -> MA5/10 Low support retest"
            : "Type1 confirmed: prior BBMA direction -> structural ranging -> MA5/10 High resistance retest");
         return RE_STATE_CONFIRMED;
      }

      return RE_STATE_CANDIDATE;
   }

   if(reEntry.State == RE_STATE_CANDIDATE)
   {
      // General Re-Entry close-side validity applies to every type.
      if(IsReEntryMAClusterCloseSideFailure(data, direction))
      {
         ResetReEntryState(reEntry, direction, data.timeframe);
         return RE_STATE_NONE;
      }

      if(reEntry.Type == RE_TYPE_1)
      {
         // Structural ownership transfer has priority.
         if(sameSignal == SIGNAL_CSM || sameSignal == SIGNAL_CSD)
         {
            if(TryStartSpecificReEntry(reEntry, pair, direction, data))
               return reEntry.State;
            ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
            return reEntry.State;
         }

         if(sameSignal == SIGNAL_ECSD)
         {
            ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
            return reEntry.State;
         }

         if(HasReEntryMAClusterTouch(data, direction))
         {
            ConfirmReEntryState(
               reEntry, data,
               (direction == DIR_BUY)
               ? "Type1 confirmed: structural ranging retest at MA5/10 Low support"
               : "Type1 confirmed: structural ranging retest at MA5/10 High resistance");
            return RE_STATE_CONFIRMED;
         }

         // No fixed expiry and no invented minimum count. Keep the candidate
         // only while no structural invalidation/supersession has occurred.
         reEntry.Type1PreviousClose = data.close;
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         SetReEntrySnapshotLevels(reEntry, data);
         reEntry.Reason = "Type1 structural ranging active; awaiting MA5/10 support/resistance validation";
         return RE_STATE_CANDIDATE;
      }

      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      SetReEntrySnapshotLevels(reEntry, data);

      if(reEntry.Type == RE_TYPE_2)
      {
         bool mostPowerful = false;
         if(!DetectReEntry_Type2(pair, direction, data, mostPowerful))
         {
            ResetReEntryState(reEntry, direction, data.timeframe);
            return RE_STATE_NONE;
         }

         reEntry.QualifyingCandles++;
         if(reEntry.QualifyingCandles < reEntry.MinCandlesRequired)
         {
            reEntry.Reason = mostPowerful
               ? "Type2 candidate: MA5/10 + MID BB + MA50 collision"
               : "Type2 candidate: MA5/10 + MID BB collision";
            return RE_STATE_CANDIDATE;
         }

         if(!HasReEntryMAClusterTouch(data, direction)) return RE_STATE_CANDIDATE;

         ConfirmReEntryState(reEntry, data,
            mostPowerful
            ? "Type2 confirmed: 3-candle MA5/10 + MID BB + MA50 confluence"
            : "Type2 confirmed: 3-candle MA5/10 + MID BB confluence");
         return RE_STATE_CONFIRMED;
      }

      if(reEntry.Type == RE_TYPE_3_CSM)
      {
         if(!HasReEntryMA5OrMA50Touch(data, direction)) return RE_STATE_CANDIDATE;

         ConfirmReEntryState(reEntry, data,
            "Type3 confirmed: post-CSM retrace to MA5 or MA50");
         return RE_STATE_CONFIRMED;
      }

      if(reEntry.Type == RE_TYPE_4_CSD)
      {
         if(!HasReEntryMAClusterTouch(data, direction)) return RE_STATE_CANDIDATE;

         ConfirmReEntryState(reEntry, data,
            "Type4 confirmed: post-CSD retrace to MA5/10");
         return RE_STATE_CONFIRMED;
      }

      return RE_STATE_CANDIDATE;
   }

   if(reEntry.State == RE_STATE_CONFIRMED)
   {
      reEntry.IsValid = true;
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
   }

   return reEntry.State;
}

bool ExportConfirmedReEntrySignal(ReEntryData &reEntry, Signal &signal)
{
   ZeroMemory(signal);
   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return false;
   if(reEntry.ConfirmationCandle <= 0 || reEntry.EntryPrice <= 0) return false;

   signal.Type = SIGNAL_RE_ENTRY;
   signal.Direction = reEntry.Direction;
   signal.Valid = true;
   signal.Timeframe = reEntry.Timeframe;
   signal.Reason = reEntry.Reason;
   signal.BarIndex = reEntry.ConfirmationBar;
   signal.ExpiryBar = reEntry.ExpiryBar;
   signal.EntryPrice = reEntry.EntryPrice;
   signal.MA5_Level = reEntry.MA5_Level;
   signal.MA10_Level = reEntry.MA10_Level;
   signal.MA50_Level = reEntry.MA50_Level;
   signal.MID_BB = reEntry.MID_BB;
   signal.Timestamp = reEntry.ConfirmationCandle;
   signal.CandleTime = reEntry.ConfirmationCandle;
   signal.Close = reEntry.EntryPrice;
   return true;
}

//+------------------------------------------------------------------+
//| MODULE 12N: NESTED MTF JOURNEY ENGINE (N1 OBSERVATION ONLY)     |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

string NMJE_DirText(ENUM_DIRECTION direction)
{
   if(direction == DIR_BUY) return "B";
   if(direction == DIR_SELL) return "S";
   return "-";
}

string NMJE_RelationText(ENUM_NESTED_RELATION relation)
{
   if(relation == NESTED_BUILDING) return "BUILDING";
   if(relation == NESTED_SUPPORTING) return "SUPPORTING";
   if(relation == NESTED_ALIGNED) return "ALIGNED";
   if(relation == NESTED_CONFLICT) return "CONFLICT";
   if(relation == NESTED_UNRESOLVED) return "UNRESOLVED";
   return "N/A";
}

string NMJE_ParentText(ENUM_NESTED_PARENT_KIND kind)
{
   if(kind == NESTED_PARENT_H4_RE) return "H4_RE";
   if(kind == NESTED_PARENT_H4_OWNER) return "H4_OWNER";
   if(kind == NESTED_PARENT_D1_RE) return "D1_RE";
   if(kind == NESTED_PARENT_D1_OWNER) return "D1_OWNER";
   return "NONE";
}

string NMJE_REStateText(ENUM_RE_STATE state)
{
   if(state == RE_STATE_CANDIDATE) return "C";
   if(state == RE_STATE_CONFIRMED) return "F";
   if(state == RE_STATE_EXPIRED) return "X";
   return "N";
}

string NMJE_ExtremeStateText(ENUM_EXTREME_MATURITY state)
{
   if(state == EXT_MAT_RAW) return "R";
   if(state == EXT_MAT_REVERSAL_CONFIRMED) return "REV";
   if(state == EXT_MAT_RETEST_PHASE) return "RT";
   if(state == EXT_MAT_RETEST_READY) return "RDY";
   if(state == EXT_MAT_VOID) return "V";
   if(state == EXT_MAT_SUPERSEDED) return "S";
   return "N";
}

string NMJE_MLVStateText(ENUM_MLV_STATE state)
{
   if(state == MLV_PARENT_READY) return "P";
   if(state == MLV_TP_COMPLETE) return "TP";
   if(state == MLV_LOSS_DEVELOPING) return "L";
   if(state == MLV_FORMATION_ESTABLISHED) return "F";
   if(state == MLV_RETEST_COMPLETE) return "RT";
   if(state == MLV_DIRECTION_TAKEN) return "T";
   if(state == MLV_VOID) return "V";
   if(state == MLV_SUPERSEDED) return "S";
   return "N";
}

string NMJE_IdentityHash(string raw)
{
   if(raw == "") return "";
   return SHORT_HASH(raw, 16);
}

string NMJE_ReEntryEventID(string pair, ReEntryData &state)
{
   if(pair == "" || state.Timeframe <= 0 || state.StartCandleTime <= 0 ||
      (state.Direction != DIR_BUY && state.Direction != DIR_SELL) ||
      state.Type == RE_NONE)
      return "";
   string raw = "RE|" + pair + "|" + IntegerToString(state.Timeframe) + "|" +
                IntegerToString((int)state.Direction) + "|" +
                IntegerToString((int)state.Type) + "|" +
                IntegerToString((int)state.StartCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_ExtremeEventID(string pair, ExtremeLifecycleData &state)
{
   if(pair == "" || state.Timeframe <= 0 || state.RawCandleTime <= 0 ||
      (state.Direction != DIR_BUY && state.Direction != DIR_SELL))
      return "";
   string raw = "EXT|" + pair + "|" + IntegerToString(state.Timeframe) + "|" +
                IntegerToString((int)state.Direction) + "|" +
                IntegerToString((int)state.RawCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_MLVEventID(string pair, MLVData &state)
{
   if(pair == "" || state.Timeframe != PERIOD_M15 ||
      state.ParentRawCandleTime <= 0 || state.ParentConfirmationCandleTime <= 0 ||
      (state.Direction != DIR_BUY && state.Direction != DIR_SELL))
      return "";
   string raw = "MLV|" + pair + "|" + IntegerToString(PERIOD_M15) + "|" +
                IntegerToString((int)state.Direction) + "|" +
                IntegerToString((int)state.ParentRawCandleTime) + "|" +
                IntegerToString((int)state.ParentConfirmationCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_D1OwnerEventID(string pair, D1MajorTrendOwner &owner)
{
   if(pair == "" || !owner.IsValid || owner.EpochStartCandleTime <= 0)
      return "";
   string raw = "D1OWN|" + pair + "|" + IntegerToString((int)owner.State) + "|" +
                IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.EpochStartCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_H4OwnerEventID(string pair, H4DirectionalOwner &owner)
{
   if(pair == "" || owner.SourceCandleTime <= 0 ||
      owner.State != H4_OWNER_ACTIVE ||
      (owner.Direction != DIR_BUY && owner.Direction != DIR_SELL) ||
      owner.SourceSignal == SIGNAL_NONE)
      return "";
   string raw = "H4OWN|" + pair + "|" + IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.SourceSignal) + "|" +
                IntegerToString((int)owner.SourceCandleTime);
   return NMJE_IdentityHash(raw);
}

void NMJE_ResetNode(NestedTFNode &node, int timeframe)
{
   ZeroMemory(node);
   node.Timeframe = timeframe;
   node.StageType = SIGNAL_NONE;
   node.Direction = DIR_NONE;
   node.StateCode = 0;
   node.CandleTime = 0;
   node.Valid = false;
   node.Resolved = false;
   node.Label = "-";
   node.CanonicalEventID = "";
}

bool NMJE_IsConfirmedRE(ReEntryData &state)
{
   return (state.State == RE_STATE_CONFIRMED && state.IsValid &&
           (state.Direction == DIR_BUY || state.Direction == DIR_SELL) &&
           state.ConfirmationCandle > 0);
}

bool NMJE_IsCandidateRE(ReEntryData &state)
{
   return (state.State == RE_STATE_CANDIDATE && state.IsValid &&
           (state.Direction == DIR_BUY || state.Direction == DIR_SELL));
}

bool NMJE_IsExtremeActive(ExtremeLifecycleData &state)
{
   if(!state.IsValid) return false;
   return (state.Maturity == EXT_MAT_RAW ||
           state.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           state.Maturity == EXT_MAT_RETEST_PHASE ||
           state.Maturity == EXT_MAT_RETEST_READY);
}

bool NMJE_IsExtremeSupporting(ExtremeLifecycleData &state)
{
   if(!state.IsValid) return false;
   return (state.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           state.Maturity == EXT_MAT_RETEST_PHASE ||
           state.Maturity == EXT_MAT_RETEST_READY);
}

bool NMJE_IsMLVActive(MLVData &state)
{
   if(!state.IsValid) return false;
   return (state.State != MLV_NONE &&
           state.State != MLV_VOID &&
           state.State != MLV_SUPERSEDED);
}

bool NMJE_IsMLVSupporting(MLVData &state)
{
   if(!state.IsValid) return false;
   return (state.State == MLV_FORMATION_ESTABLISHED ||
           state.State == MLV_RETEST_COMPLETE ||
           state.State == MLV_DIRECTION_TAKEN);
}

bool NMJE_SelectConfirmedRE(ReEntryData &buyState, ReEntryData &sellState,
                            ReEntryData &selected, bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = NMJE_IsConfirmedRE(buyState);
   bool sellValid = NMJE_IsConfirmedRE(sellState);
   ambiguous = (buyValid && sellValid);
   if(ambiguous || (!buyValid && !sellValid)) return false;
   if(buyValid) selected = buyState;
   else selected = sellState;
   return true;
}

bool NMJE_SelectCandidateRE(ReEntryData &buyState, ReEntryData &sellState,
                            ReEntryData &selected, bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = NMJE_IsCandidateRE(buyState);
   bool sellValid = NMJE_IsCandidateRE(sellState);
   ambiguous = (buyValid && sellValid);
   if(ambiguous || (!buyValid && !sellValid)) return false;
   if(buyValid) selected = buyState;
   else selected = sellState;
   return true;
}

void NMJE_SetRENode(string pair, NestedTFNode &node, ReEntryData &state, bool resolved)
{
   node.StageType = SIGNAL_RE_ENTRY;
   node.Direction = state.Direction;
   node.StateCode = (int)state.State;
   node.CandleTime = (state.ConfirmationCandle > 0)
      ? state.ConfirmationCandle : state.StartCandleTime;
   node.Valid = state.IsValid;
   node.Resolved = resolved;
   node.CanonicalEventID = NMJE_ReEntryEventID(pair, state);
   node.Label = "RE:" + NMJE_REStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}

void NMJE_SetExtremeNode(string pair, NestedTFNode &node, ExtremeLifecycleData &state)
{
   node.StageType = SIGNAL_EXTREME;
   node.Direction = state.Direction;
   node.StateCode = (int)state.Maturity;
   node.CandleTime = (state.ConfirmationCandleTime > 0)
      ? state.ConfirmationCandleTime : state.RawCandleTime;
   node.Valid = state.IsValid;
   node.Resolved = false; // Extreme is pre-direction context for N1 lineage.
   node.CanonicalEventID = NMJE_ExtremeEventID(pair, state);
   node.Label = "EXT:" + NMJE_ExtremeStateText(state.Maturity) + "/" + NMJE_DirText(state.Direction);
}

void NMJE_SetMLVNode(string pair, NestedTFNode &node, MLVData &state)
{
   node.StageType = SIGNAL_MLV;
   node.Direction = state.Direction;
   node.StateCode = (int)state.State;
   node.CandleTime = (state.ConfirmationCandleTime > 0)
      ? state.ConfirmationCandleTime : state.LastUpdateCandleTime;
   node.Valid = state.IsValid;
   node.Resolved = false; // MHV/MLV is setup/context, not final direction authority.
   node.CanonicalEventID = NMJE_MLVEventID(pair, state);
   node.Label = "MHV:" + NMJE_MLVStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}


// N1.1 coverage-only helpers. Consume existing owner snapshots only.
datetime NMJE_REOverlayCandle(ReEntryData &state)
{
   if(state.ConfirmationCandle > 0) return state.ConfirmationCandle;
   return state.StartCandleTime;
}

datetime NMJE_ExtremeOverlayCandle(ExtremeLifecycleData &state)
{
   if(state.ConfirmationCandleTime > 0) return state.ConfirmationCandleTime;
   return state.RawCandleTime;
}

datetime NMJE_MLVOverlayCandle(MLVData &state)
{
   if(state.ConfirmationCandleTime > 0) return state.ConfirmationCandleTime;
   return state.LastUpdateCandleTime;
}

void NMJE_CaptureReEntryOverlay(NestedTFNode &node,
                                ReEntryData &buyState, ReEntryData &sellState)
{
   node.ReEntryBuyState = buyState.State;
   node.ReEntrySellState = sellState.State;
   node.ReEntryBuyValid = buyState.IsValid;
   node.ReEntrySellValid = sellState.IsValid;
   node.ReEntryBuyCandleTime = NMJE_REOverlayCandle(buyState);
   node.ReEntrySellCandleTime = NMJE_REOverlayCandle(sellState);
}

void NMJE_CaptureExtremeOverlay(NestedTFNode &node,
                                ExtremeLifecycleData &buyState,
                                ExtremeLifecycleData &sellState)
{
   node.ExtremeBuyMaturity = buyState.Maturity;
   node.ExtremeSellMaturity = sellState.Maturity;
   node.ExtremeBuyValid = buyState.IsValid;
   node.ExtremeSellValid = sellState.IsValid;
   node.ExtremeBuyCandleTime = NMJE_ExtremeOverlayCandle(buyState);
   node.ExtremeSellCandleTime = NMJE_ExtremeOverlayCandle(sellState);
}

void NMJE_CaptureMLVOverlay(NestedTFNode &node,
                            MLVData &buyState, MLVData &sellState)
{
   node.MLVBuyState = buyState.State;
   node.MLVSellState = sellState.State;
   node.MLVBuyValid = buyState.IsValid;
   node.MLVSellValid = sellState.IsValid;
   node.MLVBuyCandleTime = NMJE_MLVOverlayCandle(buyState);
   node.MLVSellCandleTime = NMJE_MLVOverlayCandle(sellState);
}

void NMJE_RefreshOverlayLabel(NestedTFNode &node)
{
   node.OverlayLabel =
      "RE=" + EnumToString(node.ReEntryBuyState) + "/" + EnumToString(node.ReEntrySellState) +
      "|X=" + EnumToString(node.ExtremeBuyMaturity) + "/" + EnumToString(node.ExtremeSellMaturity) +
      "|MHV=" + EnumToString(node.MLVBuyState) + "/" + EnumToString(node.MLVSellState);
}

void NMJE_CaptureD1OpportunityOverlay(PairState &state, NestedJourneyState &journey)
{
   D1OpportunityJourney opportunity = state.d1_opportunity;
   journey.D1OpportunityActive = opportunity.Active;
   journey.D1OpportunityFamily = opportunity.Family;
   journey.D1OpportunityDirection = opportunity.Direction;
   journey.D1OpportunitySourceSignal = opportunity.SourceSignal;
   journey.D1OpportunitySourceCandleTime = opportunity.SourceCandleTime;
   journey.D1OpportunityActivationTime = opportunity.ActivationTime;
   journey.D1OpportunityTactical = opportunity.Tactical;
   journey.D1OpportunityTPWCompleted = opportunity.TPWCompleted;
   journey.D1OpportunityCycleID = opportunity.CycleID;
}

void NMJE_PrintCoverageOverlay(NestedJourneyState &journey)
{
   if(DebugLevel < DBG_SIGNAL) return;
   Print("[N1.1-NMJE-COV] ", journey.Pair,
         " OPP=", D1OpportunityFamilyText(journey.D1OpportunityFamily), "/",
                    NMJE_DirText(journey.D1OpportunityDirection), "/",
                    (journey.D1OpportunityActive ? "Y" : "N"),
         " OC=", (journey.D1OpportunityCycleID == "" ? "-" : journey.D1OpportunityCycleID),
         " D1{", journey.D1Node.OverlayLabel, "}",
         " H4{", journey.H4Node.OverlayLabel, "}",
         " H1{", journey.H1Node.OverlayLabel, "}",
         " M15{", journey.M15Node.OverlayLabel, "}");
}

void NMJE_BuildD1Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_D1);
   NMJE_CaptureReEntryOverlay(node, state.re_d1_buy_state, state.re_d1_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_d1_buy_lifecycle, state.extreme_d1_sell_lifecycle);
   NMJE_RefreshOverlayLabel(node);
   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_d1_buy_state, state.re_d1_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(state.actual_symbol, node, selected, true);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:AMB";
      return;
   }

   if((state.d1_major_trend_owner.State == D1_OWNER_BUY_CONFIRMED ||
       state.d1_major_trend_owner.State == D1_OWNER_SELL_CONFIRMED) &&
      state.d1_major_trend_owner.IsValid)
   {
      node.Direction = state.d1_major_trend_owner.Direction;
      node.CandleTime = state.d1_major_trend_owner.SourceCandleTime;
      node.Valid = true;
      node.Resolved = true;
      node.CanonicalEventID = NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner);
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }

   if(state.d1_major_trend_owner.State == D1_TRANSITION)
   {
      node.Valid = true;
      node.Resolved = true;
      node.CanonicalEventID = NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner);
      node.Label = "TRANSITION";
      return;
   }

   node.Label = "UNRESOLVED";
}

void NMJE_BuildH4Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_H4);
   NMJE_CaptureReEntryOverlay(node, state.re_h4_buy_state, state.re_h4_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_h4_buy_lifecycle, state.extreme_h4_sell_lifecycle);
   NMJE_RefreshOverlayLabel(node);
   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(state.actual_symbol, node, selected, true);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:AMB";
      return;
   }

   if(NMJE_SelectCandidateRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(state.actual_symbol, node, selected, false);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:C:AMB";
      return;
   }

   if(state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
      state.h4_direction_owner.IsValid &&
      (state.h4_direction_owner.Direction == DIR_BUY ||
       state.h4_direction_owner.Direction == DIR_SELL))
   {
      node.StageType = state.h4_direction_owner.SourceSignal;
      node.Direction = state.h4_direction_owner.Direction;
      node.CandleTime = state.h4_direction_owner.SourceCandleTime;
      node.Valid = true;
      node.Resolved = true;
      node.CanonicalEventID = NMJE_H4OwnerEventID(state.actual_symbol, state.h4_direction_owner);
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }

   bool buyExtreme = NMJE_IsExtremeActive(state.extreme_h4_buy_lifecycle);
   bool sellExtreme = NMJE_IsExtremeActive(state.extreme_h4_sell_lifecycle);
   if(buyExtreme != sellExtreme)
   {
      if(buyExtreme) NMJE_SetExtremeNode(state.actual_symbol, node, state.extreme_h4_buy_lifecycle);
      else NMJE_SetExtremeNode(state.actual_symbol, node, state.extreme_h4_sell_lifecycle);
   }
   else if(buyExtreme && sellExtreme)
      node.Label = "EXT:AMB";
}

void NMJE_BuildH1Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_H1);
   NMJE_CaptureReEntryOverlay(node, state.re_h1_buy_state, state.re_h1_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_h1_buy_lifecycle, state.extreme_h1_sell_lifecycle);
   NMJE_RefreshOverlayLabel(node);
   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_h1_buy_state, state.re_h1_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(state.actual_symbol, node, selected, true);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:AMB";
      return;
   }

   if(NMJE_SelectCandidateRE(state.re_h1_buy_state, state.re_h1_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(state.actual_symbol, node, selected, false);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:C:AMB";
      return;
   }

   bool buyExtreme = NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle);
   bool sellExtreme = NMJE_IsExtremeActive(state.extreme_h1_sell_lifecycle);
   if(buyExtreme != sellExtreme)
   {
      if(buyExtreme) NMJE_SetExtremeNode(state.actual_symbol, node, state.extreme_h1_buy_lifecycle);
      else NMJE_SetExtremeNode(state.actual_symbol, node, state.extreme_h1_sell_lifecycle);
   }
   else if(buyExtreme && sellExtreme)
      node.Label = "EXT:AMB";
}

void NMJE_BuildM15Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_M15);
   NMJE_CaptureReEntryOverlay(node, state.re_m15_buy_state, state.re_m15_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_m15_buy_lifecycle, state.extreme_m15_sell_lifecycle);
   NMJE_CaptureMLVOverlay(node, state.mlv_buy_state, state.mlv_sell_state);
   NMJE_RefreshOverlayLabel(node);
   bool buyMLV = NMJE_IsMLVActive(state.mlv_buy_state);
   bool sellMLV = NMJE_IsMLVActive(state.mlv_sell_state);
   if(buyMLV != sellMLV)
   {
      if(buyMLV) NMJE_SetMLVNode(state.actual_symbol, node, state.mlv_buy_state);
      else NMJE_SetMLVNode(state.actual_symbol, node, state.mlv_sell_state);
   }
   else if(buyMLV && sellMLV)
      node.Label = "MHV:AMB";
}

bool NMJE_ResolveParent(PairState &state,
                        ENUM_NESTED_PARENT_KIND &kind,
                        int &timeframe,
                        ENUM_SIGNAL_TYPE &signalType,
                        ENUM_DIRECTION &direction,
                        datetime &anchor,
                        string &eventID,
                        string &reason)
{
   kind = NESTED_PARENT_NONE;
   timeframe = 0;
   signalType = SIGNAL_NONE;
   direction = DIR_NONE;
   anchor = 0;
   eventID = "";
   reason = "NO_PARENT";

   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous))
   {
      kind = NESTED_PARENT_H4_RE;
      timeframe = PERIOD_H4;
      signalType = SIGNAL_RE_ENTRY;
      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      eventID = NMJE_ReEntryEventID(state.actual_symbol, selected);
      reason = "H4_RE_PARENT";
      return true;
   }
   if(ambiguous)
   {
      reason = "H4_RE_AMBIGUOUS";
      return false;
   }

   if(state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
      state.h4_direction_owner.IsValid &&
      (state.h4_direction_owner.Direction == DIR_BUY ||
       state.h4_direction_owner.Direction == DIR_SELL))
   {
      kind = NESTED_PARENT_H4_OWNER;
      timeframe = PERIOD_H4;
      signalType = state.h4_direction_owner.SourceSignal;
      direction = state.h4_direction_owner.Direction;
      anchor = state.h4_direction_owner.SourceCandleTime;
      eventID = NMJE_H4OwnerEventID(state.actual_symbol, state.h4_direction_owner);
      reason = "H4_OWNER_PARENT";
      return true;
   }

   if(NMJE_SelectConfirmedRE(state.re_d1_buy_state, state.re_d1_sell_state,
                             selected, ambiguous))
   {
      kind = NESTED_PARENT_D1_RE;
      timeframe = PERIOD_D1;
      signalType = SIGNAL_RE_ENTRY;
      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      eventID = NMJE_ReEntryEventID(state.actual_symbol, selected);
      reason = "D1_RE_PARENT";
      return true;
   }
   if(ambiguous)
   {
      reason = "D1_RE_AMBIGUOUS";
      return false;
   }

   if((state.d1_major_trend_owner.State == D1_OWNER_BUY_CONFIRMED ||
       state.d1_major_trend_owner.State == D1_OWNER_SELL_CONFIRMED) &&
      state.d1_major_trend_owner.IsValid)
   {
      kind = NESTED_PARENT_D1_OWNER;
      timeframe = PERIOD_D1;
      signalType = SIGNAL_NONE;
      direction = state.d1_major_trend_owner.Direction;
      anchor = state.d1_major_trend_owner.SourceCandleTime;
      eventID = NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner);
      reason = "D1_OWNER_PARENT";
      return true;
   }

   return false;
}

bool NMJE_HasChildActivity(PairState &state)
{
   if(NMJE_IsCandidateRE(state.re_h1_buy_state) || NMJE_IsCandidateRE(state.re_h1_sell_state)) return true;
   if(NMJE_IsConfirmedRE(state.re_h1_buy_state) || NMJE_IsConfirmedRE(state.re_h1_sell_state)) return true;
   if(NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle) || NMJE_IsExtremeActive(state.extreme_h1_sell_lifecycle)) return true;
   if(NMJE_IsCandidateRE(state.re_m15_buy_state) || NMJE_IsCandidateRE(state.re_m15_sell_state)) return true;
   if(NMJE_IsConfirmedRE(state.re_m15_buy_state) || NMJE_IsConfirmedRE(state.re_m15_sell_state)) return true;
   if(NMJE_IsExtremeActive(state.extreme_m15_buy_lifecycle) || NMJE_IsExtremeActive(state.extreme_m15_sell_lifecycle)) return true;
   if(NMJE_IsMLVActive(state.mlv_buy_state) || NMJE_IsMLVActive(state.mlv_sell_state)) return true;
   return false;
}

string NMJE_BuildJourneyID(string pair, ENUM_NESTED_PARENT_KIND kind,
                           string parentEventID)
{
   if(pair == "" || parentEventID == "") return "";
   return "J2|" + pair + "|" + NMJE_ParentText(kind) + "|" + parentEventID;
}

bool NMJE_IsRelationDomainValue(ENUM_NESTED_RELATION relation)
{
   return (relation == NESTED_NOT_APPLICABLE ||
           relation == NESTED_BUILDING ||
           relation == NESTED_SUPPORTING ||
           relation == NESTED_ALIGNED ||
           relation == NESTED_CONFLICT ||
           relation == NESTED_UNRESOLVED);
}

bool NMJE_IsMaturityDomainValue(ENUM_NMJE_JOURNEY_MATURITY maturity)
{
   return (maturity >= NMJE_MATURITY_NONE &&
           maturity <= NMJE_MATURITY_UNRESOLVED);
}

string NMJE_MaturityText(ENUM_NMJE_JOURNEY_MATURITY maturity)
{
   if(maturity == NMJE_MATURITY_OWNER_ONLY) return "OWNER_ONLY";
   if(maturity == NMJE_MATURITY_EXTREME_DEVELOPING) return "EXTREME_DEVELOPING";
   if(maturity == NMJE_MATURITY_EXTREME_MATURE) return "EXTREME_MATURE";
   if(maturity == NMJE_MATURITY_MHV_DEVELOPING) return "MHV_DEVELOPING";
   if(maturity == NMJE_MATURITY_MHV_MATURE) return "MHV_MATURE";
   if(maturity == NMJE_MATURITY_DIRECTION_STAGE) return "DIRECTION_STAGE";
   if(maturity == NMJE_MATURITY_REENTRY_CANDIDATE) return "RE_CANDIDATE";
   if(maturity == NMJE_MATURITY_REENTRY_CONFIRMED) return "RE_CONFIRMED";
   if(maturity == NMJE_MATURITY_MOMENTUM_CONTINUATION) return "MOMENTUM_CONTINUATION";
   if(maturity == NMJE_MATURITY_OWNER_TRANSITION) return "OWNER_TRANSITION";
   if(maturity == NMJE_MATURITY_UNRESOLVED) return "UNRESOLVED";
   return "NONE";
}

string NMJE_LineageClassText(ENUM_NMJE_LINEAGE_EVENT_CLASS lineageClass)
{
   if(lineageClass == NMJE_LINEAGE_FIRST) return "FIRST";
   if(lineageClass == NMJE_LINEAGE_CONTINUATION) return "CONTINUATION";
   if(lineageClass == NMJE_LINEAGE_NEW_JOURNEY) return "NEW_JOURNEY";
   if(lineageClass == NMJE_LINEAGE_UNRESOLVED) return "UNRESOLVED";
   return "NONE";
}

ENUM_NMJE_JOURNEY_MATURITY NMJE_ClassifyJourneyMaturity(
   PairState &state, NestedJourneyState &journey)
{
   if(state.d1_major_trend_owner.State == D1_OWNER_UNRESOLVED)
      return NMJE_MATURITY_UNRESOLVED;
   if(state.d1_major_trend_owner.State == D1_TRANSITION)
      return NMJE_MATURITY_OWNER_TRANSITION;
   if(journey.Relation == NESTED_NOT_APPLICABLE && journey.Resolved)
      return NMJE_MATURITY_NONE;
   if(!journey.Valid || !journey.Resolved ||
      journey.Relation == NESTED_UNRESOLVED)
      return NMJE_MATURITY_UNRESOLVED;

   if(NMJE_IsConfirmedRE(state.re_h1_buy_state) ||
      NMJE_IsConfirmedRE(state.re_h1_sell_state) ||
      NMJE_IsConfirmedRE(state.re_m15_buy_state) ||
      NMJE_IsConfirmedRE(state.re_m15_sell_state))
      return NMJE_MATURITY_REENTRY_CONFIRMED;

   if(NMJE_IsCandidateRE(state.re_h1_buy_state) ||
      NMJE_IsCandidateRE(state.re_h1_sell_state) ||
      NMJE_IsCandidateRE(state.re_m15_buy_state) ||
      NMJE_IsCandidateRE(state.re_m15_sell_state))
      return NMJE_MATURITY_REENTRY_CANDIDATE;

   if(journey.ParentKind == NESTED_PARENT_H4_OWNER &&
      journey.ParentSignal == SIGNAL_CSM)
      return NMJE_MATURITY_MOMENTUM_CONTINUATION;
   if(journey.ParentKind == NESTED_PARENT_H4_OWNER &&
      (journey.ParentSignal == SIGNAL_CSD ||
       journey.ParentSignal == SIGNAL_ECSD))
      return NMJE_MATURITY_DIRECTION_STAGE;

   if(NMJE_IsMLVSupporting(state.mlv_buy_state) ||
      NMJE_IsMLVSupporting(state.mlv_sell_state))
      return NMJE_MATURITY_MHV_MATURE;
   if(NMJE_IsMLVActive(state.mlv_buy_state) ||
      NMJE_IsMLVActive(state.mlv_sell_state))
      return NMJE_MATURITY_MHV_DEVELOPING;

   if(NMJE_IsExtremeSupporting(state.extreme_h1_buy_lifecycle) ||
      NMJE_IsExtremeSupporting(state.extreme_h1_sell_lifecycle) ||
      NMJE_IsExtremeSupporting(state.extreme_m15_buy_lifecycle) ||
      NMJE_IsExtremeSupporting(state.extreme_m15_sell_lifecycle))
      return NMJE_MATURITY_EXTREME_MATURE;
   if(NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle) ||
      NMJE_IsExtremeActive(state.extreme_h1_sell_lifecycle) ||
      NMJE_IsExtremeActive(state.extreme_m15_buy_lifecycle) ||
      NMJE_IsExtremeActive(state.extreme_m15_sell_lifecycle))
      return NMJE_MATURITY_EXTREME_DEVELOPING;

   if(journey.ParentEventID != "" && journey.JourneyID != "")
      return NMJE_MATURITY_OWNER_ONLY;
   return NMJE_MATURITY_NONE;
}

string NMJE_BuildRelationEvidenceID(PairState &state,
                                    NestedJourneyState &journey)
{
   if(!journey.Valid || !journey.Resolved ||
      journey.ParentEventID == "" || journey.JourneyID == "" ||
      !NMJE_IsRelationDomainValue(journey.Relation))
      return "";

   // Waiting/developing states without a resolved child identity are deliberately
   // not promoted to last-proven evidence.
   if(journey.Reason == "PARENT_WAITING_FOR_CHILD" ||
      journey.Reason == "LTF_STRUCTURE_BUILDING")
      return "";

   string evidence = "REL|" + journey.Pair + "|" + journey.JourneyID + "|" +
                     journey.ParentEventID + "|" +
                     IntegerToString((int)journey.Relation) + "|" + journey.Reason;
   if(journey.H1Node.CanonicalEventID != "")
      evidence += "|H1:" + journey.H1Node.CanonicalEventID;
   if(journey.M15Node.CanonicalEventID != "")
      evidence += "|M15:" + journey.M15Node.CanonicalEventID;
   if(journey.H4Node.CanonicalEventID != "")
      evidence += "|H4:" + journey.H4Node.CanonicalEventID;
   if(journey.D1Node.CanonicalEventID != "")
      evidence += "|D1:" + journey.D1Node.CanonicalEventID;

   // Parent/owner based relation reasons are themselves attributable to the
   // already-resolved canonical parent identity.
   if(StringLen(evidence) <= 0) return "";
   return NMJE_IdentityHash(evidence);
}

void NMJE_ApplyJourneyProvenanceStability(PairState &state,
                                          NestedJourneyState &previous,
                                          NestedJourneyState &journey)
{
   journey.StableRelation = journey.Relation;
   journey.RelationEvidenceID = NMJE_BuildRelationEvidenceID(state, journey);
   journey.StableRelationEvidenceID = journey.RelationEvidenceID;
   journey.ParentTransitioned = false;
   journey.PreviousParentEventID = "";
   journey.StabilityReason = "CURRENT_RAW_RELATION";

   bool previousHasParent =
      (previous.ParentEventID != "" && previous.JourneyID != "");
   bool currentHasParent =
      (journey.ParentEventID != "" && journey.JourneyID != "");

   if(previousHasParent && !currentHasParent)
   {
      journey.ParentTransitioned = true;
      journey.PreviousParentEventID = previous.ParentEventID;
      journey.StableRelationEvidenceID = "";
      journey.StabilityReason = "PARENT_CONTEXT_LOST";
      return;
   }
   if(!currentHasParent)
   {
      journey.StableRelationEvidenceID = "";
      journey.StabilityReason = "NO_CURRENT_PARENT";
      return;
   }

   bool sameParent =
      (previousHasParent &&
       previous.ParentKind == journey.ParentKind &&
       previous.ParentEventID == journey.ParentEventID &&
       previous.JourneyID == journey.JourneyID);

   if(previousHasParent && !sameParent)
   {
      journey.ParentTransitioned = true;
      journey.PreviousParentEventID = previous.ParentEventID;
      journey.StabilityReason = (journey.RelationEvidenceID != "")
         ? "PARENT_TRANSITION_CURRENT_EVIDENCE"
         : "PARENT_TRANSITION_RAW_INIT";
      return;
   }

   if(journey.RelationEvidenceID != "")
   {
      journey.StabilityReason = "CURRENT_CANONICAL_EVIDENCE";
      return;
   }

   if(sameParent && previous.StableRelationEvidenceID != "" &&
      NMJE_IsRelationDomainValue(previous.StableRelation))
   {
      journey.StableRelation = previous.StableRelation;
      journey.StableRelationEvidenceID = previous.StableRelationEvidenceID;
      journey.StabilityReason = "HOLD_LAST_PROVEN_RELATION";
      return;
   }
   journey.StabilityReason = "NO_PRIOR_PROVEN_RELATION";
}

void NMJE_ApplyStrictJourneyLineage(NestedJourneyState &previous,
                                    NestedJourneyState &journey)
{
   journey.LineageClass = NMJE_LINEAGE_NONE;
   journey.LineageRootEventID = "";
   journey.PreviousLineageRootEventID = "";
   journey.LineageReason = "NO_VALID_PARENT";

   if(!journey.Valid || !journey.Resolved ||
      journey.ParentEventID == "" || journey.JourneyID == "")
   {
      if(journey.Relation == NESTED_UNRESOLVED)
      {
         journey.LineageClass = NMJE_LINEAGE_UNRESOLVED;
         journey.LineageReason = "CURRENT_PARENT_UNRESOLVED";
      }
      return;
   }

   // Strict-A: canonical ParentEventID is the exact lineage root.
   journey.LineageRootEventID = journey.ParentEventID;
   bool previousCanonical =
      (previous.Valid && previous.Resolved &&
       previous.ParentEventID != "" && previous.JourneyID != "");

   if(previousCanonical &&
      (previous.ParentEventID != journey.ParentEventID ||
       previous.JourneyID != journey.JourneyID))
   {
      journey.LineageClass = NMJE_LINEAGE_NEW_JOURNEY;
      journey.PreviousLineageRootEventID = previous.ParentEventID;
      journey.LineageReason = "CANONICAL_JOURNEY_TRANSITION";
      return;
   }

   // CONTINUATION is intentionally never inferred: current owner exposes no
   // distinct source-owned continuation/re-arm event identity.
   journey.LineageClass = NMJE_LINEAGE_FIRST;
   journey.LineageReason = previousCanonical
      ? "CANONICAL_ROOT_STILL_CURRENT" : "CANONICAL_ROOT_CURRENT";
}

void NMJE_PrintP8StabilityShadow(NestedJourneyState &journey)
{
   string message = "[Q9-P8-STABILITY] Pair=" + journey.Pair +
                    " REL=" + NMJE_RelationText(journey.Relation) +
                    " SREL=" + NMJE_RelationText(journey.StableRelation) +
                    " REH=" + (journey.RelationEvidenceID == "" ? "-" :
                               SHORT_HASH(journey.RelationEvidenceID)) +
                    " SEH=" + (journey.StableRelationEvidenceID == "" ? "-" :
                               SHORT_HASH(journey.StableRelationEvidenceID)) +
                    " PTR=" + (journey.ParentTransitioned ? "Y" : "N") +
                    " PPEH=" + (journey.PreviousParentEventID == "" ? "-" :
                                SHORT_HASH(journey.PreviousParentEventID)) +
                    " MAT=" + NMJE_MaturityText(journey.Maturity) +
                    " LC=" + NMJE_LineageClassText(journey.LineageClass) +
                    " LRH=" + (journey.LineageRootEventID == "" ? "-" :
                               SHORT_HASH(journey.LineageRootEventID)) +
                    " PLRH=" + (journey.PreviousLineageRootEventID == "" ? "-" :
                                SHORT_HASH(journey.PreviousLineageRootEventID)) +
                    " Authority=NONE";
   ObserverPrintChanged("Q9P8|" + journey.Pair, message);
}

void NMJE_FinalizeJourneyMetadata(int pairIndex,
                                  NestedJourneyState &previous,
                                  NestedJourneyState &journey)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   NMJE_ApplyJourneyProvenanceStability(g_pair_states[pairIndex], previous, journey);
   NMJE_ApplyStrictJourneyLineage(previous, journey);
   journey.Maturity = NMJE_ClassifyJourneyMaturity(g_pair_states[pairIndex], journey);
   NMJE_PrintP8StabilityShadow(journey);
}

int NMJE_CountStructureStages(int mask)
{
   int count = 0;
   int bits[6] = {NMJE_STRUCTURE_EXTREME, NMJE_STRUCTURE_TPW, NMJE_STRUCTURE_MHV,
                  NMJE_STRUCTURE_DIRECTION, NMJE_STRUCTURE_REENTRY,
                  NMJE_STRUCTURE_MOMENTUM};
   for(int i=0; i<6; i++) if((mask & bits[i]) != 0) count++;
   return count;
}

int NMJE_BuildStructurePrefixMask(int mask)
{
   int bits[6] = {NMJE_STRUCTURE_EXTREME, NMJE_STRUCTURE_TPW, NMJE_STRUCTURE_MHV,
                  NMJE_STRUCTURE_DIRECTION, NMJE_STRUCTURE_REENTRY,
                  NMJE_STRUCTURE_MOMENTUM};
   int prefix = 0;
   for(int i=0; i<6; i++)
   {
      if((mask & bits[i]) == 0) break;
      prefix |= bits[i];
   }
   return prefix;
}

bool NMJE_IsStructuralDensityValid(NMJEStructuralDensityState &density)
{
   if(!density.Present) return true;
   if(!density.Valid) return false;
   if(density.StageMask < 0 || density.StageMask > 63) return false;
   if(density.PrefixMask < 0 || density.PrefixMask > 63) return false;
   if((density.PrefixMask & density.StageMask) != density.PrefixMask) return false;
   if(density.StageCount != NMJE_CountStructureStages(density.StageMask)) return false;
   return true;
}

void NMJE_AddComponentStructureStages(ComponentIdentity &component, int &mask)
{
   if(component.ComponentType == SIGNAL_EXTREME)
      mask |= NMJE_STRUCTURE_EXTREME;
   else if(component.ComponentType == SIGNAL_MLV)
      mask |= (NMJE_STRUCTURE_EXTREME | NMJE_STRUCTURE_TPW | NMJE_STRUCTURE_MHV);
   else if(component.ComponentType == SIGNAL_RE_ENTRY)
      mask |= NMJE_STRUCTURE_REENTRY;
}

int NMJE_BuildResolvedJourneyStructureMask(PairState &state,
                                           NestedJourneyState &journey,
                                           ENUM_DIRECTION direction)
{
   if(!journey.Valid || !journey.Resolved ||
      journey.ParentDirection != direction)
      return 0;
   int mask = 0;

   ExtremeLifecycleData xh1 = (direction == DIR_BUY)
      ? state.extreme_h1_buy_lifecycle : state.extreme_h1_sell_lifecycle;
   ExtremeLifecycleData xm15 = (direction == DIR_BUY)
      ? state.extreme_m15_buy_lifecycle : state.extreme_m15_sell_lifecycle;
   MLVData mlv = (direction == DIR_BUY) ? state.mlv_buy_state : state.mlv_sell_state;
   ReEntryData reh1 = (direction == DIR_BUY) ? state.re_h1_buy_state : state.re_h1_sell_state;
   ReEntryData rem15 = (direction == DIR_BUY) ? state.re_m15_buy_state : state.re_m15_sell_state;

   if(NMJE_IsExtremeActive(xh1) || NMJE_IsExtremeActive(xm15))
      mask |= NMJE_STRUCTURE_EXTREME;
   if(NMJE_IsMLVActive(mlv))
   {
      mask |= (NMJE_STRUCTURE_EXTREME | NMJE_STRUCTURE_TPW | NMJE_STRUCTURE_MHV);
      if(mlv.State == MLV_DIRECTION_TAKEN) mask |= NMJE_STRUCTURE_DIRECTION;
   }
   if(NMJE_IsConfirmedRE(reh1) || NMJE_IsConfirmedRE(rem15))
      mask |= NMJE_STRUCTURE_REENTRY;

   if(journey.ParentKind == NESTED_PARENT_H4_OWNER)
   {
      if(journey.ParentSignal == SIGNAL_CSD || journey.ParentSignal == SIGNAL_ECSD)
         mask |= NMJE_STRUCTURE_DIRECTION;
      if(journey.ParentSignal == SIGNAL_CSM)
         mask |= NMJE_STRUCTURE_MOMENTUM;
   }
   if(journey.ParentKind == NESTED_PARENT_H4_RE ||
      journey.ParentKind == NESTED_PARENT_D1_RE)
      mask |= NMJE_STRUCTURE_REENTRY;
   return mask;
}

void NMJE_FinalizeStructuralDensity(int mask, NMJEStructuralDensityState &density)
{
   ZeroMemory(density);
   density.Present = true;
   density.Valid = true;
   density.StageMask = mask;
   density.PrefixMask = NMJE_BuildStructurePrefixMask(mask);
   density.StageCount = NMJE_CountStructureStages(mask);
   density.Reason = (mask == 0) ? "NO_PROVEN_STAGE" : "CANONICAL_STAGE_PRESENCE";
}

void NMJE_BuildCandidateStructuralDensity(PairState &state,
                                          NestedJourneyState &journey,
                                          ValidatedSequenceCandidate &candidate,
                                          NMJEStructuralDensityState &density)
{
   ZeroMemory(density);
   if(!candidate.Valid)
   {
      density.Reason = "CANDIDATE_INVALID";
      return;
   }
   int mask = 0;
   for(int i=0; i<candidate.ComponentCount && i<3; i++)
      NMJE_AddComponentStructureStages(candidate.Components[i], mask);
   mask |= NMJE_BuildResolvedJourneyStructureMask(state, journey,
                                                   candidate.Direction);
   NMJE_FinalizeStructuralDensity(mask, density);
}

void NMJE_PrintStructuralDensityShadow(int pairIndex,
                                       ValidatedSequenceCandidate &candidates[],
                                       int count,
                                       PairState &pairState)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count || count <= 0) return;
   NestedJourneyState journey = g_nested_journeys[pairIndex];
   for(int i=0; i<count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      NMJEStructuralDensityState density;
      NMJE_BuildCandidateStructuralDensity(pairState, journey,
                                           candidates[i], density);
      bool d1Allowed = IsCandidateAllowedByD1Owner(candidates[i], pairState);
      string seq = (candidates[i].SequenceHash == "" ? "-" :
                    candidates[i].SequenceHash);
      string message = "[Q9-P7-DENSITY] Pair=" + pairState.actual_symbol +
                       " Seq=" + seq +
                       " Sig=" + EnumToString(candidates[i].SequenceType) +
                       " Dir=" + NMJE_DirText(candidates[i].Direction) +
                       " D1Allowed=" + (d1Allowed ? "Y" : "N") +
                       " Mask=" + IntegerToString(density.StageMask) +
                       " Prefix=" + IntegerToString(density.PrefixMask) +
                       " Count=" + IntegerToString(density.StageCount) +
                       " JH=" + (journey.JourneyID == "" ? "-" :
                                 SHORT_HASH(journey.JourneyID)) +
                       " PEH=" + (journey.ParentEventID == "" ? "-" :
                                  SHORT_HASH(journey.ParentEventID)) +
                       " Authority=NONE";
      ObserverPrintChanged("Q9P7|" + pairState.actual_symbol + "|" + seq, message);
   }
}

void NMJE_BuildDecisionStructuralDensity(PairState &state,
                                         NestedJourneyState &journey,
                                         BBMA_Decision &decision,
                                         NMJEStructuralDensityState &density)
{
   ZeroMemory(density);
   if(!decision.Valid || decision.DecisionState != DEC_VALIDATED)
   {
      density.Reason = "DECISION_NOT_VALIDATED";
      return;
   }
   int mask = 0;
   for(int i=0; i<decision.ComponentCount && i<3; i++)
      NMJE_AddComponentStructureStages(decision.Components[i], mask);
   mask |= NMJE_BuildResolvedJourneyStructureMask(state, journey, decision.Direction);
   NMJE_FinalizeStructuralDensity(mask, density);
}

void NMJE_FreezeValidatedDecisionAttribution(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!decision.Valid || decision.DecisionState != DEC_VALIDATED) return;

   NestedJourneyState journey = g_nested_journeys[pairIndex];
   decision.NMJESnapshotPresent = true;
   decision.NMJEJourneyID = journey.JourneyID;
   decision.NMJEParentEventID = journey.ParentEventID;
   decision.NMJERelation = journey.Relation;
   decision.NMJEStableRelation = journey.StableRelation;
   decision.NMJEStableRelationEvidenceID = journey.StableRelationEvidenceID;
   decision.NMJEParentTransitioned = journey.ParentTransitioned;
   decision.NMJEPreviousParentEventID = journey.PreviousParentEventID;
   decision.NMJELineageClass = journey.LineageClass;
   decision.NMJELineageRootEventID = journey.LineageRootEventID;
   decision.NMJEPreviousLineageRootEventID = journey.PreviousLineageRootEventID;
   decision.NMJEMaturity = journey.Maturity;
   decision.NMJEUpdateCandleTime = journey.UpdateCandleTime;
   decision.NMJEM5SnapshotPresent = journey.M5ShadowPresent;
   decision.NMJEM5ShadowEventID = journey.M5ShadowEventID;
   decision.NMJEM5ShadowClosedCandleTime = journey.M5ShadowClosedCandleTime;
   decision.NMJEM5SemanticResolved = journey.M5SemanticResolved;
   decision.NMJEM5DiagnosticRelation = journey.M5DiagnosticRelation;
   decision.NMJEM5DiagnosticReason = journey.M5DiagnosticReason;
   NMJE_BuildDecisionStructuralDensity(g_pair_states[pairIndex], journey,
                                       decision, decision.NMJEStructureDensity);

   Print("[Q9-P4PLUS-DEC] Pair=", decision.Pair,
         " DIDH=", SHORT_HASH(decision.DecisionID),
         " REL=", NMJE_RelationText(decision.NMJERelation),
         " SREL=", NMJE_RelationText(decision.NMJEStableRelation),
         " MAT=", NMJE_MaturityText(decision.NMJEMaturity),
         " LC=", NMJE_LineageClassText(decision.NMJELineageClass),
         " SEH=", (decision.NMJEStableRelationEvidenceID == "" ? "-" :
                    SHORT_HASH(decision.NMJEStableRelationEvidenceID)),
         " PTR=", decision.NMJEParentTransitioned ? "Y" : "N",
         " PPEH=", (decision.NMJEPreviousParentEventID == "" ? "-" :
                     SHORT_HASH(decision.NMJEPreviousParentEventID)),
         " LRH=", (decision.NMJELineageRootEventID == "" ? "-" :
                    SHORT_HASH(decision.NMJELineageRootEventID)),
         " PLRH=", (decision.NMJEPreviousLineageRootEventID == "" ? "-" :
                     SHORT_HASH(decision.NMJEPreviousLineageRootEventID)),
         " SD=", IntegerToString(decision.NMJEStructureDensity.StageMask),
         " M5=", decision.NMJEM5SnapshotPresent ? "Y" : "N",
         " M5SEM=", decision.NMJEM5SemanticResolved ? "Y" : "N",
         " Authority=NONE");
}

void UpdateNestedJourneyObservation(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;

   NestedJourneyState previous = g_nested_journeys[pairIndex];
   NestedJourneyState journey;
   ZeroMemory(journey);
   journey.Pair = g_pair_states[pairIndex].actual_symbol;
   journey.Relation = NESTED_NOT_APPLICABLE;
   journey.ParentKind = NESTED_PARENT_NONE;
   journey.ParentSignal = SIGNAL_NONE;
   journey.ParentDirection = DIR_NONE;
   journey.StrategicDirection = DIR_NONE;
   journey.UpdateCandleTime = g_pair_states[pairIndex].m15_data.candle_time;
   journey.Reason = "NO_ACTIVE_JOURNEY";
   NMJE_CaptureD1OpportunityOverlay(g_pair_states[pairIndex], journey);

   NMJE_BuildD1Node(g_pair_states[pairIndex], journey.D1Node);
   NMJE_BuildH4Node(g_pair_states[pairIndex], journey.H4Node);
   NMJE_BuildH1Node(g_pair_states[pairIndex], journey.H1Node);
   NMJE_BuildM15Node(g_pair_states[pairIndex], journey.M15Node);

   ENUM_D1_OWNER_STATE d1State = g_pair_states[pairIndex].d1_major_trend_owner.State;
   if(d1State == D1_OWNER_BUY_CONFIRMED || d1State == D1_OWNER_SELL_CONFIRMED)
      journey.StrategicDirection = g_pair_states[pairIndex].d1_major_trend_owner.Direction;

   if(d1State == D1_OWNER_UNRESOLVED)
   {
      journey.Relation = NESTED_UNRESOLVED;
      journey.Reason = "D1_OWNER_UNRESOLVED";
      NMJE_FinalizeJourneyMetadata(pairIndex, previous, journey);
   g_nested_journeys[pairIndex] = journey;
      NMJE_PrintCoverageOverlay(journey);
      string n1Message = "[N1-NMJE] " + journey.Pair +
                         " REL=UNRESOLVED P=NONE J=- D1=" + journey.D1Node.Label +
                         " H4=" + journey.H4Node.Label +
                         " H1=" + journey.H1Node.Label +
                         " M15=" + journey.M15Node.Label +
                         " R=" + journey.Reason;
      ObserverPrintChanged("N1|" + journey.Pair, n1Message);
      return;
   }

   ENUM_NESTED_PARENT_KIND parentKind;
   int parentTF = 0;
   ENUM_SIGNAL_TYPE parentSignal = SIGNAL_NONE;
   ENUM_DIRECTION parentDirection = DIR_NONE;
   datetime parentAnchor = 0;
   string parentEventID = "";
   string parentReason = "";
   bool hasParent = NMJE_ResolveParent(g_pair_states[pairIndex], parentKind, parentTF,
                                       parentSignal, parentDirection, parentAnchor,
                                       parentEventID, parentReason);
   if(hasParent && parentEventID == "")
   {
      hasParent = false;
      parentReason = "PARENT_EVENT_ID_UNRESOLVED";
   }

   if(!hasParent)
   {
      if(g_pair_states[pairIndex].h4_direction_owner.State == H4_OWNER_RECOVERY_UNRESOLVED ||
         NMJE_HasChildActivity(g_pair_states[pairIndex]))
      {
         journey.Relation = NESTED_UNRESOLVED;
         journey.Reason = (parentReason != "NO_PARENT") ? parentReason : "PARENT_PROVENANCE_MISSING";
      }
      else
      {
         journey.Relation = NESTED_NOT_APPLICABLE;
         journey.Reason = "NO_PARENT_NO_CHILD";
         journey.Resolved = true;
      }
      NMJE_FinalizeJourneyMetadata(pairIndex, previous, journey);
   g_nested_journeys[pairIndex] = journey;
      NMJE_PrintCoverageOverlay(journey);
      string n1Message = "[N1-NMJE] " + journey.Pair +
                         " REL=" + NMJE_RelationText(journey.Relation) +
                         " P=NONE J=- D1=" + journey.D1Node.Label +
                         " H4=" + journey.H4Node.Label +
                         " H1=" + journey.H1Node.Label +
                         " M15=" + journey.M15Node.Label +
                         " R=" + journey.Reason;
      ObserverPrintChanged("N1|" + journey.Pair, n1Message);
      return;
   }

   journey.ParentKind = parentKind;
   journey.ParentTimeframe = parentTF;
   journey.ParentSignal = parentSignal;
   journey.ParentDirection = parentDirection;
   journey.ParentCandleTime = parentAnchor;
   journey.ParentEventID = parentEventID;
   journey.JourneyID = NMJE_BuildJourneyID(journey.Pair, parentKind, parentEventID);
   journey.Valid = true;
   journey.Resolved = true;

   if(d1State == D1_TRANSITION)
   {
      journey.Relation = NESTED_BUILDING;
      journey.Reason = "D1_TRANSITION";
   }
   else if((journey.StrategicDirection == DIR_BUY || journey.StrategicDirection == DIR_SELL) &&
           parentTF == PERIOD_H4 && parentDirection != journey.StrategicDirection)
   {
      // A local H4 journey may be counter to D1 while a retracement develops.
      // N1 does not call this an autonomous reversal and does not gate it.
      journey.Relation = NESTED_BUILDING;
      journey.Reason = "H4_LOCAL_OPPOSES_D1";
   }
   else
   {
      ReEntryData h1Confirmed;
      bool h1Ambiguous = false;
      if(NMJE_SelectConfirmedRE(g_pair_states[pairIndex].re_h1_buy_state,
                                g_pair_states[pairIndex].re_h1_sell_state,
                                h1Confirmed, h1Ambiguous))
      {
         if(h1Confirmed.Direction == parentDirection)
         {
            journey.Relation = NESTED_ALIGNED;
            journey.Reason = "H1_RE_ALIGNED_WITH_PARENT";
         }
         else
         {
            journey.Relation = NESTED_CONFLICT;
            journey.Reason = "CONFIRMED_H1_RE_OPPOSES_PARENT";
         }
      }
      else if(h1Ambiguous)
      {
         journey.Relation = NESTED_UNRESOLVED;
         journey.Resolved = false;
         journey.Reason = "H1_RE_AMBIGUOUS";
      }
      else
      {
         bool supporting =
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_buy_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_sell_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_m15_buy_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_m15_sell_lifecycle) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_buy_state) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_sell_state);

         if(supporting)
         {
            journey.Relation = NESTED_SUPPORTING;
            journey.Reason = "LTF_STRUCTURE_SUPPORTING_PARENT";
         }
         else if(NMJE_HasChildActivity(g_pair_states[pairIndex]))
         {
            journey.Relation = NESTED_BUILDING;
            journey.Reason = "LTF_STRUCTURE_BUILDING";
         }
         else if(parentKind == NESTED_PARENT_D1_OWNER &&
                 g_pair_states[pairIndex].h4_direction_owner.State == H4_OWNER_ACTIVE &&
                 g_pair_states[pairIndex].h4_direction_owner.IsValid)
         {
            if(g_pair_states[pairIndex].h4_direction_owner.Direction == parentDirection)
            {
               journey.Relation = NESTED_ALIGNED;
               journey.Reason = "H4_OWNER_ALIGNED_WITH_D1";
            }
            else
            {
               journey.Relation = NESTED_BUILDING;
               journey.Reason = "H4_LOCAL_OPPOSES_D1";
            }
         }
         else
         {
            journey.Relation = NESTED_BUILDING;
            journey.Reason = "PARENT_WAITING_FOR_CHILD";
         }
      }
   }

   NMJE_FinalizeJourneyMetadata(pairIndex, previous, journey);
   g_nested_journeys[pairIndex] = journey;
   NMJE_PrintCoverageOverlay(journey);
   string n1Message = "[N1-NMJE] " + journey.Pair +
                      " REL=" + NMJE_RelationText(journey.Relation) +
                      " P=" + NMJE_ParentText(journey.ParentKind) + "/" + NMJE_DirText(journey.ParentDirection) +
                      " J=" + journey.JourneyID +
                      " PE=" + journey.ParentEventID +
                      " D1=" + journey.D1Node.Label +
                      " H4=" + journey.H4Node.Label +
                      " H1=" + journey.H1Node.Label +
                      " M15=" + journey.M15Node.Label +
                      " R=" + journey.Reason;
   ObserverPrintChanged("N1|" + journey.Pair, n1Message);
}

// N2-01: post-M16 shadow tag for validated decisions only.
// Observation metadata only. It does not mutate decision, candidate, risk or execution state.
string NMJE_LogIdentityToken(string value)
{
   // DecisionID contains a human-readable TimeToString() component with a space.
   // Encode whitespace so the diagnostic remains a deterministic single token.
   string token = value;
   StringReplace(token, " ", "~");
   StringReplace(token, "\t", "~");
   return token;
}

string D1OpportunityLTFClusterText(BBMA_Decision &decision)
{
   if(decision.D1AuthorityMode != D1_AUTH_OPPORTUNITY) return "-";
   bool hasH1=false, hasM15=false;
   for(int i=0; i<decision.ComponentCount && i<3; i++)
   {
      if(decision.Components[i].ComponentType != SIGNAL_RE_ENTRY) continue;
      if(decision.Components[i].Timeframe == PERIOD_H1) hasH1=true;
      if(decision.Components[i].Timeframe == PERIOD_M15) hasM15=true;
   }
   if(hasH1 && hasM15) return "H1+M15";
   if(hasH1) return "H1";
   if(hasM15) return "M15";
   return "-";
}

void NMJE_PrintValidatedDecisionShadow(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!decision.Valid || decision.DecisionState != DEC_VALIDATED) return;

   NestedJourneyState journey = g_nested_journeys[pairIndex];
   string journeyId = journey.JourneyID;
   if(journeyId == "") journeyId = "-";

   string decisionToken = NMJE_LogIdentityToken(decision.DecisionID);
   string decisionHash = SHORT_HASH(decision.DecisionID);

   Print("[N2-NMJE-DEC] ", decision.Pair,
         " SIG=", EnumToString(decision.SignalType),
         " DIR=", NMJE_DirText(decision.Direction),
         " REL=", NMJE_RelationText(journey.Relation),
         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " J=", journeyId,
         " DID=", decisionToken,
         " DIDH=", decisionHash,
         " AUTH=", D1AuthorityModeText(decision.D1AuthorityMode),
         " OFAM=", D1OpportunityFamilyText(decision.D1OpportunityFamily),
         " OC=", (decision.D1OpportunityCycleID == "" ? "-" : decision.D1OpportunityCycleID),
         " LTF=", D1OpportunityLTFClusterText(decision),
         " OSH=", (decision.SequenceHash == "" ? "-" : decision.SequenceHash));
}

//+------------------------------------------------------------------+
//| MODULE 13: COMBINATION ENGINE (COLLECT ONLY)                     |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

// NMJE V2 P2/P3 shadow rematerialization from current owner.
// P2 observes equal-eligibility only; it never assigns order, score, rank or rejection.
void NMJE_P2_PrintEqualEligibilityShadow(int pairIndex,
                                          ValidatedSequenceCandidate &candidates[],
                                          int count,
                                          PairState &pairState)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   // Counterfactual research state is tester-only and cycle-local. Clear first
   // so a no-longer-equal candidate set can never leak into a later execution.
   if(IsTesting())
      ZeroMemory(g_nmje_cf_pending[pairIndex]);

   if(count < 2) return;
   int eligibleCount = 0;
   for(int i = 0; i < count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;
      eligibleCount++;
   }
   if(eligibleCount < 2) return;

   g_nested_journeys[pairIndex].P2CoherencePresent = true;
   g_nested_journeys[pairIndex].P2EligibleCount = eligibleCount;
   g_nested_journeys[pairIndex].P2CandleTime = pairState.m15_data.candle_time;

   if(IsTesting() && eligibleCount <= NMJE_CF_MAX_CANDIDATES)
   {
      NMJECounterfactualPendingSet pending;
      ZeroMemory(pending);
      pending.Present = true;
      pending.Pair = pairState.actual_symbol;
      pending.M15CandleTime = pairState.m15_data.candle_time;
      pending.EligibleCount = eligibleCount;
      pending.Relation = g_nested_journeys[pairIndex].Relation;
      pending.StableRelation = g_nested_journeys[pairIndex].StableRelation;
      pending.Maturity = g_nested_journeys[pairIndex].Maturity;
      pending.M5SnapshotPresent = g_nested_journeys[pairIndex].M5ShadowPresent;
      pending.M5SemanticResolved = g_nested_journeys[pairIndex].M5SemanticResolved;

      for(int c = 0; c < count; c++)
      {
         if(!IsCandidateEligible(candidates[c])) continue;
         if(!IsCandidateAllowedByD1Owner(candidates[c], pairState)) continue;

         // #214 identity enrichment is one executable H1 Re-Entry identity,
         // not two counterfactual alternatives. Keep the enriched opportunity
         // variant when the raw pool also contains the standalone twin.
         int duplicateSlot = -1;
         bool incomingExtremeTPW =
            (candidates[c].SequenceType == SIGNAL_RE_ENTRY &&
             candidates[c].UsesD1Opportunity &&
             candidates[c].D1OpportunityFamily == D1_OPP_EXTREME_TPW);
         for(int d = 0; d < pending.Count; d++)
         {
            ValidatedSequenceCandidate existing =
               pending.Candidates[d].Candidate;
            bool existingExtremeTPW =
               (existing.SequenceType == SIGNAL_RE_ENTRY &&
                existing.UsesD1Opportunity &&
                existing.D1OpportunityFamily == D1_OPP_EXTREME_TPW);
            bool sameExecutableRE =
               (candidates[c].SequenceType == SIGNAL_RE_ENTRY &&
                existing.SequenceType == SIGNAL_RE_ENTRY &&
                candidates[c].Direction == existing.Direction &&
                candidates[c].SequenceHash != "" &&
                candidates[c].SequenceHash == existing.SequenceHash &&
                candidates[c].SequenceStartTime == existing.SequenceStartTime &&
                GetCandidateAnchorTime(candidates[c]) ==
                   GetCandidateAnchorTime(existing) &&
                incomingExtremeTPW != existingExtremeTPW &&
                (incomingExtremeTPW || existingExtremeTPW));
            if(sameExecutableRE)
            {
               duplicateSlot = d;
               break;
            }
         }

         NMJEStructuralDensityState density;
         NMJE_BuildCandidateStructuralDensity(pairState,
                                              g_nested_journeys[pairIndex],
                                              candidates[c], density);

         if(duplicateSlot >= 0)
         {
            if(incomingExtremeTPW)
            {
               pending.Candidates[duplicateSlot].Candidate = candidates[c];
               pending.Candidates[duplicateSlot].ParentMatch =
                  (g_nested_journeys[pairIndex].ParentDirection ==
                   candidates[c].Direction);
               pending.Candidates[duplicateSlot].StructureMask =
                  density.StageMask;
            }
            continue;
         }

         if(pending.Count >= NMJE_CF_MAX_CANDIDATES) break;
         int slot = pending.Count;
         pending.Candidates[slot].Present = true;
         pending.Candidates[slot].Candidate = candidates[c];
         pending.Candidates[slot].ParentMatch =
            (g_nested_journeys[pairIndex].ParentDirection == candidates[c].Direction);
         pending.Candidates[slot].StructureMask = density.StageMask;
         pending.Count++;
      }

      if(pending.Count >= 2)
      {
         pending.SetID = SHORT_HASH(pending.Pair + "|" +
                                    IntegerToString((int)pending.M15CandleTime) + "|" +
                                    IntegerToString(pending.Count), 16);
         g_nmje_cf_pending[pairIndex] = pending;
      }

      Print("[Q9-P2-CF-SET] Pair=", pairState.actual_symbol,
            " RawEligible=", IntegerToString(eligibleCount),
            " Pending=", IntegerToString(pending.Count),
            " Set=", (pending.SetID == "" ? "-" : pending.SetID),
            " Authority=NONE");
   }
   else if(IsTesting() && eligibleCount > NMJE_CF_MAX_CANDIDATES)
   {
      Print("[Q9-P2-CF-SKIP] Pair=", pairState.actual_symbol,
            " Eligible=", IntegerToString(eligibleCount),
            " Reason=CAPACITY Authority=NONE");
   }

   for(int i = 0; i < count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;
      Print("[Q9-P2-COHERENCE] Pair=", pairState.actual_symbol,
            " Eligible=", IntegerToString(eligibleCount),
            " Seq=", (candidates[i].SequenceHash == "" ? "-" : candidates[i].SequenceHash),
            " Sig=", EnumToString(candidates[i].SequenceType),
            " Dir=", NMJE_DirText(candidates[i].Direction),
            " ParentMatch=", (g_nested_journeys[pairIndex].ParentDirection == candidates[i].Direction ? "Y" : "N"),
            " M5Present=", (g_nested_journeys[pairIndex].M5ShadowPresent ? "Y" : "N"),
            " Authority=NONE");
   }
}

// P3 observes closed M5 data only. It deliberately does not classify a signal.
void NMJE_P3_UpdateClosedM5Shadow(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   PairState state = g_pair_states[pairIndex];
   g_nested_journeys[pairIndex].M5ShadowPresent = false;
   g_nested_journeys[pairIndex].M5ShadowClosedCandleTime = 0;
   g_nested_journeys[pairIndex].M5ShadowEventID = "";
   g_nested_journeys[pairIndex].M5ShadowDirection = DIR_NONE;
   g_nested_journeys[pairIndex].M5ShadowReason = "M5_CLOSED_DATA_UNAVAILABLE";
   g_nested_journeys[pairIndex].M5SemanticResolved = false;
   g_nested_journeys[pairIndex].M5DiagnosticRelation = NESTED_NOT_APPLICABLE;
   g_nested_journeys[pairIndex].M5DiagnosticReason = "M5_CONTEXT_UNAVAILABLE";
   if(state.m5_data.timeframe != PERIOD_M5 || state.m5_data.candle_time <= 0) return;
   if(!state.m5_data.is_valid || !state.m5_data.is_closed) return;
   g_nested_journeys[pairIndex].M5ShadowPresent = true;
   g_nested_journeys[pairIndex].M5ShadowClosedCandleTime = state.m5_data.candle_time;
   g_nested_journeys[pairIndex].M5ShadowEventID =
      "M5|" + state.actual_symbol + "|" + IntegerToString((int)state.m5_data.candle_time);
   g_nested_journeys[pairIndex].M5ShadowReason = "M5_CLOSED_SNAPSHOT_ONLY";
   // P5 fail-closed: Build 5.12 P3 does not own M5 Re-Entry/Extreme semantics.
   g_nested_journeys[pairIndex].M5SemanticResolved = false;
   g_nested_journeys[pairIndex].M5DiagnosticRelation = NESTED_UNRESOLVED;
   g_nested_journeys[pairIndex].M5DiagnosticReason =
      "M5_SIGNAL_SEMANTICS_NOT_MATERIALIZED_TRUE_CONFLICT_HOLD";
}

void CollectSignalSnapshots(Signal &h1_extreme_snapshot, Signal &m15_mhv_snapshot,
                            MLVData &m15_mlv_snapshot, Signal &m15_csd_snapshot,
                            Signal &m15_ecsd_snapshot, Signal &m15_csm_snapshot,
                            ReEntryData &h1_reEntry_snapshot,
                            Signal &extreme, Signal &mhv, MLVData &mlv, Signal &csd,
                            Signal &ecsd, Signal &csm, ReEntryData &reEntry)
{
   extreme = h1_extreme_snapshot;
   mhv = m15_mhv_snapshot;
   mlv = m15_mlv_snapshot;
   csd = m15_csd_snapshot;
   ecsd = m15_ecsd_snapshot;
   csm = m15_csm_snapshot;
   reEntry = h1_reEntry_snapshot;

   if(csd.Valid && ecsd.Valid &&
      csd.Direction == ecsd.Direction &&
      csd.CandleTime == ecsd.CandleTime)
   {
      ecsd.Valid = false;
      ecsd.Reason = "Suppressed by same-candle CSD classification";
   }
}

bool IsCombinationSignalReady(Signal &signal, ENUM_SIGNAL_TYPE expectedType,
                              int expectedTimeframe)
{
   return (signal.Valid &&
           signal.Type == expectedType &&
           signal.Timeframe == expectedTimeframe &&
           signal.CandleTime > 0 &&
           signal.Direction != DIR_NONE);
}

bool IsCombinationMLVReady(MLVData &mlv)
{
   return (IsCanonicalMLVMatureState(mlv.State) &&
           mlv.IsValid &&
           mlv.Direction != DIR_NONE &&
           mlv.Timeframe == PERIOD_M15 &&
           mlv.FrozenMarkedBody > 0 &&
           mlv.ConfirmationCandleTime > 0);
}

void SetCombinationComponent(ComponentIdentity &component, ENUM_SIGNAL_TYPE type,
                             ENUM_DIRECTION direction, int timeframe,
                             datetime candleTime)
{
   ZeroMemory(component);
   component.ComponentType = type;
   component.Direction = direction;
   component.Timeframe = timeframe;
   component.CandleTime = candleTime;
}

void FinalizeCombinationCandidate(ComponentSet &set, ENUM_SIGNAL_TYPE combinationType)
{
   set.CombinationType = combinationType;
   set.ComponentCount = 3;
   set.SequenceStartTime = MathMin(set.Comp1.CandleTime,
                           MathMin(set.Comp2.CandleTime, set.Comp3.CandleTime));
   set.SLTPSource = SIGNAL_NONE;
   set.SequenceHash = GenerateSequenceHash(set);
}

void BuildPossibleCombinations(ComponentSet &rem, ComponentSet &rre, ComponentSet &ree,
                               Signal &h4_reEntry, Signal &h1_extreme, MLVData &m15_mlv,
                               Signal &d1_reEntry, Signal &h4_extreme)
{
   ZeroMemory(rem);
   ZeroMemory(rre);
   ZeroMemory(ree);

   if(IsCombinationSignalReady(h4_reEntry, SIGNAL_RE_ENTRY, PERIOD_H4) &&
      IsCombinationSignalReady(h1_extreme, SIGNAL_EXTREME, PERIOD_H1) &&
      IsCombinationMLVReady(m15_mlv))
   {
      SetCombinationComponent(rem.Comp1, SIGNAL_RE_ENTRY, h4_reEntry.Direction,
                              PERIOD_H4, h4_reEntry.CandleTime);
      SetCombinationComponent(rem.Comp2, SIGNAL_EXTREME, h1_extreme.Direction,
                              PERIOD_H1, h1_extreme.CandleTime);
      SetCombinationComponent(rem.Comp3, SIGNAL_MLV, m15_mlv.Direction,
                              PERIOD_M15, m15_mlv.ConfirmationCandleTime);
      FinalizeCombinationCandidate(rem, SIGNAL_REM);
   }

   if(IsCombinationSignalReady(d1_reEntry, SIGNAL_RE_ENTRY, PERIOD_D1) &&
      IsCombinationSignalReady(h4_reEntry, SIGNAL_RE_ENTRY, PERIOD_H4) &&
      IsCombinationSignalReady(h1_extreme, SIGNAL_EXTREME, PERIOD_H1))
   {
      SetCombinationComponent(rre.Comp1, SIGNAL_RE_ENTRY, d1_reEntry.Direction,
                              PERIOD_D1, d1_reEntry.CandleTime);
      SetCombinationComponent(rre.Comp2, SIGNAL_RE_ENTRY, h4_reEntry.Direction,
                              PERIOD_H4, h4_reEntry.CandleTime);
      SetCombinationComponent(rre.Comp3, SIGNAL_EXTREME, h1_extreme.Direction,
                              PERIOD_H1, h1_extreme.CandleTime);
      FinalizeCombinationCandidate(rre, SIGNAL_RRE);
   }

   if(IsCombinationSignalReady(d1_reEntry, SIGNAL_RE_ENTRY, PERIOD_D1) &&
      IsCombinationSignalReady(h4_extreme, SIGNAL_EXTREME, PERIOD_H4) &&
      IsCombinationSignalReady(h1_extreme, SIGNAL_EXTREME, PERIOD_H1))
   {
      SetCombinationComponent(ree.Comp1, SIGNAL_RE_ENTRY, d1_reEntry.Direction,
                              PERIOD_D1, d1_reEntry.CandleTime);
      SetCombinationComponent(ree.Comp2, SIGNAL_EXTREME, h4_extreme.Direction,
                              PERIOD_H4, h4_extreme.CandleTime);
      SetCombinationComponent(ree.Comp3, SIGNAL_EXTREME, h1_extreme.Direction,
                              PERIOD_H1, h1_extreme.CandleTime);
      FinalizeCombinationCandidate(ree, SIGNAL_REE);
   }
}

//+------------------------------------------------------------------+
//| MODULE 14: SEQUENCE ENGINE (VALIDATE ONLY)                       |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsValidCombinationComponent(ComponentIdentity &component)
{
   if(component.ComponentType == SIGNAL_NONE) return false;
   if(component.Direction == DIR_NONE) return false;
   if(component.Timeframe <= 0) return false;
   if(component.CandleTime <= 0) return false;
   return true;
}

bool ValidateDirectionConsistency(ComponentSet &set)
{
   if(set.Comp1.Direction != set.Comp2.Direction) return false;
   if(set.Comp2.Direction != set.Comp3.Direction) return false;
   return set.Comp1.Direction != DIR_NONE;
}

bool ValidateCombinationSignature(ComponentSet &set)
{
   if(set.ComponentCount != 3) return false;
   if(!IsValidCombinationComponent(set.Comp1) ||
      !IsValidCombinationComponent(set.Comp2) ||
      !IsValidCombinationComponent(set.Comp3))
      return false;

   if(set.CombinationType == SIGNAL_REM)
   {
      return (set.Comp1.ComponentType == SIGNAL_RE_ENTRY &&
              set.Comp1.Timeframe == PERIOD_H4 &&
              set.Comp2.ComponentType == SIGNAL_EXTREME &&
              set.Comp2.Timeframe == PERIOD_H1 &&
              set.Comp3.ComponentType == SIGNAL_MLV &&
              set.Comp3.Timeframe == PERIOD_M15);
   }

   if(set.CombinationType == SIGNAL_RRE)
   {
      return (set.Comp1.ComponentType == SIGNAL_RE_ENTRY &&
              set.Comp1.Timeframe == PERIOD_D1 &&
              set.Comp2.ComponentType == SIGNAL_RE_ENTRY &&
              set.Comp2.Timeframe == PERIOD_H4 &&
              set.Comp3.ComponentType == SIGNAL_EXTREME &&
              set.Comp3.Timeframe == PERIOD_H1);
   }

   if(set.CombinationType == SIGNAL_REE)
   {
      return (set.Comp1.ComponentType == SIGNAL_RE_ENTRY &&
              set.Comp1.Timeframe == PERIOD_D1 &&
              set.Comp2.ComponentType == SIGNAL_EXTREME &&
              set.Comp2.Timeframe == PERIOD_H4 &&
              set.Comp3.ComponentType == SIGNAL_EXTREME &&
              set.Comp3.Timeframe == PERIOD_H1);
   }

   return false;
}

void PopulateValidatedCombination(ComponentSet &set,
                                  ValidatedSequenceCandidate &candidate)
{
   candidate.SequenceType = set.CombinationType;
   candidate.Direction = set.Comp1.Direction;
   candidate.ComponentCount = 3;
   candidate.Components[0] = set.Comp1;
   candidate.Components[1] = set.Comp2;
   candidate.Components[2] = set.Comp3;
   candidate.SequenceStartTime = set.SequenceStartTime;
   candidate.SequenceHash = GenerateSequenceHash(set);
   candidate.SLTPSource = SIGNAL_NONE;
   candidate.PriorityTier = TIER_NONE;
   candidate.RequirementCompleteness = 3;
   candidate.SequenceCompleteness = 3;
   candidate.PatternStrength = 0;
   candidate.Valid = true;
}

void ValidateSequence(ComponentSet &set, ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);

   if(!ValidateCombinationSignature(set) ||
      !ValidateDirectionConsistency(set))
   {
      candidate.Valid = false;
      return;
   }

   PopulateValidatedCombination(set, candidate);
}

//+------------------------------------------------------------------+
//| MODULE 15: PRIORITY ENGINE (FINAL SIGNAL AUTHORITY)              |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsD1MajorTrendOwnerExecutionReady(PairState &pairState)
{
   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;

   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
      return false;

   if(owner.State == D1_OWNER_BUY_CONFIRMED)
      return (owner.Direction == DIR_BUY);

   if(owner.State == D1_OWNER_SELL_CONFIRMED)
      return (owner.Direction == DIR_SELL);

   return false;
}

bool IsD1OpportunityCandidateAuthorityReady(ValidatedSequenceCandidate &candidate,
                                               PairState &pairState)
{
   if(!candidate.UsesD1Opportunity) return false;
   D1OpportunityJourney opportunity = pairState.d1_opportunity;
   if(!opportunity.Active || opportunity.CycleID == "") return false;
   if(candidate.D1OpportunityCycleID != opportunity.CycleID) return false;
   if(candidate.D1OpportunityFamily != opportunity.Family) return false;
   if(candidate.D1OpportunityDirection != opportunity.Direction) return false;
   if(candidate.Direction != opportunity.Direction) return false;
   if(candidate.D1OpportunitySourceCandleTime != opportunity.SourceCandleTime) return false;
   if(candidate.D1OpportunityActivationTime != opportunity.ActivationTime) return false;

   // Tactical Extreme/TPW may oppose MA50 or run during a valid transition,
   // but unresolved/malformed D1 strategic context still fails closed.
   if(opportunity.Family == D1_OPP_EXTREME_TPW)
   {
      D1MajorTrendOwner owner = pairState.d1_major_trend_owner;
      return (owner.IsValid && owner.SourceCandleTime > 0 &&
              owner.Close1 > 0.0 && owner.MA50_1 > 0.0 && owner.MA50_2 > 0.0 &&
              owner.State != D1_OWNER_UNRESOLVED);
   }

   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;
   return (candidate.Direction == pairState.d1_major_trend_owner.Direction);
}

bool IsCandidateAllowedByD1Owner(ValidatedSequenceCandidate &candidate,
                                 PairState &pairState)
{
   if(candidate.UsesD1Opportunity)
      return IsD1OpportunityCandidateAuthorityReady(candidate, pairState);

   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;
   return (candidate.Direction == pairState.d1_major_trend_owner.Direction);
}

bool FreezeD1OwnerSnapshot(PairState &pairState, BBMA_Decision &decision)
{
   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;

   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;
   decision.D1OwnerState = owner.State;
   decision.D1OwnerDirection = owner.Direction;
   decision.D1OwnerCandleTime = owner.SourceCandleTime;
   decision.D1OwnerClose = owner.Close1;
   decision.D1OwnerMA50Current = owner.MA50_1;
   decision.D1OwnerMA50Previous = owner.MA50_2;
   decision.D1OwnerSnapshotValid = true;
   decision.D1AuthorityMode = D1_AUTH_STRATEGIC_OWNER;
   decision.D1OpportunitySnapshotValid = false;
   return true;
}

bool FreezeD1OpportunitySnapshot(PairState &pairState,
                                 ValidatedSequenceCandidate &selected,
                                 BBMA_Decision &decision)
{
   if(!IsD1OpportunityCandidateAuthorityReady(selected, pairState)) return false;

   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;
   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
      return false;

   decision.D1OwnerState = owner.State;
   decision.D1OwnerDirection = owner.Direction;
   decision.D1OwnerCandleTime = owner.SourceCandleTime;
   decision.D1OwnerClose = owner.Close1;
   decision.D1OwnerMA50Current = owner.MA50_1;
   decision.D1OwnerMA50Previous = owner.MA50_2;
   decision.D1OwnerSnapshotValid = true;

   decision.D1AuthorityMode = D1_AUTH_OPPORTUNITY;
   decision.D1OpportunityFamily = selected.D1OpportunityFamily;
   decision.D1OpportunityDirection = selected.D1OpportunityDirection;
   decision.D1OpportunitySourceSignal = selected.D1OpportunitySourceSignal;
   decision.D1OpportunitySourceCandleTime = selected.D1OpportunitySourceCandleTime;
   decision.D1OpportunityActivationTime = selected.D1OpportunityActivationTime;
   decision.D1OpportunityCycleID = selected.D1OpportunityCycleID;
   decision.D1OpportunitySnapshotValid = true;
   return true;
}

bool IsEntryModeCandidateAllowed(ValidatedSequenceCandidate &candidate)
{
   if(EntryMode == 1)
      return (candidate.SequenceType == SIGNAL_RE_ENTRY);

   if(EntryMode == 2)
   {
      return (candidate.SequenceType == SIGNAL_EXTREME ||
              candidate.SequenceType == SIGNAL_RE_ENTRY ||
              candidate.SequenceType == SIGNAL_REM ||
              candidate.SequenceType == SIGNAL_RRE ||
              candidate.SequenceType == SIGNAL_REE);
   }

   return false;
}

bool IsCandidateEligible(ValidatedSequenceCandidate &candidate)
{
   if(!candidate.Valid) return false;
   if(candidate.Direction != DIR_BUY && candidate.Direction != DIR_SELL) return false;
   if(!IsEntryModeCandidateAllowed(candidate)) return false;
   if(candidate.Expiry > 0 && candidate.Expiry < g_processing_time) return false;
   return true;
}

void BuildConfirmedReEntryCandidate(ReEntryData &reEntry,
                                    H4DirectionalOwner &h4Owner,
                                    ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);

   if(EntryMode == 1 && reEntry.State == RE_STATE_CONFIRMED)
      Print("[P3M1][RE_EVAL] Type=", EnumToString(reEntry.Type),
            " Dir=", EnumToString(reEntry.Direction),
            " Valid=", reEntry.IsValid ? "Y" : "N",
            " Confirm=", TimeToString(reEntry.ConfirmationCandle),
            " H4State=", EnumToString(h4Owner.State),
            " H4Dir=", EnumToString(h4Owner.Direction),
            " H4Valid=", h4Owner.IsValid ? "Y" : "N",
            " H4Recovery=", h4Owner.RecoveryComplete ? "Y" : "N");

   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return;
   if(reEntry.Direction != DIR_BUY && reEntry.Direction != DIR_SELL) return;
   if(reEntry.Timeframe != PERIOD_H1) return;

   // CORE-V2-F4: standalone H1 Re-Entry is executable only under the
   // immediate H4 authoritative directional owner. No D1/EMA/current-candle
   // fallback is permitted when H4 is NO_OWNER or recovery is unresolved.
   if(!h4Owner.RecoveryComplete || !h4Owner.IsValid ||
      h4Owner.State != H4_OWNER_ACTIVE ||
      h4Owner.Direction != reEntry.Direction)
      return;

   if(reEntry.ConfirmationCandle <= 0) return;

   candidate.SequenceType = SIGNAL_RE_ENTRY;
   candidate.Direction = reEntry.Direction;
   candidate.ComponentCount = 1;
   candidate.Components[0].ComponentType = SIGNAL_RE_ENTRY;
   candidate.Components[0].Direction = reEntry.Direction;
   candidate.Components[0].Timeframe = reEntry.Timeframe;
   candidate.Components[0].CandleTime = reEntry.ConfirmationCandle;
   candidate.SequenceStartTime = reEntry.ConfirmationCandle;

   string hashInput = "RE_ENTRY|" + IntegerToString(reEntry.Direction) + "|" +
                      IntegerToString(reEntry.Timeframe) + "|" +
                      TimeToString(reEntry.ConfirmationCandle);
   candidate.SequenceHash = SHORT_HASH(hashInput, 16);
   candidate.Expiry = 0; // structural owner lifetime; no generic Re-Entry TTL
   candidate.SLTPSource = SIGNAL_NONE;
   candidate.PriorityTier = TIER_NONE;
   candidate.RequirementCompleteness = 1;
   candidate.SequenceCompleteness = 1;
   candidate.PatternStrength = 0;
   candidate.Valid = true;
   if(EntryMode == 1)
      Print("[P3M1][RE_ADMIT] Type=", EnumToString(reEntry.Type),
            " Dir=", EnumToString(reEntry.Direction),
            " Confirm=", TimeToString(reEntry.ConfirmationCandle),
            " Hash=", candidate.SequenceHash);
}

void BuildStandaloneExtremeCandidate(ExtremeLifecycleData &extreme,
                                     H4DirectionalOwner &h4Owner,
                                     ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);
   if(EntryMode != MODE_2_ALL_VALIDATED_BBMA) return;
   if(extreme.Maturity != EXT_MAT_RETEST_READY || !extreme.IsValid) return;
   if(extreme.Direction != DIR_BUY && extreme.Direction != DIR_SELL) return;
   if(extreme.Timeframe != PERIOD_H1) return;
   if(extreme.RawCandleTime <= 0 || extreme.RetestCompletionCandleTime <= 0) return;
   if(extreme.RawCandleTime > extreme.RetestCompletionCandleTime) return;

   if(!h4Owner.RecoveryComplete || !h4Owner.IsValid ||
      h4Owner.State != H4_OWNER_ACTIVE || h4Owner.Direction != extreme.Direction)
      return;

   candidate.SequenceType = SIGNAL_EXTREME;
   candidate.Direction = extreme.Direction;
   candidate.ComponentCount = 1;
   candidate.Components[0].ComponentType = SIGNAL_EXTREME;
   candidate.Components[0].Direction = extreme.Direction;
   candidate.Components[0].Timeframe = PERIOD_H1;
   candidate.Components[0].CandleTime = extreme.RetestCompletionCandleTime;
   candidate.SequenceStartTime = extreme.RawCandleTime;
   string hashInput = "EXTREME_RETEST|" + IntegerToString(extreme.Direction) + "|" +
                      TimeToString(extreme.RawCandleTime) + "|" +
                      TimeToString(extreme.RetestCompletionCandleTime);
   candidate.SequenceHash = SHORT_HASH(hashInput, 16);
   candidate.Expiry = 0;
   candidate.SLTPSource = SIGNAL_EXTREME;
   candidate.PriorityTier = TIER_NONE;
   candidate.RequirementCompleteness = 1;
   candidate.SequenceCompleteness = 1;
   candidate.PatternStrength = 0;
   candidate.Valid = true;
}

void AppendValidatedCandidate(ValidatedSequenceCandidate &candidate,
                              ValidatedSequenceCandidate &candidates[], int &count)
{
   if(!candidate.Valid) return;
   ArrayResize(candidates, count + 1);
   candidates[count] = candidate;
   count++;
}


bool IsH4OpportunityAlignmentReady(PairState &state, ENUM_DIRECTION direction)
{
   return (state.h4_direction_owner.RecoveryComplete &&
           state.h4_direction_owner.IsValid &&
           state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
           state.h4_direction_owner.Direction == direction);
}

datetime OpportunityReEntryReadyTime(ReEntryData &reEntry)
{
   if(reEntry.ConfirmationCandle <= 0 || reEntry.Timeframe <= 0) return 0;
   int tfSeconds = GetTimeframeSeconds(reEntry.Timeframe);
   if(tfSeconds <= 0) return 0;
   return reEntry.ConfirmationCandle + tfSeconds;
}

bool IsFreshOpportunityReEntry(ReEntryData &reEntry,
                               ENUM_DIRECTION direction,
                               int expectedTimeframe,
                               datetime activationTime)
{
   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return false;
   if(reEntry.Direction != direction || reEntry.Timeframe != expectedTimeframe) return false;
   if(reEntry.ConfirmationCandle <= 0 || activationTime <= 0) return false;
   return (OpportunityReEntryReadyTime(reEntry) > activationTime);
}

void SetOpportunityREComponent(ComponentIdentity &component, ReEntryData &reEntry)
{
   ZeroMemory(component);
   component.ComponentType = SIGNAL_RE_ENTRY;
   component.Direction = reEntry.Direction;
   component.Timeframe = reEntry.Timeframe;
   component.CandleTime = reEntry.ConfirmationCandle;
}

void BuildD1OpportunityCandidate(int pairIndex,
                                 ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);
   if(EntryMode != MODE_2_ALL_VALIDATED_BBMA) return;
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   PairState state = g_pair_states[pairIndex];
   D1OpportunityJourney opportunity = state.d1_opportunity;
   if(!opportunity.Active || opportunity.Family == D1_OPP_NONE ||
      opportunity.CycleID == "" || opportunity.ActivationTime <= 0 ||
      (opportunity.Direction != DIR_BUY && opportunity.Direction != DIR_SELL))
      return;

   ReEntryData h1 = (opportunity.Direction == DIR_BUY)
                     ? state.re_h1_buy_state : state.re_h1_sell_state;
   ReEntryData m15 = (opportunity.Direction == DIR_BUY)
                      ? state.re_m15_buy_state : state.re_m15_sell_state;

   bool h1Fresh = IsFreshOpportunityReEntry(h1, opportunity.Direction,
                                             PERIOD_H1, opportunity.ActivationTime);
   bool m15Fresh = IsFreshOpportunityReEntry(m15, opportunity.Direction,
                                              PERIOD_M15, opportunity.ActivationTime);
   bool h4Aligned = IsH4OpportunityAlignmentReady(state, opportunity.Direction);

   if(opportunity.Family == D1_OPP_EXTREME_TPW)
   {
      // Stronger tactical confirmation: H4 owner + H1 confirmed RE are mandatory.
      if(!h4Aligned || !h1Fresh) return;
   }
   else
   {
      // Normal families are strategic-owner aligned. M15-only requires H4 support.
      if(!IsD1MajorTrendOwnerExecutionReady(state) ||
         state.d1_major_trend_owner.Direction != opportunity.Direction)
         return;
      if(!h1Fresh && !(m15Fresh && h4Aligned)) return;
   }

   int componentCount = 0;
   if(h1Fresh)
   {
      SetOpportunityREComponent(candidate.Components[componentCount], h1);
      componentCount++;
   }

   // Same-cycle M15 is folded into the same cluster when H4 confirms lineage.
   if(m15Fresh && h4Aligned)
   {
      SetOpportunityREComponent(candidate.Components[componentCount], m15);
      componentCount++;
   }

   if(componentCount <= 0 || componentCount > 2) return;

   candidate.SequenceType = SIGNAL_RE_ENTRY;
   candidate.Direction = opportunity.Direction;
   candidate.ComponentCount = componentCount;
   // D1O-07: fresh LTF Re-Entry owns execution identity; D1 is attribution only.
   ReEntryData identityRE = h1Fresh ? h1 : m15;
   candidate.SequenceStartTime = identityRE.ConfirmationCandle;
   string canonicalIdentity = "RE_ENTRY|" + IntegerToString(identityRE.Direction) + "|" +
                              IntegerToString(identityRE.Timeframe) + "|" +
                              TimeToString(identityRE.ConfirmationCandle);
   candidate.SequenceHash = SHORT_HASH(canonicalIdentity, 16);
   candidate.Expiry = 0; // D1 opportunity freshness is structural/activation-owned
   candidate.SLTPSource = SIGNAL_RE_ENTRY;
   candidate.PriorityTier = TIER_NONE;
   candidate.RequirementCompleteness = componentCount;
   candidate.SequenceCompleteness = componentCount;
   candidate.PatternStrength = 0;
   candidate.Valid = true;

   candidate.UsesD1Opportunity = true;
   candidate.D1OpportunityFamily = opportunity.Family;
   candidate.D1OpportunityDirection = opportunity.Direction;
   candidate.D1OpportunitySourceSignal = opportunity.SourceSignal;
   candidate.D1OpportunitySourceCandleTime = opportunity.SourceCandleTime;
   candidate.D1OpportunityActivationTime = opportunity.ActivationTime;
   candidate.D1OpportunityCycleID = opportunity.CycleID;
}

datetime GetCandidateAnchorTime(ValidatedSequenceCandidate &candidate)
{
   if(candidate.UsesD1Opportunity)
   {
      for(int i=0; i<candidate.ComponentCount && i<3; i++)
      {
         if(candidate.Components[i].ComponentType == SIGNAL_RE_ENTRY &&
            candidate.Components[i].Timeframe == PERIOD_H1 &&
            candidate.Components[i].CandleTime > 0)
            return candidate.Components[i].CandleTime;
      }
   }
   datetime anchor=candidate.Components[0].CandleTime;
   for(int i=1;i<3;i++) if(candidate.Components[i].CandleTime>anchor) anchor=candidate.Components[i].CandleTime;
   return anchor;
}

bool ResolveSelectedSLTPSourceComponent(ValidatedSequenceCandidate &selected,
                                        ComponentIdentity &source)
{
   ZeroMemory(source);

   if(selected.SequenceType == SIGNAL_RE_ENTRY && selected.UsesD1Opportunity)
   {
      // H1 is the structural source preference when H1+M15 are one cluster.
      for(int pass = 0; pass < 2; pass++)
      {
         int preferredTf = (pass == 0) ? PERIOD_H1 : PERIOD_M15;
         for(int i = 0; i < selected.ComponentCount; i++)
         {
            ComponentIdentity component = selected.Components[i];
            if(component.ComponentType != SIGNAL_RE_ENTRY) continue;
            if(component.Timeframe != preferredTf) continue;
            if(component.Direction != selected.Direction || component.CandleTime <= 0) continue;
            source = component;
            return true;
         }
      }
      return false;
   }

   if(selected.SequenceType == SIGNAL_EXTREME)
   {
      for(int i = 0; i < selected.ComponentCount; i++)
      {
         ComponentIdentity component = selected.Components[i];
         if(component.ComponentType != SIGNAL_EXTREME) continue;
         if(component.Timeframe != PERIOD_H1) continue;
         if(component.Direction != selected.Direction || component.CandleTime <= 0) continue;
         source = component;
         return true;
      }
      return false;
   }

   int expectedTf = 0;
   if(selected.SequenceType == SIGNAL_RE_ENTRY)
      expectedTf = PERIOD_H1;
   else if(selected.SequenceType == SIGNAL_REM)
      expectedTf = PERIOD_H4;
   else if(selected.SequenceType == SIGNAL_RRE ||
           selected.SequenceType == SIGNAL_REE)
      expectedTf = PERIOD_D1;
   else
      return false;

   for(int i = 0; i < selected.ComponentCount; i++)
   {
      ComponentIdentity component = selected.Components[i];
      if(component.ComponentType != SIGNAL_RE_ENTRY) continue;
      if(component.Timeframe != expectedTf) continue;
      if(component.Direction != selected.Direction) continue;
      if(component.CandleTime <= 0) continue;
      source = component;
      return true;
   }
   return false;
}


bool NMJE_P2_IsSelectedCounterfactualCandidate(ValidatedSequenceCandidate &candidate,
                                                BBMA_Decision &decision)
{
   if(!decision.Valid) return false;
   if(candidate.SequenceType != decision.SignalType ||
      candidate.Direction != decision.Direction ||
      candidate.SequenceHash != decision.SequenceHash)
      return false;

   bool decisionUsesOpportunity =
      (decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY &&
       decision.D1OpportunitySnapshotValid);
   if(candidate.UsesD1Opportunity != decisionUsesOpportunity) return false;
   if(!candidate.UsesD1Opportunity) return true;

   return (candidate.D1OpportunityFamily == decision.D1OpportunityFamily &&
           candidate.D1OpportunityDirection == decision.D1OpportunityDirection &&
           candidate.D1OpportunitySourceSignal == decision.D1OpportunitySourceSignal &&
           candidate.D1OpportunitySourceCandleTime == decision.D1OpportunitySourceCandleTime &&
           candidate.D1OpportunityActivationTime == decision.D1OpportunityActivationTime &&
           candidate.D1OpportunityCycleID == decision.D1OpportunityCycleID);
}

string NMJE_P2_CounterfactualCandidateID(string setID,
                                         ValidatedSequenceCandidate &candidate,
                                         ComponentIdentity &source)
{
   string key = setID + "|" + candidate.SequenceHash + "|" +
                IntegerToString((int)candidate.SequenceType) + "|" +
                IntegerToString((int)candidate.Direction) + "|" +
                IntegerToString((int)candidate.UsesD1Opportunity) + "|" +
                IntegerToString((int)candidate.D1OpportunityFamily) + "|" +
                IntegerToString((int)source.ComponentType) + "|" +
                IntegerToString(source.Timeframe) + "|" +
                IntegerToString((int)source.CandleTime);
   return SHORT_HASH(key, 16);
}

bool NMJE_P2_BuildCounterfactualDecision(int pairIndex,
                                         ValidatedSequenceCandidate &candidate,
                                         double entryProxy,
                                         BBMA_Decision &shadow)
{
   ZeroMemory(shadow);
   if(pairIndex < 0 || pairIndex >= g_pair_count || entryProxy <= 0.0)
      return false;

   shadow.Valid = true;
   shadow.Pair = g_pair_states[pairIndex].actual_symbol;
   shadow.Direction = candidate.Direction;
   shadow.SignalType = candidate.SequenceType;
   shadow.PriorityTier = TIER_NONE;
   shadow.ComponentCount = candidate.ComponentCount;
   for(int i = 0; i < 3; i++)
      shadow.Components[i] = candidate.Components[i];
   shadow.CandidateExpiry = candidate.Expiry;
   shadow.SequenceHash = candidate.SequenceHash;
   shadow.CandleTime = GetCandidateAnchorTime(candidate);
   shadow.CycleStartTime = candidate.SequenceStartTime;
   shadow.EntryPrice = entryProxy;

   shadow.HasSLTPSourceComponent =
      ResolveSelectedSLTPSourceComponent(candidate, shadow.SLTPSourceComponent);
   if(!shadow.HasSLTPSourceComponent) return false;

   D1MajorTrendOwner owner = g_pair_states[pairIndex].d1_major_trend_owner;
   shadow.D1OwnerState = owner.State;
   shadow.D1OwnerDirection = owner.Direction;
   shadow.D1OwnerCandleTime = owner.SourceCandleTime;
   shadow.D1OwnerClose = owner.Close1;
   shadow.D1OwnerMA50Current = owner.MA50_1;
   shadow.D1OwnerMA50Previous = owner.MA50_2;
   shadow.D1OwnerSnapshotValid = owner.IsValid;

   if(candidate.UsesD1Opportunity)
   {
      shadow.D1AuthorityMode = D1_AUTH_OPPORTUNITY;
      shadow.D1OpportunityFamily = candidate.D1OpportunityFamily;
      shadow.D1OpportunityDirection = candidate.D1OpportunityDirection;
      shadow.D1OpportunitySourceSignal = candidate.D1OpportunitySourceSignal;
      shadow.D1OpportunitySourceCandleTime = candidate.D1OpportunitySourceCandleTime;
      shadow.D1OpportunityActivationTime = candidate.D1OpportunityActivationTime;
      shadow.D1OpportunityCycleID = candidate.D1OpportunityCycleID;
      shadow.D1OpportunitySnapshotValid = true;
   }
   else
   {
      shadow.D1AuthorityMode = D1_AUTH_STRATEGIC_OWNER;
      shadow.D1OpportunitySnapshotValid = false;
   }
   return true;
}

int NMJE_P2_AllocateCounterfactualTradeSet()
{
   for(int i = 0; i < NMJE_CF_MAX_ACTIVE_SETS; i++)
      if(!g_nmje_cf_active[i].Active) return i;
   return -1;
}

int NMJE_P2_FindCounterfactualTradeSet(int ticket)
{
   if(ticket <= 0) return -1;
   for(int i = 0; i < NMJE_CF_MAX_ACTIVE_SETS; i++)
      if(g_nmje_cf_active[i].Active &&
         g_nmje_cf_active[i].Ticket == ticket)
         return i;
   return -1;
}

bool NMJE_P2_CaptureC044ReplayState(
   TradeInfo &info,
   NMJECounterfactualC044ReplayState &state)
{
   ZeroMemory(state);
   if(!info.c044_lifecycle_managed || !info.c044_replay_seed_valid ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe))
      return false;

   state.Present = true;
   state.OwnerTimeframe = info.c044_owner_timeframe;
   state.OwnerReEntryCandle = info.c044_owner_reentry_candle;
   state.EpochAnchorCandle = info.c044_epoch_anchor_candle;
   state.LastProcessedOwnerCandle = info.c044_last_processed_owner_candle;
   state.State = info.c044_state;
   state.ExitReason = info.c044_exit_reason;
   state.ExitLatchedCandle = info.c044_exit_latched_candle;
   state.ReplaySeedValid = info.c044_replay_seed_valid;
   state.ReplayReEntry = info.c044_replay_reentry;
   state.ReplayExtremeBuy = info.c044_replay_extreme_buy;
   state.ReplayExtremeSell = info.c044_replay_extreme_sell;
   return true;
}

bool NMJE_P2_RestoreC044ReplayTrade(
   NMJECounterfactualTradeSet &active,
   NMJECounterfactualOutcomeCandidate &record,
   TradeInfo &info)
{
   ZeroMemory(info);
   if(!record.C044Replay.Present || active.Pair == "" ||
      (record.Direction != DIR_BUY && record.Direction != DIR_SELL) ||
      active.OpenTime <= 0)
      return false;

   info.pair = active.Pair;
   info.direction = record.Direction;
   info.open_time = active.OpenTime;
   info.c044_lifecycle_managed = true;
   info.c044_shadow_replay = true;
   info.c044_owner_timeframe = record.C044Replay.OwnerTimeframe;
   info.c044_owner_reentry_candle = record.C044Replay.OwnerReEntryCandle;
   info.c044_epoch_anchor_candle = record.C044Replay.EpochAnchorCandle;
   info.c044_last_processed_owner_candle =
      record.C044Replay.LastProcessedOwnerCandle;
   info.c044_state = record.C044Replay.State;
   info.c044_exit_reason = record.C044Replay.ExitReason;
   info.c044_exit_latched_candle = record.C044Replay.ExitLatchedCandle;
   info.c044_replay_seed_valid = record.C044Replay.ReplaySeedValid;
   info.c044_replay_reentry = record.C044Replay.ReplayReEntry;
   info.c044_replay_extreme_buy = record.C044Replay.ReplayExtremeBuy;
   info.c044_replay_extreme_sell = record.C044Replay.ReplayExtremeSell;
   info.recovery_state = REC_NORMAL;

   return (info.c044_replay_seed_valid &&
           IsValidC044OwnerTimeframe(info.c044_owner_timeframe) &&
           info.c044_last_processed_owner_candle > 0);
}

bool NMJE_P2_FindHardSLHitInClosedM1Window(
   NMJECounterfactualTradeSet &active,
   NMJECounterfactualOutcomeCandidate &record,
   datetime startTime,
   datetime endTime,
   datetime &hitTime,
   int &barsChecked)
{
   hitTime = 0;
   if(record.StopLoss <= 0.0 || active.Pair == "" ||
      (record.Direction != DIR_BUY && record.Direction != DIR_SELL))
      return false;
   if(endTime <= startTime) return true;

   datetime firstFullBar = (datetime)(((int)startTime / 60) * 60);
   if(firstFullBar < startTime) firstFullBar += 60;
   datetime lastFullBar = (datetime)((((int)endTime - 60) / 60) * 60);
   if(lastFullBar < firstFullBar) return true;

   int startShift = iBarShift(active.Pair, PERIOD_M1, firstFullBar, true);
   int endShift = iBarShift(active.Pair, PERIOD_M1, lastFullBar, true);
   if(startShift < 0 || endShift < 0 || startShift < endShift) return false;

   for(int shift = startShift; shift >= endShift; shift--)
   {
      datetime barTime = iTime(active.Pair, PERIOD_M1, shift);
      if(barTime < firstFullBar || barTime > lastFullBar) continue;
      double highBid = iHigh(active.Pair, PERIOD_M1, shift);
      double lowBid = iLow(active.Pair, PERIOD_M1, shift);
      if(highBid <= 0.0 || lowBid <= 0.0 || highBid < lowBid) return false;
      barsChecked++;

      bool slHit = (record.Direction == DIR_BUY)
         ? (lowBid <= record.StopLoss)
         : (highBid + record.FrozenSpreadPrice >= record.StopLoss);
      if(slHit)
      {
         hitTime = barTime;
         return true;
      }
   }
   return true;
}

string NMJE_P2_C044OutcomeText(ENUM_C044_EXIT_REASON reason)
{
   if(reason == C044_EXIT_FAILED_MOMENTUM) return "C044_FAILED_MOMENTUM";
   if(reason == C044_EXIT_CYCLE_SUPERSEDED) return "C044_CYCLE_SUPERSEDED";
   if(reason == C044_EXIT_OPPOSITE_CSM) return "C044_OPPOSITE_CSM";
   return "C044_EXIT_UNRESOLVED";
}

void NMJE_P2_ResolveTargetlessC044Outcome(
   NMJECounterfactualTradeSet &active,
   NMJECounterfactualOutcomeCandidate &record,
   datetime closeTime,
   string &outcome,
   datetime &hitTime,
   int &barsChecked,
   int &ownerBarsChecked)
{
   outcome = "UNCOMPARABLE_C044_REPLAY_UNRESOLVED";
   hitTime = 0;
   ownerBarsChecked = 0;

   TradeInfo replay;
   if(!NMJE_P2_RestoreC044ReplayTrade(active, record, replay))
      return;
   int pairIndex = FindPairStateIndex(active.Pair);
   if(pairIndex < 0)
   {
      for(int p = 0; p < g_pair_count; p++)
      {
         if(g_pair_states[p].actual_symbol == active.Pair)
         {
            pairIndex = p;
            break;
         }
      }
   }
   if(pairIndex < 0 || closeTime <= active.OpenTime) return;

   int tfSeconds = GetTimeframeSeconds(replay.c044_owner_timeframe);
   int previousShift = iBarShift(active.Pair, replay.c044_owner_timeframe,
                                 replay.c044_last_processed_owner_candle, true);
   if(tfSeconds <= 0 || previousShift < 1)
   {
      outcome = "UNCOMPARABLE_C044_OWNER_HISTORY";
      return;
   }

   datetime cursorTime = active.OpenTime;
   for(int shift = previousShift - 1; shift >= 1; shift--)
   {
      datetime candleTime = iTime(active.Pair, replay.c044_owner_timeframe, shift);
      if(candleTime <= replay.c044_last_processed_owner_candle)
      {
         outcome = "UNCOMPARABLE_C044_CANDLE_ORDER";
         return;
      }
      datetime eventTime = candleTime + tfSeconds;
      if(eventTime > closeTime) break;

      datetime slHitTime = 0;
      if(!NMJE_P2_FindHardSLHitInClosedM1Window(active, record,
                                                 cursorTime, eventTime,
                                                 slHitTime, barsChecked))
      {
         outcome = "UNCOMPARABLE_C044_M1_HISTORY";
         return;
      }
      if(slHitTime > 0)
      {
         outcome = "SL_FIRST_TARGETLESS";
         hitTime = slHitTime;
         return;
      }

      if(!ProcessC044OwnerClosedCandle(replay, pairIndex, candleTime) ||
         replay.c044_state == C044_LIFE_FROZEN)
      {
         outcome = "UNCOMPARABLE_C044_REPLAY_FROZEN";
         return;
      }
      ownerBarsChecked++;
      cursorTime = eventTime;

      if(replay.c044_state == C044_LIFE_EXIT_LATCHED)
      {
         outcome = NMJE_P2_C044OutcomeText(replay.c044_exit_reason);
         hitTime = eventTime;
         return;
      }
   }

   datetime finalSLHit = 0;
   if(!NMJE_P2_FindHardSLHitInClosedM1Window(active, record,
                                              cursorTime, closeTime,
                                              finalSLHit, barsChecked))
   {
      outcome = "UNCOMPARABLE_C044_M1_HISTORY";
      return;
   }
   if(finalSLHit > 0)
   {
      outcome = "SL_FIRST_TARGETLESS";
      hitTime = finalSLHit;
      return;
   }

   outcome = "C044_HOLD_AT_BASELINE_CLOSE";
}

bool NMJE_P2_IsSameCounterfactualExecutionIdentity(
   NMJECounterfactualOutcomeCandidate &a,
   NMJECounterfactualOutcomeCandidate &b,
   double tolerance)
{
   if(!a.Present || !b.Present) return false;
   if(a.SignalType != b.SignalType ||
      a.Direction != b.Direction ||
      a.SequenceHash != b.SequenceHash ||
      a.AnchorTime != b.AnchorTime ||
      a.SequenceStartTime != b.SequenceStartTime)
      return false;

   if(a.SLTPSourceType != b.SLTPSourceType ||
      a.SLTPSourceTimeframe != b.SLTPSourceTimeframe ||
      a.SLTPSourceCandleTime != b.SLTPSourceCandleTime ||
      a.SLTPResolved != b.SLTPResolved ||
      a.Targetless != b.Targetless)
      return false;

   if(a.SLTPResolved)
   {
      if(MathAbs(a.StopLoss - b.StopLoss) > tolerance) return false;
      if(MathAbs(a.TakeProfit - b.TakeProfit) > tolerance) return false;
   }
   return true;
}

void NMJE_P2_RegisterCounterfactualOpen(int pairIndex,
                                        BBMA_Decision &decision,
                                        TradeInfo &info,
                                        RiskValidationSnapshot &snapshot)
{
   if(!IsTesting()) return;
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(info.ticket <= 0 || info.initial_entry_price <= 0.0 || info.open_time <= 0) return;

   NMJECounterfactualPendingSet pending = g_nmje_cf_pending[pairIndex];
   if(!pending.Present || pending.Count < 2 ||
      pending.Pair != info.pair ||
      pending.M15CandleTime != g_pair_states[pairIndex].m15_data.candle_time)
      return;

   int activeIndex = NMJE_P2_AllocateCounterfactualTradeSet();
   if(activeIndex < 0)
   {
      Print("[Q9-P2-CF-SKIP] Pair=", info.pair,
            " Ticket=", IntegerToString(info.ticket),
            " Reason=ACTIVE_CAPACITY Authority=NONE");
      return;
   }

   NMJECounterfactualTradeSet active;
   ZeroMemory(active);
   active.Active = true;
   active.Ticket = info.ticket;
   active.Pair = info.pair;
   active.SetID = pending.SetID;
   active.BaselineDecisionHash =
      (info.execution_hash == "" ? SHORT_HASH(decision.DecisionID) : info.execution_hash);
   active.OpenTime = info.open_time;

   double tolerance = (snapshot.TickSize_Price > 0.0)
      ? snapshot.TickSize_Price + 0.000000001 : 0.000000001;

   // Two passes guarantee the real baseline-selected variant is retained when
   // the raw equal-eligible pool contains execution-equivalent metadata twins.
   for(int pass = 0; pass < 2; pass++)
   {
      for(int i = 0; i < pending.Count && i < NMJE_CF_MAX_CANDIDATES; i++)
      {
         if(!pending.Candidates[i].Present) continue;
         ValidatedSequenceCandidate candidate = pending.Candidates[i].Candidate;
         bool selected = NMJE_P2_IsSelectedCounterfactualCandidate(candidate, decision);
         if(pass == 0 && !selected) continue;
         if(pass == 1 && selected) continue;

         BBMA_Decision shadow;
         bool built = NMJE_P2_BuildCounterfactualDecision(pairIndex, candidate,
                                                           info.initial_entry_price,
                                                           shadow);
         RiskValidationSnapshot shadowSnapshot = snapshot;
         shadowSnapshot.EntryPrice = info.initial_entry_price;

         bool resolved = false;
         if(built)
            resolved = ResolveApprovedInitialSLTP(shadow, shadowSnapshot);

         bool targetless = (resolved && IsTargetlessLifecycleDecision(shadow));
         bool geometryValid = (resolved && ValidateDirectionalSLTPGeometry(shadow));

         bool baseMatch = true;
         if(selected)
         {
            baseMatch = resolved &&
               MathAbs(shadow.StopLoss - info.initial_stop_loss) <= tolerance &&
               MathAbs(shadow.TakeProfit - info.initial_take_profit) <= tolerance;
         }

         ComponentIdentity source;
         ZeroMemory(source);
         if(built) source = shadow.SLTPSourceComponent;

         NMJECounterfactualOutcomeCandidate record;
         ZeroMemory(record);
         record.Present = true;
         record.CandidateID = NMJE_P2_CounterfactualCandidateID(pending.SetID,
                                                                 candidate, source);
         record.Selected = selected;
         record.SignalType = candidate.SequenceType;
         record.Direction = candidate.Direction;
         record.SequenceHash = candidate.SequenceHash;
         record.AnchorTime = GetCandidateAnchorTime(candidate);
         record.SequenceStartTime = candidate.SequenceStartTime;
         record.EntryProxy = info.initial_entry_price;
         record.StopLoss = resolved ? shadow.StopLoss : 0.0;
         record.TakeProfit = resolved ? shadow.TakeProfit : 0.0;
         record.SLTPResolved = (resolved && geometryValid);
         record.Targetless = targetless;
         record.BaseGeometryMatch = baseMatch;
         record.FrozenSpreadPrice = snapshot.CurrentSpreadPrice;
         record.SLTPSourceType = source.ComponentType;
         record.SLTPSourceTimeframe = source.Timeframe;
         record.SLTPSourceCandleTime = source.CandleTime;
         record.ParentMatch = pending.Candidates[i].ParentMatch;
         record.StructureMask = pending.Candidates[i].StructureMask;
         record.C044SeedMatch = true;

         if(targetless && built && shadow.C044LifecycleManaged &&
            !shadow.D1TPWLifecycleManaged)
         {
            TradeInfo replayInfo;
            ZeroMemory(replayInfo);
            replayInfo.pair = info.pair;
            replayInfo.direction = shadow.Direction;
            replayInfo.open_time = info.open_time;

            bool replayReady =
               InitializeC044TradeStateFromDecision(replayInfo, shadow);
            if(replayReady)
            {
               replayInfo.c044_shadow_replay = true;
               replayReady =
                  NMJE_P2_CaptureC044ReplayState(replayInfo, record.C044Replay);
            }

            if(selected)
            {
               record.C044SeedMatch =
                  (replayReady && info.c044_lifecycle_managed &&
                   info.c044_owner_timeframe == record.C044Replay.OwnerTimeframe &&
                   info.c044_owner_reentry_candle ==
                      record.C044Replay.OwnerReEntryCandle &&
                   info.c044_epoch_anchor_candle ==
                      record.C044Replay.EpochAnchorCandle &&
                   info.c044_last_processed_owner_candle ==
                      record.C044Replay.LastProcessedOwnerCandle &&
                   info.c044_state == record.C044Replay.State);
            }
         }

         bool duplicate = false;
         for(int d = 0; d < active.Count; d++)
         {
            if(NMJE_P2_IsSameCounterfactualExecutionIdentity(active.Candidates[d],
                                                              record, tolerance))
            {
               duplicate = true;
               break;
            }
         }
         if(duplicate) continue;

         int slot = active.Count;
         if(slot >= NMJE_CF_MAX_CANDIDATES) break;
         active.Candidates[slot] = record;
         active.Count++;


      }
   }

   if(active.Count >= 2)
   {
      g_nmje_cf_active[activeIndex] = active;
      for(int o = 0; o < active.Count; o++)
      {
         NMJECounterfactualOutcomeCandidate row = active.Candidates[o];
         Print("[Q9-P2-CF-OPEN] Pair=", info.pair,
               " Ticket=", IntegerToString(info.ticket),
               " DIDH=", active.BaselineDecisionHash,
               " Set=", pending.SetID,
               " CID=", row.CandidateID,
               " Selected=", row.Selected ? "Y" : "N",
               " Sig=", EnumToString(row.SignalType),
               " Dir=", NMJE_DirText(row.Direction),
               " Seq=", row.SequenceHash,
               " Anchor=", IntegerToString((int)row.AnchorTime),
               " Start=", IntegerToString((int)row.SequenceStartTime),
               " Open=", IntegerToString((int)info.open_time),
               " EntryProxy=", DoubleToString(row.EntryProxy, snapshot.Digits),
               " SL=", DoubleToString(row.StopLoss, snapshot.Digits),
               " TP=", DoubleToString(row.TakeProfit, snapshot.Digits),
               " SLTP=", row.SLTPResolved ? "Y" : "N",
               " Targetless=", row.Targetless ? "Y" : "N",
               " BaseMatch=", row.Selected ?
                  (row.BaseGeometryMatch ? "Y" : "N") : "-",
               " Src=", EnumToString(row.SLTPSourceType),
               "/", IntegerToString(row.SLTPSourceTimeframe),
               "/", IntegerToString((int)row.SLTPSourceCandleTime),
               " ParentMatch=", row.ParentMatch ? "Y" : "N",
               " SD=", IntegerToString(row.StructureMask),
               " REL=", NMJE_RelationText(pending.Relation),
               " SREL=", NMJE_RelationText(pending.StableRelation),
               " MAT=", NMJE_MaturityText(pending.Maturity),
               " M5SEM=", pending.M5SemanticResolved ? "Y" : "N",
               " C044R=", row.C044Replay.Present ? "Y" : "N",
               " C044SeedMatch=", (row.Selected && row.Targetless) ?
                  (row.C044SeedMatch ? "Y" : "N") : "-",
               " OwnerTF=", IntegerToString(row.C044Replay.OwnerTimeframe),
               " Spread=", DoubleToString(row.FrozenSpreadPrice, snapshot.Digits),
               " Method=BASELINE_FILL_PROXY Authority=NONE");
      }
   }
   else
      ZeroMemory(active);
}

void NMJE_P2_ResolvePairedWindowOutcome(NMJECounterfactualTradeSet &active,
                                        NMJECounterfactualOutcomeCandidate &record,
                                        datetime closeTime,
                                        string &outcome,
                                        datetime &hitTime,
                                        int &barsChecked,
                                        int &ownerBarsChecked)
{
   outcome = "UNRESOLVED_AT_BASELINE_CLOSE";
   hitTime = 0;
   barsChecked = 0;
   ownerBarsChecked = 0;

   if(record.Targetless)
   {
      if(record.C044Replay.Present)
         NMJE_P2_ResolveTargetlessC044Outcome(active, record, closeTime,
                                               outcome, hitTime,
                                               barsChecked, ownerBarsChecked);
      else
         outcome = "UNCOMPARABLE_TARGETLESS_NO_C044_REPLAY";
      return;
   }
   if(!record.SLTPResolved || record.StopLoss <= 0.0 || record.TakeProfit <= 0.0)
   {
      outcome = "UNCOMPARABLE_SLTP_UNRESOLVED";
      return;
   }
   if(active.OpenTime <= 0 || closeTime <= active.OpenTime)
   {
      outcome = "UNCOMPARABLE_WINDOW";
      return;
   }

   // Conservative paired-window proxy: use only complete M1 bars entirely
   // after the baseline fill and entirely before/equal to baseline close.
   datetime firstFullBar =
      (datetime)(((int)active.OpenTime / 60) * 60);
   if(firstFullBar < active.OpenTime) firstFullBar += 60;
   datetime lastFullBar =
      (datetime)((((int)closeTime - 60) / 60) * 60);
   if(lastFullBar < firstFullBar)
   {
      outcome = "UNRESOLVED_NO_FULL_M1_BAR";
      return;
   }

   int startShift = iBarShift(active.Pair, PERIOD_M1, firstFullBar, true);
   int endShift = iBarShift(active.Pair, PERIOD_M1, lastFullBar, true);
   if(startShift < 0 || endShift < 0 || startShift < endShift)
   {
      outcome = "UNCOMPARABLE_M1_HISTORY";
      return;
   }

   for(int shift = startShift; shift >= endShift; shift--)
   {
      datetime barTime = iTime(active.Pair, PERIOD_M1, shift);
      if(barTime < firstFullBar || barTime > lastFullBar) continue;
      double highBid = iHigh(active.Pair, PERIOD_M1, shift);
      double lowBid = iLow(active.Pair, PERIOD_M1, shift);
      if(highBid <= 0.0 || lowBid <= 0.0) continue;
      barsChecked++;

      bool slHit = false;
      bool tpHit = false;
      if(record.Direction == DIR_BUY)
      {
         slHit = (lowBid <= record.StopLoss);
         tpHit = (highBid >= record.TakeProfit);
      }
      else if(record.Direction == DIR_SELL)
      {
         // MT4 bar history is Bid. Use the preflight-frozen spread as an
         // explicit engineering proxy for the Ask-side SELL trigger geometry.
         double highAskProxy = highBid + record.FrozenSpreadPrice;
         double lowAskProxy = lowBid + record.FrozenSpreadPrice;
         slHit = (highAskProxy >= record.StopLoss);
         tpHit = (lowAskProxy <= record.TakeProfit);
      }
      else
      {
         outcome = "UNCOMPARABLE_DIRECTION";
         return;
      }

      if(slHit && tpHit)
      {
         outcome = "AMBIGUOUS_SAME_M1_BAR";
         hitTime = barTime;
         return;
      }
      if(slHit)
      {
         outcome = "SL_FIRST";
         hitTime = barTime;
         return;
      }
      if(tpHit)
      {
         outcome = "TP_FIRST";
         hitTime = barTime;
         return;
      }
   }
}

void NMJE_P2_PrintCounterfactualOutcomes(int ticket, datetime closeTime)
{
   if(!IsTesting()) return;
   int activeIndex = NMJE_P2_FindCounterfactualTradeSet(ticket);
   if(activeIndex < 0) return;

   NMJECounterfactualTradeSet active = g_nmje_cf_active[activeIndex];
   for(int i = 0; i < active.Count && i < NMJE_CF_MAX_CANDIDATES; i++)
   {
      if(!active.Candidates[i].Present) continue;
      string outcome = "";
      datetime hitTime = 0;
      int barsChecked = 0;
      int ownerBarsChecked = 0;
      NMJE_P2_ResolvePairedWindowOutcome(active, active.Candidates[i],
                                         closeTime, outcome,
                                         hitTime, barsChecked,
                                         ownerBarsChecked);

      Print("[Q9-P2-CF-OUT] Pair=", active.Pair,
            " Ticket=", IntegerToString(active.Ticket),
            " DIDH=", active.BaselineDecisionHash,
            " Set=", active.SetID,
            " CID=", active.Candidates[i].CandidateID,
            " Selected=", active.Candidates[i].Selected ? "Y" : "N",
            " Sig=", EnumToString(active.Candidates[i].SignalType),
            " Dir=", NMJE_DirText(active.Candidates[i].Direction),
            " Outcome=", outcome,
            " Hit=", IntegerToString((int)hitTime),
            " Bars=", IntegerToString(barsChecked),
            " OwnerBars=", IntegerToString(ownerBarsChecked),
            " WindowClose=", IntegerToString((int)closeTime),
            " Method=PAIRED_BASELINE_WINDOW_CLOSED_M1_C044_REPLAY Authority=NONE");
   }
   ZeroMemory(g_nmje_cf_active[activeIndex]);
}

bool IsExactExtremeTPWIdentityEnrichmentPair(ValidatedSequenceCandidate &a,
                                             ValidatedSequenceCandidate &b)
{
   if(a.SequenceType != SIGNAL_RE_ENTRY || b.SequenceType != SIGNAL_RE_ENTRY)
      return false;
   if(a.Direction != b.Direction ||
      (a.Direction != DIR_BUY && a.Direction != DIR_SELL))
      return false;
   if(a.SequenceHash == "" || a.SequenceHash != b.SequenceHash)
      return false;

   datetime aAnchor = GetCandidateAnchorTime(a);
   datetime bAnchor = GetCandidateAnchorTime(b);
   if(aAnchor <= 0 || aAnchor != bAnchor) return false;
   if(a.SequenceStartTime <= 0 || a.SequenceStartTime != b.SequenceStartTime)
      return false;

   bool aHasH1Identity = false;
   bool bHasH1Identity = false;
   for(int i = 0; i < a.ComponentCount && i < 3; i++)
   {
      if(a.Components[i].ComponentType == SIGNAL_RE_ENTRY &&
         a.Components[i].Direction == a.Direction &&
         a.Components[i].Timeframe == PERIOD_H1 &&
         a.Components[i].CandleTime == aAnchor)
         aHasH1Identity = true;
   }
   for(int j = 0; j < b.ComponentCount && j < 3; j++)
   {
      if(b.Components[j].ComponentType == SIGNAL_RE_ENTRY &&
         b.Components[j].Direction == b.Direction &&
         b.Components[j].Timeframe == PERIOD_H1 &&
         b.Components[j].CandleTime == bAnchor)
         bHasH1Identity = true;
   }
   if(!aHasH1Identity || !bHasH1Identity) return false;

   bool aExtremeTPW = (a.UsesD1Opportunity &&
                       a.D1OpportunityFamily == D1_OPP_EXTREME_TPW);
   bool bExtremeTPW = (b.UsesD1Opportunity &&
                       b.D1OpportunityFamily == D1_OPP_EXTREME_TPW);
   bool aStandalone = !a.UsesD1Opportunity;
   bool bStandalone = !b.UsesD1Opportunity;

   return ((aExtremeTPW && bStandalone) ||
           (bExtremeTPW && aStandalone));
}

int CompareCanonicalCandidates(ValidatedSequenceCandidate &a,
                               ValidatedSequenceCandidate &b)
{
   datetime aAnchor = GetCandidateAnchorTime(a);
   datetime bAnchor = GetCandidateAnchorTime(b);
   if(aAnchor > bAnchor) return 1;
   if(aAnchor < bAnchor) return -1;

   if(a.SequenceStartTime > b.SequenceStartTime) return 1;
   if(a.SequenceStartTime < b.SequenceStartTime) return -1;

   if(a.SequenceHash > b.SequenceHash) return 1;
   if(a.SequenceHash < b.SequenceHash) return -1;

   // #214: exact same H1 Re-Entry identity is one executable identity.
   // Only the specific EXTREME_TPW overlap enriches that identity with
   // D1 TP-Wajib attribution/lifecycle semantics. This is not generic
   // D1 Opportunity precedence.
   if(IsExactExtremeTPWIdentityEnrichmentPair(a, b))
   {
      bool aExtremeTPW = (a.UsesD1Opportunity &&
                          a.D1OpportunityFamily == D1_OPP_EXTREME_TPW);
      bool bExtremeTPW = (b.UsesD1Opportunity &&
                          b.D1OpportunityFamily == D1_OPP_EXTREME_TPW);
      if(aExtremeTPW && !bExtremeTPW) return 1;
      if(bExtremeTPW && !aExtremeTPW) return -1;
   }

   return 0;
}

void PriorityEngine_Atomic(ValidatedSequenceCandidate &candidates[], int count,
                           PairState &pairState,
                           BBMA_Decision &decision, OppositeConflictPackage &conflict)
{
   int structurallyEligible = 0;
   for(int i = 0; i < count; i++)
      if(IsCandidateEligible(candidates[i])) structurallyEligible++;

   // D1O-02: authority is evaluated per candidate. Legacy candidates remain
   // MA50-strategic gated; only explicit Mode-2 D1 opportunity candidates may
   // use the separately frozen opportunity authority.
   int buyCount = 0;
   int sellCount = 0;

   for(int i = 0; i < count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;
      if(candidates[i].Direction == DIR_BUY) buyCount++;
      else if(candidates[i].Direction == DIR_SELL) sellCount++;
   }

   if(DebugLevel >= DBG_SIGNAL && EntryMode == 1 && (buyCount > 0 || sellCount > 0))
      Print("[P3M1][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));
   if(DebugLevel >= DBG_SIGNAL && EntryMode == 2 && (buyCount > 0 || sellCount > 0))
      Print("[P3M2][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));

   if(buyCount > 0 && sellCount > 0)
   {
      conflict.Exists = true;
      conflict.ConflictType = CONFLICT_DIRECTION_VIOLATION;
      conflict.ConflictReason = "Opposite validated BBMA entries coexist";
      conflict.FrozenSnapshotTime = g_processing_time;
      if(EntryMode == 1)
         Print("[P3M1][M15_CONFLICT] Opposite eligible RE candidates; no winner selected");
      if(EntryMode == 2)
         Print("[P3M2][M15_CONFLICT] Opposite eligible Mode2 candidates; no winner selected");
      return;
   }

   ENUM_DIRECTION targetDirection = DIR_NONE;
   if(buyCount > 0) targetDirection = DIR_BUY;
   else if(sellCount > 0) targetDirection = DIR_SELL;
   else return;

   int canonicalIdx = -1;
   for(int i = 0; i < count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;
      if(candidates[i].Direction != targetDirection) continue;

      if(canonicalIdx < 0 ||
         CompareCanonicalCandidates(candidates[i], candidates[canonicalIdx]) > 0)
      {
         canonicalIdx = i;
      }
   }

   if(canonicalIdx < 0) return;

   ValidatedSequenceCandidate selected = candidates[canonicalIdx];
   bool authorityFrozen = selected.UsesD1Opportunity
                          ? FreezeD1OpportunitySnapshot(pairState, selected, decision)
                          : FreezeD1OwnerSnapshot(pairState, decision);
   if(!authorityFrozen)
   {
      Print("[D1O][M15_D1_BLOCK] Pair=", pairState.actual_symbol,
            " Reason=authority_freeze_failed");
      return;
   }

   decision.Valid = true;
   decision.Direction = selected.Direction;
   decision.SignalType = selected.SequenceType;
   decision.PriorityTier = TIER_NONE;
   decision.ComponentCount = selected.ComponentCount;
   for(int c = 0; c < 3; c++)
      decision.Components[c] = selected.Components[c];
   decision.HasSLTPSourceComponent =
      ResolveSelectedSLTPSourceComponent(selected, decision.SLTPSourceComponent);

   decision.CandidateExpiry = selected.Expiry;
   decision.SequenceHash = selected.SequenceHash;
   decision.SequenceValid = true;
   decision.PatternValid = true;
   decision.CandleTime = GetCandidateAnchorTime(selected);
   decision.CycleStartTime = selected.SequenceStartTime;
   decision.SLTPSource = SIGNAL_NONE;
   decision.DecisionState = DEC_CREATED;

   decision.DecisionID = GenerateDecisionID(decision.Pair, decision.CandleTime,
                                             decision.Direction,
                                             decision.SignalType,
                                             decision.SequenceHash);
   if(EntryMode == 1)
   {
      string selectMessageM1 = "[P3M1][M15_SELECT] Pair=" + decision.Pair +
                             " Signal=" + EnumToString(decision.SignalType) +
                             " Dir=" + EnumToString(decision.Direction) +
                             " D1State=" + EnumToString(decision.D1OwnerState) +
                             " D1Candle=" + TimeToString(decision.D1OwnerCandleTime) +
                             " Candle=" + TimeToString(decision.CandleTime) +
                             " DecisionID=" + decision.DecisionID;
      ObserverPrintChanged("M15_SELECT_M1|" + decision.Pair, selectMessageM1);
   }
   if(EntryMode == 2)
   {
      string selectMessageM2 = "[P3M2][M15_SELECT] Pair=" + decision.Pair +
                             " Signal=" + EnumToString(decision.SignalType) +
                             " Dir=" + EnumToString(decision.Direction) +
                             " D1State=" + EnumToString(decision.D1OwnerState) +
                             " D1Candle=" + TimeToString(decision.D1OwnerCandleTime) +
                             " Candle=" + TimeToString(decision.CandleTime) +
                             " Components=" + IntegerToString(decision.ComponentCount) +
                             " DecisionID=" + decision.DecisionID;
      ObserverPrintChanged("M15_SELECT_M2|" + decision.Pair, selectMessageM2);
   }
}

//+------------------------------------------------------------------+
//| MODULE 16: CONFLICT & INVALIDATION ENGINE                        |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

void UpdatePersistentExtremeState(Signal &matureExtreme, Signal &state)
{
   // M08 lifecycle exclusively owns Extreme validity through structural
   // VOID/supersession. M16 mirrors the current exact owner; age is metadata only.
   if(!matureExtreme.Valid)
   {
      ZeroMemory(state);
      return;
   }

   state = matureExtreme;
}

bool IsPersistentExtremeComponentValid(PairState &pairState,
                                       ComponentIdentity &component,
                                       bool &expired)
{
   expired = false;

   // Standalone H1 Extreme uses the exact M08 RETEST/ENTRY-READY lifecycle
   // identity. Combination Extremes continue through the existing maturity
   // snapshot path below and remain reversal-confirmed component semantics.
   ExtremeLifecycleData lifecycle;
   ZeroMemory(lifecycle);
   if(component.Timeframe == PERIOD_H1 && component.Direction == DIR_BUY)
      lifecycle = pairState.extreme_h1_buy_lifecycle;
   else if(component.Timeframe == PERIOD_H1 && component.Direction == DIR_SELL)
      lifecycle = pairState.extreme_h1_sell_lifecycle;

   if(lifecycle.Maturity == EXT_MAT_RETEST_READY && lifecycle.IsValid &&
      lifecycle.Direction == component.Direction && lifecycle.Timeframe == PERIOD_H1 &&
      lifecycle.RawCandleTime > 0 && lifecycle.RetestCompletionCandleTime > 0 &&
      lifecycle.RawCandleTime <= lifecycle.RetestCompletionCandleTime &&
      lifecycle.RetestCompletionCandleTime == component.CandleTime)
      return true;

   Signal state;
   ZeroMemory(state);

   if(component.Timeframe == PERIOD_H1 && component.Direction == DIR_BUY)
      state = pairState.extreme_h1_buy_state;
   else if(component.Timeframe == PERIOD_H1 && component.Direction == DIR_SELL)
      state = pairState.extreme_h1_sell_state;
   else if(component.Timeframe == PERIOD_H4 && component.Direction == DIR_BUY)
      state = pairState.extreme_h4_buy_state;
   else if(component.Timeframe == PERIOD_H4 && component.Direction == DIR_SELL)
      state = pairState.extreme_h4_sell_state;
   else
      return false;

   return (state.Valid &&
           state.Type == SIGNAL_EXTREME &&
           state.Direction == component.Direction &&
           state.Timeframe == component.Timeframe &&
           state.CandleTime == component.CandleTime);
}

bool IsPersistentMLVComponentValid(PairState &pairState,
                                   ComponentIdentity &component,
                                   bool &expired)
{
   expired = false;
   if(component.Timeframe != PERIOD_M15) return false;

   MLVData mlv;
   ZeroMemory(mlv);
   if(component.Direction == DIR_BUY) mlv = pairState.mlv_buy_state;
   else if(component.Direction == DIR_SELL) mlv = pairState.mlv_sell_state;
   else return false;

   // F1 lifecycle has no generic candle/session/day expiry. Exact formation
   // identity stays valid until structural VOID or atomic cycle supersession.
   return (IsCanonicalMLVMatureState(mlv.State) &&
           mlv.IsValid &&
           mlv.Timeframe == PERIOD_M15 &&
           mlv.FrozenMarkedBody > 0 &&
           mlv.Direction == component.Direction &&
           mlv.ConfirmationCandleTime == component.CandleTime);
}

bool IsPersistentReEntryComponentValid(PairState &pairState,
                                       ComponentIdentity &component,
                                       bool &expired)
{
   expired = false;
   ReEntryData reEntry;
   ZeroMemory(reEntry);

   if(component.Timeframe == PERIOD_H1 && component.Direction == DIR_BUY)
      reEntry = pairState.re_h1_buy_state;
   else if(component.Timeframe == PERIOD_H1 && component.Direction == DIR_SELL)
      reEntry = pairState.re_h1_sell_state;
   else if(component.Timeframe == PERIOD_H4 && component.Direction == DIR_BUY)
      reEntry = pairState.re_h4_buy_state;
   else if(component.Timeframe == PERIOD_H4 && component.Direction == DIR_SELL)
      reEntry = pairState.re_h4_sell_state;
   else if(component.Timeframe == PERIOD_D1 && component.Direction == DIR_BUY)
      reEntry = pairState.re_d1_buy_state;
   else if(component.Timeframe == PERIOD_D1 && component.Direction == DIR_SELL)
      reEntry = pairState.re_d1_sell_state;
   else if(component.Timeframe == PERIOD_M15 && component.Direction == DIR_BUY)
      reEntry = pairState.re_m15_buy_state;
   else if(component.Timeframe == PERIOD_M15 && component.Direction == DIR_SELL)
      reEntry = pairState.re_m15_sell_state;
   else
      return false;

   return (reEntry.State == RE_STATE_CONFIRMED &&
           reEntry.IsValid &&
           reEntry.Direction == component.Direction &&
           reEntry.Timeframe == component.Timeframe &&
           reEntry.ConfirmationCandle == component.CandleTime);
}

bool IsDecisionComponentOwnerValid(PairState &pairState,
                                   ComponentIdentity &component,
                                   bool &expired)
{
   expired = false;
   if(component.ComponentType == SIGNAL_RE_ENTRY)
      return IsPersistentReEntryComponentValid(pairState, component, expired);
   if(component.ComponentType == SIGNAL_MLV)
      return IsPersistentMLVComponentValid(pairState, component, expired);
   if(component.ComponentType == SIGNAL_EXTREME)
      return IsPersistentExtremeComponentValid(pairState, component, expired);
   return false;
}

bool ValidateDecisionD1OwnerSnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(!decision.D1OwnerSnapshotValid) return false;

   PairState state = g_pair_states[pairIndex];
   if(!IsD1MajorTrendOwnerExecutionReady(state)) return false;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   if(decision.D1OwnerState != owner.State) return false;
   if(decision.D1OwnerDirection != owner.Direction) return false;
   if(decision.Direction != owner.Direction) return false;
   if(decision.D1OwnerCandleTime != owner.SourceCandleTime) return false;
   if(decision.D1OwnerClose != owner.Close1) return false;
   if(decision.D1OwnerMA50Current != owner.MA50_1) return false;
   if(decision.D1OwnerMA50Previous != owner.MA50_2) return false;

   return true;
}

bool ValidateDecisionD1OpportunitySnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(decision.D1AuthorityMode != D1_AUTH_OPPORTUNITY ||
      !decision.D1OpportunitySnapshotValid || !decision.D1OwnerSnapshotValid)
      return false;

   PairState state = g_pair_states[pairIndex];
   D1OpportunityJourney opportunity = state.d1_opportunity;
   if(!opportunity.Active || opportunity.CycleID == "") return false;
   if(decision.D1OpportunityFamily != opportunity.Family) return false;
   if(decision.D1OpportunityDirection != opportunity.Direction) return false;
   if(decision.D1OpportunitySourceSignal != opportunity.SourceSignal) return false;
   if(decision.D1OpportunitySourceCandleTime != opportunity.SourceCandleTime) return false;
   if(decision.D1OpportunityActivationTime != opportunity.ActivationTime) return false;
   if(decision.D1OpportunityCycleID != opportunity.CycleID) return false;
   if(decision.Direction != opportunity.Direction) return false;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
      return false;
   if(decision.D1OwnerState != owner.State ||
      decision.D1OwnerDirection != owner.Direction ||
      decision.D1OwnerCandleTime != owner.SourceCandleTime ||
      decision.D1OwnerClose != owner.Close1 ||
      decision.D1OwnerMA50Current != owner.MA50_1 ||
      decision.D1OwnerMA50Previous != owner.MA50_2)
      return false;

   if(opportunity.Family != D1_OPP_EXTREME_TPW)
   {
      if(!IsD1MajorTrendOwnerExecutionReady(state)) return false;
      if(decision.Direction != owner.Direction) return false;
   }
   else if(owner.State == D1_OWNER_UNRESOLVED)
      return false;

   return true;
}

bool ValidateDecisionD1AuthoritySnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY)
      return ValidateDecisionD1OpportunitySnapshot(pairIndex, decision);
   if(decision.D1AuthorityMode == D1_AUTH_STRATEGIC_OWNER)
      return ValidateDecisionD1OwnerSnapshot(pairIndex, decision);
   return false;
}

bool ValidateDecisionOwnerSnapshot(int pairIndex, BBMA_Decision &decision,
                                   bool &expired)
{
   expired = false;
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(decision.ComponentCount < 1 || decision.ComponentCount > 3) return false;

   for(int i = 0; i < decision.ComponentCount; i++)
   {
      bool componentExpired = false;
      if(!IsDecisionComponentOwnerValid(g_pair_states[pairIndex],
                                        decision.Components[i],
                                        componentExpired))
      {
         if(componentExpired) expired = true;
         return false;
      }
   }
   return true;
}

void InvalidationEngine_Atomic(int pairIndex, BBMA_Decision &decision,
                               OppositeConflictPackage &conflict)
{
   if(decision.DecisionState != DEC_CREATED) return;

   if(conflict.Exists &&
      (conflict.ConflictType == CONFLICT_DIRECTION_VIOLATION ||
       conflict.BreaksSequence))
   {
      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_OPPOSITE_SIGNAL;
      if(EntryMode == 1)
         Print("[P3M1][M16_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      if(EntryMode == 2)
         Print("[P3M2][M16_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      return;
   }

   if(!ValidateDecisionD1AuthoritySnapshot(pairIndex, decision))
   {
      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_SEQUENCE_BREAK;
      Print("[D1O][M16_D1_REJECT] Pair=", decision.Pair,
            " DecisionID=", decision.DecisionID,
            " Authority=", D1AuthorityModeText(decision.D1AuthorityMode),
            " Opp=", D1OpportunityFamilyText(decision.D1OpportunityFamily),
            " FrozenState=", EnumToString(decision.D1OwnerState),
            " FrozenDir=", EnumToString(decision.D1OwnerDirection),
            " FrozenCandle=", TimeToString(decision.D1OwnerCandleTime));
      return;
   }

   bool ownerExpired = false;
   if(!ValidateDecisionOwnerSnapshot(pairIndex, decision, ownerExpired))
   {
      if(ownerExpired)
      {
         decision.DecisionState = DEC_EXPIRED;
         decision.RejectionReason = REJ_EXPIRED;
      }
      else
      {
         decision.DecisionState = DEC_INVALIDATED;
         decision.RejectionReason = REJ_SEQUENCE_BREAK;
      }
      if(EntryMode == 2)
         Print("[P3M2][M16_OWNER_REJECT] DecisionID=", decision.DecisionID,
               " State=", EnumToString(decision.DecisionState),
               " Reason=", EnumToString(decision.RejectionReason));
      return;
   }

   if(decision.CandidateExpiry > 0 && g_processing_time > decision.CandidateExpiry)
   {
      decision.DecisionState = DEC_EXPIRED;
      decision.RejectionReason = REJ_EXPIRED;
      return;
   }

   decision.DecisionState = DEC_VALIDATED;
   decision.RejectionReason = REJ_NONE;
   if(EntryMode == 1)
   {
      string passMessageM1 = "[P3M1][M16_PASS] DecisionID=" + decision.DecisionID +
                           " Signal=" + EnumToString(decision.SignalType) +
                           " Candle=" + TimeToString(decision.CandleTime);
      ObserverPrintChanged("M16_PASS_M1|" + decision.Pair, passMessageM1);
   }
   if(EntryMode == 2)
   {
      string passMessageM2 = "[P3M2][M16_PASS] DecisionID=" + decision.DecisionID +
                           " Signal=" + EnumToString(decision.SignalType) +
                           " Candle=" + TimeToString(decision.CandleTime);
      ObserverPrintChanged("M16_PASS_M2|" + decision.Pair, passMessageM2);
   }
}

//+------------------------------------------------------------------+
//| MODULE 17: SL/TP VALIDATION                                      |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool IsApprovedSLTPSourceComponent(BBMA_Decision &decision,
                                   ComponentIdentity &source)
{
   if(!decision.HasSLTPSourceComponent) return false;
   if(source.Direction != decision.Direction) return false;
   if(source.CandleTime <= 0) return false;

   if(decision.SignalType == SIGNAL_EXTREME)
      return (source.ComponentType == SIGNAL_EXTREME && source.Timeframe == PERIOD_H1);

   if(source.ComponentType != SIGNAL_RE_ENTRY) return false;
   if(decision.SignalType == SIGNAL_RE_ENTRY)
   {
      if(decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY &&
         decision.D1OpportunitySnapshotValid)
         return (source.Timeframe == PERIOD_H1 || source.Timeframe == PERIOD_M15);
      return (source.Timeframe == PERIOD_H1);
   }

   if(decision.SignalType == SIGNAL_REM)
      return (source.Timeframe == PERIOD_H4);

   if(decision.SignalType == SIGNAL_RRE ||
      decision.SignalType == SIGNAL_REE)
      return (source.Timeframe == PERIOD_D1);

   return false;
}

int ResolveClosedSourceShift(string pair, ComponentIdentity &source)
{
   if(source.Timeframe <= 0 || source.CandleTime <= 0) return -1;

   int shift = iBarShift(pair, source.Timeframe, source.CandleTime, true);
   if(shift < 1) return -1;

   datetime resolvedTime = iTime(pair, source.Timeframe, shift);
   if(resolvedTime != source.CandleTime) return -1;
   return shift;
}

// M17-SLRANGE-01: resolve the exact M12 Re-Entry lifecycle that owns
// the approved SLTP source component. This does not redetect Re-Entry.
bool ResolveMatchingReEntryLifecycle(string pair, ComponentIdentity &source,
                                     ReEntryData &reEntry)
{
   ZeroMemory(reEntry);

   int pairIndex = FindPairStateIndex(pair);
   if(pairIndex < 0)
   {
      for(int i = 0; i < g_pair_count; i++)
      {
         if(g_pair_states[i].actual_symbol == pair)
         {
            pairIndex = i;
            break;
         }
      }
   }
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;

   if(source.Timeframe == PERIOD_H1 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_h1_buy_state;
   else if(source.Timeframe == PERIOD_H1 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_h1_sell_state;
   else if(source.Timeframe == PERIOD_H4 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_h4_buy_state;
   else if(source.Timeframe == PERIOD_H4 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_h4_sell_state;
   else if(source.Timeframe == PERIOD_D1 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_d1_buy_state;
   else if(source.Timeframe == PERIOD_D1 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_d1_sell_state;
   else if(source.Timeframe == PERIOD_M15 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_m15_buy_state;
   else if(source.Timeframe == PERIOD_M15 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_m15_sell_state;
   else
      return false;

   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return false;
   if(reEntry.Direction != source.Direction || reEntry.Timeframe != source.Timeframe)
      return false;
   if(reEntry.ConfirmationCandle != source.CandleTime) return false;
   if(reEntry.StartCandleTime <= 0 || reEntry.ConfirmationCandle <= 0) return false;
   if(reEntry.StartCandleTime > reEntry.ConfirmationCandle) return false;
   return true;
}

// M17-SLRANGE-01: reconstruct only the source-owned lifecycle window
// StartCandleTime..ConfirmationCandle inclusive. No arbitrary swing lookback.
bool ResolveSourceOwnedStructuralAnchor(string pair, ComponentIdentity &source,
                                        ENUM_DIRECTION direction, double &anchor,
                                        datetime &startTime,
                                        datetime &confirmationTime,
                                        double &confirmationWick)
{
   anchor = 0.0;
   startTime = 0;
   confirmationTime = 0;
   confirmationWick = 0.0;

   ReEntryData reEntry;
   if(!ResolveMatchingReEntryLifecycle(pair, source, reEntry)) return false;

   startTime = reEntry.StartCandleTime;
   confirmationTime = reEntry.ConfirmationCandle;

   int startShift = iBarShift(pair, source.Timeframe, startTime, true);
   int confirmationShift = iBarShift(pair, source.Timeframe,
                                     confirmationTime, true);
   if(startShift < 1 || confirmationShift < 1) return false;
   if(startShift < confirmationShift) return false;
   if(iTime(pair, source.Timeframe, startShift) != startTime) return false;
   if(iTime(pair, source.Timeframe, confirmationShift) != confirmationTime)
      return false;

   int tfSeconds = GetTimeframeSeconds(source.Timeframe);
   if(tfSeconds <= 0) return false;

   for(int shift = confirmationShift; shift <= startShift; shift++)
   {
      datetime barTime = iTime(pair, source.Timeframe, shift);
      if(barTime <= 0 || barTime < startTime || barTime > confirmationTime)
         return false;
      if(!IsCandleClosed(barTime, tfSeconds)) return false;

      double low = iLow(pair, source.Timeframe, shift);
      double high = iHigh(pair, source.Timeframe, shift);
      if(low <= 0.0 || high <= 0.0 || high < low) return false;

      if(direction == DIR_BUY)
      {
         if(anchor <= 0.0 || low < anchor) anchor = low;
      }
      else if(direction == DIR_SELL)
      {
         if(anchor <= 0.0 || high > anchor) anchor = high;
      }
      else
         return false;
   }

   if(direction == DIR_BUY)
      confirmationWick = iLow(pair, source.Timeframe, confirmationShift);
   else if(direction == DIR_SELL)
      confirmationWick = iHigh(pair, source.Timeframe, confirmationShift);
   else
      return false;

   return (anchor > 0.0 && confirmationWick > 0.0);
}

bool ResolveMatchingStandaloneExtremeLifecycle(string pair, ComponentIdentity &source,
                                              ExtremeLifecycleData &extreme)
{
   ZeroMemory(extreme);
   if(source.ComponentType != SIGNAL_EXTREME || source.Timeframe != PERIOD_H1) return false;
   int pairIndex = FindPairStateIndex(pair);
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;

   if(source.Direction == DIR_BUY)
      extreme = g_pair_states[pairIndex].extreme_h1_buy_lifecycle;
   else if(source.Direction == DIR_SELL)
      extreme = g_pair_states[pairIndex].extreme_h1_sell_lifecycle;
   else
      return false;

   if(extreme.Maturity != EXT_MAT_RETEST_READY || !extreme.IsValid) return false;
   if(extreme.Direction != source.Direction || extreme.Timeframe != PERIOD_H1) return false;
   if(extreme.RawCandleTime <= 0 || extreme.RetestCompletionCandleTime <= 0) return false;
   if(extreme.RawCandleTime > extreme.RetestCompletionCandleTime) return false;
   return (extreme.RetestCompletionCandleTime == source.CandleTime);
}

bool ResolveStandaloneExtremeStructuralAnchor(string pair, ComponentIdentity &source,
                                              ENUM_DIRECTION direction, double &anchor,
                                              datetime &startTime, datetime &completionTime,
                                              double &completionWick)
{
   anchor = 0.0; startTime = 0; completionTime = 0; completionWick = 0.0;
   ExtremeLifecycleData extreme;
   if(!ResolveMatchingStandaloneExtremeLifecycle(pair, source, extreme)) return false;
   if(direction != source.Direction) return false;

   startTime = extreme.RawCandleTime;
   completionTime = extreme.RetestCompletionCandleTime;
   int rawShift = iBarShift(pair, PERIOD_H1, startTime, true);
   int completionShift = iBarShift(pair, PERIOD_H1, completionTime, true);
   if(rawShift < 1 || completionShift < 1 || rawShift < completionShift) return false;
   if(iTime(pair, PERIOD_H1, rawShift) != startTime ||
      iTime(pair, PERIOD_H1, completionShift) != completionTime) return false;

   int tfSeconds = GetTimeframeSeconds(PERIOD_H1);
   if(tfSeconds <= 0) return false;
   for(int shift = completionShift; shift <= rawShift; shift++)
   {
      datetime barTime = iTime(pair, PERIOD_H1, shift);
      if(barTime <= 0 || barTime < startTime || barTime > completionTime) return false;
      if(!IsCandleClosed(barTime, tfSeconds)) return false;
      double low = iLow(pair, PERIOD_H1, shift);
      double high = iHigh(pair, PERIOD_H1, shift);
      if(low <= 0.0 || high <= 0.0 || high < low) return false;
      if(direction == DIR_BUY && (anchor <= 0.0 || low < anchor)) anchor = low;
      else if(direction == DIR_SELL && (anchor <= 0.0 || high > anchor)) anchor = high;
   }
   completionWick = (direction == DIR_BUY)
                    ? iLow(pair, PERIOD_H1, completionShift)
                    : iHigh(pair, PERIOD_H1, completionShift);
   return (anchor > 0.0 && completionWick > 0.0);
}

bool ResolveApprovedBBDestination(string pair, ComponentIdentity &source,
                                  ENUM_DIRECTION direction, double &destination)
{
   destination = 0.0;
   int shift = ResolveClosedSourceShift(pair, source);
   if(shift < 1) return false;

   int mode = (direction == DIR_BUY) ? MODE_UPPER :
              (direction == DIR_SELL ? MODE_LOWER : -1);
   if(mode < 0) return false;

   destination = iBands(pair, source.Timeframe,
                        BB_PERIOD, BB_DEVIATION, 0, PRICE_CLOSE,
                        mode, shift);
   return (destination > 0.0);
}

bool ResolveStandaloneExtremeTPWajib(string pair, ComponentIdentity &source,
                                      ENUM_DIRECTION direction, double &destination)
{
   destination = 0.0;
   if(source.ComponentType != SIGNAL_EXTREME || source.Timeframe != PERIOD_H1) return false;
   int shift = ResolveClosedSourceShift(pair, source);
   if(shift < 1) return false;

   double ma5 = 0.0;
   double ma10 = 0.0;
   if(direction == DIR_BUY)
   {
      ma5 = BBMAHighMA(pair, PERIOD_H1, MA5_HIGH_PERIOD, shift);
      ma10 = BBMAHighMA(pair, PERIOD_H1, MA10_HIGH_PERIOD, shift);
      if(ma5 <= 0.0 || ma10 <= 0.0) return false;
      destination = MathMin(ma5, ma10);
   }
   else if(direction == DIR_SELL)
   {
      ma5 = BBMALowMA(pair, PERIOD_H1, MA5_LOW_PERIOD, shift);
      ma10 = BBMALowMA(pair, PERIOD_H1, MA10_LOW_PERIOD, shift);
      if(ma5 <= 0.0 || ma10 <= 0.0) return false;
      destination = MathMax(ma5, ma10);
   }
   else
      return false;

   return (destination > 0.0);
}

bool IsF7LifecycleIdentity(BBMA_Decision &decision)
{
   if(!EnableC044Lifecycle || !decision.HasSLTPSourceComponent) return false;
   ComponentIdentity source = decision.SLTPSourceComponent;
   if(source.ComponentType != SIGNAL_RE_ENTRY || source.Direction != decision.Direction ||
      source.CandleTime <= 0) return false;
   if(decision.SignalType == SIGNAL_RE_ENTRY) return (source.Timeframe == PERIOD_H1);
   if(decision.SignalType == SIGNAL_REM) return (source.Timeframe == PERIOD_H4);
   if(decision.SignalType == SIGNAL_RRE || decision.SignalType == SIGNAL_REE)
      return (source.Timeframe == PERIOD_D1);
   return false;
}

bool IsD1TPWLifecycleIdentity(BBMA_Decision &decision)
{
   return (decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY &&
           decision.D1OpportunitySnapshotValid &&
           decision.D1OpportunityFamily == D1_OPP_EXTREME_TPW &&
           decision.D1OpportunitySourceSignal == SIGNAL_EXTREME &&
           decision.D1OpportunityDirection == decision.Direction &&
           decision.D1OpportunitySourceCandleTime > 0 &&
           decision.D1OpportunityCycleID != "");
}

bool IsTargetlessLifecycleDecision(BBMA_Decision &decision)
{
   return (decision.C044LifecycleManaged || decision.D1TPWLifecycleManaged);
}

bool ResolveApprovedInitialSLTP(BBMA_Decision &decision,
                                RiskValidationSnapshot &snapshot)
{
   if(!IsApprovedSLTPSourceComponent(decision,
                                     decision.SLTPSourceComponent))
      return false;

   bool standaloneExtreme = (decision.SignalType == SIGNAL_EXTREME);
   bool d1TPWLifecycle = IsD1TPWLifecycleIdentity(decision);
   if(d1TPWLifecycle && !EnableD1TPWLifecycle)
      return false; // never execute EXTREME_TPW with the legacy RE outer-BB TP
   d1TPWLifecycle = d1TPWLifecycle && EnableD1TPWLifecycle;
   bool c044Lifecycle = IsF7LifecycleIdentity(decision) && !d1TPWLifecycle;
   bool targetlessLifecycle = (d1TPWLifecycle || c044Lifecycle);

   double structuralAnchor = 0.0;
   datetime structuralStart = 0;
   datetime structuralConfirmation = 0;
   double confirmationWick = 0.0;
   double destination = 0.0;
   bool structuralResolved = standaloneExtreme
      ? ResolveStandaloneExtremeStructuralAnchor(decision.Pair,
                                                 decision.SLTPSourceComponent,
                                                 decision.Direction,
                                                 structuralAnchor,
                                                 structuralStart,
                                                 structuralConfirmation,
                                                 confirmationWick)
      : ResolveSourceOwnedStructuralAnchor(decision.Pair,
                                           decision.SLTPSourceComponent,
                                           decision.Direction,
                                           structuralAnchor,
                                           structuralStart,
                                           structuralConfirmation,
                                           confirmationWick);
   if(!structuralResolved) return false;

   // C044 is intentionally fail-safe gated OFF until M23/M24 lifecycle support
   // is complete. While OFF, preserve the v4.52 static destination exactly.
   if(!targetlessLifecycle)
   {
      bool destinationResolved = standaloneExtreme
         ? ResolveStandaloneExtremeTPWajib(decision.Pair,
                                           decision.SLTPSourceComponent,
                                           decision.Direction,
                                           destination)
         : ResolveApprovedBBDestination(decision.Pair,
                                        decision.SLTPSourceComponent,
                                        decision.Direction,
                                        destination);
      if(!destinationResolved) return false;

      if(decision.Direction == DIR_BUY && destination <= decision.EntryPrice)
         return false;
      if(decision.Direction == DIR_SELL && destination >= decision.EntryPrice)
         return false;
   }

   if(snapshot.Point <= 0.0 || decision.EntryPrice <= 0.0) return false;

   double safetyBuffer = snapshot.Point;
   if(standaloneExtreme)
   {
      double pipValue = GetPipValue(decision.Pair);
      if(pipValue <= 0.0) return false;
      safetyBuffer = EXTREME_WICK_BUFFER_PIPS * pipValue;
   }
   double structuralSL = (decision.Direction == DIR_BUY)
      ? structuralAnchor - safetyBuffer
      : structuralAnchor + safetyBuffer;

   // M17-SLRANGE-01: direction-aware broker hard-SL normalization.
   // BUY closes on Bid, aligned with Bid-chart structure: no spread buffer.
   // SELL closes on Ask: add the approved frozen rounded spread buffer.
   double brokerSL = structuralSL;
   double rawSpreadPips = 0.0;
   double roundedSpreadBufferPips = 0.0;
   if(decision.Direction == DIR_SELL)
   {
      double pipValue = GetPipValue(decision.Pair);
      if(pipValue <= 0.0 || snapshot.CurrentSpreadPrice < 0.0) return false;

      rawSpreadPips = snapshot.CurrentSpreadPrice / pipValue;
      roundedSpreadBufferPips = MathCeil(rawSpreadPips - 0.000000001);
      if(roundedSpreadBufferPips < 2.0)
         roundedSpreadBufferPips = 2.0;

      brokerSL += roundedSpreadBufferPips * pipValue;
   }

   if(snapshot.TickSize_Price <= 0.0 || snapshot.Digits < 0) return false;

   double slTicks = brokerSL / snapshot.TickSize_Price;
   double normalizedSL = 0.0;
   if(decision.Direction == DIR_BUY)
      normalizedSL = MathFloor(slTicks + 0.000000001) * snapshot.TickSize_Price;
   else if(decision.Direction == DIR_SELL)
      normalizedSL = MathCeil(slTicks - 0.000000001) * snapshot.TickSize_Price;
   else
      return false;

   normalizedSL = NormalizeDouble(normalizedSL, snapshot.Digits);
   if(normalizedSL <= 0.0) return false;

   double normalizedTP = 0.0;
   if(!targetlessLifecycle)
   {
      double tpTicks = destination / snapshot.TickSize_Price;
      if(decision.Direction == DIR_BUY)
         normalizedTP = MathFloor(tpTicks + 0.000000001) * snapshot.TickSize_Price;
      else if(decision.Direction == DIR_SELL)
         normalizedTP = MathCeil(tpTicks - 0.000000001) * snapshot.TickSize_Price;
      else
         return false;

      normalizedTP = NormalizeDouble(normalizedTP, snapshot.Digits);
      if(normalizedTP <= 0.0) return false;
   }

   decision.StopLoss = normalizedSL;
   decision.TakeProfit = targetlessLifecycle ? 0.0 : normalizedTP;
   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;
   decision.D1TPWLifecycleManaged = d1TPWLifecycle;
   decision.C044LifecycleManaged = c044Lifecycle;

   if(DebugLevel >= DBG_TRADE)
   {
      Print("[M17-SL][STRUCT] Pair=", decision.Pair,
            " Dir=", EnumToString(decision.Direction),
            " TF=", IntegerToString(decision.SLTPSourceComponent.Timeframe),
            " Start=", TimeToString(structuralStart),
            " Confirm=", TimeToString(structuralConfirmation),
            " StructuralAnchor=", DoubleToString(structuralAnchor, snapshot.Digits),
            " ConfirmationWick=", DoubleToString(confirmationWick, snapshot.Digits),
            " RawSpreadPips=", DoubleToString(rawSpreadPips, 4),
            " SpreadBufferPips=", DoubleToString(roundedSpreadBufferPips, 1),
            " StructuralSL=", DoubleToString(structuralSL, snapshot.Digits),
            " FinalBrokerSL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " C044=", decision.C044LifecycleManaged ? "Y" : "N",
            " D1TPW=", decision.D1TPWLifecycleManaged ? "Y" : "N",
            " Extreme=", standaloneExtreme ? "Y" : "N");
   }
   return true;
}

double GetDirectionalClosePrice(RiskValidationSnapshot &snapshot, ENUM_DIRECTION direction)
{
   if(direction == DIR_BUY) return snapshot.Bid;
   if(direction == DIR_SELL) return snapshot.Ask;
   return 0.0;
}

bool ResolveExecutionReferencePrice(BBMA_Decision &decision, RiskValidationSnapshot &snapshot)
{
   double price = 0.0;
   if(decision.Direction == DIR_BUY) price = snapshot.Ask;
   else if(decision.Direction == DIR_SELL) price = snapshot.Bid;

   if(price <= 0.0) return false;

   decision.EntryPrice = price;
   snapshot.EntryPrice = price;
   return true;
}

bool HasSourceResolvedSLTP(BBMA_Decision &decision)
{
   if(decision.SLTPSource == SIGNAL_NONE) return false;
   if(IsTargetlessLifecycleDecision(decision))
      return (decision.StopLoss > 0.0 && decision.TakeProfit == 0.0);
   return (decision.StopLoss > 0.0 && decision.TakeProfit > 0.0);
}

bool ValidateDirectionalSLTPGeometry(BBMA_Decision &decision)
{
   if(IsTargetlessLifecycleDecision(decision))
   {
      if(decision.TakeProfit != 0.0) return false;
      if(decision.Direction == DIR_BUY)
         return (decision.StopLoss < decision.EntryPrice);
      if(decision.Direction == DIR_SELL)
         return (decision.StopLoss > decision.EntryPrice);
      return false;
   }

   if(decision.Direction == DIR_BUY)
      return (decision.StopLoss < decision.EntryPrice &&
              decision.TakeProfit > decision.EntryPrice);

   if(decision.Direction == DIR_SELL)
      return (decision.StopLoss > decision.EntryPrice &&
              decision.TakeProfit < decision.EntryPrice);

   return false;
}

bool ValidateFrozenBrokerDistanceGeometry(BBMA_Decision &decision,
                                          RiskValidationSnapshot &snapshot,
                                          bool validateTP,
                                          ENUM_REJECTION_REASON &rejection)
{
   if(snapshot.Point <= 0.0 || snapshot.StopLevel < 0.0 ||
      snapshot.FreezeLevel < 0.0)
   {
      rejection = REJ_BROKER_SPEC_INVALID;
      return false;
   }

   double closePrice = GetDirectionalClosePrice(snapshot, decision.Direction);
   if(closePrice <= 0.0)
   {
      rejection = REJ_MARKET_PRICE_INVALID;
      return false;
   }

   double stopDistance = snapshot.StopLevel * snapshot.Point;
   double freezeDistance = snapshot.FreezeLevel * snapshot.Point;
   double requiredDistance = MathMax(stopDistance, freezeDistance);

   if(decision.Direction == DIR_BUY)
   {
      if(decision.StopLoss >= closePrice ||
         (requiredDistance > 0.0 &&
          (closePrice - decision.StopLoss) < requiredDistance))
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      if(validateTP &&
         (decision.TakeProfit <= closePrice ||
          (requiredDistance > 0.0 &&
           (decision.TakeProfit - closePrice) < requiredDistance)))
      {
         rejection = REJ_INVALID_TP;
         return false;
      }
      return true;
   }

   if(decision.Direction == DIR_SELL)
   {
      if(decision.StopLoss <= closePrice ||
         (requiredDistance > 0.0 &&
          (decision.StopLoss - closePrice) < requiredDistance))
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      if(validateTP &&
         (decision.TakeProfit >= closePrice ||
          (requiredDistance > 0.0 &&
           (closePrice - decision.TakeProfit) < requiredDistance)))
      {
         rejection = REJ_INVALID_TP;
         return false;
      }
      return true;
   }

   rejection = REJ_MARKET_PRICE_INVALID;
   return false;
}

bool ValidateSLTP(BBMA_Decision &decision, RiskValidationSnapshot &snapshot,
                  ENUM_REJECTION_REASON &rejection)
{
   rejection = REJ_NONE;

   if(decision.EntryPrice <= 0.0 || snapshot.EntryPrice <= 0.0)
   {
      rejection = REJ_MARKET_PRICE_INVALID;
      return false;
   }

   if(!HasSourceResolvedSLTP(decision))
   {
      rejection = REJ_SLTP_UNRESOLVED;
      return false;
   }

   if(decision.StopLoss <= 0.0)
   {
      rejection = REJ_INVALID_SL;
      return false;
   }

   if(IsTargetlessLifecycleDecision(decision))
   {
      if(decision.TakeProfit != 0.0)
      {
         rejection = REJ_INVALID_TP;
         return false;
      }

      if(!ValidateDirectionalSLTPGeometry(decision))
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
      if(slDistance <= 0.0)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      double pipPrice = GetPipValue(decision.Pair);
      if(MaxSLPips > 0.0 && pipPrice > 0.0 && slDistance > MaxSLPips * pipPrice)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      // Targetless lifecycle has no deterministic fixed reward coordinate.
      // If the optional MinRR filter is enabled, fail closed rather than
      // bypassing it or manufacturing a reward target.
      if(MinRRRatio > 0.0)
      {
         rejection = REJ_INVALID_RR;
         return false;
      }

      if(!ValidateFrozenBrokerDistanceGeometry(decision, snapshot, false, rejection))
         return false;

      decision.StopLossPoints = slDistance / snapshot.Point;
      return true;
   }

   if(decision.TakeProfit <= 0.0)
   {
      rejection = REJ_INVALID_TP;
      return false;
   }

   if(!ValidateDirectionalSLTPGeometry(decision))
   {
      rejection = (decision.StopLoss == decision.EntryPrice)
         ? REJ_INVALID_SL : REJ_INVALID_TP;
      return false;
   }

   double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
   double tpDistance = MathAbs(decision.TakeProfit - decision.EntryPrice);
   if(slDistance <= 0.0 || tpDistance <= 0.0)
   {
      rejection = (slDistance <= 0.0) ? REJ_INVALID_SL : REJ_INVALID_TP;
      return false;
   }

   double pipPrice = GetPipValue(decision.Pair);
   if(MaxSLPips > 0.0 && pipPrice > 0.0)
   {
      double maxSLPrice = MaxSLPips * pipPrice;
      if(slDistance > maxSLPrice)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }
   }

   if(MinRRRatio > 0.0 && (tpDistance / slDistance) < MinRRRatio)
   {
      rejection = REJ_INVALID_RR;
      return false;
   }

   if(!ValidateFrozenBrokerDistanceGeometry(decision, snapshot, true, rejection))
      return false;

   decision.StopLossPoints = slDistance / snapshot.Point;
   return true;
}

//+------------------------------------------------------------------+
//| MODULE 18: SIGNAL SCORING ENGINE (LABEL ONLY)                    |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

SignalScoreResult CalculateSignalScore(BBMA_Decision &decision)
{
   SignalScoreResult result;
   result.Score = 0;
   result.Level = LEVEL_NONE;
   result.ScoreBreakdown = "";

   if(!decision.Valid) return result;

   result.ScoreBreakdown = "LABEL_ONLY|Type:" + EnumToString(decision.SignalType) +
                           "|Direction:" + EnumToString(decision.Direction) + "|";

   if(decision.HasSLTPSourceComponent)
      result.ScoreBreakdown += "SourceTF:" +
                               IntegerToString(decision.SLTPSourceComponent.Timeframe) + "|";

   return result;
}

string GetSignalLevelString(ENUM_SIGNAL_LEVEL level)
{
   switch(level)
   {
      case LEVEL_A_PLUS: return "A+";
      case LEVEL_A: return "A";
      case LEVEL_B: return "B";
      case LEVEL_C: return "C";
      case LEVEL_D: return "D";
      default: return "NONE";
   }
}

//+------------------------------------------------------------------+
//| MODULE 19: RISK ENGINE (FILTER ONLY)                             |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

double CalculateDrawdownPercent_EA()
{
   if(g_protection_reference_equity <= 0) return 0;

   double equity = AccountEquity();
   if(equity <= 0) return 100.0;

   double drawdownMoney = g_protection_reference_equity - equity;
   if(drawdownMoney <= 0) return 0;

   return drawdownMoney / g_protection_reference_equity * 100.0;
}

double CalculateBasketLossPercent_EA(bool &valid)
{
   valid = true;
   double floatingLoss = 0;
   
   for(int i = 0; i < g_monitored_count; i++)
   {
      ENUM_PORTFOLIO_OWNERSHIP_STATE ownership =
         GetLiveEAOwnedPortfolioTradeState(i);
      if(ownership == PORT_OWNERSHIP_UNKNOWN)
      {
         valid = false;
         return 0;
      }
      if(ownership != PORT_OWNERSHIP_LIVE_OWNED) continue;

      double profit = OrderProfit() + OrderSwap() + OrderCommission();
      if(profit < 0)
         floatingLoss += MathAbs(profit);
   }
   
   if(g_protection_reference_equity <= 0) return 0;
   return floatingLoss / g_protection_reference_equity * 100;
}

double CalculateTotalRisk(string pair, double newLot, double newEntry, double newSL,
                          RiskValidationSnapshot &snapshot, bool &valid)
{
   valid = true;
   double totalRisk = 0;

   for(int i = 0; i < g_monitored_count; i++)
   {
      ResetLastError();
      if(!OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
      {
         valid = false;
         return 0;
      }
      if(OrderCloseTime() != 0)
         continue;

      // Apply the existing ownership predicate to this selected order.
      // The boolean portfolio helper reselects and hides selection failure.
      int pairIdx = FindPairStateIndex(g_monitored_trades[i].pair);
      if(pairIdx < 0) continue;
      int expectedMagic = g_pair_states[pairIdx].magic_number;
      if(expectedMagic <= 0 ||
         g_monitored_trades[i].magic_number != expectedMagic ||
         OrderMagicNumber() != expectedMagic)
         continue;

      if(g_monitored_trades[i].remaining_lot <= 0)
         continue;

      double riskDistance = MathAbs(g_monitored_trades[i].entry_price -
                                    g_monitored_trades[i].current_sl);

      if(riskDistance <= 0)
         continue;

      if(g_monitored_trades[i].current_sl <= 0)
      {
         valid = false;
         return 0;
      }

      double existingRisk = CalculateTradeRiskMoney(g_monitored_trades[i].pair,
                                                     g_monitored_trades[i].remaining_lot,
                                                     g_monitored_trades[i].entry_price,
                                                     g_monitored_trades[i].current_sl);
      if(existingRisk <= 0)
      {
         valid = false;
         return 0;
      }
      totalRisk += existingRisk;
   }

   double newRisk = CalculateTradeRiskMoney(pair, newLot, newEntry, newSL);
   if(newRisk <= 0)
   {
      valid = false;
      return 0;
   }
   totalRisk += newRisk;

   return totalRisk;
}

RiskStatus CheckRiskBeforeTrade(BBMA_Decision &decision, RiskValidationSnapshot &snapshot, double calculatedLot)
{
   RiskStatus status;
   status.allowed = true;
   status.reason = "";
   status.rejection_reason = REJ_NONE;

   double pipValue = GetPipValue(decision.Pair);
   if(pipValue <= 0)
   {
      status.allowed = false;
      status.reason = "Invalid pip specification";
      status.rejection_reason = REJ_BROKER_SPEC_INVALID;
      return status;
   }

   double spreadPips = snapshot.CurrentSpreadPrice / pipValue;
   if(spreadPips > MaxSpreadPips)
   {
      status.allowed = false;
      status.reason = "Spread too high";
      status.rejection_reason = REJ_SPREAD_HIGH;
      return status;
   }

   double dd = CalculateDrawdownPercent_EA();
   if(dd >= MaxDrawdownPercent)
   {
      status.allowed = false;
      status.reason = "Drawdown limit exceeded";
      status.rejection_reason = REJ_DD_LIMIT;
      return status;
   }

   bool basketValid = true;
   double basketLoss = CalculateBasketLossPercent_EA(basketValid);
   if(!basketValid)
   {
      status.allowed = false;
      status.reason = "Unable to calculate basket loss safely";
      status.rejection_reason = REJ_BASKET_LOSS;
      return status;
   }
   if(basketLoss >= BasketLossPercent)
   {
      status.allowed = false;
      status.reason = "Basket loss limit exceeded";
      status.rejection_reason = REJ_BASKET_LOSS;
      return status;
   }

   bool riskValid = true;
   double totalRisk = CalculateTotalRisk(decision.Pair, calculatedLot,
                                         decision.EntryPrice, decision.StopLoss,
                                         snapshot, riskValid);
   if(!riskValid)
   {
      status.allowed = false;
      status.reason = "Unable to calculate total EA risk safely";
      status.rejection_reason = REJ_TOTAL_RISK;
      return status;
   }

   double equity = snapshot.Equity;
   if(equity <= 0)
   {
      status.allowed = false;
      status.reason = "Invalid equity for total-risk validation";
      status.rejection_reason = REJ_TOTAL_RISK;
      return status;
   }

   if(totalRisk / equity * 100.0 > MaxTotalRiskPercent)
   {
      status.allowed = false;
      status.reason = "Total risk limit exceeded";
      status.rejection_reason = REJ_TOTAL_RISK;
      return status;
   }

   return status;
}

//+------------------------------------------------------------------+
//| MODULE 20: PORTFOLIO RISK & PROTECTION ENGINE                    |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

ENUM_PORTFOLIO_OWNERSHIP_STATE GetLiveEAOwnedPortfolioTradeState(int monitoredIndex)
{
   if(monitoredIndex < 0 || monitoredIndex >= g_monitored_count)
      return PORT_OWNERSHIP_EXCLUDED;

   ResetLastError();
   if(!OrderSelect(g_monitored_trades[monitoredIndex].ticket, SELECT_BY_TICKET))
      return PORT_OWNERSHIP_UNKNOWN;
   if(OrderCloseTime() != 0)
      return PORT_OWNERSHIP_EXCLUDED;

   int pairIdx = FindPairStateIndex(g_monitored_trades[monitoredIndex].pair);
   if(pairIdx < 0)
      return PORT_OWNERSHIP_EXCLUDED;

   int expectedMagic = g_pair_states[pairIdx].magic_number;
   if(expectedMagic <= 0)
      return PORT_OWNERSHIP_EXCLUDED;
   if(g_monitored_trades[monitoredIndex].magic_number != expectedMagic)
      return PORT_OWNERSHIP_EXCLUDED;
   if(OrderMagicNumber() != expectedMagic)
      return PORT_OWNERSHIP_EXCLUDED;
   return PORT_OWNERSHIP_LIVE_OWNED;
}

PortfolioStatus CheckPortfolioLimits()
{
   PortfolioStatus status;
   status.allowed = true;
   status.reason = "";
   status.active_pairs = 0;
   status.total_trades = 0;
   ArrayInitialize(status.trades_per_pair, 0);
   
   for(int i = 0; i < g_monitored_count; i++)
   {
      ENUM_PORTFOLIO_OWNERSHIP_STATE ownership =
         GetLiveEAOwnedPortfolioTradeState(i);
      if(ownership == PORT_OWNERSHIP_UNKNOWN)
      {
         status.allowed = false;
         status.reason = "Unable to resolve monitored portfolio ownership";
         return status;
      }
      if(ownership != PORT_OWNERSHIP_LIVE_OWNED) continue;

      int idx = FindPairStateIndex(g_monitored_trades[i].pair);
      if(idx < 0) continue;

      status.total_trades++;
      status.trades_per_pair[idx]++;
   }

   for(int p = 0; p < g_pair_count; p++)
      if(status.trades_per_pair[p] > 0)
         status.active_pairs++;
   
   if(status.active_pairs > g_effective_max_active_pair)
   {
      status.allowed = false;
      status.reason = "Max active pairs exceeded";
      return status;
   }
   
   if(status.total_trades > MaxTotalTrade)
   {
      status.allowed = false;
      status.reason = "Max total trades exceeded";
      return status;
   }
   
   for(int i = 0; i < g_pair_count; i++)
   {
      if(status.trades_per_pair[i] > MaxTradePerPair)
      {
         status.allowed = false;
         status.reason = "Max trade per pair exceeded for " + g_pair_names[i];
         return status;
      }
   }
   
   return status;
}

void FinalPortfolioGuard(BBMA_Decision &decision)
{
   if(decision.DecisionState != DEC_VALIDATED) return;
   
   PortfolioStatus status = CheckPortfolioLimits();

   if(!status.allowed)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_PORTFOLIO_LIMIT_ATOMIC;
      return;
   }

   int pairIdx = FindPairStateIndex(decision.Pair);
   if(pairIdx < 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_PORTFOLIO_LIMIT_ATOMIC;
      return;
   }
   
   int wouldBeTotal = status.total_trades + 1;
   int wouldBePairTrades = status.trades_per_pair[pairIdx] + 1;
   int wouldBePairs = status.active_pairs + ((status.trades_per_pair[pairIdx] == 0) ? 1 : 0);
   
   if(wouldBePairs > g_effective_max_active_pair)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_PORTFOLIO_LIMIT_ATOMIC;
      return;
   }
   
   if(wouldBeTotal > MaxTotalTrade)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_PORTFOLIO_LIMIT_ATOMIC;
      return;
   }

   if(wouldBePairTrades > MaxTradePerPair)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_PORTFOLIO_LIMIT_ATOMIC;
      return;
   }
}

int CountLiveEAOwnedPortfolioTrades()
{
   int count = 0;
   for(int i = 0; i < g_monitored_count; i++)
   {
      ENUM_PORTFOLIO_OWNERSHIP_STATE ownership =
         GetLiveEAOwnedPortfolioTradeState(i);
      if(ownership == PORT_OWNERSHIP_UNKNOWN) return -1;
      if(ownership == PORT_OWNERSHIP_LIVE_OWNED) count++;
   }
   return count;
}

bool BrokerConfirmsNoLiveEAOwnedOrders()
{
   if(!IsTerminalConnected()) return false;

   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      ResetLastError();
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
         return false;

      if(OrderCloseTime() != 0) continue;

      int pairIdx = -1;
      if(IsExactEAOwnedSelectedOrder(pairIdx))
         return false;
   }

   return true;
}

void ManagePortfolio()
{
   static bool basketObservationUncertainLogged = false;

   if(g_portfolio_emergency_close_requested)
   {
      if(BrokerConfirmsNoLiveEAOwnedOrders())
         g_portfolio_emergency_close_requested = false;
      return;
   }

   bool basketValid = true;
   double basketLoss = CalculateBasketLossPercent_EA(basketValid);
   if(!basketValid)
   {
      if(!basketObservationUncertainLogged)
      {
         Log(DBG_ERROR, "Portfolio basket observation uncertain; threshold evaluation deferred");
         basketObservationUncertainLogged = true;
      }
      return;
   }

   basketObservationUncertainLogged = false;
   if(BasketLossPercent > 0 && basketLoss >= BasketLossPercent)
      g_portfolio_emergency_close_requested = true;
}

//+------------------------------------------------------------------+
//| MODULE 21: MONEY MANAGEMENT                                      |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

double NormalizeLotDownFromSnapshot(double lot, RiskValidationSnapshot &snapshot)
{
   if(lot <= 0 || snapshot.LotStep <= 0 || snapshot.LotDigits < 0)
      return 0;

   double stepped = MathFloor((lot / snapshot.LotStep) + 0.000000001) * snapshot.LotStep;
   return NormalizeDouble(stepped, snapshot.LotDigits);
}

bool IsValidSnapshotLotStep(double lot, RiskValidationSnapshot &snapshot)
{
   if(lot <= 0 || snapshot.LotStep <= 0) return false;
   double ratio = lot / snapshot.LotStep;
   return MathAbs(ratio - MathRound(ratio)) < 0.00001;
}

// P2-LOTDIAG-01: observability-only explanation for an already-failed M21 lot result.
// IMPORTANT: CalculateLotSize() remains the sole sizing authority and is unchanged.
// This helper never queries live broker/account state, changes lot, clamps values,
// or changes rejection semantics. It only reads the same frozen decision/snapshot.
string DiagnoseInvalidLotReason(BBMA_Decision &decision,
                                RiskValidationSnapshot &snapshot,
                                double &rawLot,
                                double &normalizedLot,
                                double &effectiveMaxLot)
{
   rawLot = 0.0;
   normalizedLot = 0.0;
   effectiveMaxLot = 0.0;

   if(decision.DecisionState != DEC_VALIDATED || decision.Pair == "" ||
      decision.EntryPrice <= 0 || decision.StopLoss <= 0)
      return "INVALID_DECISION";

   if(snapshot.Point <= 0 || snapshot.TickSize_Price <= 0 || snapshot.TickValue <= 0 ||
      snapshot.LotStep <= 0 || snapshot.MinLot <= 0 ||
      snapshot.MaxLot < snapshot.MinLot || snapshot.LotDigits < 0 || snapshot.Equity <= 0)
      return "BROKER_SNAPSHOT_INVALID";

   double payloadTolerance = snapshot.Point * 0.5;
   if(MathAbs(snapshot.EntryPrice - decision.EntryPrice) > payloadTolerance ||
      MathAbs(snapshot.StopLoss - decision.StopLoss) > payloadTolerance)
      return "PAYLOAD_MISMATCH";

   if(MMMode == 1)
   {
      if(AutoLotPercent <= 0 || MaxAutoLot <= 0)
         return "MM_CONFIG_INVALID";

      double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
      if(slDistance <= 0)
         return "SL_DISTANCE_INVALID";

      double riskPerLot = slDistance * snapshot.TickValue / snapshot.TickSize_Price;
      if(riskPerLot <= 0)
         return "RISK_PER_LOT_INVALID";

      double riskAmount = snapshot.Equity * (AutoLotPercent / 100.0);
      if(riskAmount <= 0)
         return "RISK_AMOUNT_INVALID";

      rawLot = riskAmount / riskPerLot;
      normalizedLot = NormalizeLotDownFromSnapshot(rawLot, snapshot);
      effectiveMaxLot = MathMin(snapshot.MaxLot, MaxAutoLot);

      if(normalizedLot < snapshot.MinLot)
         return "BELOW_MIN";
      if(effectiveMaxLot < snapshot.MinLot)
         return "MAXAUTOLOT_BELOW_MIN";
      if(normalizedLot > effectiveMaxLot)
         return "ABOVE_MAX";
      if(!IsValidSnapshotLotStep(normalizedLot, snapshot))
         return "STEP_MISMATCH";

      return "AUTOLOT_FAILURE_UNCLASSIFIED";
   }

   if(MMMode == 2)
   {
      rawLot = FixedLot;
      normalizedLot = FixedLot;
      effectiveMaxLot = snapshot.MaxLot;

      if(FixedLot <= 0 || FixedLot < snapshot.MinLot || FixedLot > snapshot.MaxLot)
         return "FIXEDLOT_INVALID";
      if(!IsValidSnapshotLotStep(FixedLot, snapshot))
         return "STEP_MISMATCH";

      return "FIXEDLOT_FAILURE_UNCLASSIFIED";
   }

   return "MMMODE_INVALID";
}

void PrintInvalidLotDiagnostic(BBMA_Decision &decision,
                               RiskValidationSnapshot &snapshot,
                               string reasonTag,
                               double rawLot,
                               double normalizedLot,
                               double effectiveMaxLot)
{
   double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);

   Print("[LOT_DIAG][REJ_INVALID_LOT] Pair=", decision.Pair,
         " Reason=", reasonTag,
         " MMMode=", IntegerToString(MMMode),
         " RawLot=", DoubleToString(rawLot, 8),
         " NormalizedLot=", DoubleToString(normalizedLot, 8),
         " MinLot=", DoubleToString(snapshot.MinLot, 8),
         " MaxLot=", DoubleToString(snapshot.MaxLot, 8),
         " EffectiveMaxLot=", DoubleToString(effectiveMaxLot, 8),
         " LotStep=", DoubleToString(snapshot.LotStep, 8),
         " LotDigits=", IntegerToString(snapshot.LotDigits),
         " TickValue=", DoubleToString(snapshot.TickValue, 8),
         " TickSize=", DoubleToString(snapshot.TickSize_Price, 8),
         " Point=", DoubleToString(snapshot.Point, 10),
         " SLDistance=", DoubleToString(slDistance, 10),
         " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
         " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
         " Equity=", DoubleToString(snapshot.Equity, 2),
         " AutoPct=", DoubleToString(AutoLotPercent, 4),
         " MaxAutoLot=", DoubleToString(MaxAutoLot, 8),
         " FixedLot=", DoubleToString(FixedLot, 8));
}

double CalculateLotSize(BBMA_Decision &decision, RiskValidationSnapshot &snapshot, bool &valid)
{
   valid = true;

   if(decision.DecisionState != DEC_VALIDATED || decision.Pair == "" ||
      decision.EntryPrice <= 0 || decision.StopLoss <= 0)
   {
      valid = false;
      return 0;
   }

   if(snapshot.Point <= 0 || snapshot.TickSize_Price <= 0 || snapshot.TickValue <= 0 ||
      snapshot.LotStep <= 0 || snapshot.MinLot <= 0 ||
      snapshot.MaxLot < snapshot.MinLot || snapshot.LotDigits < 0 || snapshot.Equity <= 0)
   {
      valid = false;
      return 0;
   }

   double payloadTolerance = snapshot.Point * 0.5;
   if(MathAbs(snapshot.EntryPrice - decision.EntryPrice) > payloadTolerance ||
      MathAbs(snapshot.StopLoss - decision.StopLoss) > payloadTolerance)
   {
      valid = false;
      return 0;
   }

   if(MMMode == 1)
   {
      if(AutoLotPercent <= 0 || MaxAutoLot <= 0)
      {
         valid = false;
         return 0;
      }

      double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
      if(slDistance <= 0)
      {
         valid = false;
         return 0;
      }

      double riskPerLot = slDistance * snapshot.TickValue / snapshot.TickSize_Price;
      if(riskPerLot <= 0)
      {
         valid = false;
         return 0;
      }

      double riskAmount = snapshot.Equity * (AutoLotPercent / 100.0);
      if(riskAmount <= 0)
      {
         valid = false;
         return 0;
      }

      double rawLot = riskAmount / riskPerLot;
      double calcLot = NormalizeLotDownFromSnapshot(rawLot, snapshot);

      if(calcLot < snapshot.MinLot)
      {
         valid = false;
         return 0;
      }

      double maxLot = MathMin(snapshot.MaxLot, MaxAutoLot);
      if(maxLot < snapshot.MinLot)
      {
         valid = false;
         return 0;
      }

      if(calcLot > maxLot)
      {
         valid = false;
         return 0;
      }

      if(!IsValidSnapshotLotStep(calcLot, snapshot))
      {
         valid = false;
         return 0;
      }

      return calcLot;
   }
   else if(MMMode == 2)
   {
      double lot = FixedLot;
      if(lot <= 0 || lot < snapshot.MinLot || lot > snapshot.MaxLot)
      {
         valid = false;
         return 0;
      }

      if(!IsValidSnapshotLotStep(lot, snapshot))
      {
         valid = false;
         return 0;
      }

      return lot;
   }

   valid = false;
   return 0;
}

//+------------------------------------------------------------------+
//| MODULE 22: ORDER EXECUTION ENGINE (DUMB EXECUTOR)                |
//| LEVEL: EXPERT                                                    |
//+------------------------------------------------------------------+

bool IsRetryableError(int error)
{
   return (error == 135 || error == 138 || error == 146);
}

bool IsFatalError(int error)
{
   return (error == 130 || error == 131 || error == 134 || error == 148);
}

bool IsAmbiguousError(int error)
{
   return (error == 4 || error == 6 || error == 128 || error == 141);
}

int FindExistingExecutionTicket(string pair, int direction, int magicNumber,
                                string decisionID)
{
   if(pair == "" || magicNumber <= 0 || decisionID == "") return -1;

   // P0: durable terminal identity is authoritative.
   int persistedTicket = FindPersistedExecutionTicket(decisionID, pair,
                                                       direction, magicNumber);
   if(persistedTicket > 0) return persistedTicket;

   // Secondary fallback for legacy/current brokers that preserve the compact tag.
   string executionTag = "BBMA|H:" + SHORT_HASH(decisionID);
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      if(OrderCloseTime() != 0) continue;
      if(OrderSymbol() != pair) continue;
      if(OrderMagicNumber() != magicNumber) continue;
      if(OrderType() != direction) continue;

      if(StringFind(OrderComment(), executionTag) == 0)
         return OrderTicket();
   }

   return -1;
}

bool IsSignalAllowed(BBMA_Decision &decision, string pair, int magicNumber)
{
   if(IsDecisionExecuted(decision.DecisionID))
      return false;
   
   if(decision.DecisionState != DEC_VALIDATED)
      return false;

   if(decision.Pair != pair || pair == "" || magicNumber <= 0 || decision.DecisionID == "")
      return false;
   
   if(TradeLockMode == LOCK_ONE_POSITION)
   {
      for(int i = 0; i < g_monitored_count; i++)
      {
         ENUM_PORTFOLIO_OWNERSHIP_STATE ownership =
            GetLiveEAOwnedPortfolioTradeState(i);
         if(ownership == PORT_OWNERSHIP_UNKNOWN)
            return false;
         if(ownership != PORT_OWNERSHIP_LIVE_OWNED) continue;
         if(g_monitored_trades[i].pair == pair)
            return false;
      }
   }
   else if(TradeLockMode == LOCK_SAME_DIRECTION)
   {
      // Pair-direction lock: once this EA already has a live position on the
      // pair, additional positions may only follow that same direction.
      // The previous comparison was reversed: it blocked same-direction adds
      // and allowed BUY+SELL coexistence, contradicting SAME_DIRECTION mode.
      for(int i = 0; i < g_monitored_count; i++)
      {
         ENUM_PORTFOLIO_OWNERSHIP_STATE ownership =
            GetLiveEAOwnedPortfolioTradeState(i);
         if(ownership == PORT_OWNERSHIP_UNKNOWN)
            return false;
         if(ownership != PORT_OWNERSHIP_LIVE_OWNED) continue;
         if(g_monitored_trades[i].pair == pair &&
            g_monitored_trades[i].direction != decision.Direction)
            return false;
      }
   }
   
   return true;
}

int SendOrderWithRetry(string pair, int direction, double lot,
                       double stopLoss, double takeProfit, string comment, 
                       int magicNumber, double frozenAllowedDeviation, 
                       double decisionEntryPrice, string decisionID)
{
   if(MaxRetry <= 0 || pair == "" || lot <= 0 || stopLoss <= 0 || takeProfit < 0.0 ||
      magicNumber <= 0 || decisionID == "")
      return -1;

   int retry = 0;
   while(retry < MaxRetry)
   {
      int existingTicket = FindExistingExecutionTicket(pair, direction, magicNumber, decisionID);
      if(existingTicket > 0)
         return existingTicket;

      RefreshRates();
      
      double bid = MarketInfo(pair, MODE_BID);
      double ask = MarketInfo(pair, MODE_ASK);
      if(bid <= 0 || ask <= 0)
         return -1;
      
      double executionPrice = (direction == OP_BUY) ? ask : bid;
      double deviation = MathAbs(executionPrice - decisionEntryPrice);
      
      if(deviation > frozenAllowedDeviation)
      {
         return -3;
      }
      
      int ticket = OrderSend(pair, direction, lot, executionPrice, Slippage, 
                             stopLoss, takeProfit, comment, magicNumber, 0, clrNONE);
      
      if(ticket > 0)
         return ticket;
      
      int error = GetLastError();
      
      if(IsFatalError(error))
         return -1;
      
      if(IsAmbiguousError(error))
      {
         int reconciled = FindExistingExecutionTicket(pair, direction, magicNumber, decisionID);
         if(reconciled > 0)
            return reconciled;
         return -2;
      }
      
      if(IsRetryableError(error))
      {
         retry++;
         if(retry < MaxRetry)
            Sleep(RETRY_SLEEP_MS);
      }
      else
      {
         return -1;
      }
   }
   return -1;
}

double NMJE_DirectionNormalizedDisplacementPips(ENUM_DIRECTION direction,
                                                double fromPrice,
                                                double toPrice,
                                                double pipValue)
{
   if(pipValue <= 0.0 || fromPrice <= 0.0 || toPrice <= 0.0) return 0.0;
   if(direction == DIR_BUY) return (toPrice - fromPrice) / pipValue;
   if(direction == DIR_SELL) return (fromPrice - toPrice) / pipValue;
   return 0.0;
}

bool NMJE_IsEntryDisplacementValid(NMJEEntryDisplacementState &state)
{
   if(!state.Present) return true;
   if(state.SourceSignal != SIGNAL_RE_ENTRY &&
      state.SourceSignal != SIGNAL_EXTREME) return false;
   if(state.SourceTimeframe <= 0 || state.SourceCandleTime <= 0) return false;
   if(state.SourceReferencePrice <= 0.0 ||
      state.PreflightReferencePrice <= 0.0 ||
      state.BrokerOpenPrice <= 0.0) return false;
   return true;
}

bool NMJE_BuildEntryDisplacementAttribution(BBMA_Decision &decision,
                                            double brokerOpenPrice,
                                            NMJEEntryDisplacementState &state)
{
   ZeroMemory(state);
   if(!decision.HasSLTPSourceComponent ||
      decision.EntryPrice <= 0.0 || brokerOpenPrice <= 0.0)
      return false;
   ComponentIdentity source = decision.SLTPSourceComponent;
   if(!IsApprovedSLTPSourceComponent(decision, source)) return false;
   int shift = ResolveClosedSourceShift(decision.Pair, source);
   if(shift < 1) return false;
   double sourcePrice = iClose(decision.Pair, source.Timeframe, shift);
   double pipValue = GetPipValue(decision.Pair);
   if(sourcePrice <= 0.0 || pipValue <= 0.0) return false;

   state.Present = true;
   state.SourceSignal = source.ComponentType;
   state.SourceTimeframe = source.Timeframe;
   state.SourceCandleTime = source.CandleTime;
   state.SourceReferencePrice = sourcePrice;
   state.PreflightReferencePrice = decision.EntryPrice;
   state.BrokerOpenPrice = brokerOpenPrice;
   state.SourceToPreflightPips =
      NMJE_DirectionNormalizedDisplacementPips(decision.Direction,
                                               sourcePrice, decision.EntryPrice, pipValue);
   state.PreflightToOpenPips =
      NMJE_DirectionNormalizedDisplacementPips(decision.Direction,
                                               decision.EntryPrice, brokerOpenPrice, pipValue);
   state.SourceToOpenPips =
      NMJE_DirectionNormalizedDisplacementPips(decision.Direction,
                                               sourcePrice, brokerOpenPrice, pipValue);
   return NMJE_IsEntryDisplacementValid(state);
}

void NMJE_BuildTradeAttribution(BBMA_Decision &decision,
                                TradeInfo &info)
{
   ZeroMemory(info.nmje_attribution);
   if(!decision.NMJESnapshotPresent) return;
   NMJEShadowAttributionState a;
   ZeroMemory(a);
   a.Present = true;
   a.Durable = false;
   a.JourneyHash = (decision.NMJEJourneyID == "") ? "" : SHORT_HASH(decision.NMJEJourneyID);
   a.ParentEventHash = (decision.NMJEParentEventID == "") ? "" : SHORT_HASH(decision.NMJEParentEventID);
   a.Relation = decision.NMJERelation;
   a.StableRelation = decision.NMJEStableRelation;
   a.Maturity = decision.NMJEMaturity;
   a.LineageClass = decision.NMJELineageClass;
   if(decision.NMJELineageRootEventID != "")
      a.LineageRootHash = SHORT_HASH(decision.NMJELineageRootEventID);
   if(decision.NMJEPreviousLineageRootEventID != "")
      a.PreviousLineageRootHash = SHORT_HASH(decision.NMJEPreviousLineageRootEventID);
   a.StructureDensity = decision.NMJEStructureDensity;
   a.EntryDisplacement = info.entry_displacement;
   a.M5SnapshotPresent = decision.NMJEM5SnapshotPresent;
   if(decision.NMJEM5ShadowEventID != "")
      a.M5EventHash = SHORT_HASH(decision.NMJEM5ShadowEventID);
   a.M5ClosedCandleTime = decision.NMJEM5ShadowClosedCandleTime;
   a.M5SemanticResolved = decision.NMJEM5SemanticResolved;
   a.M5DiagnosticRelation = decision.NMJEM5DiagnosticRelation;
   if(decision.NMJEM5DiagnosticReason != "")
      a.M5ReasonHash = SHORT_HASH(decision.NMJEM5DiagnosticReason);
   info.nmje_attribution = a;
}

string NMJEAttributionGVBase(int ticket)
{
   return "BBXQ9|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(ticket) + "|";
}

bool NMJESetAttributionGV(string key, double value, string step)
{
   if(SetTerminalGlobalExact(key, value)) return true;
   Print("[Q9-P4PLUS-PERSIST-FAIL] Step=", step,
         " Key=", key,
         " Error=", IntegerToString(GetLastError()));
   return false;
}

bool NMJEStoreHash16(string base, string prefix, string value)
{
   if(StringLen(value) != 16)
   {
      Print("[Q9-P4PLUS-PERSIST-FAIL] Step=HASH_LENGTH Prefix=", prefix,
            " Len=", IntegerToString(StringLen(value)));
      return false;
   }
   for(int i=0; i<4; i++)
   {
      double v = Hex4ToNumber(StringSubstr(value, i*4, 4));
      if(v < 0 || !NMJESetAttributionGV(base + prefix + IntegerToString(i), v,
                                        "HASH_" + prefix + IntegerToString(i)))
         return false;
   }
   return true;
}

string NMJELoadHash16(string base, string prefix)
{
   string result = "";
   for(int i=0; i<4; i++)
   {
      string key = base + prefix + IntegerToString(i);
      if(!GlobalVariableCheck(key)) return "";
      result += NumberToHex4(GlobalVariableGet(key));
   }
   return result;
}

void ClearNMJEShadowAttribution(int ticket)
{
   if(ticket <= 0) return;
   string base = NMJEAttributionGVBase(ticket);
   string keys[54] = {
      "V","M","O","R","SR","JM","LC","SDP","SDM","SDX","SDC",
      "M5P","M5T","M5S","M5R","DP","DSG","DTF","DCT","DSP","DPP","DBP",
      "D12","D2B","D1B",
      "X0","X1","X2","X3","J0","J1","J2","J3","P0","P1","P2","P3",
      "L0","L1","L2","L3","N0","N1","N2","N3","E0","E1","E2","E3",
      "Q0","Q1","Q2","Q3","Z"
   };
   for(int i=0; i<54; i++) DeleteTerminalGlobalExact(base + keys[i]);
}

bool SaveNMJEShadowAttribution(TradeInfo &info)
{
   NMJEShadowAttributionState a = info.nmje_attribution;
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0 ||
      StringLen(info.execution_hash) != 16 || !a.Present)
   {
      Print("[Q9-P4PLUS-PERSIST-FAIL] Step=IDENTITY_PRECONDITION");
      return false;
   }
   if(StringLen(a.JourneyHash) != 16 || StringLen(a.ParentEventHash) != 16)
   {
      Print("[Q9-P4PLUS-PERSIST-FAIL] Step=ATTR_HASH_PRECONDITION",
            " JLen=", IntegerToString(StringLen(a.JourneyHash)),
            " PLen=", IntegerToString(StringLen(a.ParentEventHash)));
      return false;
   }
   if(!NMJE_IsMaturityDomainValue(a.Maturity) ||
      !NMJE_IsRelationDomainValue(a.Relation) ||
      !NMJE_IsRelationDomainValue(a.StableRelation) ||
      !NMJE_IsStructuralDensityValid(a.StructureDensity) ||
      !NMJE_IsEntryDisplacementValid(a.EntryDisplacement))
   {
      Print("[Q9-P4PLUS-PERSIST-FAIL] Step=DOMAIN_PRECONDITION",
            " REL=", IntegerToString((int)a.Relation),
            " SREL=", IntegerToString((int)a.StableRelation),
            " MAT=", IntegerToString((int)a.Maturity),
            " SDP=", a.StructureDensity.Present ? "Y" : "N",
            " SDV=", a.StructureDensity.Valid ? "Y" : "N",
            " DISP=", a.EntryDisplacement.Present ? "Y" : "N");
      return false;
   }

   // Strict-A persistence never accepts inferred continuation.
   if(a.LineageClass == NMJE_LINEAGE_CONTINUATION)
   {
      Print("[Q9-P4PLUS-PERSIST-FAIL] Step=CONTINUATION_HOLD");
      return false;
   }

   string base = NMJEAttributionGVBase(info.ticket);
   ClearNMJEShadowAttribution(info.ticket);
   bool ok = true;
   if(!NMJESetAttributionGV(base+"M",(double)info.magic_number,"M")) ok=false;
   if(!NMJESetAttributionGV(base+"O",(double)info.open_time,"O")) ok=false;
   if(!NMJESetAttributionGV(base+"R",(double)a.Relation,"R")) ok=false;
   if(!NMJESetAttributionGV(base+"SR",(double)a.StableRelation,"SR")) ok=false;
   if(!NMJESetAttributionGV(base+"JM",(double)a.Maturity,"JM")) ok=false;
   if(!NMJESetAttributionGV(base+"LC",(double)a.LineageClass,"LC")) ok=false;
   if(!NMJESetAttributionGV(base+"SDP",a.StructureDensity.Present?1.0:0.0,"SDP")) ok=false;
   if(!NMJESetAttributionGV(base+"SDM",(double)a.StructureDensity.StageMask,"SDM")) ok=false;
   if(!NMJESetAttributionGV(base+"SDX",(double)a.StructureDensity.PrefixMask,"SDX")) ok=false;
   if(!NMJESetAttributionGV(base+"SDC",(double)a.StructureDensity.StageCount,"SDC")) ok=false;
   if(!NMJESetAttributionGV(base+"M5P",a.M5SnapshotPresent?1.0:0.0,"M5P")) ok=false;
   if(!NMJESetAttributionGV(base+"M5T",(double)a.M5ClosedCandleTime,"M5T")) ok=false;
   if(!NMJESetAttributionGV(base+"M5S",a.M5SemanticResolved?1.0:0.0,"M5S")) ok=false;
   if(!NMJESetAttributionGV(base+"M5R",(double)a.M5DiagnosticRelation,"M5R")) ok=false;
   if(!NMJESetAttributionGV(base+"DP",a.EntryDisplacement.Present?1.0:0.0,"DP")) ok=false;
   if(a.EntryDisplacement.Present)
   {
      if(!NMJESetAttributionGV(base+"DSG",(double)a.EntryDisplacement.SourceSignal,"DSG")) ok=false;
      if(!NMJESetAttributionGV(base+"DTF",(double)a.EntryDisplacement.SourceTimeframe,"DTF")) ok=false;
      if(!NMJESetAttributionGV(base+"DCT",(double)a.EntryDisplacement.SourceCandleTime,"DCT")) ok=false;
      if(!NMJESetAttributionGV(base+"DSP",a.EntryDisplacement.SourceReferencePrice,"DSP")) ok=false;
      if(!NMJESetAttributionGV(base+"DPP",a.EntryDisplacement.PreflightReferencePrice,"DPP")) ok=false;
      if(!NMJESetAttributionGV(base+"DBP",a.EntryDisplacement.BrokerOpenPrice,"DBP")) ok=false;
      if(!NMJESetAttributionGV(base+"D12",a.EntryDisplacement.SourceToPreflightPips,"D12")) ok=false;
      if(!NMJESetAttributionGV(base+"D2B",a.EntryDisplacement.PreflightToOpenPips,"D2B")) ok=false;
      if(!NMJESetAttributionGV(base+"D1B",a.EntryDisplacement.SourceToOpenPips,"D1B")) ok=false;
   }
   if(!NMJEStoreHash16(base,"X",info.execution_hash)) ok=false;
   if(!NMJEStoreHash16(base,"J",a.JourneyHash)) ok=false;
   if(!NMJEStoreHash16(base,"P",a.ParentEventHash)) ok=false;
   if(StringLen(a.LineageRootHash) > 0)
   {
      if(!NMJEStoreHash16(base,"L",a.LineageRootHash)) ok=false;
   }
   if(StringLen(a.PreviousLineageRootHash) > 0)
   {
      if(!NMJEStoreHash16(base,"N",a.PreviousLineageRootHash)) ok=false;
   }
   if(StringLen(a.M5EventHash) > 0)
   {
      if(!NMJEStoreHash16(base,"E",a.M5EventHash)) ok=false;
   }
   if(StringLen(a.M5ReasonHash) > 0)
   {
      if(!NMJEStoreHash16(base,"Q",a.M5ReasonHash)) ok=false;
   }
   if(!ok)
   {
      ClearNMJEShadowAttribution(info.ticket);
      return false;
   }
   // Commit marker last.
   if(!NMJESetAttributionGV(base+"V",1.0,"COMMIT"))
   {
      ClearNMJEShadowAttribution(info.ticket);
      return false;
   }
   GlobalVariablesFlush();
   a.Durable = true;
   info.nmje_attribution = a;
   return true;
}

bool LoadNMJEShadowAttribution(TradeInfo &info)
{
   ZeroMemory(info.nmje_attribution);
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0 ||
      StringLen(info.execution_hash) != 16) return false;
   string base = NMJEAttributionGVBase(info.ticket);
   if(!GlobalVariableCheck(base+"V") || GlobalVariableGet(base+"V") != 1.0)
      return false;
   if(!GlobalVariableCheck(base+"M") || !GlobalVariableCheck(base+"O")) return false;
   if((int)GlobalVariableGet(base+"M") != info.magic_number ||
      (datetime)((int)GlobalVariableGet(base+"O")) != info.open_time) return false;
   if(NMJELoadHash16(base,"X") != info.execution_hash) return false;

   NMJEShadowAttributionState a;
   ZeroMemory(a);
   a.Present = true; a.Durable = true;
   a.JourneyHash = NMJELoadHash16(base,"J");
   a.ParentEventHash = NMJELoadHash16(base,"P");
   if(a.JourneyHash=="" || a.ParentEventHash=="") { ZeroMemory(a); return false; }
   if(!GlobalVariableCheck(base+"R") || !GlobalVariableCheck(base+"SR") ||
      !GlobalVariableCheck(base+"JM") || !GlobalVariableCheck(base+"LC"))
   { ZeroMemory(a); return false; }
   a.Relation=(ENUM_NESTED_RELATION)((int)GlobalVariableGet(base+"R"));
   a.StableRelation=(ENUM_NESTED_RELATION)((int)GlobalVariableGet(base+"SR"));
   a.Maturity=(ENUM_NMJE_JOURNEY_MATURITY)((int)GlobalVariableGet(base+"JM"));
   a.LineageClass=(ENUM_NMJE_LINEAGE_EVENT_CLASS)((int)GlobalVariableGet(base+"LC"));
   if(a.LineageClass==NMJE_LINEAGE_CONTINUATION) a.LineageClass=NMJE_LINEAGE_UNRESOLVED;
   a.LineageRootHash=NMJELoadHash16(base,"L");
   a.PreviousLineageRootHash=NMJELoadHash16(base,"N");

   if(GlobalVariableCheck(base+"SDP") && GlobalVariableGet(base+"SDP")==1.0)
   {
      a.StructureDensity.Present=true; a.StructureDensity.Valid=true;
      a.StructureDensity.StageMask=(int)GlobalVariableGet(base+"SDM");
      a.StructureDensity.PrefixMask=(int)GlobalVariableGet(base+"SDX");
      a.StructureDensity.StageCount=(int)GlobalVariableGet(base+"SDC");
      a.StructureDensity.Reason="RECOVERED_RESEARCH_METADATA";
   }
   a.M5SnapshotPresent=(GlobalVariableCheck(base+"M5P") &&
                        GlobalVariableGet(base+"M5P")==1.0);
   if(GlobalVariableCheck(base+"M5T"))
      a.M5ClosedCandleTime=(datetime)((int)GlobalVariableGet(base+"M5T"));
   a.M5SemanticResolved=(GlobalVariableCheck(base+"M5S") &&
                         GlobalVariableGet(base+"M5S")==1.0);
   if(GlobalVariableCheck(base+"M5R"))
      a.M5DiagnosticRelation=(ENUM_NESTED_RELATION)((int)GlobalVariableGet(base+"M5R"));
   a.M5EventHash=NMJELoadHash16(base,"E");
   a.M5ReasonHash=NMJELoadHash16(base,"Q");

   if(GlobalVariableCheck(base+"DP") && GlobalVariableGet(base+"DP")==1.0)
   {
      a.EntryDisplacement.Present=true;
      a.EntryDisplacement.SourceSignal=(ENUM_SIGNAL_TYPE)((int)GlobalVariableGet(base+"DSG"));
      a.EntryDisplacement.SourceTimeframe=(int)GlobalVariableGet(base+"DTF");
      a.EntryDisplacement.SourceCandleTime=(datetime)((int)GlobalVariableGet(base+"DCT"));
      a.EntryDisplacement.SourceReferencePrice=GlobalVariableGet(base+"DSP");
      a.EntryDisplacement.PreflightReferencePrice=GlobalVariableGet(base+"DPP");
      a.EntryDisplacement.BrokerOpenPrice=GlobalVariableGet(base+"DBP");
      a.EntryDisplacement.SourceToPreflightPips=GlobalVariableGet(base+"D12");
      a.EntryDisplacement.PreflightToOpenPips=GlobalVariableGet(base+"D2B");
      a.EntryDisplacement.SourceToOpenPips=GlobalVariableGet(base+"D1B");
   }
   if(!NMJE_IsRelationDomainValue(a.Relation) ||
      !NMJE_IsRelationDomainValue(a.StableRelation) ||
      !NMJE_IsMaturityDomainValue(a.Maturity) ||
      !NMJE_IsStructuralDensityValid(a.StructureDensity) ||
      !NMJE_IsEntryDisplacementValid(a.EntryDisplacement))
   { ZeroMemory(a); return false; }
   info.nmje_attribution = a;
   return true;
}

bool NMJE_OptionalStringEqual(string left, string right)
{
   if(StringLen(left) == 0 && StringLen(right) == 0) return true;
   return (left == right);
}

bool NMJE_AttributionEquivalent(NMJEShadowAttributionState &left,
                                NMJEShadowAttributionState &right)
{
   if(left.Present != right.Present) return false;
   if(!left.Present) return true;
   if(left.JourneyHash != right.JourneyHash ||
      left.ParentEventHash != right.ParentEventHash ||
      left.Relation != right.Relation ||
      left.StableRelation != right.StableRelation ||
      left.Maturity != right.Maturity ||
      left.LineageClass != right.LineageClass ||
      !NMJE_OptionalStringEqual(left.LineageRootHash, right.LineageRootHash) ||
      !NMJE_OptionalStringEqual(left.PreviousLineageRootHash,
                                right.PreviousLineageRootHash))
      return false;
   if(left.StructureDensity.Present != right.StructureDensity.Present ||
      left.StructureDensity.StageMask != right.StructureDensity.StageMask ||
      left.StructureDensity.PrefixMask != right.StructureDensity.PrefixMask ||
      left.StructureDensity.StageCount != right.StructureDensity.StageCount)
      return false;
   if(left.M5SnapshotPresent != right.M5SnapshotPresent ||
      !NMJE_OptionalStringEqual(left.M5EventHash, right.M5EventHash) ||
      left.M5ClosedCandleTime != right.M5ClosedCandleTime ||
      left.M5SemanticResolved != right.M5SemanticResolved ||
      left.M5DiagnosticRelation != right.M5DiagnosticRelation ||
      !NMJE_OptionalStringEqual(left.M5ReasonHash, right.M5ReasonHash))
      return false;
   if(left.EntryDisplacement.Present != right.EntryDisplacement.Present)
      return false;
   if(left.EntryDisplacement.Present)
   {
      if(left.EntryDisplacement.SourceSignal != right.EntryDisplacement.SourceSignal ||
         left.EntryDisplacement.SourceTimeframe != right.EntryDisplacement.SourceTimeframe ||
         left.EntryDisplacement.SourceCandleTime != right.EntryDisplacement.SourceCandleTime ||
         left.EntryDisplacement.SourceReferencePrice != right.EntryDisplacement.SourceReferencePrice ||
         left.EntryDisplacement.PreflightReferencePrice != right.EntryDisplacement.PreflightReferencePrice ||
         left.EntryDisplacement.BrokerOpenPrice != right.EntryDisplacement.BrokerOpenPrice ||
         left.EntryDisplacement.SourceToPreflightPips != right.EntryDisplacement.SourceToPreflightPips ||
         left.EntryDisplacement.PreflightToOpenPips != right.EntryDisplacement.PreflightToOpenPips ||
         left.EntryDisplacement.SourceToOpenPips != right.EntryDisplacement.SourceToOpenPips)
         return false;
   }
   return true;
}

// N2-13: read-only closed-order outcome telemetry.
// Called only after OrderSelect() proves that the monitored ticket is closed.
// It never changes order state, trade lifecycle, risk, exit logic or registry identity.
void NMJE_PrintClosedOutcomeShadow(TradeInfo &info)
{
   if(info.ticket <= 0 || info.pair == "") return;
   if(OrderTicket() != info.ticket) return;
   if(OrderCloseTime() == 0) return;

   // Fail closed on registry/order identity mismatch rather than attributing
   // realized P/L to the wrong research identity.
   if(OrderSymbol() != info.pair) return;
   if(info.magic_number <= 0 || OrderMagicNumber() != info.magic_number) return;

   string decisionToken = "-";
   if(info.decision_id != "")
      decisionToken = NMJE_LogIdentityToken(info.decision_id);

   string decisionHash = info.execution_hash;
   if(decisionHash == "") decisionHash = "-";

   double netProfit = OrderProfit() + OrderSwap() + OrderCommission();

   // P4 runtime durability proof: reload exact ticket/open-time/hash-bound
   // research metadata at outcome time. Failure remains diagnostic only.
   TradeInfo durableRead = info;
   ZeroMemory(durableRead.nmje_attribution);
   bool durableLoad = LoadNMJEShadowAttribution(durableRead);
   bool durableMatch = durableLoad &&
      NMJE_AttributionEquivalent(info.nmje_attribution,
                                 durableRead.nmje_attribution);

   Print("[N2-NMJE-OUT] PAIR=", info.pair,
         " TICKET=", IntegerToString(info.ticket),
         " DID=", decisionToken,
         " DIDH=", decisionHash,
         " NET=", DoubleToString(netProfit, 8),
         " CLOSE=", IntegerToString((int)OrderCloseTime()),
         " REC=", EnumToString(info.recovery_state),
         " ATTR=", info.nmje_attribution.Present ? "Y" : "N",
         " DUR=", info.nmje_attribution.Durable ? "Y" : "N",
         " DLOAD=", durableLoad ? "Y" : "N",
         " DMATCH=", durableMatch ? "Y" : "N",
         " JH=", info.nmje_attribution.JourneyHash == "" ? "-" : info.nmje_attribution.JourneyHash,
         " REL=", NMJE_RelationText(info.nmje_attribution.Relation),
         " SREL=", NMJE_RelationText(info.nmje_attribution.StableRelation),
         " MAT=", NMJE_MaturityText(info.nmje_attribution.Maturity),
         " LC=", NMJE_LineageClassText(info.nmje_attribution.LineageClass),
         " SD=", IntegerToString(info.nmje_attribution.StructureDensity.StageMask),
         " M5SEM=", info.nmje_attribution.M5SemanticResolved ? "Y" : "N",
         " DISP=", info.entry_displacement.Present ? "Y" : "N");

   NMJE_P2_PrintCounterfactualOutcomes(info.ticket, OrderCloseTime());
}

void CompactMonitoredTrades()
{
   int write = 0;
   for(int i = 0; i < g_monitored_count; i++)
   {
      bool removeClosed = false;
      if(OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
         removeClosed = (OrderCloseTime() != 0);
      if(removeClosed)
      {
         // Emit at most once: the row is discarded immediately afterwards.
         NMJE_PrintClosedOutcomeShadow(g_monitored_trades[i]);
         ClearNMJEShadowAttribution(g_monitored_trades[i].ticket);
         if(g_monitored_trades[i].c044_lifecycle_managed)
            ClearC044Checkpoint(g_monitored_trades[i]);
         if(g_monitored_trades[i].d1_tpw_lifecycle_managed)
            ClearD1TPWCheckpoint(g_monitored_trades[i]);
         continue;
      }
      if(write != i) g_monitored_trades[write] = g_monitored_trades[i];
      write++;
   }
   g_monitored_count = write;
}

bool EnsureMonitoredRegistryCapacity()
{
   CompactMonitoredTrades();
   return (g_monitored_count < MAX_MONITORED);
}

void AddToMonitoredTrades(TradeInfo &info)
{
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(g_monitored_trades[i].ticket == info.ticket)
      {
         g_monitored_trades[i] = info;
         return;
      }
   }
   CompactMonitoredTrades();
   if(g_monitored_count < MAX_MONITORED)
   {
      g_monitored_trades[g_monitored_count] = info;
      g_monitored_count++;
      return;
   }
   Log(DBG_ERROR, "Monitored registry full; unable to register ticket=" + IntegerToString(info.ticket));
}

// F07: execution ambiguity is an EA-wide admission safety state, not Strategy Core.
// The minimal identity is persisted so restart cannot silently erase an unknown
// broker-acceptance outcome. There is no timeout or automatic resend.
string ExecutionAmbiguityGVBase()
{
   return "BBXA|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|";
}

bool SaveExecutionAmbiguityHold()
{
   if(!g_execution_ambiguity.Active ||
      StringLen(g_execution_ambiguity.ExecutionHash) != 16 ||
      g_execution_ambiguity.MagicNumber <= 0 ||
      (g_execution_ambiguity.Direction != DIR_BUY &&
       g_execution_ambiguity.Direction != DIR_SELL))
      return false;

   double h0 = Hex4ToNumber(StringSubstr(g_execution_ambiguity.ExecutionHash, 0, 4));
   double h1 = Hex4ToNumber(StringSubstr(g_execution_ambiguity.ExecutionHash, 4, 4));
   double h2 = Hex4ToNumber(StringSubstr(g_execution_ambiguity.ExecutionHash, 8, 4));
   double h3 = Hex4ToNumber(StringSubstr(g_execution_ambiguity.ExecutionHash, 12, 4));
   if(h0 < 0 || h1 < 0 || h2 < 0 || h3 < 0) return false;

   string base = ExecutionAmbiguityGVBase();

   // Active marker is committed first. A crash during the remaining writes
   // therefore reloads as an unresolved/corrupt HOLD rather than fail-open.
   if(GlobalVariableSet(base + "A", 1.0) == 0) return false;

   bool ok = true;
   if(GlobalVariableSet(base + "H0", h0) == 0) ok = false;
   if(GlobalVariableSet(base + "H1", h1) == 0) ok = false;
   if(GlobalVariableSet(base + "H2", h2) == 0) ok = false;
   if(GlobalVariableSet(base + "H3", h3) == 0) ok = false;
   if(GlobalVariableSet(base + "M", (double)g_execution_ambiguity.MagicNumber) == 0) ok = false;
   if(GlobalVariableSet(base + "D", (double)g_execution_ambiguity.Direction) == 0) ok = false;
   if(GlobalVariableSet(base + "T", (double)g_execution_ambiguity.LatchedTime) == 0) ok = false;
   GlobalVariablesFlush();
   if(!ok) return false;

   string keys[7] = {"H0","H1","H2","H3","M","D","T"};
   for(int i = 0; i < 7; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;

   string verifyHash =
      NumberToHex4(GlobalVariableGet(base + "H0")) +
      NumberToHex4(GlobalVariableGet(base + "H1")) +
      NumberToHex4(GlobalVariableGet(base + "H2")) +
      NumberToHex4(GlobalVariableGet(base + "H3"));

   return GlobalVariableCheck(base + "A") &&
          GlobalVariableGet(base + "A") == 1.0 &&
          verifyHash == g_execution_ambiguity.ExecutionHash &&
          (int)GlobalVariableGet(base + "M") == g_execution_ambiguity.MagicNumber &&
          (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D")) == g_execution_ambiguity.Direction;
}

bool LoadExecutionAmbiguityHold()
{
   ZeroMemory(g_execution_ambiguity);
   string base = ExecutionAmbiguityGVBase();
   if(!GlobalVariableCheck(base + "A") || GlobalVariableGet(base + "A") != 1.0)
      return true;

   // Once the active marker exists, any incomplete payload remains a HOLD.
   g_execution_ambiguity.Active = true;
   g_execution_ambiguity.PersistenceValid = false;

   string keys[7] = {"H0","H1","H2","H3","M","D","T"};
   for(int i = 0; i < 7; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;

   string executionHash =
      NumberToHex4(GlobalVariableGet(base + "H0")) +
      NumberToHex4(GlobalVariableGet(base + "H1")) +
      NumberToHex4(GlobalVariableGet(base + "H2")) +
      NumberToHex4(GlobalVariableGet(base + "H3"));
   int magic = (int)GlobalVariableGet(base + "M");
   ENUM_DIRECTION direction =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   datetime latchedTime = (datetime)((int)GlobalVariableGet(base + "T"));

   if(StringLen(executionHash) != 16 || magic <= 0 || latchedTime <= 0 ||
      (direction != DIR_BUY && direction != DIR_SELL))
      return false;

   g_execution_ambiguity.ExecutionHash = executionHash;
   g_execution_ambiguity.MagicNumber = magic;
   g_execution_ambiguity.Direction = direction;
   g_execution_ambiguity.LatchedTime = latchedTime;

   for(int p = 0; p < g_pair_count; p++)
   {
      if(g_pair_states[p].magic_number != magic) continue;
      g_execution_ambiguity.Pair = g_pair_states[p].actual_symbol;
      break;
   }

   if(g_execution_ambiguity.Pair == "")
      return false;

   g_execution_ambiguity.PersistenceValid = true;
   Print("[F07][AMBIGUITY_HOLD_RECOVERED] Pair=", g_execution_ambiguity.Pair,
         " Dir=", EnumToString(g_execution_ambiguity.Direction),
         " Hash=", g_execution_ambiguity.ExecutionHash);
   return true;
}

bool ClearExecutionAmbiguityHold()
{
   string base = ExecutionAmbiguityGVBase();
   string keys[7] = {"H0","H1","H2","H3","M","D","T"};

   // Remove payload first and active marker last. Until A is deleted, restart
   // remains fail-closed even if cleanup is interrupted.
   for(int i = 0; i < 7; i++)
      if(!DeleteTerminalGlobalExact(base + keys[i])) return false;
   if(!DeleteTerminalGlobalExact(base + "A")) return false;
   GlobalVariablesFlush();

   ZeroMemory(g_execution_ambiguity);
   return true;
}

bool LatchExecutionAmbiguity(BBMA_Decision &decision, string pair, int magicNumber)
{
   if(decision.DecisionID == "" || pair == "" || magicNumber <= 0 ||
      (decision.Direction != DIR_BUY && decision.Direction != DIR_SELL))
      return false;

   string executionHash = SHORT_HASH(decision.DecisionID);
   if(StringLen(executionHash) != 16) return false;

   if(g_execution_ambiguity.Active)
   {
      bool same = (g_execution_ambiguity.ExecutionHash == executionHash &&
                   g_execution_ambiguity.Pair == pair &&
                   g_execution_ambiguity.Direction == decision.Direction &&
                   g_execution_ambiguity.MagicNumber == magicNumber);
      if(!same)
         Log(DBG_ERROR, "F07 ambiguity collision; existing HOLD preserved");
      return same && g_execution_ambiguity.PersistenceValid;
   }

   ZeroMemory(g_execution_ambiguity);
   g_execution_ambiguity.Active = true;
   g_execution_ambiguity.DecisionID = decision.DecisionID; // same-session aid only
   g_execution_ambiguity.ExecutionHash = executionHash;
   g_execution_ambiguity.Pair = pair;
   g_execution_ambiguity.Direction = decision.Direction;
   g_execution_ambiguity.MagicNumber = magicNumber;
   g_execution_ambiguity.LatchedTime = TimeCurrent();
   g_execution_ambiguity.PersistenceValid = SaveExecutionAmbiguityHold();

   Print("[F07][AMBIGUITY_HOLD_LATCHED] Pair=", pair,
         " Dir=", EnumToString(decision.Direction),
         " Hash=", executionHash,
         " Persist=", g_execution_ambiguity.PersistenceValid ? "PASS" : "FAIL");
   return g_execution_ambiguity.PersistenceValid;
}

int FindExecutionAmbiguityTicket(bool &isOpen)
{
   isOpen = false;
   if(!g_execution_ambiguity.Active || !g_execution_ambiguity.PersistenceValid ||
      g_execution_ambiguity.Pair == "" ||
      StringLen(g_execution_ambiguity.ExecutionHash) != 16)
      return -1;

   int orderType = (g_execution_ambiguity.Direction == DIR_BUY) ? OP_BUY : OP_SELL;

   if(g_execution_ambiguity.DecisionID != "")
   {
      int currentTicket = FindExistingExecutionTicket(
         g_execution_ambiguity.Pair, orderType,
         g_execution_ambiguity.MagicNumber, g_execution_ambiguity.DecisionID);
      if(currentTicket > 0)
      {
         isOpen = true;
         return currentTicket;
      }
   }

   string executionTag = "BBMA|H:" + g_execution_ambiguity.ExecutionHash;
   for(int pass = 0; pass < 2; pass++)
   {
      int total = (pass == 0) ? OrdersTotal() : OrdersHistoryTotal();
      int pool = (pass == 0) ? MODE_TRADES : MODE_HISTORY;
      for(int i = 0; i < total; i++)
      {
         if(!OrderSelect(i, SELECT_BY_POS, pool))
            return -1;
         if(OrderSymbol() != g_execution_ambiguity.Pair) continue;
         if(OrderMagicNumber() != g_execution_ambiguity.MagicNumber) continue;
         if(OrderType() != orderType) continue;
         if(StringFind(OrderComment(), executionTag) != 0) continue;

         bool open = (OrderCloseTime() == 0);
         if(pass == 0 && !open) continue;
         if(pass == 1 && open) continue;
         isOpen = open;
         return OrderTicket();
      }
   }
   return -1;
}

bool AdoptAmbiguousExecutionTicket(int ticket, bool isOpen)
{
   if(ticket <= 0 || !g_execution_ambiguity.Active ||
      !g_execution_ambiguity.PersistenceValid)
      return false;
   if(!OrderSelect(ticket, SELECT_BY_TICKET)) return false;

   int expectedType =
      (g_execution_ambiguity.Direction == DIR_BUY) ? OP_BUY : OP_SELL;
   if(OrderSymbol() != g_execution_ambiguity.Pair ||
      OrderMagicNumber() != g_execution_ambiguity.MagicNumber ||
      OrderType() != expectedType)
      return false;

   string brokerHash = "";
   if(!ExtractExecutionHash(OrderComment(), brokerHash) ||
      brokerHash != g_execution_ambiguity.ExecutionHash)
      return false;

   datetime openTime = OrderOpenTime();
   if(openTime <= 0) return false;

   if(!isOpen)
   {
      if(OrderCloseTime() == 0) return false;
      if(!SaveExecutionIdentityHash(g_execution_ambiguity.ExecutionHash, ticket,
                                    g_execution_ambiguity.Pair,
                                    g_execution_ambiguity.Direction,
                                    g_execution_ambiguity.MagicNumber, openTime))
         return false;
      UpsertExecutionHashTombstone(g_execution_ambiguity.ExecutionHash, ticket,
                                   g_execution_ambiguity.Pair,
                                   g_execution_ambiguity.Direction, openTime);
      return true;
   }

   if(OrderCloseTime() != 0) return false;
   if(!EnsureMonitoredRegistryCapacity()) return false;

   TradeInfo info;
   ZeroMemory(info);
   info.ticket = ticket;
   info.magic_number = g_execution_ambiguity.MagicNumber;
   info.pair = g_execution_ambiguity.Pair;
   info.direction = g_execution_ambiguity.Direction;
   info.signal_type = SIGNAL_NONE;
   info.initial_entry_price = OrderOpenPrice();
   info.initial_stop_loss = OrderStopLoss();
   info.initial_take_profit = OrderTakeProfit();
   info.initial_lot = OrderLots();
   info.initial_risk_price_distance =
      MathAbs(info.initial_entry_price - info.initial_stop_loss);
   info.entry_price = info.initial_entry_price;
   info.current_sl = info.initial_stop_loss;
   info.current_tp = info.initial_take_profit;
   info.lot = OrderLots();
   info.remaining_lot = OrderLots();
   info.open_time = openTime;
   info.point = GetPointSize(info.pair);
   info.digits = GetDigits(info.pair);
   info.stop_level = GetStopLevel(info.pair);
   info.freeze_level = GetFreezeLevel(info.pair);
   // N2/#233: preserve exact same-session identity when F07 still owns it.
   // Restart recovery leaves DecisionID empty; no identity is reconstructed.
   info.decision_id = g_execution_ambiguity.DecisionID;
   info.execution_hash = g_execution_ambiguity.ExecutionHash;
   info.sequence_hash_short = "";
   ResetC044TradeState(info);
   ResetD1TPWTradeState(info);
   info.recovery_state = REC_AMBIGUOUS_EXECUTION_FROZEN;

   AddToMonitoredTrades(info);

   bool registered = false;
   for(int i = 0; i < g_monitored_count; i++)
      if(g_monitored_trades[i].ticket == ticket)
      {
         registered = true;
         break;
      }
   if(!registered) return false;

   if(!SaveExecutionIdentityHash(g_execution_ambiguity.ExecutionHash, ticket,
                                 g_execution_ambiguity.Pair,
                                 g_execution_ambiguity.Direction,
                                 g_execution_ambiguity.MagicNumber, openTime))
      return false;

   UpsertExecutionHashTombstone(g_execution_ambiguity.ExecutionHash, ticket,
                                g_execution_ambiguity.Pair,
                                g_execution_ambiguity.Direction, openTime);
   Print("[F07][AMBIGUITY_ORDER_ADOPTED] Ticket=", IntegerToString(ticket),
         " Pair=", info.pair,
         " State=", EnumToString(info.recovery_state));
   return true;
}

bool ReconcileExecutionAmbiguityHold()
{
   if(!g_execution_ambiguity.Active) return true;
   if(!g_execution_ambiguity.PersistenceValid) return false;

   bool isOpen = false;
   int ticket = FindExecutionAmbiguityTicket(isOpen);
   if(ticket <= 0) return false;

   if(!AdoptAmbiguousExecutionTicket(ticket, isOpen))
      return false;

   string pair = g_execution_ambiguity.Pair;
   string executionHash = g_execution_ambiguity.ExecutionHash;
   string decisionID = g_execution_ambiguity.DecisionID;
   int magicNumber = g_execution_ambiguity.MagicNumber;
   if(!ClearExecutionAmbiguityHold())
   {
      Log(DBG_ERROR, "F07 ambiguity resolved but HOLD persistence cleanup failed");
      return false;
   }

   if(!isOpen)
   {
      // AdoptAmbiguousExecutionTicket() already selected and identity-validated
      // this exact closed ticket. ClearExecutionAmbiguityHold() performs only
      // terminal-GV cleanup, so the selected closed order remains authoritative.
      TradeInfo outcomeInfo;
      ZeroMemory(outcomeInfo);
      outcomeInfo.ticket = ticket;
      outcomeInfo.magic_number = magicNumber;
      outcomeInfo.pair = pair;
      outcomeInfo.decision_id = decisionID;
      outcomeInfo.execution_hash = executionHash;
      outcomeInfo.recovery_state = REC_AMBIGUOUS_EXECUTION_FROZEN;
      NMJE_PrintClosedOutcomeShadow(outcomeInfo);
   }

   Print("[F07][AMBIGUITY_HOLD_CLEARED] Pair=", pair,
         " Hash=", executionHash,
         " Ticket=", IntegerToString(ticket),
         " Open=", isOpen ? "Y" : "N");
   return true;
}

void ProcessEntry(BBMA_Decision &decision, string pair,
                  RiskValidationSnapshot &snapshot, double frozenLot)
{
   if(decision.DecisionState != DEC_VALIDATED) return;

   bool targetlessLifecycle = IsTargetlessLifecycleDecision(decision);
   bool tpPayloadValid = targetlessLifecycle
      ? (decision.TakeProfit == 0.0)
      : (decision.TakeProfit > 0.0);

   if(targetlessLifecycle &&
      (!decision.HasSLTPSourceComponent ||
       decision.SLTPSourceComponent.ComponentType != SIGNAL_RE_ENTRY ||
       decision.SLTPSourceComponent.Direction != decision.Direction ||
       decision.SLTPSourceComponent.Timeframe <= 0 ||
       decision.SLTPSourceComponent.CandleTime <= 0))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_DECISION_STATE;
      return;
   }

   if(pair == "" || decision.Pair != pair || decision.DecisionID == "" ||
      decision.Direction == DIR_NONE || decision.EntryPrice <= 0 ||
      decision.StopLoss <= 0 || !tpPayloadValid)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_DECISION_STATE;
      return;
   }
   
   double lot = frozenLot;
   if(lot <= 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_LOT;
      return;
   }
   
   if(IsDecisionExecuted(decision.DecisionID))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_DUPLICATE;
      return;
   }

   int pairIdx = FindPairStateIndex(pair);
   if(pairIdx < 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_BROKER_SPEC_INVALID;
      return;
   }
   int magic = g_pair_states[pairIdx].magic_number;
   if(magic <= 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_BROKER_SPEC_INVALID;
      return;
   }
   
   if(!IsSignalAllowed(decision, pair, magic))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_TRADE_LOCK;
      return;
   }
   
   int existingTicket = FindExistingExecutionTicket(pair,
                           (decision.Direction == DIR_BUY) ? OP_BUY : OP_SELL,
                           magic, decision.DecisionID);
   if(existingTicket > 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_DUPLICATE;
      return;
   }

   if(!EnsureMonitoredRegistryCapacity())
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_PORTFOLIO_LIMIT_ATOMIC;
      Log(DBG_ERROR, "Pre-send monitored registry capacity exhausted for " + pair);
      return;
   }
   
   RefreshRates();
   double bid = MarketInfo(pair, MODE_BID);
   double ask = MarketInfo(pair, MODE_ASK);
   int orderType = (decision.Direction == DIR_BUY) ? OP_BUY : OP_SELL;
   double executionPrice = (orderType == OP_BUY) ? ask : bid;
   
   double frozenAllowedDeviation = GetAllowedExecutionDeviation(pair, snapshot);
   double deviation = MathAbs(executionPrice - decision.EntryPrice);
   if(deviation > frozenAllowedDeviation)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_EXECUTION_DEVIATION_EXCEEDED;
      return;
   }
   
   string comment = CreateOrderComment(decision.DecisionID, pair, decision.Direction,
                                       decision.SignalType, executionPrice, 
                                       decision.StopLoss, lot, 0, decision.SequenceHash,
                                       decision.CandleTime);
   
   int ticket = SendOrderWithRetry(pair, orderType, lot,
                                    decision.StopLoss, decision.TakeProfit,
                                    comment, magic, frozenAllowedDeviation,
                                    decision.EntryPrice, decision.DecisionID);
   
   if(ticket > 0)
   {
      if(OrderSelect(ticket, SELECT_BY_TICKET))
      {
         TradeInfo info;
         info.ticket = ticket;
         info.magic_number = magic;
         info.pair = pair;
         info.direction = decision.Direction;
         info.signal_type = decision.SignalType;
         info.initial_entry_price = OrderOpenPrice();
         info.initial_stop_loss = OrderStopLoss();
         info.initial_take_profit = OrderTakeProfit();
         info.initial_lot = OrderLots();
         info.initial_risk_price_distance = MathAbs(info.initial_entry_price - info.initial_stop_loss);
         info.entry_price = info.initial_entry_price;
         info.current_sl = info.initial_stop_loss;
         info.current_tp = info.initial_take_profit;
         info.lot = OrderLots();
         info.remaining_lot = OrderLots();
         info.partial_closed = false;
         info.partial_available = false;
         info.partial_attempted = false;
         info.breakeven_set = false;
         info.be_attempted = false;
         info.be_last_attempt_time = 0;
         info.partial_last_attempt_time = 0;
         info.open_time = OrderOpenTime();
         info.point = snapshot.Point;
         info.digits = snapshot.Digits;
         info.stop_level = GetStopLevel(pair);
         info.freeze_level = GetFreezeLevel(pair);
         info.decision_id = decision.DecisionID;
         info.sequence_hash_short = SHORT_HASH(decision.SequenceHash);

         ResetC044TradeState(info);
         ResetD1TPWTradeState(info);
         bool lifecycleStateReady = true;
         if(decision.D1TPWLifecycleManaged)
            lifecycleStateReady = InitializeD1TPWTradeStateFromDecision(info, decision);
         else if(decision.C044LifecycleManaged)
            lifecycleStateReady = InitializeC044TradeStateFromDecision(info, decision);

         string expectedExecutionHash = SHORT_HASH(decision.DecisionID);
         bool localIdentityPersisted = SaveExecutionIdentityHash(
            expectedExecutionHash, ticket, pair, decision.Direction, magic, OrderOpenTime());

         string persistedComment = OrderComment();
         string brokerExecutionHash = "";
         bool brokerHashFound = ExtractExecutionHash(persistedComment, brokerExecutionHash);
         bool brokerHashMatch = (brokerHashFound &&
                                 brokerExecutionHash == expectedExecutionHash);

         info.execution_hash = localIdentityPersisted
            ? expectedExecutionHash
            : (brokerHashMatch ? brokerExecutionHash : "");
         info.recovery_state = (localIdentityPersisted && lifecycleStateReady)
            ? REC_NORMAL : REC_IDENTITY_MISSING_FROZEN;

         if(!localIdentityPersisted)
            Log(DBG_ERROR, "Execution identity persistence failed ticket=" + IntegerToString(ticket));

         if(info.d1_tpw_lifecycle_managed && lifecycleStateReady &&
            !SaveD1TPWCheckpoint(info))
         {
            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
            Log(DBG_ERROR, "D1TPW checkpoint persist failed ticket=" + IntegerToString(ticket));
         }
         else if(info.c044_lifecycle_managed && lifecycleStateReady &&
                 !SaveC044Checkpoint(info))
         {
            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
            Log(DBG_ERROR, "C044 checkpoint persist failed ticket=" + IntegerToString(ticket));
         }

         // Q9 P10 measures post-fill displacement only; no rejection/filter.
         NMJE_BuildEntryDisplacementAttribution(decision, info.initial_entry_price,
                                                info.entry_displacement);
         // Q9 P4 binds frozen observer metadata to exact ticket/open-time/hash.
         NMJE_BuildTradeAttribution(decision, info);
         bool nmjeAttributionPersisted = false;
         if(info.execution_hash != "" && info.nmje_attribution.Present)
            nmjeAttributionPersisted = SaveNMJEShadowAttribution(info);
         Print("[Q9-P4PLUS-OPEN] Ticket=", IntegerToString(ticket),
               " DIDH=", expectedExecutionHash,
               " ATTR=", info.nmje_attribution.Present ? "Y" : "N",
               " DUR=", nmjeAttributionPersisted ? "Y" : "N",
               " DISP=", info.entry_displacement.Present ? "Y" : "N",
               " Authority=NONE");

         // P2 counterfactual attribution uses only the already-real baseline
         // fill as an engineering entry proxy. No alternate order is sent.
         NMJE_P2_RegisterCounterfactualOpen(pairIdx, decision, info, snapshot);

         Print("[P3S5][EXEC_ID] Ticket=", IntegerToString(ticket),
               " Pair=", pair,
               " Persist=", localIdentityPersisted ? "PASS" : "FAIL",
               " Local=", localIdentityPersisted ? "Y" : "N",
               " BrokerHashFound=", brokerHashFound ? "Y" : "N",
               " BrokerHashMatch=", brokerHashMatch ? "Y" : "N",
               " ExpectedHash=", expectedExecutionHash,
               " BrokerHash=", brokerExecutionHash,
               " RawLen=", IntegerToString(StringLen(persistedComment)),
               " RawComment=<", persistedComment, ">");
         
         AddToMonitoredTrades(info);
         
         decision.DecisionState = DEC_EXECUTED;
         MarkDecisionExecuted(decision.DecisionID, ticket);
         decision.DecisionState = DEC_EXECUTED;
         decision.RejectionReason = REJ_NONE;
         F7ProspectiveContextTelemetry(pairIdx, decision, ticket);
         if(EntryMode == 1)
            Print("[P3M1][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(info.open_time));
         if(EntryMode == 2)
            Print("[P3M2][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(info.open_time));
         return;
      }

      LatchExecutionAmbiguity(decision, pair, magic);
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_AMBIGUOUS_RESULT;
      return;
   }

   decision.DecisionState = DEC_REJECTED;
   if(ticket == -2)
   {
      LatchExecutionAmbiguity(decision, pair, magic);
      decision.RejectionReason = REJ_AMBIGUOUS_RESULT;
   }
   else if(ticket == -3)
      decision.RejectionReason = REJ_EXECUTION_DEVIATION_EXCEEDED;
   else
   {
      decision.RejectionReason = REJ_BROKER_ERROR;
   }
}

bool RunEntryPreflightAndExecute(BBMA_Decision &decision, string pair)
{
   if(decision.DecisionState != DEC_VALIDATED) return false;
   if(pair == "" || decision.Pair != pair) return false;
   if(g_execution_ambiguity.Active)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_AMBIGUOUS_RESULT;
      return false;
   }
   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_START] Pair=", pair,
            " DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " ValidateCandle=", TimeToString(decision.CandleTime),
            " ProcessTime=", TimeToString(g_processing_time));
   if(EntryMode == 2)
      Print("[P3M2][PREFLIGHT_START] Pair=", pair,
            " DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " ValidateCandle=", TimeToString(decision.CandleTime),
            " ProcessTime=", TimeToString(g_processing_time));

   // One frozen execution/risk snapshot for this decision. Strategy semantics
   // are already frozen by the closed-M15 M15/M16/M17 path; only broker/account
   // conditions are live here.
   RiskValidationSnapshot snapshot;
   BuildRiskValidationSnapshot(pair, decision, snapshot);

   // M17 runtime wiring: strategy eligibility is already frozen by M15/M16,
   // while market execution geometry must use the live broker side.
   // BUY references ASK; SELL references BID.
   if(!ResolveExecutionReferencePrice(decision, snapshot))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_MARKET_PRICE_INVALID;
      return false;
   }

   // Resolve only the already-approved source-owned BBMA SL/TP. No fixed-pip,
   // RR-derived or alternate destination is manufactured here.
   if(!ResolveApprovedInitialSLTP(decision, snapshot))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_SLTP_UNRESOLVED;
      return false;
   }

   // M17 finalized SL; freeze the same value into the atomic risk snapshot.
   snapshot.StopLoss = decision.StopLoss;

   ENUM_REJECTION_REASON sltpRejection = REJ_NONE;
   if(!ValidateSLTP(decision, snapshot, sltpRejection))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = (sltpRejection != REJ_NONE) ?
                                 sltpRejection : REJ_SLTP_UNRESOLVED;
      return false;
   }

   bool lotValid = true;
   double lot = CalculateLotSize(decision, snapshot, lotValid);
   if(!lotValid || lot <= 0)
   {
      double rawLotDiagnostic = 0.0;
      double normalizedLotDiagnostic = 0.0;
      double effectiveMaxLotDiagnostic = 0.0;
      string lotReasonTag = DiagnoseInvalidLotReason(
         decision, snapshot, rawLotDiagnostic, normalizedLotDiagnostic,
         effectiveMaxLotDiagnostic);
      PrintInvalidLotDiagnostic(decision, snapshot, lotReasonTag,
                                rawLotDiagnostic, normalizedLotDiagnostic,
                                effectiveMaxLotDiagnostic);

      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_LOT;
      return false;
   }

   RiskStatus riskStatus = CheckRiskBeforeTrade(decision, snapshot, lot);
   if(!riskStatus.allowed)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = (riskStatus.rejection_reason != REJ_NONE) ?
                                 riskStatus.rejection_reason : REJ_TOTAL_RISK;
      return false;
   }

   if(g_portfolio_emergency_close_requested)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_BASKET_LOSS;
      return false;
   }

   FinalPortfolioGuard(decision);
   if(decision.DecisionState != DEC_VALIDATED)
   {
      if(EntryMode == 1)
         Print("[P3M1][PORTFOLIO_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      return false;
   }

   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_PASS] DecisionID=", decision.DecisionID,
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " Lot=", DoubleToString(lot, snapshot.LotDigits));
   if(EntryMode == 2)
      Print("[P3M2][PREFLIGHT_PASS] DecisionID=", decision.DecisionID,
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " Lot=", DoubleToString(lot, snapshot.LotDigits));

   ProcessEntry(decision, pair, snapshot, lot);
   return (decision.DecisionState == DEC_EXECUTED);
}

//+------------------------------------------------------------------+
//| MODULE 23: POSITION MANAGEMENT (TICK-DRIVEN)                     |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

// C044 Step3: strategy evidence is consumed only after M08/M12 owners have
// been updated by the closed-M15 ProcessPair cycle. M23 still owns the latch
// and close action; these helpers never redetect or mutate upstream owners.
bool GetC044OwnerReEntrySnapshot(int pairIndex, int timeframe,
                                  ENUM_DIRECTION direction,
                                  ReEntryData &reEntry)
{
   ZeroMemory(reEntry);
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   if(timeframe == PERIOD_M15 && direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_m15_buy_state;
   else if(timeframe == PERIOD_M15 && direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_m15_sell_state;
   else if(timeframe == PERIOD_H1 && direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_h1_buy_state;
   else if(timeframe == PERIOD_H1 && direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_h1_sell_state;
   else if(timeframe == PERIOD_H4 && direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_h4_buy_state;
   else if(timeframe == PERIOD_H4 && direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_h4_sell_state;
   else if(timeframe == PERIOD_D1 && direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_d1_buy_state;
   else if(timeframe == PERIOD_D1 && direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_d1_sell_state;
   else
      return false;

   return true;
}

bool GetC044OwnerExtremeSnapshot(int pairIndex, int timeframe,
                                 ENUM_DIRECTION direction,
                                 ExtremeLifecycleData &extreme)
{
   ZeroMemory(extreme);
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   if(timeframe == PERIOD_M15 && direction == DIR_BUY)
      extreme = g_pair_states[pairIndex].extreme_m15_buy_lifecycle;
   else if(timeframe == PERIOD_M15 && direction == DIR_SELL)
      extreme = g_pair_states[pairIndex].extreme_m15_sell_lifecycle;
   else if(timeframe == PERIOD_H1 && direction == DIR_BUY)
      extreme = g_pair_states[pairIndex].extreme_h1_buy_lifecycle;
   else if(timeframe == PERIOD_H1 && direction == DIR_SELL)
      extreme = g_pair_states[pairIndex].extreme_h1_sell_lifecycle;
   else if(timeframe == PERIOD_H4 && direction == DIR_BUY)
      extreme = g_pair_states[pairIndex].extreme_h4_buy_lifecycle;
   else if(timeframe == PERIOD_H4 && direction == DIR_SELL)
      extreme = g_pair_states[pairIndex].extreme_h4_sell_lifecycle;
   else if(timeframe == PERIOD_D1 && direction == DIR_BUY)
      extreme = g_pair_states[pairIndex].extreme_d1_buy_lifecycle;
   else if(timeframe == PERIOD_D1 && direction == DIR_SELL)
      extreme = g_pair_states[pairIndex].extreme_d1_sell_lifecycle;
   else
      return false;

   return true;
}

bool FreezeC044Lifecycle(TradeInfo &info, string reason)
{
   if(!info.c044_lifecycle_managed) return false;

   info.c044_state = C044_LIFE_FROZEN;
   info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
   info.c044_exit_reason = C044_EXIT_NONE;
   info.c044_exit_latched_candle = 0;
   bool persisted = SaveC044Checkpoint(info);
   if(!persisted)
      Log(DBG_ERROR, "C044 freeze checkpoint failed ticket=" + IntegerToString(info.ticket));

   F7Telemetry("LIFECYCLE_FROZEN", info,
               (persisted ? "Persist=PASS " : "Persist=FAIL ") + "Cause=" + reason);
   Log(DBG_ERROR, "C044 lifecycle frozen ticket=" + IntegerToString(info.ticket) +
       " pair=" + info.pair + " reason=" + reason);
   return false;
}

bool ProcessC044OwnerClosedCandle(TradeInfo &info, int pairIndex,
                                  datetime candleTime)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return true;
   if(pairIndex < 0 || pairIndex >= g_pair_count || candleTime <= 0)
      return FreezeC044Lifecycle(info, "INVALID_OWNER_EVENT_IDENTITY");
   if(info.c044_state == C044_LIFE_EXIT_LATCHED ||
      info.c044_state == C044_LIFE_FROZEN)
      return true;
   if(!info.c044_replay_seed_valid)
      return FreezeC044Lifecycle(info, "REPLAY_SEED_MISSING");

   string pair = g_pair_states[pairIndex].actual_symbol;
   if(pair == "" || info.pair != pair ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe))
      return FreezeC044Lifecycle(info, "OWNER_EVENT_PAIR_OR_TF_MISMATCH");

   int shift = iBarShift(pair, info.c044_owner_timeframe, candleTime, true);
   if(shift < 1)
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CANDLE_NOT_EXACT_CLOSED_BAR");

   TimeframeData data;
   InitTimeframeData(data);
   GetDataForTimeframe(pair, info.c044_owner_timeframe, candleTime, data);
   if(!data.is_valid || !data.is_closed || data.candle_time != candleTime ||
      data.barIndex != shift)
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CLOSED_DATA_UNAVAILABLE");

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);

   // Deterministic replay uses the same canonical M08 and M12 state machines on
   // private C044 snapshots. No Extreme/Re-Entry formula is reimplemented here.
   bool rawBuy = DetectExtreme(pair, DIR_BUY, data, band);
   bool rawSell = DetectExtreme(pair, DIR_SELL, data, band);
   UpdateExtremeLifecycle(info.c044_replay_extreme_buy, pair, DIR_BUY,
                          data, band, rawBuy);
   UpdateExtremeLifecycle(info.c044_replay_extreme_sell, pair, DIR_SELL,
                          data, band, rawSell);
   ResolveOppositeExtremeSupersession(info.c044_replay_extreme_buy,
                                      info.c044_replay_extreme_sell, data);
   UpdateReEntryState(info.c044_replay_reentry, pair, info.direction, data);

   bool sameReEntryEvent =
      (info.c044_replay_reentry.State == RE_STATE_CONFIRMED &&
       info.c044_replay_reentry.IsValid &&
       info.c044_replay_reentry.Direction == info.direction &&
       info.c044_replay_reentry.Timeframe == info.c044_owner_timeframe &&
       info.c044_replay_reentry.ConfirmationCandle == candleTime &&
       candleTime > info.c044_epoch_anchor_candle);

   bool oppositeExtremeEvent = false;
   if(info.direction == DIR_BUY)
   {
      bool mature =
         (info.c044_replay_extreme_sell.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
          info.c044_replay_extreme_sell.Maturity == EXT_MAT_RETEST_PHASE ||
          info.c044_replay_extreme_sell.Maturity == EXT_MAT_RETEST_READY);
      oppositeExtremeEvent =
         (info.c044_replay_extreme_sell.IsValid && mature &&
          info.c044_replay_extreme_sell.ConfirmationCandleTime == candleTime &&
          candleTime > info.c044_epoch_anchor_candle);
   }
   else if(info.direction == DIR_SELL)
   {
      bool mature =
         (info.c044_replay_extreme_buy.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
          info.c044_replay_extreme_buy.Maturity == EXT_MAT_RETEST_PHASE ||
          info.c044_replay_extreme_buy.Maturity == EXT_MAT_RETEST_READY);
      oppositeExtremeEvent =
         (info.c044_replay_extreme_buy.IsValid && mature &&
          info.c044_replay_extreme_buy.ConfirmationCandleTime == candleTime &&
          candleTime > info.c044_epoch_anchor_candle);
   }

   info.c044_last_processed_owner_candle = candleTime;

   if(oppositeExtremeEvent)
   {
      if(!LatchC044Exit(info, C044_EXIT_CYCLE_SUPERSEDED, candleTime))
         return FreezeC044Lifecycle(info, "CYCLE_SUPERSESSION_LATCH_FAILED");
      return true;
   }

   if(info.c044_state == C044_LIFE_WAIT_NEXT_REENTRY)
   {
      if(sameReEntryEvent)
      {
         info.c044_owner_reentry_candle = candleTime;
         info.c044_epoch_anchor_candle = candleTime;
         info.c044_state = C044_LIFE_MOMENTUM_PENDING;
         info.c044_exit_reason = C044_EXIT_NONE;
         info.c044_exit_latched_candle = 0;
      }
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "WAIT_NEXT_REENTRY_CHECKPOINT_FAILED");
      if(sameReEntryEvent)
         F7Telemetry("REENTRY_REARM", info, "Persist=PASS ReEntryCandle="+TimeToString(candleTime,TIME_DATE|TIME_MINUTES));
      return true;
   }

   if(info.c044_state != C044_LIFE_MOMENTUM_PENDING)
      return FreezeC044Lifecycle(info, "UNEXPECTED_OWNER_EVENT_STATE");

   if(candleTime <= info.c044_epoch_anchor_candle)
   {
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "EPOCH_BOUNDARY_CHECKPOINT_FAILED");
      return true;
   }

   ENUM_DIRECTION oppositeDirection = (info.direction == DIR_BUY) ? DIR_SELL : DIR_BUY;
   bool sameMomentum = DetectCSM(pair, info.c044_owner_timeframe,
                                 info.direction, shift);
   bool oppositeMomentum = DetectCSM(pair, info.c044_owner_timeframe,
                                     oppositeDirection, shift);
   bool reverseConfirmation = (info.direction == DIR_BUY)
      ? (data.close < data.open)
      : (data.close > data.open);

   // F7 precedence: canonical CSM classification before the weaker reverse-colour test.
   if(sameMomentum)
   {
      info.c044_state = C044_LIFE_WAIT_NEXT_REENTRY;
      info.c044_exit_reason = C044_EXIT_NONE;
      info.c044_exit_latched_candle = 0;
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "MOMENTUM_HOLD_CHECKPOINT_FAILED");
      F7Telemetry("MOMENTUM_HOLD", info, "Persist=PASS HoldCandle="+TimeToString(candleTime,TIME_DATE|TIME_MINUTES));
      return true;
   }

   if(oppositeMomentum)
   {
      if(!LatchC044Exit(info, C044_EXIT_OPPOSITE_CSM, candleTime))
         return FreezeC044Lifecycle(info, "OPPOSITE_CSM_LATCH_FAILED");
      return true;
   }

   if(reverseConfirmation)
   {
      if(!LatchC044Exit(info, C044_EXIT_FAILED_MOMENTUM, candleTime))
         return FreezeC044Lifecycle(info, "FAILED_MOMENTUM_LATCH_FAILED");
      return true;
   }

   if(!SaveC044Checkpoint(info))
      return FreezeC044Lifecycle(info, "MOMENTUM_PENDING_CHECKPOINT_FAILED");
   return true;
}

bool AdvanceC044OwnerEventOneCandle(TradeInfo &info, int pairIndex)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return true;
   if(info.c044_state == C044_LIFE_EXIT_LATCHED ||
      info.c044_state == C044_LIFE_FROZEN)
      return true;
   if(info.c044_last_processed_owner_candle <= 0 ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe))
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CURSOR_INVALID");
   if(!info.c044_replay_seed_valid)
      return FreezeC044Lifecycle(info, "REPLAY_SEED_MISSING");

   datetime latestClosed = GetLatestClosedCandleTime(
      info.pair, info.c044_owner_timeframe);
   if(latestClosed <= 0)
      return FreezeC044Lifecycle(info, "LATEST_OWNER_CANDLE_UNAVAILABLE");
   if(latestClosed <= info.c044_last_processed_owner_candle)
      return true;

   int latestShift = iBarShift(info.pair, info.c044_owner_timeframe,
                               latestClosed, true);
   int previousShift = iBarShift(info.pair, info.c044_owner_timeframe,
                                 info.c044_last_processed_owner_candle, true);
   if(latestShift < 1 || previousShift < 1 || previousShift <= latestShift)
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CURSOR_NOT_IN_HISTORY");

   // Replay every missed closed owner candle from oldest to newest. Historical
   // data must be exact; any missing candle freezes the lifecycle rather than
   // guessing whether a Re-Entry, Extreme or failed Momentum occurred.
   for(int shift = previousShift - 1; shift >= latestShift; shift--)
   {
      datetime candleTime = iTime(info.pair, info.c044_owner_timeframe, shift);
      if(candleTime <= info.c044_last_processed_owner_candle)
         return FreezeC044Lifecycle(info, "REPLAY_CANDLE_ORDER_INVALID");
      if(!ProcessC044OwnerClosedCandle(info, pairIndex, candleTime))
         return false;
      if(info.c044_state == C044_LIFE_EXIT_LATCHED ||
         info.c044_state == C044_LIFE_FROZEN)
         return true;
   }

   if(info.c044_last_processed_owner_candle != latestClosed)
      return FreezeC044Lifecycle(info, "REPLAY_CURSOR_DID_NOT_REACH_LATEST");
   return true;
}

void AdvanceC044OwnerEventsForPair(int pairIndex)
{
   if(!EnableC044Lifecycle) return;
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   string pair = g_pair_states[pairIndex].actual_symbol;
   for(int i = 0; i < g_monitored_count; i++)
   {
      // Avoid a local reference alias: pass the registry element directly for
      // conservative MQL4 compiler compatibility.
      if(!g_monitored_trades[i].c044_lifecycle_managed ||
         g_monitored_trades[i].pair != pair)
         continue;
      if(g_monitored_trades[i].recovery_state != REC_NORMAL &&
         g_monitored_trades[i].recovery_state != REC_PARTIAL_INFERRED)
         continue;
      if(g_monitored_trades[i].c044_state == C044_LIFE_EXIT_LATCHED ||
         g_monitored_trades[i].c044_state == C044_LIFE_FROZEN)
         continue;

      AdvanceC044OwnerEventOneCandle(g_monitored_trades[i], pairIndex);
   }
}

void F7TelemetryWrite(string line)
{
   int h=FileOpen("BBMA_F7_TELEMETRY.log", FILE_TXT|FILE_READ|FILE_WRITE|FILE_SHARE_READ);
   if(h==INVALID_HANDLE) return;
   FileSeek(h,0,SEEK_END); FileWriteString(h,line+"\r\n"); FileFlush(h); FileClose(h);
}

void F7BuildIdentityTelemetry()
{
   string line="[F7-BUILD] EA=BBMA_EA Build=5.20 BuildTag="+string(BBMA_BUILD_TAG)+
      " SourceRev="+string(BBMA_SOURCE_REV_TAG)+
      " InitTime="+TimeToString(TimeLocal(),TIME_DATE|TIME_SECONDS);
   Print(line);
   F7TelemetryWrite(line);
}

void F7Telemetry(string eventName, TradeInfo &info, string detail="")
{
   if(info.c044_shadow_replay) return;
   string line="[F7-TELEM] Event="+eventName+" Ticket="+IntegerToString(info.ticket)+" Pair="+info.pair+
      " State="+EnumToString(info.c044_state)+" Reason="+EnumToString(info.c044_exit_reason)+
      " DecisionID="+info.decision_id+" Hash="+info.execution_hash+" OwnerTF="+IntegerToString(info.c044_owner_timeframe)+
      " Candle="+TimeToString(info.c044_last_processed_owner_candle,TIME_DATE|TIME_MINUTES)+(detail==""?"":" "+detail);
   Print(line); F7TelemetryWrite(line);
}

void F7ProspectiveContextTelemetry(int pairIndex, BBMA_Decision &decision, int ticket)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!decision.Valid || decision.DecisionState != DEC_EXECUTED) return;
   if(decision.SignalType != SIGNAL_RE_ENTRY) return;
   if(!decision.C044LifecycleManaged) return;

   ExtremeLifecycleData ext;
   ReEntryData h1re;
   if(decision.Direction == DIR_BUY)
   {
      ext = g_pair_states[pairIndex].extreme_m15_buy_lifecycle;
      h1re = g_pair_states[pairIndex].re_h1_buy_state;
   }
   else if(decision.Direction == DIR_SELL)
   {
      ext = g_pair_states[pairIndex].extreme_m15_sell_lifecycle;
      h1re = g_pair_states[pairIndex].re_h1_sell_state;
   }
   else return;

   NestedJourneyState journey = g_nested_journeys[pairIndex];
   string journeyId = (journey.JourneyID == "" ? "-" : journey.JourneyID);
   string line = "[F7-PROSPECTIVE] Ticket="+IntegerToString(ticket)+" Pair="+decision.Pair+
      " DecisionID="+NMJE_LogIdentityToken(decision.DecisionID)+
      " DIDH="+SHORT_HASH(decision.DecisionID)+
      " Dir="+NMJE_DirText(decision.Direction)+
      " ExtremeState="+EnumToString(ext.Maturity)+
      " RawTime="+TimeToString(ext.RawCandleTime,TIME_DATE|TIME_MINUTES)+
      " ConfirmTime="+TimeToString(ext.ConfirmationCandleTime,TIME_DATE|TIME_MINUTES)+
      " H1ReType="+EnumToString(h1re.Type)+
      " H1ReState="+EnumToString(h1re.State)+
      " H1ConfirmTime="+TimeToString(h1re.ConfirmationCandle,TIME_DATE|TIME_MINUTES)+
      " NMJE="+NMJE_RelationText(journey.Relation)+
      " H4Parent="+NMJE_ParentText(journey.ParentKind)+"/"+NMJE_DirText(journey.ParentDirection)+
      " JourneyID="+journeyId;
   Print(line);
   F7TelemetryWrite(line);
}

void F7TelemetryHeartbeat()
{
   static datetime lastBeat=0; datetime now=TimeLocal();
   if(lastBeat>0 && now-lastBeat<300) return; lastBeat=now;
   int managed=0; for(int i=0;i<g_monitored_count;i++) if(g_monitored_trades[i].c044_lifecycle_managed) managed++;
   string line="[F7-TELEM] Event=HEARTBEAT Init="+IntegerToString(g_is_initialized)+" Connected="+IntegerToString(IsTerminalConnected())+
      " Monitored="+IntegerToString(g_monitored_count)+" F7Managed="+IntegerToString(managed)+" Time="+TimeToString(now,TIME_DATE|TIME_SECONDS);
   Print(line); F7TelemetryWrite(line);
}

bool LatchC044Exit(TradeInfo &info, ENUM_C044_EXIT_REASON reason, datetime candleTime)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return false;
   if(reason == C044_EXIT_NONE || candleTime <= 0) return false;

   if(info.c044_state == C044_LIFE_EXIT_LATCHED)
      return (info.c044_exit_reason == reason);

   if(info.c044_state != C044_LIFE_MOMENTUM_PENDING &&
      info.c044_state != C044_LIFE_WAIT_NEXT_REENTRY)
      return false;

   info.c044_state = C044_LIFE_EXIT_LATCHED;
   info.c044_exit_reason = reason;
   info.c044_exit_latched_candle = candleTime;
   bool persisted = SaveC044Checkpoint(info);
   if(!persisted)
      Log(DBG_ERROR, "C044 latch checkpoint failed ticket=" + IntegerToString(info.ticket));
   F7Telemetry("EXIT_LATCHED", info, (persisted ? "Persist=PASS " : "Persist=FAIL ")+
               "LatchCandle="+TimeToString(candleTime,TIME_DATE|TIME_MINUTES));
   return true;
}

bool ExecuteLatchedC044Close(TradeInfo &info)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return false;
   if(info.c044_state != C044_LIFE_EXIT_LATCHED ||
      info.c044_exit_reason == C044_EXIT_NONE) return false;
   if(info.ticket <= 0 || info.pair == "" || info.magic_number <= 0) return false;

   ResetLastError();
   if(!OrderSelect(info.ticket, SELECT_BY_TICKET)) return false;
   if(OrderCloseTime() != 0)
   {
      ClearC044Checkpoint(info);
      return true;
   }
   if(OrderSymbol() != info.pair || OrderMagicNumber() != info.magic_number)
      return false;

   double closePrice = (info.direction == DIR_BUY)
      ? MarketInfo(info.pair, MODE_BID)
      : (info.direction == DIR_SELL ? MarketInfo(info.pair, MODE_ASK) : 0.0);
   if(closePrice <= 0.0) return false;

   ResetLastError();
   if(OrderClose(info.ticket, OrderLots(), closePrice, Slippage))
   {
      F7Telemetry("CLOSE_SUCCESS", info, "ClosePrice="+DoubleToString(closePrice, info.digits));
      ClearC044Checkpoint(info);
      return true;
   }

   int error = GetLastError();
   Log(DBG_ERROR, "C044 close failed ticket=" + IntegerToString(info.ticket) +
       " error=" + IntegerToString(error));
   return false;
}


// D1TPW-01: lifecycle evidence is consumed on the M15 processing clock only.
// The D1 Extreme remains TP semantic owner; M23 only latches/executes full close.
bool FreezeD1TPWLifecycle(TradeInfo &info, string reason)
{
   if(!info.d1_tpw_lifecycle_managed) return false;
   info.d1_tpw_frozen = true;
   info.d1_tpw_exit_latched = false;
   info.d1_tpw_exit_latched_candle = 0;
   info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
   if(!SaveD1TPWCheckpoint(info))
      Log(DBG_ERROR, "D1TPW freeze checkpoint failed ticket=" + IntegerToString(info.ticket));
   Log(DBG_ERROR, "D1TPW lifecycle frozen ticket=" + IntegerToString(info.ticket) +
       " pair=" + info.pair + " reason=" + reason);
   return false;
}

bool LatchD1TPWExit(TradeInfo &info, datetime candleTime)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed ||
      info.d1_tpw_frozen || candleTime <= 0)
      return false;
   if(info.d1_tpw_exit_latched)
      return (info.d1_tpw_exit_latched_candle == candleTime);

   info.d1_tpw_exit_latched = true;
   info.d1_tpw_exit_latched_candle = candleTime;
   if(!SaveD1TPWCheckpoint(info))
      return FreezeD1TPWLifecycle(info, "EXIT_LATCH_CHECKPOINT_FAILED");
   return true;
}

bool ProcessD1TPWClosedCandle(TradeInfo &info, int pairIndex, datetime candleTime)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed) return true;
   if(info.d1_tpw_frozen || info.d1_tpw_exit_latched) return true;
   if(pairIndex < 0 || pairIndex >= g_pair_count || candleTime <= 0 ||
      info.d1_tpw_extreme_candle <= 0 || candleTime <= info.d1_tpw_extreme_candle)
      return FreezeD1TPWLifecycle(info, "INVALID_D1_EVENT_IDENTITY");

   string pair = g_pair_states[pairIndex].actual_symbol;
   if(pair == "" || pair != info.pair)
      return FreezeD1TPWLifecycle(info, "PAIR_MISMATCH");

   int shift = iBarShift(pair, PERIOD_D1, candleTime, true);
   if(shift < 1 || iTime(pair, PERIOD_D1, shift) != candleTime)
      return FreezeD1TPWLifecycle(info, "D1_CANDLE_NOT_EXACT_CLOSED_BAR");

   int tfSeconds = GetTimeframeSeconds(PERIOD_D1);
   if(tfSeconds <= 0 || !IsCandleClosed(candleTime, tfSeconds))
      return FreezeD1TPWLifecycle(info, "D1_CANDLE_NOT_CLOSED");

   double high = iHigh(pair, PERIOD_D1, shift);
   double low = iLow(pair, PERIOD_D1, shift);
   if(high <= 0.0 || low <= 0.0 || high < low)
      return FreezeD1TPWLifecycle(info, "D1_PRICE_HISTORY_INVALID");

   // Validate MA history explicitly; IsD1TPWCompletionAtShift(false) alone
   // cannot distinguish 'not reached' from unavailable MA history.
   if(info.direction == DIR_SELL)
   {
      if(BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift) <= 0.0 ||
         BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift) <= 0.0)
         return FreezeD1TPWLifecycle(info, "D1_TPW_MA_HISTORY_INVALID");
   }
   else if(info.direction == DIR_BUY)
   {
      if(BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift) <= 0.0 ||
         BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift) <= 0.0)
         return FreezeD1TPWLifecycle(info, "D1_TPW_MA_HISTORY_INVALID");
   }
   else
      return FreezeD1TPWLifecycle(info, "DIRECTION_INVALID");

   info.d1_tpw_last_processed_d1_candle = candleTime;
   if(IsD1TPWCompletionAtShift(pair, info.direction, shift))
      return LatchD1TPWExit(info, candleTime);

   if(!SaveD1TPWCheckpoint(info))
      return FreezeD1TPWLifecycle(info, "D1_CURSOR_CHECKPOINT_FAILED");
   return true;
}

bool AdvanceD1TPWLifecycleForTrade(TradeInfo &info, int pairIndex)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed) return true;
   if(info.d1_tpw_frozen || info.d1_tpw_exit_latched) return true;
   if(info.d1_tpw_last_processed_d1_candle <= 0)
      return FreezeD1TPWLifecycle(info, "D1_CURSOR_INVALID");

   datetime latestClosed = GetLatestClosedCandleTime(info.pair, PERIOD_D1);
   if(latestClosed <= 0)
      return FreezeD1TPWLifecycle(info, "LATEST_D1_UNAVAILABLE");
   if(latestClosed <= info.d1_tpw_last_processed_d1_candle) return true;

   int latestShift = iBarShift(info.pair, PERIOD_D1, latestClosed, true);
   int previousShift = iBarShift(info.pair, PERIOD_D1,
                                 info.d1_tpw_last_processed_d1_candle, true);
   if(latestShift < 1 || previousShift < 1 || previousShift <= latestShift)
      return FreezeD1TPWLifecycle(info, "D1_CURSOR_NOT_IN_HISTORY");

   for(int shift = previousShift - 1; shift >= latestShift; shift--)
   {
      datetime candleTime = iTime(info.pair, PERIOD_D1, shift);
      if(candleTime <= 0)
         return FreezeD1TPWLifecycle(info, "MISSED_D1_CANDLE_UNAVAILABLE");
      if(!ProcessD1TPWClosedCandle(info, pairIndex, candleTime)) return false;
      if(info.d1_tpw_exit_latched || info.d1_tpw_frozen) break;
   }
   return true;
}

void AdvanceD1TPWLifecycleForPair(int pairIndex)
{
   if(!EnableD1TPWLifecycle || pairIndex < 0 || pairIndex >= g_pair_count) return;
   string pair = g_pair_states[pairIndex].actual_symbol;
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(!g_monitored_trades[i].d1_tpw_lifecycle_managed ||
         g_monitored_trades[i].pair != pair)
         continue;
      if(g_monitored_trades[i].recovery_state != REC_NORMAL &&
         g_monitored_trades[i].recovery_state != REC_PARTIAL_INFERRED)
         continue;
      AdvanceD1TPWLifecycleForTrade(g_monitored_trades[i], pairIndex);
   }
}

bool ExecuteLatchedD1TPWClose(TradeInfo &info)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed ||
      info.d1_tpw_frozen || !info.d1_tpw_exit_latched ||
      info.d1_tpw_exit_latched_candle <= 0)
      return false;
   if(info.ticket <= 0 || info.pair == "" || info.magic_number <= 0) return false;
   if(!OrderSelect(info.ticket, SELECT_BY_TICKET) || OrderCloseTime() != 0) return false;
   if(OrderSymbol() != info.pair || OrderMagicNumber() != info.magic_number) return false;

   double closePrice = (info.direction == DIR_BUY)
      ? MarketInfo(info.pair, MODE_BID)
      : (info.direction == DIR_SELL ? MarketInfo(info.pair, MODE_ASK) : 0.0);
   if(closePrice <= 0.0) return false;

   ResetLastError();
   if(OrderClose(info.ticket, OrderLots(), closePrice, Slippage))
   {
      ClearD1TPWCheckpoint(info);
      return true;
   }

   int error = GetLastError();
   Log(DBG_ERROR, "D1TPW close failed ticket=" + IntegerToString(info.ticket) +
       " error=" + IntegerToString(error));
   return false;
}

void ManagePositions()
{
   if(g_is_managing_trade) return;
   g_is_managing_trade = true;
   
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(!OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
         continue;
      if(OrderCloseTime() != 0)
         continue;

      int pairIdx = FindPairStateIndex(OrderSymbol());
      if(pairIdx < 0) continue;
      int expectedMagic = g_pair_states[pairIdx].magic_number;
      if(expectedMagic <= 0 || OrderMagicNumber() != expectedMagic ||
         g_monitored_trades[i].magic_number != expectedMagic)
         continue;

      string pair = OrderSymbol();
      double bid = MarketInfo(pair, MODE_BID);
      double ask = MarketInfo(pair, MODE_ASK);

      g_monitored_trades[i].entry_price = OrderOpenPrice();
      g_monitored_trades[i].current_sl = OrderStopLoss();
      g_monitored_trades[i].current_tp = OrderTakeProfit();
      g_monitored_trades[i].lot = OrderLots();
      g_monitored_trades[i].remaining_lot = OrderLots();
      
      if(g_portfolio_emergency_close_requested)
      {
         double closePrice = (g_monitored_trades[i].direction == DIR_BUY) ? bid : ask;
         if(closePrice <= 0) continue;

         ResetLastError();
         if(!OrderClose(OrderTicket(), OrderLots(), closePrice, Slippage))
         {
            int error = GetLastError();
            Log(DBG_ERROR, "Emergency close failed ticket=" + IntegerToString(OrderTicket()) +
                " error=" + IntegerToString(error));
         }
         continue;
      }

      if(g_monitored_trades[i].recovery_state == REC_CORRUPTED ||
         g_monitored_trades[i].recovery_state == REC_RECOVERY_INVALID ||
         g_monitored_trades[i].recovery_state == REC_IDENTITY_MISSING_FROZEN ||
         g_monitored_trades[i].recovery_state == REC_AMBIGUOUS_EXECUTION_FROZEN)
      {
         continue;
      }

      // M20 emergency handling above retains precedence. D1 TPW and C044
      // are mutually exclusive normal strategy lifecycle owners.
      if(EnableD1TPWLifecycle && g_monitored_trades[i].d1_tpw_lifecycle_managed &&
         g_monitored_trades[i].d1_tpw_exit_latched &&
         !g_monitored_trades[i].d1_tpw_frozen)
      {
         ExecuteLatchedD1TPWClose(g_monitored_trades[i]);
         continue;
      }

      // C044 close execution is dormant while its internal feature gate is OFF.
      if(EnableC044Lifecycle && g_monitored_trades[i].c044_lifecycle_managed &&
         g_monitored_trades[i].c044_state == C044_LIFE_EXIT_LATCHED)
      {
         ExecuteLatchedC044Close(g_monitored_trades[i]);
         continue;
      }
   }
   
   g_is_managing_trade = false;
}

//+------------------------------------------------------------------+
//| MODULE 24: RECOVERY ENGINE                                       |
//| LEVEL: EXPERT                                                    |
//+------------------------------------------------------------------+

void ResetD1TPWTradeState(TradeInfo &info)
{
   info.d1_tpw_lifecycle_managed = false;
   info.d1_tpw_extreme_candle = 0;
   info.d1_tpw_last_processed_d1_candle = 0;
   info.d1_tpw_exit_latched = false;
   info.d1_tpw_exit_latched_candle = 0;
   info.d1_tpw_frozen = false;
}

string D1TPWCheckpointBase(TradeInfo &info)
{
   return "D1TPW|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(info.ticket) + "|";
}

bool DeleteTerminalGlobalExact(string key)
{
   if(!GlobalVariableCheck(key)) return true;
   ResetLastError();
   if(!GlobalVariableDel(key)) return false;
   return !GlobalVariableCheck(key);
}

bool SetTerminalGlobalExact(string key, double value)
{
   ResetLastError();
   if(GlobalVariableSet(key, value) == 0) return false;
   if(!GlobalVariableCheck(key)) return false;
   return (GlobalVariableGet(key) == value);
}

bool D1TPWGenerationPayloadExists(TradeInfo &info, double generation)
{
   if(info.ticket <= 0 || generation <= 0.0) return false;
   string base = D1TPWCheckpointBase(info);
   if(!GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "G") != generation)
      return false;
   string keys[8] = {"D","X","LP","L","XL","F","OT","MG"};
   for(int i = 0; i < 8; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   return true;
}

bool D1TPWCheckpointExists(TradeInfo &info)
{
   if(info.ticket <= 0) return false;
   string base = D1TPWCheckpointBase(info);
   if(!GlobalVariableCheck(base + "CM")) return false;
   double committed = GlobalVariableGet(base + "CM");
   if(committed <= 0.0) return false;
   return D1TPWGenerationPayloadExists(info, committed);
}

void ClearD1TPWCheckpoint(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = D1TPWCheckpointBase(info);
   bool cleared = DeleteTerminalGlobalExact(base + "CM");
   GlobalVariablesFlush();

   string keys[10] = {"D","X","LP","L","XL","F","OT","MG","G","GN"};
   for(int i = 0; i < 10; i++)
      if(!DeleteTerminalGlobalExact(base + keys[i])) cleared = false;
   GlobalVariablesFlush();
   if(!cleared)
      Log(DBG_ERROR, "D1TPW checkpoint clear incomplete ticket=" +
          IntegerToString(info.ticket));
}

bool SaveD1TPWCheckpoint(TradeInfo &info)
{
   if(!info.d1_tpw_lifecycle_managed || info.ticket <= 0 ||
      info.magic_number <= 0 || info.open_time <= 0 ||
      (info.direction != DIR_BUY && info.direction != DIR_SELL) ||
      info.d1_tpw_extreme_candle <= 0 ||
      info.d1_tpw_last_processed_d1_candle < info.d1_tpw_extreme_candle)
      return false;

   string base = D1TPWCheckpointBase(info);

   // Generation-atomic checkpoint replacement: invalidate the old commit marker
   // before mutating payload and publish the new commit marker last.
   if(!DeleteTerminalGlobalExact(base + "CM")) return false;
   GlobalVariablesFlush();
   if(GlobalVariableCheck(base + "CM")) return false;

   double priorGeneration =
      GlobalVariableCheck(base + "GN") ? GlobalVariableGet(base + "GN") : 0.0;
   if(priorGeneration < 0.0 || priorGeneration > 9000000000000000.0)
      priorGeneration = 0.0;
   double generation = MathFloor(priorGeneration) + 1.0;

   if(!SetTerminalGlobalExact(base + "GN", generation)) return false;
   if(!SetTerminalGlobalExact(base + "D", (double)info.direction)) return false;
   if(!SetTerminalGlobalExact(base + "X", (double)info.d1_tpw_extreme_candle)) return false;
   if(!SetTerminalGlobalExact(base + "LP",
                              (double)info.d1_tpw_last_processed_d1_candle)) return false;
   if(!SetTerminalGlobalExact(base + "L",
                              info.d1_tpw_exit_latched ? 1.0 : 0.0)) return false;
   if(!SetTerminalGlobalExact(base + "XL",
                              (double)info.d1_tpw_exit_latched_candle)) return false;
   if(!SetTerminalGlobalExact(base + "F",
                              info.d1_tpw_frozen ? 1.0 : 0.0)) return false;
   if(!SetTerminalGlobalExact(base + "OT", (double)info.open_time)) return false;
   if(!SetTerminalGlobalExact(base + "MG", (double)info.magic_number)) return false;
   if(!SetTerminalGlobalExact(base + "G", generation)) return false;
   GlobalVariablesFlush();

   if(!D1TPWGenerationPayloadExists(info, generation))
      return false;

   if(!SetTerminalGlobalExact(base + "CM", generation)) return false;
   GlobalVariablesFlush();
   return (D1TPWCheckpointExists(info) &&
           GlobalVariableGet(base + "CM") == generation &&
           GlobalVariableGet(base + "G") == generation);
}

bool LoadD1TPWCheckpoint(TradeInfo &info)
{
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0) return false;
   if(!D1TPWCheckpointExists(info)) return false;

   string base = D1TPWCheckpointBase(info);
   double committedGeneration = GlobalVariableGet(base + "CM");
   ENUM_DIRECTION direction = (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   datetime extremeCandle = (datetime)((int)GlobalVariableGet(base + "X"));
   datetime lastProcessed = (datetime)((int)GlobalVariableGet(base + "LP"));
   bool latched = (GlobalVariableGet(base + "L") > 0.5);
   datetime exitCandle = (datetime)((int)GlobalVariableGet(base + "XL"));
   bool frozen = (GlobalVariableGet(base + "F") > 0.5);
   datetime openTime = (datetime)((int)GlobalVariableGet(base + "OT"));
   int magic = (int)GlobalVariableGet(base + "MG");

   if(direction != info.direction || magic != info.magic_number ||
      openTime != info.open_time || extremeCandle <= 0 ||
      lastProcessed < extremeCandle || (latched && exitCandle <= 0) ||
      (!latched && exitCandle != 0))
      return false;

   if(!GlobalVariableCheck(base + "CM") || !GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "CM") != committedGeneration ||
      GlobalVariableGet(base + "G") != committedGeneration)
      return false;

   int extremeShift = iBarShift(info.pair, PERIOD_D1, extremeCandle, true);
   int cursorShift = iBarShift(info.pair, PERIOD_D1, lastProcessed, true);
   if(extremeShift < 1 || cursorShift < 1 ||
      iTime(info.pair, PERIOD_D1, extremeShift) != extremeCandle ||
      iTime(info.pair, PERIOD_D1, cursorShift) != lastProcessed)
      return false;

   if(!GlobalVariableCheck(base + "CM") || !GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "CM") != committedGeneration ||
      GlobalVariableGet(base + "G") != committedGeneration)
      return false;

   ResetD1TPWTradeState(info);
   info.d1_tpw_lifecycle_managed = true;
   info.d1_tpw_extreme_candle = extremeCandle;
   info.d1_tpw_last_processed_d1_candle = lastProcessed;
   info.d1_tpw_exit_latched = latched;
   info.d1_tpw_exit_latched_candle = exitCandle;
   info.d1_tpw_frozen = frozen;
   return true;
}

bool InitializeD1TPWTradeStateFromDecision(TradeInfo &info, BBMA_Decision &decision)
{
   ResetD1TPWTradeState(info);
   if(!decision.D1TPWLifecycleManaged) return true;
   if(!EnableD1TPWLifecycle || !IsD1TPWLifecycleIdentity(decision) ||
      decision.D1OpportunitySourceCandleTime <= 0 ||
      decision.D1OpportunityDirection != decision.Direction)
      return false;

   int pairIndex = FindPairStateIndex(decision.Pair);
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   string pair = g_pair_states[pairIndex].actual_symbol;
   if(pair == "" || pair != decision.Pair) return false;

   int extremeShift = iBarShift(pair, PERIOD_D1,
                                decision.D1OpportunitySourceCandleTime, true);
   if(extremeShift < 1 ||
      iTime(pair, PERIOD_D1, extremeShift) != decision.D1OpportunitySourceCandleTime)
      return false;

   datetime latestClosed = GetLatestClosedCandleTime(pair, PERIOD_D1);
   if(latestClosed <= 0 || latestClosed < decision.D1OpportunitySourceCandleTime)
      return false;

   info.d1_tpw_lifecycle_managed = true;
   info.d1_tpw_extreme_candle = decision.D1OpportunitySourceCandleTime;
   // Position-management events start when the broker position exists; any
   // earlier D1 candles were already part of opportunity eligibility/provenance.
   info.d1_tpw_last_processed_d1_candle = latestClosed;
   info.d1_tpw_exit_latched = false;
   info.d1_tpw_exit_latched_candle = 0;
   info.d1_tpw_frozen = false;
   return true;
}

void ResetC044TradeState(TradeInfo &info)
{
   info.c044_lifecycle_managed = false;
   info.c044_owner_timeframe = 0;
   info.c044_owner_reentry_candle = 0;
   info.c044_epoch_anchor_candle = 0;
   info.c044_last_processed_owner_candle = 0;
   info.c044_state = C044_LIFE_NONE;
   info.c044_exit_reason = C044_EXIT_NONE;
   info.c044_exit_latched_candle = 0;
   info.c044_replay_seed_valid = false;
   info.c044_shadow_replay = false;
   ZeroMemory(info.c044_replay_reentry);
   ZeroMemory(info.c044_replay_extreme_buy);
   ZeroMemory(info.c044_replay_extreme_sell);
}

bool IsValidC044OwnerTimeframe(int timeframe)
{
   return (timeframe == PERIOD_H1 || timeframe == PERIOD_H4 ||
           timeframe == PERIOD_D1);
}

bool CaptureC044ReplaySeed(TradeInfo &info, int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(info.direction != DIR_BUY && info.direction != DIR_SELL) return false;
   if(!IsValidC044OwnerTimeframe(info.c044_owner_timeframe)) return false;

   if(!GetC044OwnerReEntrySnapshot(pairIndex, info.c044_owner_timeframe,
                                   info.direction, info.c044_replay_reentry))
      return false;
   if(!GetC044OwnerExtremeSnapshot(pairIndex, info.c044_owner_timeframe,
                                   DIR_BUY, info.c044_replay_extreme_buy))
      return false;
   if(!GetC044OwnerExtremeSnapshot(pairIndex, info.c044_owner_timeframe,
                                   DIR_SELL, info.c044_replay_extreme_sell))
      return false;

   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   info.c044_replay_seed_valid = true;
   return true;
}

bool InitializeC044TradeStateFromDecision(TradeInfo &info, BBMA_Decision &decision)
{
   ResetC044TradeState(info);
   if(!decision.C044LifecycleManaged) return true;
   if(!decision.HasSLTPSourceComponent ||
      decision.SLTPSourceComponent.ComponentType != SIGNAL_RE_ENTRY ||
      decision.SLTPSourceComponent.Direction != decision.Direction ||
      !IsValidC044OwnerTimeframe(decision.SLTPSourceComponent.Timeframe) ||
      decision.SLTPSourceComponent.CandleTime <= 0)
      return false;

   int pairIndex = FindPairStateIndex(decision.Pair);
   if(pairIndex < 0)
   {
      for(int i = 0; i < g_pair_count; i++)
      {
         if(g_pair_states[i].actual_symbol == decision.Pair)
         {
            pairIndex = i;
            break;
         }
      }
   }
   if(pairIndex < 0) return false;

   string ownerPair = g_pair_states[pairIndex].actual_symbol;
   if(ownerPair == "") return false;
   datetime latestClosed = GetLatestClosedCandleTime(
      ownerPair, decision.SLTPSourceComponent.Timeframe);
   if(latestClosed <= 0 || latestClosed < decision.SLTPSourceComponent.CandleTime)
      return false;

   info.c044_lifecycle_managed = true;
   info.c044_owner_timeframe = decision.SLTPSourceComponent.Timeframe;
   info.c044_owner_reentry_candle = decision.SLTPSourceComponent.CandleTime;
   info.c044_epoch_anchor_candle = decision.SLTPSourceComponent.CandleTime;

   // Runtime ownership starts when the broker position exists. Closed owner
   // candles between the source Re-Entry and actual order creation are provenance,
   // not lifecycle events for a position that did not yet exist.
   info.c044_last_processed_owner_candle = latestClosed;
   info.c044_state = C044_LIFE_MOMENTUM_PENDING;
   info.c044_exit_reason = C044_EXIT_NONE;
   info.c044_exit_latched_candle = 0;

   if(!CaptureC044ReplaySeed(info, pairIndex))
   {
      ResetC044TradeState(info);
      return false;
   }
   return true;
}

string C044CheckpointBase(TradeInfo &info)
{
   return "C044|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(info.ticket) + "|";
}

bool C044CheckpointExists(TradeInfo &info)
{
   if(info.ticket <= 0) return false;
   string base = C044CheckpointBase(info);
   if(!GlobalVariableCheck(base + "CM") || !GlobalVariableCheck(base + "G")) return false;
   double committed = GlobalVariableGet(base + "CM");
   double generation = GlobalVariableGet(base + "G");
   if(committed <= 0.0 || generation != committed) return false;
   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   return true;
}

string C044ReplayGVBase(TradeInfo &info)
{
   return C044CheckpointBase(info) + "R|";
}

string C044ReplayGVKey(string base, string group, int index)
{
   return base + group + IntegerToString(index);
}

bool C044DeleteGVExact(string key)
{
   return DeleteTerminalGlobalExact(key);
}

bool C044SetGVExact(string key, double value)
{
   return SetTerminalGlobalExact(key, value);
}

bool C044ReplayPayloadAbsent(string base)
{
   if(GlobalVariableCheck(base + "V") || GlobalVariableCheck(base + "G")) return false;
   for(int i = 0; i < 20; i++)
      if(GlobalVariableCheck(C044ReplayGVKey(base, "R", i))) return false;
   for(int j = 0; j < 19; j++)
   {
      if(GlobalVariableCheck(C044ReplayGVKey(base, "B", j))) return false;
      if(GlobalVariableCheck(C044ReplayGVKey(base, "S", j))) return false;
   }
   return true;
}

bool ClearC044ReplaySeedExact(TradeInfo &info)
{
   if(info.ticket <= 0) return false;
   string base = C044ReplayGVBase(info);
   if(!C044DeleteGVExact(base + "V")) return false;
   if(!C044DeleteGVExact(base + "G")) return false;
   for(int i = 0; i < 20; i++)
      if(!C044DeleteGVExact(C044ReplayGVKey(base, "R", i))) return false;
   for(int j = 0; j < 19; j++)
   {
      if(!C044DeleteGVExact(C044ReplayGVKey(base, "B", j))) return false;
      if(!C044DeleteGVExact(C044ReplayGVKey(base, "S", j))) return false;
   }
   GlobalVariablesFlush();
   return C044ReplayPayloadAbsent(base);
}

bool ClearC044GenerationPayloadExact(TradeInfo &info)
{
   if(info.ticket <= 0) return false;
   string base = C044CheckpointBase(info);
   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!C044DeleteGVExact(base + keys[i])) return false;
   if(!C044DeleteGVExact(base + "G")) return false;
   if(!ClearC044ReplaySeedExact(info)) return false;
   GlobalVariablesFlush();
   for(int j = 0; j < 10; j++)
      if(GlobalVariableCheck(base + keys[j])) return false;
   if(GlobalVariableCheck(base + "G")) return false;
   return true;
}

void ClearC044ReplaySeed(TradeInfo &info)
{
   ClearC044ReplaySeedExact(info);
}

bool SaveC044ReplaySeed(TradeInfo &info, double generation)
{
   if(!info.c044_replay_seed_valid || info.ticket <= 0 || generation <= 0.0) return false;
   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   string base = C044ReplayGVBase(info);
   if(!C044ReplayPayloadAbsent(base)) return false;
   if(!C044SetGVExact(base + "V", 2.0)) return false;

   if(!C044SetGVExact(C044ReplayGVKey(base,"R",0),  (double)info.c044_replay_reentry.Type)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",1),  (double)info.c044_replay_reentry.State)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",2),  (double)info.c044_replay_reentry.Direction)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",3),  (double)info.c044_replay_reentry.Timeframe)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",4),  (double)info.c044_replay_reentry.StartBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",5),  (double)info.c044_replay_reentry.StartCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",6),  (double)info.c044_replay_reentry.LastUpdateBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",7),  (double)info.c044_replay_reentry.LastUpdateCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",8),  (double)info.c044_replay_reentry.ConfirmationBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",9),  (double)info.c044_replay_reentry.ConfirmationCandle)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",10), (double)info.c044_replay_reentry.ExpiryBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",11), (double)info.c044_replay_reentry.ExpiryCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",12), (double)info.c044_replay_reentry.MinCandlesRequired)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",13), (double)info.c044_replay_reentry.QualifyingCandles)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",14), (double)info.c044_replay_reentry.Type1ContextState)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",15), (double)info.c044_replay_reentry.Type1OwnerSignal)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",16), (double)info.c044_replay_reentry.Type1OwnerCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",17), (double)info.c044_replay_reentry.Type1RangingStartCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",18), info.c044_replay_reentry.Type1PreviousClose)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"R",19), info.c044_replay_reentry.IsValid ? 1.0 : 0.0)) return false;

   ExtremeLifecycleData buy = info.c044_replay_extreme_buy;
   ExtremeLifecycleData sell = info.c044_replay_extreme_sell;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",0),  (double)buy.Maturity)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",1),  (double)buy.Direction)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",2),  (double)buy.Timeframe)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",3),  (double)buy.RawBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",4),  (double)buy.RawCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",5),  (double)buy.ConfirmationBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",6),  (double)buy.ConfirmationCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",7),  buy.ConfirmationClose)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",8),  (double)buy.LastUpdateBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",9),  (double)buy.LastUpdateCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",10), buy.PreviousClose)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",11), buy.ProvisionalBodyAnchor)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",12), buy.FrozenBodyAnchor)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",13), buy.RelevantMA5)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",14), (double)buy.RetestStartBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",15), (double)buy.RetestStartCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",16), (double)buy.RetestCompletionBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",17), (double)buy.RetestCompletionCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"B",18), buy.IsValid ? 1.0 : 0.0)) return false;

   if(!C044SetGVExact(C044ReplayGVKey(base,"S",0),  (double)sell.Maturity)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",1),  (double)sell.Direction)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",2),  (double)sell.Timeframe)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",3),  (double)sell.RawBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",4),  (double)sell.RawCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",5),  (double)sell.ConfirmationBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",6),  (double)sell.ConfirmationCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",7),  sell.ConfirmationClose)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",8),  (double)sell.LastUpdateBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",9),  (double)sell.LastUpdateCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",10), sell.PreviousClose)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",11), sell.ProvisionalBodyAnchor)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",12), sell.FrozenBodyAnchor)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",13), sell.RelevantMA5)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",14), (double)sell.RetestStartBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",15), (double)sell.RetestStartCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",16), (double)sell.RetestCompletionBar)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",17), (double)sell.RetestCompletionCandleTime)) return false;
   if(!C044SetGVExact(C044ReplayGVKey(base,"S",18), sell.IsValid ? 1.0 : 0.0)) return false;
   if(!C044SetGVExact(base + "G", generation)) return false;
   GlobalVariablesFlush();
   if(!GlobalVariableCheck(base + "V") || (int)GlobalVariableGet(base + "V") != 2) return false;
   if(!GlobalVariableCheck(base + "G") || GlobalVariableGet(base + "G") != generation) return false;
   return true;
}


bool ReadC044ReplayGV(string base, string group, int index, double &value)
{
   string key = C044ReplayGVKey(base, group, index);
   if(!GlobalVariableCheck(key)) return false;
   value = GlobalVariableGet(key);
   return true;
}

bool LoadC044ReplaySeed(TradeInfo &info, double expectedGeneration)
{
   if(expectedGeneration <= 0.0) return false;
   string base = C044ReplayGVBase(info);
   if(!GlobalVariableCheck(base + "V") ||
      (int)GlobalVariableGet(base + "V") != 2 ||
      !GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "G") != expectedGeneration)
      return false;

   ZeroMemory(info.c044_replay_reentry);
   ZeroMemory(info.c044_replay_extreme_buy);
   ZeroMemory(info.c044_replay_extreme_sell);
   double v = 0.0;

   if(!ReadC044ReplayGV(base,"R",0,v)) return false; info.c044_replay_reentry.Type=(ENUM_RE_TYPE)((int)v);
   if(!ReadC044ReplayGV(base,"R",1,v)) return false; info.c044_replay_reentry.State=(ENUM_RE_STATE)((int)v);
   if(!ReadC044ReplayGV(base,"R",2,v)) return false; info.c044_replay_reentry.Direction=(ENUM_DIRECTION)((int)v);
   if(!ReadC044ReplayGV(base,"R",3,v)) return false; info.c044_replay_reentry.Timeframe=(int)v;
   if(!ReadC044ReplayGV(base,"R",4,v)) return false; info.c044_replay_reentry.StartBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",5,v)) return false; info.c044_replay_reentry.StartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",6,v)) return false; info.c044_replay_reentry.LastUpdateBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",7,v)) return false; info.c044_replay_reentry.LastUpdateCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",8,v)) return false; info.c044_replay_reentry.ConfirmationBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",9,v)) return false; info.c044_replay_reentry.ConfirmationCandle=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",10,v)) return false; info.c044_replay_reentry.ExpiryBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",11,v)) return false; info.c044_replay_reentry.ExpiryCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",12,v)) return false; info.c044_replay_reentry.MinCandlesRequired=(int)v;
   if(!ReadC044ReplayGV(base,"R",13,v)) return false; info.c044_replay_reentry.QualifyingCandles=(int)v;
   if(!ReadC044ReplayGV(base,"R",14,v)) return false; info.c044_replay_reentry.Type1ContextState=(ENUM_TYPE1_CONTEXT_STATE)((int)v);
   if(!ReadC044ReplayGV(base,"R",15,v)) return false; info.c044_replay_reentry.Type1OwnerSignal=(ENUM_SIGNAL_TYPE)((int)v);
   if(!ReadC044ReplayGV(base,"R",16,v)) return false; info.c044_replay_reentry.Type1OwnerCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",17,v)) return false; info.c044_replay_reentry.Type1RangingStartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",18,v)) return false; info.c044_replay_reentry.Type1PreviousClose=v;
   if(!ReadC044ReplayGV(base,"R",19,v)) return false; info.c044_replay_reentry.IsValid=(v > 0.5);

   if(!ReadC044ReplayGV(base,"B",0,v)) return false; info.c044_replay_extreme_buy.Maturity=(ENUM_EXTREME_MATURITY)((int)v);
   if(!ReadC044ReplayGV(base,"B",1,v)) return false; info.c044_replay_extreme_buy.Direction=(ENUM_DIRECTION)((int)v);
   if(!ReadC044ReplayGV(base,"B",2,v)) return false; info.c044_replay_extreme_buy.Timeframe=(int)v;
   if(!ReadC044ReplayGV(base,"B",3,v)) return false; info.c044_replay_extreme_buy.RawBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",4,v)) return false; info.c044_replay_extreme_buy.RawCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",5,v)) return false; info.c044_replay_extreme_buy.ConfirmationBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",6,v)) return false; info.c044_replay_extreme_buy.ConfirmationCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",7,v)) return false; info.c044_replay_extreme_buy.ConfirmationClose=v;
   if(!ReadC044ReplayGV(base,"B",8,v)) return false; info.c044_replay_extreme_buy.LastUpdateBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",9,v)) return false; info.c044_replay_extreme_buy.LastUpdateCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",10,v)) return false; info.c044_replay_extreme_buy.PreviousClose=v;
   if(!ReadC044ReplayGV(base,"B",11,v)) return false; info.c044_replay_extreme_buy.ProvisionalBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"B",12,v)) return false; info.c044_replay_extreme_buy.FrozenBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"B",13,v)) return false; info.c044_replay_extreme_buy.RelevantMA5=v;
   if(!ReadC044ReplayGV(base,"B",14,v)) return false; info.c044_replay_extreme_buy.RetestStartBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",15,v)) return false; info.c044_replay_extreme_buy.RetestStartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",16,v)) return false; info.c044_replay_extreme_buy.RetestCompletionBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",17,v)) return false; info.c044_replay_extreme_buy.RetestCompletionCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",18,v)) return false; info.c044_replay_extreme_buy.IsValid=(v > 0.5);

   if(!ReadC044ReplayGV(base,"S",0,v)) return false; info.c044_replay_extreme_sell.Maturity=(ENUM_EXTREME_MATURITY)((int)v);
   if(!ReadC044ReplayGV(base,"S",1,v)) return false; info.c044_replay_extreme_sell.Direction=(ENUM_DIRECTION)((int)v);
   if(!ReadC044ReplayGV(base,"S",2,v)) return false; info.c044_replay_extreme_sell.Timeframe=(int)v;
   if(!ReadC044ReplayGV(base,"S",3,v)) return false; info.c044_replay_extreme_sell.RawBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",4,v)) return false; info.c044_replay_extreme_sell.RawCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",5,v)) return false; info.c044_replay_extreme_sell.ConfirmationBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",6,v)) return false; info.c044_replay_extreme_sell.ConfirmationCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",7,v)) return false; info.c044_replay_extreme_sell.ConfirmationClose=v;
   if(!ReadC044ReplayGV(base,"S",8,v)) return false; info.c044_replay_extreme_sell.LastUpdateBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",9,v)) return false; info.c044_replay_extreme_sell.LastUpdateCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",10,v)) return false; info.c044_replay_extreme_sell.PreviousClose=v;
   if(!ReadC044ReplayGV(base,"S",11,v)) return false; info.c044_replay_extreme_sell.ProvisionalBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"S",12,v)) return false; info.c044_replay_extreme_sell.FrozenBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"S",13,v)) return false; info.c044_replay_extreme_sell.RelevantMA5=v;
   if(!ReadC044ReplayGV(base,"S",14,v)) return false; info.c044_replay_extreme_sell.RetestStartBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",15,v)) return false; info.c044_replay_extreme_sell.RetestStartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",16,v)) return false; info.c044_replay_extreme_sell.RetestCompletionBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",17,v)) return false; info.c044_replay_extreme_sell.RetestCompletionCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",18,v)) return false; info.c044_replay_extreme_sell.IsValid=(v > 0.5);

   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   if(!GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "G") != expectedGeneration)
      return false;
   info.c044_replay_seed_valid = true;
   return true;
}

void ClearC044Checkpoint(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = C044CheckpointBase(info);
   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(GlobalVariableCheck(base + keys[i])) GlobalVariableDel(base + keys[i]);
   if(GlobalVariableCheck(base + "G")) GlobalVariableDel(base + "G");
   if(GlobalVariableCheck(base + "GN")) GlobalVariableDel(base + "GN");
   if(GlobalVariableCheck(base + "CM")) GlobalVariableDel(base + "CM");
   ClearC044ReplaySeed(info);
   GlobalVariablesFlush();
}

bool SaveC044Checkpoint(TradeInfo &info)
{
   // Tester-only counterfactual replay reuses the canonical C044 state machine
   // without writing terminal globals or requiring a broker ticket.
   if(info.c044_shadow_replay) return true;
   if(!info.c044_lifecycle_managed || info.ticket <= 0 ||
      info.magic_number <= 0 || info.open_time <= 0 ||
      (info.direction != DIR_BUY && info.direction != DIR_SELL) ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe) ||
      info.c044_owner_reentry_candle <= 0 || info.c044_epoch_anchor_candle <= 0 ||
      info.c044_last_processed_owner_candle <= 0 ||
      info.c044_state == C044_LIFE_NONE)
      return false;

   string base = C044CheckpointBase(info);
   if(!C044DeleteGVExact(base + "CM")) return false;
   GlobalVariablesFlush();
   if(GlobalVariableCheck(base + "CM")) return false;
   if(!ClearC044GenerationPayloadExact(info)) return false;

   double priorGeneration = GlobalVariableCheck(base + "GN") ? GlobalVariableGet(base + "GN") : 0.0;
   if(priorGeneration < 0.0 || priorGeneration > 9000000000000000.0) priorGeneration = 0.0;
   double generation = MathFloor(priorGeneration) + 1.0;
   if(!C044SetGVExact(base + "GN", generation)) return false;
   if(!GlobalVariableCheck(base + "GN") || GlobalVariableGet(base + "GN") != generation) return false;

   if(info.c044_state != C044_LIFE_FROZEN &&
      (!info.c044_replay_seed_valid || !SaveC044ReplaySeed(info, generation)))
      return false;
   if(!C044SetGVExact(base + "D",  (double)info.direction)) return false;
   if(!C044SetGVExact(base + "TF", (double)info.c044_owner_timeframe)) return false;
   if(!C044SetGVExact(base + "OR", (double)info.c044_owner_reentry_candle)) return false;
   if(!C044SetGVExact(base + "EP", (double)info.c044_epoch_anchor_candle)) return false;
   if(!C044SetGVExact(base + "LP", (double)info.c044_last_processed_owner_candle)) return false;
   if(!C044SetGVExact(base + "ST", (double)info.c044_state)) return false;
   if(!C044SetGVExact(base + "XR", (double)info.c044_exit_reason)) return false;
   if(!C044SetGVExact(base + "XL", (double)info.c044_exit_latched_candle)) return false;
   if(!C044SetGVExact(base + "OT", (double)info.open_time)) return false;
   if(!C044SetGVExact(base + "MG", (double)info.magic_number)) return false;
   if(!C044SetGVExact(base + "G", generation)) return false;
   GlobalVariablesFlush();

   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   if(!GlobalVariableCheck(base + "G") || GlobalVariableGet(base + "G") != generation) return false;
   if(info.c044_state != C044_LIFE_FROZEN)
   {
      string replayBase = C044ReplayGVBase(info);
      if(!GlobalVariableCheck(replayBase + "V") || (int)GlobalVariableGet(replayBase + "V") != 2 ||
         !GlobalVariableCheck(replayBase + "G") || GlobalVariableGet(replayBase + "G") != generation)
         return false;
   }

   if(!C044SetGVExact(base + "CM", generation)) return false;
   GlobalVariablesFlush();
   return (GlobalVariableCheck(base + "CM") &&
           GlobalVariableGet(base + "CM") == generation &&
           GlobalVariableGet(base + "G") == generation);
}


bool LoadC044Checkpoint(TradeInfo &info)
{
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0) return false;
   if(!C044CheckpointExists(info)) return false;
   string base = C044CheckpointBase(info);
   double committedGeneration = GlobalVariableGet(base + "CM");
   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;

   ENUM_DIRECTION direction = (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   int timeframe = (int)GlobalVariableGet(base + "TF");
   datetime ownerRe = (datetime)((int)GlobalVariableGet(base + "OR"));
   datetime epoch = (datetime)((int)GlobalVariableGet(base + "EP"));
   datetime lastProcessed = (datetime)((int)GlobalVariableGet(base + "LP"));
   ENUM_C044_LIFECYCLE_STATE state =
      (ENUM_C044_LIFECYCLE_STATE)((int)GlobalVariableGet(base + "ST"));
   ENUM_C044_EXIT_REASON exitReason =
      (ENUM_C044_EXIT_REASON)((int)GlobalVariableGet(base + "XR"));
   datetime exitCandle = (datetime)((int)GlobalVariableGet(base + "XL"));
   datetime openTime = (datetime)((int)GlobalVariableGet(base + "OT"));
   int magic = (int)GlobalVariableGet(base + "MG");

   if(direction != info.direction || magic != info.magic_number || openTime != info.open_time)
      return false;
   if(!IsValidC044OwnerTimeframe(timeframe) || ownerRe <= 0 || epoch <= 0 ||
      lastProcessed <= 0)
      return false;
   if(state != C044_LIFE_MOMENTUM_PENDING &&
      state != C044_LIFE_WAIT_NEXT_REENTRY &&
      state != C044_LIFE_EXIT_LATCHED && state != C044_LIFE_FROZEN)
      return false;
   if(state == C044_LIFE_EXIT_LATCHED &&
      (exitReason == C044_EXIT_NONE || exitCandle <= 0 ||
       exitCandle > lastProcessed))
      return false;
   if(state != C044_LIFE_EXIT_LATCHED &&
      (exitReason != C044_EXIT_NONE || exitCandle != 0))
      return false;

   if(!GlobalVariableCheck(base + "CM") || !GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "CM") != committedGeneration ||
      GlobalVariableGet(base + "G") != committedGeneration)
      return false;

   info.c044_lifecycle_managed = true;
   info.c044_owner_timeframe = timeframe;
   info.c044_owner_reentry_candle = ownerRe;
   info.c044_epoch_anchor_candle = epoch;
   info.c044_last_processed_owner_candle = lastProcessed;
   info.c044_state = state;
   info.c044_exit_reason = exitReason;
   info.c044_exit_latched_candle = exitCandle;

   if(state == C044_LIFE_FROZEN)
   {
      info.c044_replay_seed_valid = false;
      return true;
   }
   if(!LoadC044ReplaySeed(info, committedGeneration))
   {
      ResetC044TradeState(info);
      return false;
   }
   if(!GlobalVariableCheck(base + "CM") || !GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "CM") != committedGeneration ||
      GlobalVariableGet(base + "G") != committedGeneration)
   {
      ResetC044TradeState(info);
      return false;
   }
   return true;
}

string H4OwnerGVBase(PairState &state)
{
   return "F4H4|" + IntegerToString(StrategyID) + "|" +
          IntegerToString(InstanceID) + "|" + state.base_symbol + "|";
}

void ResetH4DirectionalOwner(H4DirectionalOwner &owner,
                             ENUM_H4_OWNER_STATE state)
{
   ZeroMemory(owner);
   owner.State = state;
   owner.Direction = DIR_NONE;
   owner.SourceSignal = SIGNAL_NONE;
   owner.LastAdvanceSignal = SIGNAL_NONE;
   owner.IsValid = false;
   owner.RecoveryComplete = (state != H4_OWNER_RECOVERY_UNRESOLVED);
   owner.RecoveredFromCheckpoint = false;
}

void ClearH4OwnerCheckpoint(PairState &state)
{
   string base = H4OwnerGVBase(state);
   if(GlobalVariableCheck(base + "D")) GlobalVariableDel(base + "D");
   if(GlobalVariableCheck(base + "S")) GlobalVariableDel(base + "S");
   if(GlobalVariableCheck(base + "T")) GlobalVariableDel(base + "T");
}

void SaveH4OwnerCheckpoint(PairState &state)
{
   if(state.h4_direction_owner.State != H4_OWNER_ACTIVE ||
      !state.h4_direction_owner.IsValid ||
      (state.h4_direction_owner.Direction != DIR_BUY &&
       state.h4_direction_owner.Direction != DIR_SELL) ||
      state.h4_direction_owner.SourceCandleTime <= 0 ||
      (state.h4_direction_owner.SourceSignal != SIGNAL_ECSD &&
       state.h4_direction_owner.SourceSignal != SIGNAL_CSD &&
       state.h4_direction_owner.SourceSignal != SIGNAL_CSM))
   {
      ClearH4OwnerCheckpoint(state);
      return;
   }

   string base = H4OwnerGVBase(state);
   GlobalVariableSet(base + "D", (double)state.h4_direction_owner.Direction);
   GlobalVariableSet(base + "S", (double)state.h4_direction_owner.SourceSignal);
   GlobalVariableSet(base + "T", (double)state.h4_direction_owner.SourceCandleTime);
   GlobalVariablesFlush();
}

ENUM_SIGNAL_TYPE ClassifyH4AuthoritativeSignal(string pair,
                                                ENUM_DIRECTION direction,
                                                TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return SIGNAL_NONE;
   if(!data.is_valid || !data.is_closed || data.timeframe != PERIOD_H4 ||
      data.barIndex < 1 || data.candle_time <= 0)
      return SIGNAL_NONE;

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);

   // One canonical same-candle classification: Momentum > CSD > eCSD.
   if(DetectCSM(pair, PERIOD_H4, direction, data.barIndex))
      return SIGNAL_CSM;
   if(DetectCSD(pair, PERIOD_H4, direction, data.barIndex, ma, band))
      return SIGNAL_CSD;
   if(DetectECSD(pair, PERIOD_H4, direction, data.barIndex, ma))
      return SIGNAL_ECSD;
   return SIGNAL_NONE;
}

void ApplyH4AuthoritativeEvent(PairState &state,
                               ENUM_DIRECTION direction,
                               ENUM_SIGNAL_TYPE signalType,
                               datetime candleTime,
                               bool recovered)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return;
   if(signalType != SIGNAL_ECSD && signalType != SIGNAL_CSD &&
      signalType != SIGNAL_CSM) return;
   if(candleTime <= 0) return;

   bool handover = (state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
                    state.h4_direction_owner.IsValid &&
                    state.h4_direction_owner.Direction != DIR_NONE &&
                    state.h4_direction_owner.Direction != direction);

   state.h4_direction_owner.State = H4_OWNER_ACTIVE;
   state.h4_direction_owner.Direction = direction;
   state.h4_direction_owner.SourceSignal = signalType;
   state.h4_direction_owner.SourceCandleTime = candleTime;
   state.h4_direction_owner.LastAdvanceSignal = signalType;
   state.h4_direction_owner.LastAdvanceCandleTime = candleTime;
   state.h4_direction_owner.IsValid = true;
   state.h4_direction_owner.RecoveryComplete = true;
   state.h4_direction_owner.RecoveredFromCheckpoint = recovered;
   state.h4_direction_owner.Reason = handover
      ? "Atomic H4 owner handover by opposite source-valid direction/momentum"
      : "H4 authoritative directional owner established/advanced";
}

bool VerifyH4OwnerCheckpoint(PairState &state,
                             ENUM_DIRECTION direction,
                             ENUM_SIGNAL_TYPE signalType,
                             datetime candleTime)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return false;
   if(signalType != SIGNAL_ECSD && signalType != SIGNAL_CSD &&
      signalType != SIGNAL_CSM) return false;
   if(candleTime <= 0 || state.actual_symbol == "") return false;

   int shift = iBarShift(state.actual_symbol, PERIOD_H4, candleTime, true);
   if(shift < 1) return false; // checkpoint must reference a CLOSED H4 candle.

   TimeframeData data;
   InitTimeframeData(data);
   GetDataForTimeframe(state.actual_symbol, PERIOD_H4, candleTime, data);
   if(!data.is_valid || !data.is_closed) return false;

   ENUM_SIGNAL_TYPE verified =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, direction, data);
   return (verified == signalType);
}

bool LoadVerifiedH4OwnerCheckpoint(PairState &state)
{
   string base = H4OwnerGVBase(state);
   if(!GlobalVariableCheck(base + "D") ||
      !GlobalVariableCheck(base + "S") ||
      !GlobalVariableCheck(base + "T"))
      return false;

   ENUM_DIRECTION direction =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   ENUM_SIGNAL_TYPE signalType =
      (ENUM_SIGNAL_TYPE)((int)GlobalVariableGet(base + "S"));
   datetime candleTime = (datetime)((int)GlobalVariableGet(base + "T"));

   if(!VerifyH4OwnerCheckpoint(state, direction, signalType, candleTime))
   {
      ClearH4OwnerCheckpoint(state);
      return false;
   }

   ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_ACTIVE);
   ApplyH4AuthoritativeEvent(state, direction, signalType, candleTime, true);
   state.h4_direction_owner.RecoveredFromCheckpoint = true;
   return true;
}

void ApplyH4ReplayCandle(PairState &state, TimeframeData &data)
{
   ENUM_SIGNAL_TYPE buySignal =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, DIR_BUY, data);
   ENUM_SIGNAL_TYPE sellSignal =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, DIR_SELL, data);

   // Simultaneous opposite authoritative classifications are fail-closed.
   if(buySignal != SIGNAL_NONE && sellSignal != SIGNAL_NONE)
   {
      ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_NONE);
      state.h4_direction_owner.LastProcessedH4CandleTime = data.candle_time;
      state.h4_direction_owner.Reason =
         "Ambiguous simultaneous H4 BUY/SELL authoritative events -> NO_OWNER";
      ClearH4OwnerCheckpoint(state);
      return;
   }

   if(buySignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(state, DIR_BUY, buySignal, data.candle_time, true);
   else if(sellSignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(state, DIR_SELL, sellSignal, data.candle_time, true);
   // Neutral H4 candle intentionally preserves inherited owner.

   state.h4_direction_owner.LastProcessedH4CandleTime = data.candle_time;
}

void RecoverH4DirectionalOwnerForPair(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                           H4_OWNER_RECOVERY_UNRESOLVED);

   if(!g_pair_states[pairIndex].pair_enabled ||
      g_pair_states[pairIndex].actual_symbol == "")
   {
      ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                              H4_OWNER_NONE);
      g_pair_states[pairIndex].h4_direction_owner.Reason =
         "H4 recovery unavailable for disabled/unresolved pair";
      return;
   }

   bool checkpointValid = LoadVerifiedH4OwnerCheckpoint(g_pair_states[pairIndex]);
   int bars = iBars(g_pair_states[pairIndex].actual_symbol, PERIOD_H4);
   if(bars < 3)
   {
      if(!checkpointValid)
      {
         ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                                 H4_OWNER_NONE);
         g_pair_states[pairIndex].h4_direction_owner.Reason =
            "Insufficient closed H4 history -> NO_OWNER";
      }
      g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete = true;
      return;
   }

   int startShift = bars - 2;
   if(checkpointValid)
   {
      int checkpointShift = iBarShift(
         g_pair_states[pairIndex].actual_symbol, PERIOD_H4,
         g_pair_states[pairIndex].h4_direction_owner.SourceCandleTime, true);
      if(checkpointShift >= 1)
         startShift = checkpointShift - 1;
      else
      {
         ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                                 H4_OWNER_NONE);
         checkpointValid = false;
         startShift = bars - 2;
      }
   }

   for(int shift = startShift; shift >= 1; shift--)
   {
      datetime candleTime =
         iTime(g_pair_states[pairIndex].actual_symbol, PERIOD_H4, shift);
      if(candleTime <= 0) continue;

      TimeframeData data;
      InitTimeframeData(data);
      GetDataForTimeframe(g_pair_states[pairIndex].actual_symbol,
                          PERIOD_H4, candleTime, data);
      if(!data.is_valid || !data.is_closed) continue;

      ApplyH4ReplayCandle(g_pair_states[pairIndex], data);
   }

   g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete = true;
   if(g_pair_states[pairIndex].h4_direction_owner.State != H4_OWNER_ACTIVE ||
      !g_pair_states[pairIndex].h4_direction_owner.IsValid)
   {
      g_pair_states[pairIndex].h4_direction_owner.State = H4_OWNER_NONE;
      g_pair_states[pairIndex].h4_direction_owner.Direction = DIR_NONE;
      g_pair_states[pairIndex].h4_direction_owner.IsValid = false;
      g_pair_states[pairIndex].h4_direction_owner.Reason =
         "Closed-H4 replay could not prove authoritative owner -> NO_OWNER";
      ClearH4OwnerCheckpoint(g_pair_states[pairIndex]);
      return;
   }

   SaveH4OwnerCheckpoint(g_pair_states[pairIndex]);
}

void RecoverH4DirectionalOwners()
{
   for(int i = 0; i < g_pair_count; i++)
      RecoverH4DirectionalOwnerForPair(i);
}

void UpdateRuntimeH4DirectionalOwner(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   if(!g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete) return;
   if(!g_pair_states[pairIndex].h4_data.is_valid ||
      !g_pair_states[pairIndex].h4_data.is_closed ||
      g_pair_states[pairIndex].h4_data.timeframe != PERIOD_H4 ||
      g_pair_states[pairIndex].h4_data.candle_time <= 0)
      return;
   if(g_pair_states[pairIndex].h4_data.candle_time ==
      g_pair_states[pairIndex].h4_direction_owner.LastProcessedH4CandleTime)
      return;

   ENUM_SIGNAL_TYPE buySignal = ClassifyH4AuthoritativeSignal(
      g_pair_states[pairIndex].actual_symbol, DIR_BUY,
      g_pair_states[pairIndex].h4_data);
   ENUM_SIGNAL_TYPE sellSignal = ClassifyH4AuthoritativeSignal(
      g_pair_states[pairIndex].actual_symbol, DIR_SELL,
      g_pair_states[pairIndex].h4_data);

   if(buySignal != SIGNAL_NONE && sellSignal != SIGNAL_NONE)
   {
      ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                              H4_OWNER_NONE);
      g_pair_states[pairIndex].h4_direction_owner.LastProcessedH4CandleTime =
         g_pair_states[pairIndex].h4_data.candle_time;
      g_pair_states[pairIndex].h4_direction_owner.Reason =
         "Ambiguous simultaneous H4 BUY/SELL authoritative events -> NO_OWNER";
      ClearH4OwnerCheckpoint(g_pair_states[pairIndex]);
      return;
   }

   if(buySignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(g_pair_states[pairIndex], DIR_BUY, buySignal,
                                g_pair_states[pairIndex].h4_data.candle_time, false);
   else if(sellSignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(g_pair_states[pairIndex], DIR_SELL, sellSignal,
                                g_pair_states[pairIndex].h4_data.candle_time, false);

   g_pair_states[pairIndex].h4_direction_owner.LastProcessedH4CandleTime =
      g_pair_states[pairIndex].h4_data.candle_time;
   if(g_pair_states[pairIndex].h4_direction_owner.State == H4_OWNER_ACTIVE &&
      g_pair_states[pairIndex].h4_direction_owner.IsValid)
      SaveH4OwnerCheckpoint(g_pair_states[pairIndex]);
}

void NoteH4ReEntryInheritance(int pairIndex, ReEntryData &reEntry)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   if(!g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete ||
      !g_pair_states[pairIndex].h4_direction_owner.IsValid ||
      g_pair_states[pairIndex].h4_direction_owner.State != H4_OWNER_ACTIVE ||
      reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid ||
      reEntry.Timeframe != PERIOD_H4 ||
      reEntry.Direction != g_pair_states[pairIndex].h4_direction_owner.Direction ||
      reEntry.ConfirmationCandle <= 0)
      return;

   g_pair_states[pairIndex].h4_direction_owner.LastAdvanceSignal = SIGNAL_RE_ENTRY;
   g_pair_states[pairIndex].h4_direction_owner.LastAdvanceCandleTime =
      reEntry.ConfirmationCandle;
   g_pair_states[pairIndex].h4_direction_owner.Reason =
      "Same-direction H4 Re-Entry inherited existing directional owner";
}

void RecoverExistingOrders()
{
   int total = OrdersTotal();
   
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
         continue;
      if(OrderCloseTime() != 0)
         continue;
      
      int pairIdx = -1;
      if(!IsExactEAOwnedSelectedOrder(pairIdx)) continue;

      int magic = OrderMagicNumber();
      string pair = OrderSymbol();
      string comment = OrderComment();
      ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;

      string executionHash = "";
      bool localIdentity = LoadPersistedExecutionHashForTicket(
         OrderTicket(), pair, liveDirection, magic, OrderOpenTime(), executionHash);
      string brokerExecutionHash = "";
      bool brokerHashFound = ExtractExecutionHash(comment, brokerExecutionHash);
      if(!localIdentity && brokerHashFound)
      {
         executionHash = brokerExecutionHash;
         localIdentity = SaveExecutionIdentityHash(executionHash, OrderTicket(), pair,
                                                   liveDirection, magic, OrderOpenTime());
      }
      bool hasExecutionHash = (executionHash != "");
      string decisionHash, parsedPair, sequenceHash;
      ENUM_DIRECTION parsedDirection = DIR_NONE;
      ENUM_SIGNAL_TYPE signalType = SIGNAL_NONE;
      double intendedEntry, intendedSL, intendedLot, intendedRisk;
      datetime candleTime = 0;

      bool fullMetadata = brokerHashFound &&
                          ParseOrderCommentFull(comment, decisionHash, parsedPair,
                                                parsedDirection, signalType,
                                                intendedEntry, intendedSL,
                                                intendedLot, intendedRisk,
                                                sequenceHash, candleTime);

      if(fullMetadata &&
         (decisionHash != brokerExecutionHash || parsedPair != pair ||
          parsedDirection != liveDirection))
      {
         Log(DBG_ERROR, "Recovery metadata mismatch ticket=" + IntegerToString(OrderTicket()));
         fullMetadata = false;
         signalType = SIGNAL_NONE;
         sequenceHash = "";
      }

      TradeInfo info;
      info.ticket = OrderTicket();
      info.magic_number = magic;
      info.pair = pair;
      info.direction = liveDirection;
      info.signal_type = signalType;
      info.initial_entry_price = OrderOpenPrice();
      info.initial_stop_loss = OrderStopLoss();
      info.initial_take_profit = OrderTakeProfit();
      info.initial_lot = OrderLots();
      info.initial_risk_price_distance = MathAbs(info.initial_entry_price - info.initial_stop_loss);
      info.entry_price = info.initial_entry_price;
      info.current_sl = info.initial_stop_loss;
      info.current_tp = info.initial_take_profit;
      info.lot = OrderLots();
      info.remaining_lot = OrderLots();
      info.partial_closed = false;
      info.partial_available = false;
      info.partial_attempted = false;
      info.breakeven_set = false;
      info.be_attempted = false;
      info.be_last_attempt_time = 0;
      info.partial_last_attempt_time = 0;
      info.open_time = OrderOpenTime();
      info.point = GetPointSize(pair);
      info.digits = GetDigits(pair);
      info.stop_level = GetStopLevel(pair);
      info.freeze_level = GetFreezeLevel(pair);
      info.decision_id = "";
      info.execution_hash = executionHash;
      info.sequence_hash_short = sequenceHash;

      ResetC044TradeState(info);
      ResetD1TPWTradeState(info);
      bool targetless = (info.initial_take_profit == 0.0);
      bool c044Checkpoint = targetless && C044CheckpointExists(info);
      bool d1TPWCheckpoint = targetless && D1TPWCheckpointExists(info);
      bool checkpointAmbiguous = (c044Checkpoint && d1TPWCheckpoint);
      bool targetlessRecovered = false;
      if(targetless && !checkpointAmbiguous)
      {
         if(d1TPWCheckpoint)
            targetlessRecovered = LoadD1TPWCheckpoint(info);
         else if(c044Checkpoint)
            targetlessRecovered = LoadC044Checkpoint(info);
      }

      bool geometryValid = (info.initial_entry_price > 0 &&
                            info.initial_stop_loss > 0);
      if(geometryValid && liveDirection == DIR_BUY)
         geometryValid = (info.initial_stop_loss < info.initial_entry_price &&
                          (targetless ? targetlessRecovered
                                      : info.initial_entry_price < info.initial_take_profit));
      else if(geometryValid && liveDirection == DIR_SELL)
         geometryValid = (info.initial_stop_loss > info.initial_entry_price &&
                          (targetless ? targetlessRecovered
                                      : info.initial_take_profit < info.initial_entry_price));

      string recoveryCause = "";
      double currentLot = OrderLots();
      if(targetless && checkpointAmbiguous)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_CHECKPOINT_AMBIGUOUS";
      }
      else if(targetless && targetlessRecovered && info.d1_tpw_lifecycle_managed &&
              info.d1_tpw_frozen)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "D1TPW_CHECKPOINT_FROZEN";
      }
      else if(targetless && targetlessRecovered && info.c044_lifecycle_managed &&
              info.c044_state == C044_LIFE_FROZEN)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "C044_CHECKPOINT_FROZEN";
      }
      else if(targetless && !targetlessRecovered)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_CHECKPOINT_MISSING_OR_INVALID";
      }
      else if(targetless && !hasExecutionHash)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_DURABLE_IDENTITY_REQUIRED";
      }
      else if(!geometryValid)
      {
         info.recovery_state = REC_RECOVERY_INVALID;
         recoveryCause = "INVALID_GEOMETRY";
      }
      else if(currentLot <= 0)
      {
         info.recovery_state = REC_RECOVERY_INVALID;
         recoveryCause = "NONPOSITIVE_LIVE_LOT";
      }
      else if(!IsValidLotStep(currentLot, pair))
      {
         info.recovery_state = REC_RECOVERY_INVALID;
         recoveryCause = "INVALID_LIVE_LOT_STEP";
      }
      else if(targetless && targetlessRecovered && hasExecutionHash && !fullMetadata)
      {
         info.recovery_state = REC_NORMAL;
         recoveryCause = "TARGETLESS_CHECKPOINT_IDENTITY_MATCH";
      }
      else if(fullMetadata && intendedLot > 0 && currentLot > intendedLot + 0.0000001)
      {
         info.recovery_state = REC_CORRUPTED;
         recoveryCause = "LIVE_LOT_ABOVE_INTENDED";
      }
      else if(fullMetadata && intendedLot > 0 && currentLot < intendedLot - 0.0000001)
      {
         info.recovery_state = REC_PARTIAL_INFERRED;
         info.remaining_lot = currentLot;
         recoveryCause = "LIVE_LOT_BELOW_INTENDED";
      }
      else if(fullMetadata)
      {
         info.recovery_state = REC_NORMAL;
         recoveryCause = "FULL_METADATA_MATCH";
      }
      else if(hasExecutionHash)
      {
         info.recovery_state = REC_IDENTITY_HASH_ONLY;
         recoveryCause = "EXECUTION_HASH_ONLY";
      }
      else
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "MISSING_EXECUTION_HASH";
      }

      info.partial_closed = false;
      info.partial_available = false;
      info.partial_attempted = false;
      info.breakeven_set = false;
      info.be_attempted = false;

      // Q9 P4 recovery is optional research metadata only.
      if(hasExecutionHash) LoadNMJEShadowAttribution(info);
      info.entry_displacement = info.nmje_attribution.EntryDisplacement;

      AddToMonitoredTrades(info);

      if(targetlessRecovered && info.c044_lifecycle_managed)
      {
         string recoveryEvent = (info.recovery_state == REC_NORMAL ||
                                 info.recovery_state == REC_PARTIAL_INFERRED)
            ? "RECOVERY_RESTORED" : "RECOVERY_BLOCKED";
         F7Telemetry(recoveryEvent, info,
                     "RecoveryState="+EnumToString(info.recovery_state)+
                     " Cause="+recoveryCause+
                     " PersistedCheckpoint=Y");
      }

      Print("[P3S5][RECOVERY] Ticket=", IntegerToString(info.ticket),
            " Pair=", pair,
            " State=", EnumToString(info.recovery_state),
            " Cause=", recoveryCause,
            " HashFound=", hasExecutionHash ? "Y" : "N",
            " FullMeta=", fullMetadata ? "Y" : "N");

      if(hasExecutionHash)
         UpsertExecutionHashTombstone(executionHash, info.ticket, pair,
                                      liveDirection, info.open_time);
   }
}

//+------------------------------------------------------------------+
//| MODULE 25: DASHBOARD ENGINE                                      |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

int CountDashboardLiveEAOwnedTrades()
{
   int count = 0;
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;

      int pairIdx = -1;
      if(IsExactEAOwnedSelectedOrder(pairIdx))
         count++;
   }
   return count;
}

void BuildDashboardSnapshot()
{
   // P2-DASHCOUNT-01: broker live-order pool + exact symbol/magic ownership is
   // the display source of truth. No registry compaction or lifecycle mutation.
   int liveTradeCount = CountDashboardLiveEAOwnedTrades();

   g_dashboard_snapshot = "";
   g_dashboard_snapshot += "=== BBMA EA " + string(BBMA_BUILD_TAG) + " ===\n";
   g_dashboard_snapshot += "Time: " + TimeToString(TimeCurrent()) + "\n";
   g_dashboard_snapshot += "Balance: " + DoubleToString(AccountBalance(), 2) + "\n";
   g_dashboard_snapshot += "Equity: " + DoubleToString(AccountEquity(), 2) + "\n";
   g_dashboard_snapshot += "Trades: " + IntegerToString(liveTradeCount) + "\n";
   g_dashboard_snapshot += "Protection Ref: " + DoubleToString(g_protection_reference_equity, 2) + "\n";
   
   g_dashboard_snapshot += "\n--- SIGNALS ---\n";
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      g_dashboard_snapshot += g_pair_states[i].actual_symbol + ": ";
      if(g_pair_states[i].last_decision.Valid)
      {
         g_dashboard_snapshot += EnumToString(g_pair_states[i].last_decision.SignalType) + " ";
         g_dashboard_snapshot += EnumToString(g_pair_states[i].last_decision.Direction) + " ";
         g_dashboard_snapshot += "State:" + EnumToString(g_pair_states[i].last_decision.DecisionState);
         if(g_pair_states[i].last_decision.RejectionReason != REJ_NONE)
            g_dashboard_snapshot += " (" + EnumToString(g_pair_states[i].last_decision.RejectionReason) + ")";
      }
      else
      {
         g_dashboard_snapshot += "No Signal";
      }
      g_dashboard_snapshot += "\n";
   }
}

void UpdateDashboard()
{
   if(!ShowDashboard) return;
   Comment(g_dashboard_snapshot);
}

void RefreshDashboardLiveTradeCount()
{
   if(!ShowDashboard) return;

   static int lastDisplayedLiveCount = -1;
   int currentLiveCount = CountDashboardLiveEAOwnedTrades();
   if(currentLiveCount == lastDisplayedLiveCount) return;

   BuildDashboardSnapshot();
   UpdateDashboard();
   g_dashboard_needs_update = false;
   lastDisplayedLiveCount = currentLiveCount;
}

//+------------------------------------------------------------------+
//| MODULE 26: INITIALIZATION & CLEANUP                              |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

void NormalizeRuntimeLimits()
{
   int requested = MaxActivePair;
   g_effective_max_active_pair = requested;
   g_max_active_pair_sanitized = false;
   g_pair_list_truncated = false;

   if(g_effective_max_active_pair < 1)
   {
      g_effective_max_active_pair = 1;
      g_max_active_pair_sanitized = true;
   }
   else if(g_effective_max_active_pair > MAX_PAIRS)
   {
      g_effective_max_active_pair = MAX_PAIRS;
      g_max_active_pair_sanitized = true;
   }

   if(g_max_active_pair_sanitized)
   {
      Print("[INPUT WARNING] MaxActivePair=", IntegerToString(requested),
            " outside supported runtime range 1-", IntegerToString(MAX_PAIRS),
            ". EffectiveMaxActivePair=", IntegerToString(g_effective_max_active_pair),
            ". EA remains attached.");
   }

   string pairs[];
   SplitString(PairList, ",", pairs);
   if(ArraySize(pairs) > MAX_PAIRS)
   {
      g_pair_list_truncated = true;
      Print("[INPUT WARNING] PairList contains ", IntegerToString(ArraySize(pairs)),
            " entries; runtime capacity is ", IntegerToString(MAX_PAIRS),
            ". Extra entries are ignored. EA remains attached.");
   }
}

bool ValidateInputParameters()
{
   if(MaxRetry <= 0) return false;
   if(Slippage < 0 || AllowedExecutionDeviation_MinPoints < 0) return false;
   if(TradeLockMode < LOCK_OFF || TradeLockMode > LOCK_ONE_POSITION) return false;
   if(MMMode != 1 && MMMode != 2) return false;
   if(MMMode == 1 && AutoLotPercent <= 0) return false;
   if(MMMode == 1 && MaxAutoLot <= 0) return false;
   if(MMMode == 2 && FixedLot <= 0) return false;

   if(MaxTradePerPair > MAX_TRADES_PER_PAIR) return false;
   if(MaxTotalTrade > MAX_MONITORED) return false;
   if(StrategyID < STRATEGY_ID_MIN || StrategyID > STRATEGY_ID_MAX) return false;
   if(InstanceID < INSTANCE_ID_MIN || InstanceID > INSTANCE_ID_MAX) return false;
   
   string pairs[];
   SplitString(PairList, ",", pairs);

   if(EntryMode < 1 || EntryMode > 2) return false;

   return true;
}

bool ValidatePairIDCollision()
{
   for(int i = 0; i < g_pair_count; i++)
   {
      int pid = g_pair_states[i].pair_id;
      if(pid < PAIR_ID_MIN || pid > PAIR_ID_MAX)
      {
         g_pair_states[i].pair_enabled = false;
         Log(DBG_ERROR, "PairID out of range for " + g_pair_names[i]);
         return false;
      }

      for(int j = 0; j < i; j++)
      {
         if(g_pair_states[j].pair_id == pid)
         {
            g_pair_states[i].pair_enabled = false;
            Log(DBG_ERROR, "PairID collision for " + g_pair_names[i] +
                " with " + g_pair_names[j] +
                " (PID=" + IntegerToString(pid) + ")");
            return false;
         }
      }
   }
   return true;
}

bool ValidateMagicCollision()
{
   int usedMagics[MAX_PAIRS];
   ArrayInitialize(usedMagics, 0);
   
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      int magic = g_pair_states[i].magic_number;
      if(magic == 0)
      {
         g_pair_states[i].pair_enabled = false;
         Log(DBG_ERROR, "Invalid magic number for " + g_pair_names[i]);
         return false;
      }
      for(int j = 0; j < i; j++)
      {
         if(!g_pair_states[j].pair_enabled) continue;
         if(usedMagics[j] == magic)
         {
            g_pair_states[i].pair_enabled = false;
            Log(DBG_ERROR, "Magic collision for " + g_pair_names[i] + 
                " with " + g_pair_names[j]);
            return false;
         }
      }
      usedMagics[i] = magic;
   }
   return true;
}

void LoadPairs()
{
   string pairs[];
   SplitString(PairList, ",", pairs);
   g_pair_count = 0;
   
   for(int i = 0; i < ArraySize(pairs); i++)
   {
      if(i >= MAX_PAIRS) break;
      
      string pair = pairs[i];
      pair = StringTrimLeft(pair);
      pair = StringTrimRight(pair);
      if(pair == "") continue;
      
      Print("[P3S1] Pair request=", pair);

      string actual = FindActualSymbol(pair);
      if(actual == "")
      {
         Print("[P3S1][FAIL] Symbol resolution failed for ", pair);
         Log(DBG_ERROR, "Symbol not found: " + pair);
         continue;
      }

      Print("[P3S1] Symbol resolved ", pair, " -> ", actual);
      
      g_pair_names[g_pair_count] = pair;
      InitPairState(g_pair_states[g_pair_count]);
      g_pair_states[g_pair_count].base_symbol = pair;
      g_pair_states[g_pair_count].actual_symbol = actual;
      g_pair_states[g_pair_count].pair_id = GeneratePairID(pair);
      g_pair_states[g_pair_count].point = GetPointSize(actual);
      g_pair_states[g_pair_count].digits = GetDigits(actual);
      g_pair_states[g_pair_count].tick_value = GetTickValue(actual);
      g_pair_states[g_pair_count].tick_size_price = GetTickSize_Price(actual);
      g_pair_states[g_pair_count].min_lot = GetMinLot(actual);
      g_pair_states[g_pair_count].max_lot = GetMaxLot(actual);
      g_pair_states[g_pair_count].lot_step = GetLotStep(actual);
      g_pair_states[g_pair_count].lot_digits = GetLotDigits(actual);
      g_pair_states[g_pair_count].stop_level = GetStopLevel(actual);
      g_pair_states[g_pair_count].freeze_level = GetFreezeLevel(actual);
      g_pair_states[g_pair_count].magic_number = GenerateMagicNumber(StrategyID, InstanceID, g_pair_states[g_pair_count].pair_id);
      
      if(ValidateBrokerSpecificationWithRetry(actual, g_pair_states[g_pair_count]))
      {
         g_pair_states[g_pair_count].pair_enabled = true;
         Print("[P3S1][PASS] Broker spec ", actual,
               " PID=", IntegerToString(g_pair_states[g_pair_count].pair_id),
               " Magic=", IntegerToString(g_pair_states[g_pair_count].magic_number));
      }
      else
      {
         g_pair_states[g_pair_count].pair_enabled = false;
         Print("[P3S1][FAIL] Broker spec ", actual,
               " Point=", DoubleToString(g_pair_states[g_pair_count].point, 8),
               " Digits=", IntegerToString(g_pair_states[g_pair_count].digits),
               " TickValue=", DoubleToString(g_pair_states[g_pair_count].tick_value, 8),
               " TickSize=", DoubleToString(g_pair_states[g_pair_count].tick_size_price, 8),
               " MinLot=", DoubleToString(g_pair_states[g_pair_count].min_lot, 4),
               " MaxLot=", DoubleToString(g_pair_states[g_pair_count].max_lot, 4),
               " LotStep=", DoubleToString(g_pair_states[g_pair_count].lot_step, 4),
               " StopLevel=", IntegerToString(g_pair_states[g_pair_count].stop_level),
               " FreezeLevel=", IntegerToString(g_pair_states[g_pair_count].freeze_level));
      }
      
      g_pair_states[g_pair_count].is_cent_account = DetectCentAccount();
      g_pair_states[g_pair_count].cent_factor = GetCentFactor();
      
      g_processed_candle_time[g_pair_count] = 0;
      g_pair_count++;
   }
}

int InitializeEA()
{
   g_is_initialized = false;
   g_is_scanning = false;
   g_is_managing_trade = false;
   g_terminal_connected = IsTerminalConnected();
   g_portfolio_emergency_close_requested = false;
   g_processing_time = GetProcessingTime();

   g_last_risk_check_time = 0;
   g_cached_risk_allowed = false;
   g_cached_risk_reason = "";
   g_cached_balance = 0.0;

   Print("[P3S1] InitializeEA start PairList=", PairList,
         " RequestedMaxActivePair=", IntegerToString(MaxActivePair),
         " EffectiveMaxActivePair=", IntegerToString(g_effective_max_active_pair));

   InitBrokerInfo();
   LoadPairs();
   Print("[P3S1] LoadPairs completed count=", IntegerToString(g_pair_count));
   if(g_pair_count == 0)
   {
      Print("[P3S1][FAIL] No valid pairs loaded");
      Log(DBG_ERROR, "No valid pairs loaded");
      return INIT_FAILED;
   }
   
   if(!ValidatePairIDCollision())
   {
      Print("[P3S1][FAIL] PairID validation failed");
      Log(DBG_ERROR, "PairID collision detected");
      return INIT_PARAMETERS_INCORRECT;
   }
   Print("[P3S1][PASS] PairID validation");

   if(!ValidateMagicCollision())
   {
      Print("[P3S1][FAIL] Magic validation failed");
      Log(DBG_ERROR, "Magic collision detected");
      return INIT_PARAMETERS_INCORRECT;
   }
   Print("[P3S1][PASS] Magic validation");
   
   ArrayResize(g_global_signal_history, 0);
   g_global_signal_count = 0;
   g_monitored_count = 0;

   g_protection_reference_equity = AccountEquity();
   if(g_protection_reference_equity <= 0)
   {
      Log(DBG_ERROR, "Invalid protection reference equity during initialization");
      return INIT_FAILED;
   }
   g_last_reset_date = GetTodayStart();
   g_last_daily_profit = 0;
   g_cumulative_profit = 0;
   g_dashboard_needs_update = true;

   // CORE-V2-F4: reconstruct H4 directional context before any standalone H1
   // Re-Entry can be admitted. Failure resolves per-pair to NO_OWNER.
   RecoverH4DirectionalOwners();

   RebuildExecutionHistory();
   RecoverExistingOrders();

   if(!LoadExecutionAmbiguityHold() && g_execution_ambiguity.Active)
      Log(DBG_ERROR, "F07 persisted ambiguity HOLD is incomplete; new entries remain blocked");

   g_portfolio_emergency_close_requested = false;

   g_is_initialized = true;
   Print("[P3S1][PASS] EA initialized successfully with ",
         IntegerToString(g_pair_count), " pairs");
   Log(DBG_FULL, "EA initialized successfully with " + IntegerToString(g_pair_count) + " pairs");
   
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| MODULE 27: MAIN CONTROLLER (ORCHESTRATOR ONLY)                   |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsNewCandle(string pair, int pairIndex)
{
   datetime m15Closed = GetLatestClosedCandleTime(pair, PERIOD_M15);
   if(m15Closed == 0) return false;
   if(m15Closed != g_processed_candle_time[pairIndex])
   {
      return true;
   }
   return false;
}

string D10Dir(ENUM_DIRECTION d)
{
   if(d == DIR_BUY) return "B";
   if(d == DIR_SELL) return "S";
   return "-";
}

string D10RE(ENUM_RE_STATE s)
{
   if(s == RE_STATE_CANDIDATE) return "C";
   if(s == RE_STATE_CONFIRMED) return "F";
   if(s == RE_STATE_EXPIRED) return "X";
   return "N";
}

string D10EXT(ENUM_EXTREME_MATURITY s)
{
   if(s == EXT_MAT_RAW) return "R";
   if(s == EXT_MAT_REVERSAL_CONFIRMED) return "REV";
   if(s == EXT_MAT_RETEST_PHASE) return "RT";
   if(s == EXT_MAT_RETEST_READY) return "RDY";
   if(s == EXT_MAT_VOID) return "V";
   if(s == EXT_MAT_SUPERSEDED) return "S";
   return "N";
}

string D10MLV(ENUM_MLV_STATE s)
{
   if(s == MLV_PARENT_READY) return "P";
   if(s == MLV_TP_COMPLETE) return "TP";
   if(s == MLV_LOSS_DEVELOPING) return "L";
   if(s == MLV_FORMATION_ESTABLISHED) return "F";
   if(s == MLV_RETEST_COMPLETE) return "RT";
   if(s == MLV_DIRECTION_TAKEN) return "T";
   if(s == MLV_VOID) return "V";
   if(s == MLV_SUPERSEDED) return "S";
   return "N";
}

string D10D1(ENUM_D1_OWNER_STATE s)
{
   if(s == D1_OWNER_BUY_CONFIRMED) return "B";
   if(s == D1_OWNER_SELL_CONFIRMED) return "S";
   if(s == D1_TRANSITION) return "T";
   return "U";
}

string D10H4(ENUM_H4_OWNER_STATE s, ENUM_DIRECTION d)
{
   if(s == H4_OWNER_ACTIVE) return D10Dir(d);
   if(s == H4_OWNER_RECOVERY_UNRESOLVED) return "U";
   return "N";
}

void PrintSignalBottleneckDiagnostic(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;

   string pair = g_pair_states[pairIndex].actual_symbol;
   string finalCandidate = "NONE";
   if(decision.Valid)
   {
      finalCandidate = EnumToString(decision.SignalType) + "/" +
                       D10Dir(decision.Direction) + "/" +
                       EnumToString(decision.DecisionState);
      if(decision.RejectionReason != REJ_NONE)
         finalCandidate += "/" + EnumToString(decision.RejectionReason);
   }

   string d10a = "[D1-10A] " + pair +
                   " D1=" + D10D1(g_pair_states[pairIndex].d1_major_trend_owner.State) +
                   " H4=" + D10H4(g_pair_states[pairIndex].h4_direction_owner.State,
                                  g_pair_states[pairIndex].h4_direction_owner.Direction) +
                   " F=" + finalCandidate;
   ObserverPrintChanged("D10A|" + pair, d10a);

   string d10b = "[D1-10B] " + pair +
                   " RE H1=" + D10RE(g_pair_states[pairIndex].re_h1_buy_state.State) + "/" +
                                D10RE(g_pair_states[pairIndex].re_h1_sell_state.State) +
                   " H4=" + D10RE(g_pair_states[pairIndex].re_h4_buy_state.State) + "/" +
                             D10RE(g_pair_states[pairIndex].re_h4_sell_state.State) +
                   " D1=" + D10RE(g_pair_states[pairIndex].re_d1_buy_state.State) + "/" +
                             D10RE(g_pair_states[pairIndex].re_d1_sell_state.State) +
                   " M15=" + D10RE(g_pair_states[pairIndex].re_m15_buy_state.State) + "/" +
                              D10RE(g_pair_states[pairIndex].re_m15_sell_state.State) +
                   " OPP=" + D1OpportunityFamilyText(g_pair_states[pairIndex].d1_opportunity.Family) + "/" +
                             D10Dir(g_pair_states[pairIndex].d1_opportunity.Direction) + "/" +
                             (g_pair_states[pairIndex].d1_opportunity.Active ? "Y" : "N");
   ObserverPrintChanged("D10B|" + pair, d10b);

   string d10c = "[D1-10C] " + pair +
                   " X H1=" + D10EXT(g_pair_states[pairIndex].extreme_h1_buy_lifecycle.Maturity) + "/" +
                               D10EXT(g_pair_states[pairIndex].extreme_h1_sell_lifecycle.Maturity) +
                   " H4=" + D10EXT(g_pair_states[pairIndex].extreme_h4_buy_lifecycle.Maturity) + "/" +
                            D10EXT(g_pair_states[pairIndex].extreme_h4_sell_lifecycle.Maturity) +
                   " M15=" + D10MLV(g_pair_states[pairIndex].mlv_buy_state.State) + "/" +
                              D10MLV(g_pair_states[pairIndex].mlv_sell_state.State);
   ObserverPrintChanged("D10C|" + pair, d10c);
}

void ProcessPair(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;
   if(g_pair_states[pairIndex].is_processing) return;
   
   g_pair_states[pairIndex].is_processing = true;
   
   string pair = g_pair_names[pairIndex];
   string actual = g_pair_states[pairIndex].actual_symbol;
   
   BuildTimeframeSnapshot(actual, g_pair_states[pairIndex].tf_snapshot);
   
   GetDataForTimeframe(actual, PERIOD_D1, g_pair_states[pairIndex].tf_snapshot.D1_CandleTime, 
                       g_pair_states[pairIndex].d1_data);
   GetDataForTimeframe(actual, PERIOD_H4, g_pair_states[pairIndex].tf_snapshot.H4_CandleTime,
                       g_pair_states[pairIndex].h4_data);
   GetDataForTimeframe(actual, PERIOD_H1, g_pair_states[pairIndex].tf_snapshot.H1_CandleTime,
                       g_pair_states[pairIndex].h1_data);
   GetDataForTimeframe(actual, PERIOD_M15, g_pair_states[pairIndex].tf_snapshot.M15_CandleTime,
                       g_pair_states[pairIndex].m15_data);

   // NMJE P3 reads one closed M5 snapshot from the M15-owned cycle only.
   GetDataForTimeframe(actual, PERIOD_M5,
                       GetLatestClosedCandleTime(actual, PERIOD_M5),
                       g_pair_states[pairIndex].m5_data);

   // D1-01: classify strategic D1/MA50 owner from fully closed D1 data.
   // Producer only in this step; M15/M16 consumption is intentionally later.
   UpdateD1MajorTrendOwner(actual, g_pair_states[pairIndex]);

   // H4 owner is persistent across neutral H4 candles and changes only on
   // source-valid authoritative H4 direction/momentum events.
   UpdateRuntimeH4DirectionalOwner(pairIndex);

   BollingerBand d1Band, h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band;
   ZeroMemory(d1Band); ZeroMemory(h1Band); ZeroMemory(h1PrevBand);
   ZeroMemory(h4Band); ZeroMemory(h4PrevBand); ZeroMemory(m15Band);

   d1Band.TOP_BB = g_pair_states[pairIndex].d1_data.bollinger[0];
   d1Band.MID_BB = g_pair_states[pairIndex].d1_data.bollinger[1];
   d1Band.LOW_BB = g_pair_states[pairIndex].d1_data.bollinger[2];
   d1Band.Width = d1Band.TOP_BB - d1Band.LOW_BB;
   d1Band.State = BB_NONE;

   h1Band.TOP_BB = g_pair_states[pairIndex].h1_data.bollinger[0];
   h1Band.MID_BB = g_pair_states[pairIndex].h1_data.bollinger[1];
   h1Band.LOW_BB = g_pair_states[pairIndex].h1_data.bollinger[2];
   h1Band.Width = h1Band.TOP_BB - h1Band.LOW_BB;
   h1Band.State = BB_NONE;

   h4Band.TOP_BB = g_pair_states[pairIndex].h4_data.bollinger[0];
   h4Band.MID_BB = g_pair_states[pairIndex].h4_data.bollinger[1];
   h4Band.LOW_BB = g_pair_states[pairIndex].h4_data.bollinger[2];
   h4Band.Width = h4Band.TOP_BB - h4Band.LOW_BB;
   h4Band.State = BB_NONE;

   m15Band.TOP_BB = g_pair_states[pairIndex].m15_data.bollinger[0];
   m15Band.MID_BB = g_pair_states[pairIndex].m15_data.bollinger[1];
   m15Band.LOW_BB = g_pair_states[pairIndex].m15_data.bollinger[2];
   m15Band.Width = m15Band.TOP_BB - m15Band.LOW_BB;
   m15Band.State = BB_NONE;

   if(EnableBBShapeEngine)
   {
      BuildBBShapeState(actual, g_pair_states[pairIndex].h1_data, h1Band, h1PrevBand);
      BuildBBShapeState(actual, g_pair_states[pairIndex].h4_data, h4Band, h4PrevBand);
   }

   g_pair_states[pairIndex].current_bollinger = h1Band;
   g_pair_states[pairIndex].prev_bollinger = h1PrevBand;

   ValidatedSequenceCandidate allCandidates[];
   int allCandidateCount = 0;

   // D1O-02: D1 Extreme is a tactical opportunity source only after the
   // existing F2 reversal-confirmation maturity. RAW never authorizes entry.
   bool d1RawBuyExtreme = DetectExtreme(actual, DIR_BUY,
                                         g_pair_states[pairIndex].d1_data, d1Band);
   bool d1RawSellExtreme = DetectExtreme(actual, DIR_SELL,
                                          g_pair_states[pairIndex].d1_data, d1Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_d1_buy_lifecycle,
                          actual, DIR_BUY, g_pair_states[pairIndex].d1_data,
                          d1Band, d1RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_d1_sell_lifecycle,
                          actual, DIR_SELL, g_pair_states[pairIndex].d1_data,
                          d1Band, d1RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_d1_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_d1_sell_lifecycle,
                                      g_pair_states[pairIndex].d1_data);

   // F1 parent provenance: M15 Extreme maturity uses the already-resolved F2
   // lifecycle. RAW Extreme alone cannot parent canonical MHV/MLV.
   bool m15RawBuyExtreme = DetectExtreme(actual, DIR_BUY,
                                          g_pair_states[pairIndex].m15_data, m15Band);
   bool m15RawSellExtreme = DetectExtreme(actual, DIR_SELL,
                                           g_pair_states[pairIndex].m15_data, m15Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_buy_lifecycle,
                          actual, DIR_BUY, g_pair_states[pairIndex].m15_data,
                          m15Band, m15RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_sell_lifecycle,
                          actual, DIR_SELL, g_pair_states[pairIndex].m15_data,
                          m15Band, m15RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_m15_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_m15_sell_lifecycle,
                                      g_pair_states[pairIndex].m15_data);

   bool h1RawBuyExtreme = DetectExtreme(actual, DIR_BUY, g_pair_states[pairIndex].h1_data, h1Band);
   bool h1RawSellExtreme = DetectExtreme(actual, DIR_SELL, g_pair_states[pairIndex].h1_data, h1Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_buy_lifecycle, actual, DIR_BUY,
                          g_pair_states[pairIndex].h1_data, h1Band, h1RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_sell_lifecycle, actual, DIR_SELL,
                          g_pair_states[pairIndex].h1_data, h1Band, h1RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_h1_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_h1_sell_lifecycle,
                                      g_pair_states[pairIndex].h1_data);

   bool h4RawBuyExtreme = DetectExtreme(actual, DIR_BUY, g_pair_states[pairIndex].h4_data, h4Band);
   bool h4RawSellExtreme = DetectExtreme(actual, DIR_SELL, g_pair_states[pairIndex].h4_data, h4Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_buy_lifecycle, actual, DIR_BUY,
                          g_pair_states[pairIndex].h4_data, h4Band, h4RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_sell_lifecycle, actual, DIR_SELL,
                          g_pair_states[pairIndex].h4_data, h4Band, h4RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_h4_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_h4_sell_lifecycle,
                                      g_pair_states[pairIndex].h4_data);

   Signal resolvedH1BuyExtreme, resolvedH1SellExtreme, resolvedH4BuyExtreme, resolvedH4SellExtreme;
   ZeroMemory(resolvedH1BuyExtreme); ZeroMemory(resolvedH1SellExtreme);
   ZeroMemory(resolvedH4BuyExtreme); ZeroMemory(resolvedH4SellExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h1_buy_lifecycle, resolvedH1BuyExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h1_sell_lifecycle, resolvedH1SellExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h4_buy_lifecycle, resolvedH4BuyExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h4_sell_lifecycle, resolvedH4SellExtreme);
   UpdatePersistentExtremeState(resolvedH1BuyExtreme, g_pair_states[pairIndex].extreme_h1_buy_state);
   UpdatePersistentExtremeState(resolvedH1SellExtreme, g_pair_states[pairIndex].extreme_h1_sell_state);
   UpdatePersistentExtremeState(resolvedH4BuyExtreme, g_pair_states[pairIndex].extreme_h4_buy_state);
   UpdatePersistentExtremeState(resolvedH4SellExtreme, g_pair_states[pairIndex].extreme_h4_sell_state);

   Signal m15CSDSnapshots[2], m15ECSDSnapshots[2], m15CSMSnapshots[2];
   for(int snapIdx = 0; snapIdx < 2; snapIdx++)
   {
      ZeroMemory(m15CSDSnapshots[snapIdx]);
      ZeroMemory(m15ECSDSnapshots[snapIdx]);
      ZeroMemory(m15CSMSnapshots[snapIdx]);
   }

   // M27 locked Phase A: update all M06-M12 owners for both directions first.
   for(int dirIdx = 0; dirIdx < 2; dirIdx++)
   {
      ENUM_DIRECTION direction = (dirIdx == 0) ? DIR_BUY : DIR_SELL;

      Signal m15CSDSnapshot, m15ECSDSnapshot, m15CSMSnapshot;
      ZeroMemory(m15CSDSnapshot);
      ZeroMemory(m15ECSDSnapshot);
      ZeroMemory(m15CSMSnapshot);

      MovingAverage m15MA;
      m15MA.MA5_High = g_pair_states[pairIndex].m15_data.ma[0];
      m15MA.MA10_High = g_pair_states[pairIndex].m15_data.ma[1];
      m15MA.MA5_Low = g_pair_states[pairIndex].m15_data.ma[2];
      m15MA.MA10_Low = g_pair_states[pairIndex].m15_data.ma[3];
      m15MA.EMA50 = g_pair_states[pairIndex].m15_data.ma[4];
      int m15Shift = g_pair_states[pairIndex].m15_data.barIndex;

      if(DetectCSD(actual, PERIOD_M15, direction, m15Shift, m15MA, m15Band))
      {
         m15CSDSnapshot.Type = SIGNAL_CSD;
         m15CSDSnapshot.Direction = direction;
         m15CSDSnapshot.Valid = true;
         m15CSDSnapshot.Timeframe = PERIOD_M15;
         m15CSDSnapshot.BarIndex = m15Shift;
         m15CSDSnapshot.CandleTime = g_pair_states[pairIndex].m15_data.candle_time;
         m15CSDSnapshot.Timestamp = m15CSDSnapshot.CandleTime;
         m15CSDSnapshot.Close = g_pair_states[pairIndex].m15_data.close;
      }

      if(DetectECSD(actual, PERIOD_M15, direction, m15Shift, m15MA))
      {
         m15ECSDSnapshot.Type = SIGNAL_ECSD;
         m15ECSDSnapshot.Direction = direction;
         m15ECSDSnapshot.Valid = true;
         m15ECSDSnapshot.Timeframe = PERIOD_M15;
         m15ECSDSnapshot.BarIndex = m15Shift;
         m15ECSDSnapshot.CandleTime = g_pair_states[pairIndex].m15_data.candle_time;
         m15ECSDSnapshot.Timestamp = m15ECSDSnapshot.CandleTime;
         m15ECSDSnapshot.Close = g_pair_states[pairIndex].m15_data.close;
      }

      if(DetectCSM(actual, PERIOD_M15, direction, m15Shift))
      {
         m15CSMSnapshot.Type = SIGNAL_CSM;
         m15CSMSnapshot.Direction = direction;
         m15CSMSnapshot.Valid = true;
         m15CSMSnapshot.Timeframe = PERIOD_M15;
         m15CSMSnapshot.BarIndex = m15Shift;
         m15CSMSnapshot.CandleTime = g_pair_states[pairIndex].m15_data.candle_time;
         m15CSMSnapshot.Timestamp = m15CSMSnapshot.CandleTime;
         m15CSMSnapshot.Close = g_pair_states[pairIndex].m15_data.close;
      }

      MLVData mlvSnapshot;
      ReEntryData h1ReEntrySnapshot, h4ReEntryState, d1ReEntryState;
      ZeroMemory(mlvSnapshot);
      ZeroMemory(h1ReEntrySnapshot); ZeroMemory(h4ReEntryState); ZeroMemory(d1ReEntryState);

      if(direction == DIR_BUY)
      {
         UpdateCanonicalMLVState(
            g_pair_states[pairIndex].mlv_buy_state, actual, DIR_BUY,
            g_pair_states[pairIndex].m15_data, m15Band,
            g_pair_states[pairIndex].extreme_m15_sell_lifecycle,
            (m15CSDSnapshot.Valid || m15ECSDSnapshot.Valid));
         mlvSnapshot = g_pair_states[pairIndex].mlv_buy_state;

         UpdateReEntryState(g_pair_states[pairIndex].re_h1_buy_state, actual, direction,
                            g_pair_states[pairIndex].h1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_h4_buy_state, actual, direction,
                            g_pair_states[pairIndex].h4_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_d1_buy_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m15_buy_state, actual, direction,
                            g_pair_states[pairIndex].m15_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_buy_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_buy_state;
         NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);
      }
      else
      {
         UpdateCanonicalMLVState(
            g_pair_states[pairIndex].mlv_sell_state, actual, DIR_SELL,
            g_pair_states[pairIndex].m15_data, m15Band,
            g_pair_states[pairIndex].extreme_m15_buy_lifecycle,
            (m15CSDSnapshot.Valid || m15ECSDSnapshot.Valid));
         mlvSnapshot = g_pair_states[pairIndex].mlv_sell_state;

         UpdateReEntryState(g_pair_states[pairIndex].re_h1_sell_state, actual, direction,
                            g_pair_states[pairIndex].h1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_h4_sell_state, actual, direction,
                            g_pair_states[pairIndex].h4_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_d1_sell_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m15_sell_state, actual, direction,
                            g_pair_states[pairIndex].m15_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
         NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);
      }

      m15CSDSnapshots[dirIdx] = m15CSDSnapshot;
      m15ECSDSnapshots[dirIdx] = m15ECSDSnapshot;
      m15CSMSnapshots[dirIdx] = m15CSMSnapshot;
   }

   // M12N observes only after both direction owners are current for this cycle.
   UpdateNestedJourneyObservation(pairIndex);
   NMJE_P3_UpdateClosedM5Shadow(pairIndex);

   // M27 locked Phase B: M13/M14 assembly consumes the frozen owner snapshots.
   for(int assembleDirIdx = 0; assembleDirIdx < 2; assembleDirIdx++)
   {
      ENUM_DIRECTION direction = (assembleDirIdx == 0) ? DIR_BUY : DIR_SELL;
      Signal h1ExtremeSnapshot, h4ExtremeSnapshot, m15MHVSnapshot;
      Signal m15CSDSnapshot, m15ECSDSnapshot, m15CSMSnapshot;
      ZeroMemory(h1ExtremeSnapshot); ZeroMemory(h4ExtremeSnapshot);
      ZeroMemory(m15MHVSnapshot); ZeroMemory(m15CSDSnapshot);
      ZeroMemory(m15ECSDSnapshot); ZeroMemory(m15CSMSnapshot);
      m15CSDSnapshot = m15CSDSnapshots[assembleDirIdx];
      m15ECSDSnapshot = m15ECSDSnapshots[assembleDirIdx];
      m15CSMSnapshot = m15CSMSnapshots[assembleDirIdx];

      MLVData mlvSnapshot;
      ReEntryData h1ReEntrySnapshot, h4ReEntryState, d1ReEntryState;
      ZeroMemory(mlvSnapshot);
      ZeroMemory(h1ReEntrySnapshot); ZeroMemory(h4ReEntryState); ZeroMemory(d1ReEntryState);
      if(direction == DIR_BUY)
      {
         mlvSnapshot = g_pair_states[pairIndex].mlv_buy_state;
         ExportCanonicalMHVSignal(g_pair_states[pairIndex].mlv_buy_state, m15MHVSnapshot);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_buy_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_buy_state;
      }
      else
      {
         mlvSnapshot = g_pair_states[pairIndex].mlv_sell_state;
         ExportCanonicalMHVSignal(g_pair_states[pairIndex].mlv_sell_state, m15MHVSnapshot);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
      }

      Signal extreme, mhv, csd, ecsd, csm;
      MLVData mlv;
      ReEntryData reEntry;
      ZeroMemory(extreme); ZeroMemory(mhv); ZeroMemory(csd);
      ZeroMemory(ecsd); ZeroMemory(csm); ZeroMemory(mlv); ZeroMemory(reEntry);

      CollectSignalSnapshots(h1ExtremeSnapshot, m15MHVSnapshot, mlvSnapshot,
                             m15CSDSnapshot, m15ECSDSnapshot, m15CSMSnapshot,
                             h1ReEntrySnapshot, extreme, mhv, mlv, csd, ecsd, csm, reEntry);

      Signal h4_reEntry, d1_reEntry, h4_extreme;
      ZeroMemory(h4_reEntry); ZeroMemory(d1_reEntry); ZeroMemory(h4_extreme);
      ExportConfirmedReEntrySignal(h4ReEntryState, h4_reEntry);
      ExportConfirmedReEntrySignal(d1ReEntryState, d1_reEntry);
      h4_extreme = h4ExtremeSnapshot;

      ComponentSet rem, rre, ree;
      BuildPossibleCombinations(rem, rre, ree, h4_reEntry, extreme, mlv,
                                d1_reEntry, h4_extreme);
      
      ValidatedSequenceCandidate reEntryCandidate;
      BuildConfirmedReEntryCandidate(
         reEntry, g_pair_states[pairIndex].h4_direction_owner, reEntryCandidate);
      AppendValidatedCandidate(reEntryCandidate, allCandidates, allCandidateCount);

      ValidatedSequenceCandidate standaloneExtremeCandidate;
      if(direction == DIR_BUY)
         BuildStandaloneExtremeCandidate(g_pair_states[pairIndex].extreme_h1_buy_lifecycle,
                                         g_pair_states[pairIndex].h4_direction_owner,
                                         standaloneExtremeCandidate);
      else
         BuildStandaloneExtremeCandidate(g_pair_states[pairIndex].extreme_h1_sell_lifecycle,
                                         g_pair_states[pairIndex].h4_direction_owner,
                                         standaloneExtremeCandidate);
      AppendValidatedCandidate(standaloneExtremeCandidate, allCandidates, allCandidateCount);

      ComponentSet allSets[3];
      allSets[0] = rem;
      allSets[1] = rre;
      allSets[2] = ree;
      for(int s = 0; s < 3; s++)
      {
         ValidatedSequenceCandidate cand;
         ZeroMemory(cand);
         ValidateSequence(allSets[s], cand);
         AppendValidatedCandidate(cand, allCandidates, allCandidateCount);
      }
   }

   // C044 Step3: consume lifecycle events only after both direction passes have
   // updated canonical M08 Extreme and M12 Re-Entry owner state for this closed
   // M15 processing cycle. The feature gate is still OFF in this staged build.
   AdvanceC044OwnerEventsForPair(pairIndex);
   AdvanceD1TPWLifecycleForPair(pairIndex);

   // D1O-02: all D1/H4/H1/M15 owners are now current. Materialize one
   // canonical Mode-2 opportunity cluster at most; M15 remains final authority.
   UpdateD1OpportunityJourney(pairIndex, d1Band);
   ValidatedSequenceCandidate d1OpportunityCandidate;
   BuildD1OpportunityCandidate(pairIndex, d1OpportunityCandidate);
   AppendValidatedCandidate(d1OpportunityCandidate, allCandidates, allCandidateCount);

   BBMA_Decision decision;
   OppositeConflictPackage conflict;
   ZeroMemory(decision);
   ZeroMemory(conflict);
   decision.Pair = actual;

   // NMJE P2 remains telemetry-only; comparator/order is untouched.
   NMJE_P2_PrintEqualEligibilityShadow(pairIndex, allCandidates,
                                        allCandidateCount,
                                        g_pair_states[pairIndex]);
   // Q9 P7 is candidate-observation telemetry only; it cannot rank or reject.
   NMJE_PrintStructuralDensityShadow(pairIndex, allCandidates,
                                     allCandidateCount,
                                     g_pair_states[pairIndex]);

   PriorityEngine_Atomic(allCandidates, allCandidateCount,
                         g_pair_states[pairIndex], decision, conflict);

   // Counterfactual research observes the already-selected baseline decision.
   // It never changes candidate ordering or the decision itself.
   if(IsTesting() && g_nmje_cf_pending[pairIndex].Present && decision.Valid)
      Print("[Q9-P2-CF-BASE] Pair=", actual,
            " Set=", g_nmje_cf_pending[pairIndex].SetID,
            " Sig=", EnumToString(decision.SignalType),
            " Dir=", NMJE_DirText(decision.Direction),
            " Seq=", decision.SequenceHash,
            " DIDH=", SHORT_HASH(decision.DecisionID),
            " Authority=NONE");

   // D1-07: M16 may only consume an actual M15-created decision.
   // ZeroMemory() leaves enum value 0 (= DEC_CREATED), so state alone is not
   // sufficient to prove that M15 selected/froze a decision.
   if(decision.Valid && decision.DecisionState == DEC_CREATED)
   {
      InvalidationEngine_Atomic(pairIndex, decision, conflict);
   }

   if(decision.DecisionState == DEC_VALIDATED)
   {
      // Q9 P4+ freezes observer metadata only after canonical validation.
      NMJE_FreezeValidatedDecisionAttribution(pairIndex, decision);
      // N2-01 shadow metadata only; execution path remains unchanged.
      NMJE_PrintValidatedDecisionShadow(pairIndex, decision);
      RunEntryPreflightAndExecute(decision, actual);
   }

   if(EntryMode == 2 && decision.Valid)
      Print("[P3M2][DECISION_FINAL] Pair=", actual,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " State=", EnumToString(decision.DecisionState),
            " Reason=", EnumToString(decision.RejectionReason),
            " DecisionID=", decision.DecisionID);

   PrintSignalBottleneckDiagnostic(pairIndex, decision);

   g_pair_states[pairIndex].last_decision = decision;

   datetime m15Closed = GetLatestClosedCandleTime(actual, PERIOD_M15);
   if(m15Closed > 0)
      g_processed_candle_time[pairIndex] = m15Closed;
   
   BuildDashboardSnapshot();
   g_dashboard_needs_update = true;
   
   g_pair_states[pairIndex].is_processing = false;
}

void OnTickMain()
{
   if(!g_is_initialized) return;

   ManagePortfolio();
   ManagePositions();
   // M23 lifecycle housekeeping owns registry compaction; telemetry remains read-only.
   CompactMonitoredTrades();

   // F07: protection/lifecycle always runs before reconciliation. A tick that
   // begins with an ambiguity HOLD never admits new exposure, even when exact
   // reconciliation succeeds on that tick. The newly materialized broker order
   // must pass the protection/lifecycle phase on the next operational tick first.
   bool hadExecutionAmbiguityHold = g_execution_ambiguity.Active;
   if(hadExecutionAmbiguityHold)
   {
      ReconcileExecutionAmbiguityHold();
      return;
   }

   if(g_portfolio_emergency_close_requested) return;
   
   if(g_is_scanning) return;
   g_is_scanning = true;
   
   g_processing_time = GetProcessingTime();
   
   for(int i = 0; i < g_pair_count; i++)
   {
      if(g_execution_ambiguity.Active) break;
      if(!g_pair_states[i].pair_enabled) continue;
      if(g_pair_states[i].is_processing) continue;
      if(IsNewCandle(g_pair_states[i].actual_symbol, i))
      {
         ProcessPair(i);
      }
   }
   
   if(g_dashboard_needs_update)
   {
      UpdateDashboard();
      g_dashboard_needs_update = false;
   }
   
   g_is_scanning = false;
}

//+------------------------------------------------------------------+
//| EXPERT INITIALIZATION FUNCTION                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   F7BuildIdentityTelemetry();
   NormalizeRuntimeLimits();
   if(!ValidateInputParameters())
   {
      Log(DBG_ERROR, "Input parameter validation failed");
      return INIT_PARAMETERS_INCORRECT;
   }
   
   if(InitializeEA() != INIT_SUCCEEDED)
   {
      Log(DBG_ERROR, "EA initialization failed");
      return INIT_FAILED;
   }

   ResetLastError();
   if(!EventSetTimer(1))
   {
      int timerError = GetLastError();
      g_is_initialized = false;
      Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));
      return INIT_FAILED;
   }
   
   Log(DBG_FULL, "BBMA EA " + string(BBMA_BUILD_TAG) + " initialized successfully");
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| EXPERT DEINITIALIZATION FUNCTION                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   EventKillTimer();

   g_is_initialized = false;
   g_is_scanning = false;
   g_is_managing_trade = false;
   g_dashboard_needs_update = false;
   if(ShowDashboard)
      Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));
}

//+------------------------------------------------------------------+
//| EXPERT TICK FUNCTION                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   if(!g_is_initialized) return;
   if(!IsTerminalConnected()) return;
   OnTickMain();
}

//+------------------------------------------------------------------+
//| EXPERT TIMER FUNCTION                                            |
//+------------------------------------------------------------------+
void OnTimer()
{
   if(!g_is_initialized) return;

   CleanupSignalHistoryEntries();
   CleanupGlobalSignalHistory();
   F7TelemetryHeartbeat();

   datetime todayStart = GetTodayStart();
   if(todayStart > g_last_reset_date)
   {
      double resetEquity = AccountEquity();
      if(resetEquity > 0)
         g_protection_reference_equity = resetEquity;
      g_last_reset_date = todayStart;
      g_last_daily_profit = 0;
      Log(DBG_FULL, "Daily reset: protection reference = " + DoubleToString(g_protection_reference_equity, 2));
   }

   if(!IsTerminalConnected()) return;
   OnTickMain();

   // P2-DASHCOUNT-01: refresh presentation only when live exact-owned count
   // changes. Timer cadence prevents stale closed-trade rows on the display.
   RefreshDashboardLiveTradeCount();
}

//+------------------------------------------------------------------+
//| END OF EXPERT ADVISOR                                            |
//+------------------------------------------------------------------+
