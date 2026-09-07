//+------------------------------------------------------------------+
//|                                           BBMA_EA.mq4 |
//| Version 4.7.5 - C10 Audit Ledger Stage B                    |
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
#property version   "4.75"
#property strict

//+------------------------------------------------------------------+
//| MODULE 01: HEADER & INPUTS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

//--- USER INPUT ENUMS (numeric values preserved for compatibility)
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
input double   MinRRRatio                         = 0.0;        // 08 Advanced | optional Min RR filter; 0=disabled
input double   MaxSLPips                          = 100.0;      // 08 Advanced | maximum accepted SL distance
input int      Slippage                           = 3;          // 08 Advanced | broker slippage in points
input ENUM_DEBUG_LEVEL DebugLevel                 = DBG_OFF;    // 08 Advanced | OFF / ERROR / SIGNAL / TRADE / FULL
input int      StrategyID                         = 1;          // 08 Advanced | strategy identity 1-99
input int      InstanceID                         = 0;          // 08 Advanced | instance identity 0-99
input bool     EnableC10StatisticsLedger          = false;      // 08 Advanced | audit-only C10 CSV ledger; no trade authority

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
// C044 staged implementation gate. Keep OFF until M23/M24 lifecycle
// close + restart reconstruction are implemented and verified.
bool           EnableC044Lifecycle                = false;
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
#define MAX_PAIRS               40
#define MAX_TRADES_PER_PAIR     20
#define MAX_MONITORED           400
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
#define C10_SIGNAL_SCHEMA       "C10S1"
#define C10_OUTCOME_SCHEMA      "C10O1"
#define C10_LEDGER_FOLDER       "BBMA_C10"
#define C10_LEDGER_MAX_BYTES    33554432
#define C10_LEDGER_MAX_PARTS    99
#define C10_SOURCE_HASH         "C502B6892383D612D194A26F3A3C7A92684E6A53E683603A2A58DC13CEC5CA64"

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

// Issue #101 Stage-C2 shadow-only canonical M5 context families.
enum ENUM_NMJE_M5_CONTEXT_CODE
{
   NMJE_M5_CONTEXT_NONE = 0,
   NMJE_M5_CONTEXT_RE_ENTRY = 1,
   NMJE_M5_CONTEXT_EXTREME = 2
};

// Issue #101 P5 diagnostic-only conflict family. This never changes the
// canonical top-level relation or any candidate/decision authority.
enum ENUM_NMJE_CONFLICT_SUBTYPE
{
   NMJE_CONFLICT_NONE,
   NMJE_CONFLICT_TEMPORARY_RETRACEMENT,
   NMJE_CONFLICT_LOCAL_CHILD_OPPOSITION,
   NMJE_CONFLICT_PARENT_DIRECTION,
   NMJE_CONFLICT_OWNER_TRANSITION,
   NMJE_CONFLICT_STRUCTURAL,
   NMJE_CONFLICT_UNRESOLVED_PROVENANCE
};

// Issue #101 P6 categorical BBMA journey maturity. No score or threshold.
enum ENUM_NMJE_JOURNEY_MATURITY
{
   NMJE_MATURITY_NONE,
   NMJE_MATURITY_OWNER_ONLY,
   NMJE_MATURITY_EXTREME_DEVELOPING,
   NMJE_MATURITY_EXTREME_MATURE,
   NMJE_MATURITY_REENTRY_CANDIDATE,
   NMJE_MATURITY_REENTRY_CONFIRMED,
   NMJE_MATURITY_MHV_DEVELOPING,
   NMJE_MATURITY_MHV_MATURE,
   NMJE_MATURITY_CONFLICTED,
   NMJE_MATURITY_OWNER_TRANSITION,
   NMJE_MATURITY_UNRESOLVED
};

// Issue #101 P10 research-only directional displacement class. It is emitted
// after execution and never participates in validation or execution authority.
enum ENUM_NMJE_ENTRY_DISPLACEMENT
{
   NMJE_DISPLACEMENT_UNRESOLVED,
   NMJE_DISPLACEMENT_FLAT,
   NMJE_DISPLACEMENT_FAVORABLE,
   NMJE_DISPLACEMENT_ADVERSE
};

// Issue #101 P11 shadow-only canonical event-phase lineage.
enum ENUM_NMJE_EVENT_PHASE
{
   NMJE_EVENT_PHASE_UNRESOLVED,
   NMJE_EVENT_PHASE_FIRST,
   NMJE_EVENT_PHASE_CONTINUATION,
   NMJE_EVENT_PHASE_NEW_JOURNEY
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
                           REC_IDENTITY_HASH_ONLY, REC_IDENTITY_MISSING_FROZEN };

// C044 staged targetless lifecycle state. Execution remains gated OFF until
// owner-event evaluation and recovery activation pass their final gate.
enum ENUM_C044_LIFECYCLE_STATE
{
   C044_LIFE_NONE,
   C044_LIFE_WAIT_OUTER_TEST,
   C044_LIFE_WAIT_NEXT_REENTRY,
   C044_LIFE_EXIT_LATCHED,
   C044_LIFE_FROZEN
};

enum ENUM_C044_EXIT_REASON
{
   C044_EXIT_NONE,
   C044_EXIT_FAILED_MOMENTUM,
   C044_EXIT_CYCLE_SUPERSEDED
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
   // N3 provenance-only epoch anchor. Changes only when canonical owner
   // State/Direction changes; never changes the D1 strategy formula.
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
   // N3 provenance-only deterministic identity. Never strategy authority.
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

// NMJE v2 Stage-C2 provenance/shadow storage. It has no
// processing-clock, candidate, rejection, ranking or execution authority.
struct NMJEM5RefinementState
{
   bool                 Present;
   string               EventID;
   string               ParentEventID;
   string               JourneyID;
   ENUM_DIRECTION       Direction;
   int                  ContextCode;
   int                  ContextStateCode;
   datetime             EventStartCandleTime;
   datetime             ClosedCandleTime;
   ENUM_NESTED_RELATION Relation;
   ENUM_NMJE_CONFLICT_SUBTYPE ConflictSubtype;
   ENUM_NMJE_JOURNEY_MATURITY Maturity;
   bool                 Valid;
   bool                 Resolved;
   string               Reason;
};

// Issue #101 P4 research-only attribution payload. String identities are
// reduced to deterministic hashes for durable MT4 GlobalVariable storage.
struct NMJEShadowAttributionState
{
   bool                 Present;
   bool                 Durable;
   string               JourneyHash;
   string               ParentEventHash;
   bool                 ParentRetained;
   string               ParentSelectionReasonHash;
   ENUM_NESTED_RELATION Relation;
   ENUM_NMJE_CONFLICT_SUBTYPE ConflictSubtype;
   ENUM_NMJE_JOURNEY_MATURITY Maturity;
   bool                 M5Present;
   string               M5EventHash;
   ENUM_NESTED_RELATION M5Relation;
   ENUM_NMJE_CONFLICT_SUBTYPE M5ConflictSubtype;
   ENUM_NMJE_JOURNEY_MATURITY M5Maturity;
   ENUM_DIRECTION       M5Direction;
   int                  M5ContextCode;
   int                  M5ContextStateCode;
   datetime             M5EventStartCandleTime;
   datetime             M5ClosedCandleTime;
   string               M5ReasonHash;
   int                  StructureMask;
   int                  StructureCount;
   int                  RequirementCompleteness;
   int                  SequenceCompleteness;
   bool                 EntryDisplacementPresent;
   ENUM_NMJE_ENTRY_DISPLACEMENT EntryDisplacementClass;
   double               SourceConfirmationPrice;
   double               ValidationEntryPrice;
   double               BrokerExecutionPrice;
   double               StructuralAnchorPrice;
   double               ConfirmationToValidationPips;
   double               ValidationToExecutionPips;
   double               ExecutionFromAnchorPips;
   ENUM_NMJE_EVENT_PHASE EventPhase;
   bool                 EventPhaseCheckpointDurable;
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
   // N3 provenance-only identity of the exact canonical owner chosen as parent.
   string                  ParentEventID;
   bool                    ParentRetained;
   string                  ParentSelectionReason;
   ENUM_NMJE_EVENT_PHASE   EventPhase;
   bool                    EventPhaseCheckpointDurable;
   ENUM_DIRECTION          StrategicDirection;
   ENUM_NESTED_RELATION    Relation;
   ENUM_NMJE_CONFLICT_SUBTYPE ConflictSubtype;
   ENUM_NMJE_JOURNEY_MATURITY Maturity;
   bool                    Resolved;
   bool                    Valid;
   datetime                UpdateCandleTime;
   string                  Reason;
   NestedTFNode            D1Node;
   NestedTFNode            H4Node;
   NestedTFNode            H1Node;
   NestedTFNode            M15Node;
   // NMJE v2 Stage-C2 shadow-only M5 relation; never decision authority.
   NMJEM5RefinementState    M5Refinement;

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
   datetime M5_CandleTime;
   bool     M5_IsClosed;
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

   // N3 shadow-only frozen NMJE provenance. No execution authority at this stage.
   string                       NMJEJourneyID;
   string                       NMJEParentEventID;
   bool                         NMJEParentRetained;
   string                       NMJEParentSelectionReason;
   ENUM_NESTED_RELATION         NMJERelation;
   ENUM_NMJE_CONFLICT_SUBTYPE   NMJEConflictSubtype;
   ENUM_NMJE_JOURNEY_MATURITY   NMJEMaturity;
   datetime                     NMJEUpdateCandleTime;
   bool                         NMJESnapshotPresent;
   // Issue #101 P4 frozen research payload; never candidate/authority input.
   NMJEM5RefinementState        NMJEM5Refinement;
   // Issue #101 P7 descriptive completeness of the already-selected decision.
   int                          NMJEStructureMask;
   int                          NMJEStructureCount;
   int                          NMJERequirementCompleteness;
   int                          NMJESequenceCompleteness;
   // Issue #101 P10 research-only source geometry, frozen by M17.
   bool                         NMJEEntryDisplacementSourcePresent;
   double                       NMJESourceConfirmationPrice;
   double                       NMJEStructuralAnchorPrice;
   // Issue #101 P11 canonical identity-transition metadata only.
   ENUM_NMJE_EVENT_PHASE        NMJEEventPhase;
   bool                         NMJEEventPhaseCheckpointDurable;
   
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
   // Issue #101 Stage-C1 read-only data acquisition on the M15 clock.
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
   // Issue #101 Stage-C2 canonical detector state, observed on M15 clock only.
   ReEntryData          re_m5_buy_state;
   ReEntryData          re_m5_sell_state;
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
   // Issue #101 Stage-C2 shadow context; never exported as a candidate.
   ExtremeLifecycleData extreme_m5_buy_lifecycle;
   ExtremeLifecycleData extreme_m5_sell_lifecycle;
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
   // Issue #101 P4 durable research metadata, keyed by execution identity.
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
   ReEntryData          c044_replay_reentry;
   ExtremeLifecycleData c044_replay_extreme_buy;
   ExtremeLifecycleData c044_replay_extreme_sell;

   // D1 Extreme TP-Wajib lifecycle. Independent of C044.
   bool                 d1_tpw_lifecycle_managed;
   string               d1_tpw_cycle_hash;
   datetime             d1_tpw_extreme_candle;
   datetime             d1_tpw_last_processed_d1_candle;
   bool                 d1_tpw_exit_latched;
   datetime             d1_tpw_exit_latched_candle;
   bool                 d1_tpw_frozen;

   ENUM_RECOVERY_STATE  recovery_state;
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
bool                 g_timer_registered;
const int            TESTER_FUNCTION_NOT_ALLOWED = 4059;

//--- Manual mode
ENUM_PRIORITY_TIER   g_manual_priority_tiers[];

//--- Dashboard
string               g_dashboard_snapshot;
bool                 g_dashboard_needs_update;

//--- C10 Stage-A audit ledger. It is evidence-only and default OFF.
bool                 g_c10_ledger_ready;
bool                 g_c10_integrity_failed;
string               g_c10_run_id;
string               g_c10_config_fingerprint;
string               g_c10_source_hash;

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

   // C3-T01: a disconnected portable Strategy Tester can expose the exact
   // chart symbol and history while withholding broker catalogue-selection
   // authority. Admit only that exact tester symbol; live resolution below is
   // unchanged, and LoadPairs still performs the full broker-spec fail-closed
   // validation before enabling the pair.
   if(IsTesting() && requested == Symbol())
      return requested;

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
   if(IsTesting()) return true;
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
   InitTimeframeData(state.m5_data);

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

   state.extreme_m5_buy_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_m5_buy_lifecycle.Direction = DIR_BUY;
   state.extreme_m5_buy_lifecycle.Timeframe = PERIOD_M5;
   state.extreme_m5_sell_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_m5_sell_lifecycle.Direction = DIR_SELL;
   state.extreme_m5_sell_lifecycle.Timeframe = PERIOD_M5;

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
   state.re_m5_buy_state.State = RE_STATE_NONE;
   state.re_m5_buy_state.Direction = DIR_BUY;
   state.re_m5_buy_state.Timeframe = PERIOD_M5;
   state.re_m5_sell_state.State = RE_STATE_NONE;
   state.re_m5_sell_state.Direction = DIR_SELL;
   state.re_m5_sell_state.Timeframe = PERIOD_M5;

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

//+------------------------------------------------------------------+
//| C10 STAGE-B AUDIT LEDGER                                         |
//| Evidence only: no signal, filter, risk, sizing or broker authority|
//+------------------------------------------------------------------+
string C10_SignalHeader()
{
   return "Schema,BuildID,SourceHash,ConfigFingerprint,RunID,EventID,EventTimeUTC,DecisionID,AttemptSeq,Pair,Direction,SetupFamily,EntryTimeframe,D1OwnerEpochID,H4JourneyID,H1SetupID,M15CandidateID,M5EventID,NMJERelation,SignalState,ReasonCode,IntendedEntry,IntendedSL,IntendedTP,SLSource,TPSource,SpreadPips";
}

string C10_OutcomeHeader()
{
   return "Schema,BuildID,SourceHash,ConfigFingerprint,RunID,OutcomeEventID,OutcomeTimeUTC,Mode,DecisionID,ExecutionID,OrderTicket,Pair,Direction,SetupFamily,EntryTimeframe,EntryTimeUTC,ExitTimeUTC,EntryPrice,ExitPrice,IntendedSL,IntendedTP,Lot,SpreadPips,SlippagePips,GrossPL,Commission,Swap,NetPL,RiskAmount,RMultiple,MFEPips,MAEPips,HoldingSeconds,ExitReason,EvidenceResolution";
}

string C10_CSVField(string value)
{
   StringReplace(value, "\r", "\\r");
   StringReplace(value, "\n", "\\n");
   StringReplace(value, "\"", "\"\"");
   return "\"" + value + "\"";
}

string C10_BuildCSVLine(string &fields[], int count)
{
   string line = "";
   for(int i = 0; i < count; i++)
   {
      if(i > 0) line += ",";
      line += C10_CSVField(fields[i]);
   }
   return line;
}

string C10_UTCText(datetime value)
{
   if(value <= 0) return "NA";
   string text = TimeToString(value, TIME_DATE | TIME_SECONDS);
   StringReplace(text, ".", "-");
   StringReplace(text, " ", "T");
   return text + "Z";
}

string C10_DayKey(datetime value)
{
   if(value <= 0) return "";
   string text = TimeToString(value, TIME_DATE);
   StringReplace(text, ".", "");
   return text;
}

string C10_ValueOrNA(string value)
{
   return (value == "") ? "NA" : value;
}

string C10_PriceOrNA(double value, int digits)
{
   if(value <= 0.0 || digits < 0) return "NA";
   return DoubleToString(value, digits);
}

string C10_BuildConfigFingerprint()
{
   string raw = PairList + "|" + IntegerToString((int)EntryMode) + "|" +
                IntegerToString(MaxTradePerPair) + "|" +
                IntegerToString(MaxTotalTrade) + "|" +
                IntegerToString(MaxActivePair) + "|" +
                IntegerToString((int)MMMode) + "|" +
                DoubleToString(AutoLotPercent, 8) + "|" +
                DoubleToString(FixedLot, 8) + "|" +
                DoubleToString(MaxAutoLot, 8) + "|" +
                IntegerToString((int)TradeLockMode) + "|" +
                DoubleToString(MaxSpreadPips, 8) + "|" +
                DoubleToString(MaxDrawdownPercent, 8) + "|" +
                DoubleToString(BasketLossPercent, 8) + "|" +
                DoubleToString(MaxTotalRiskPercent, 8) + "|" +
                DoubleToString(MinRRRatio, 8) + "|" +
                DoubleToString(MaxSLPips, 8) + "|" +
                IntegerToString(Slippage) + "|" +
                IntegerToString(StrategyID) + "|" +
                IntegerToString(InstanceID) + "|" +
                (EnableC10StatisticsLedger ? "1" : "0");
   return SHORT_HASH(raw, 16);
}

string C10_LedgerFileName(string prefix, string schema, string dayKey, int part)
{
   return C10_LEDGER_FOLDER + "\\" + prefix + "_" + schema + "_" +
          dayKey + "_part" + StringFormat("%02d", part) + ".csv";
}

long C10_ExistingFileSize(string fileName)
{
   if(!FileIsExist(fileName)) return 0;
   int handle = FileOpen(fileName, FILE_READ | FILE_BIN | FILE_SHARE_READ);
   if(handle == INVALID_HANDLE) return -1;
   long size = (long)FileSize(handle);
   FileClose(handle);
   return size;
}

bool C10_IsCompleteCSVRow(string line, int expectedColumns)
{
   if(expectedColumns <= 0 || StringLen(line) < 2) return false;
   if(StringSubstr(line, 0, 1) != "\"" ||
      StringSubstr(line, StringLen(line) - 1, 1) != "\"") return false;

   int separators = 0;
   int cursor = 0;
   while(true)
   {
      int found = StringFind(line, "\",\"", cursor);
      if(found < 0) break;
      separators++;
      cursor = found + 3;
   }
   return (separators == expectedColumns - 1);
}

bool C10_FileEndsWithCRLF(string fileName)
{
   int handle = FileOpen(fileName, FILE_READ | FILE_BIN | FILE_SHARE_READ);
   if(handle == INVALID_HANDLE) return false;
   long size = (long)FileSize(handle);
   if(size < 2)
   {
      FileClose(handle);
      return false;
   }
   if(!FileSeek(handle, size - 2, SEEK_SET))
   {
      FileClose(handle);
      return false;
   }
   int cr = FileReadInteger(handle, CHAR_VALUE);
   int lf = FileReadInteger(handle, CHAR_VALUE);
   FileClose(handle);
   return (cr == 13 && lf == 10);
}

bool C10_InspectLedgerFile(string fileName, string expectedHeader,
                           int expectedColumns, bool &tornTail)
{
   tornTail = false;
   int handle = FileOpen(fileName, FILE_READ | FILE_TXT | FILE_ANSI |
                         FILE_SHARE_READ, 0, CP_UTF8);
   if(handle == INVALID_HANDLE) return false;
   if((long)FileSize(handle) <= 0)
   {
      FileClose(handle);
      return false;
   }

   bool committedTail = C10_FileEndsWithCRLF(fileName);
   int rowIndex = 0;
   while(!FileIsEnding(handle))
   {
      string line = FileReadString(handle);
      bool atEnd = FileIsEnding(handle);
      if(rowIndex == 0)
      {
         if(line != expectedHeader)
         {
            FileClose(handle);
            return false;
         }
         if(atEnd && !committedTail)
         {
            FileClose(handle);
            return false;
         }
      }
      else if(atEnd && !committedTail)
      {
         tornTail = true;
         break;
      }
      else if(!C10_IsCompleteCSVRow(line, expectedColumns))
      {
         FileClose(handle);
         return false;
      }
      rowIndex++;
   }
   FileClose(handle);
   return (rowIndex > 0);
}

bool C10_RepairTornTail(string fileName, string expectedHeader,
                        int expectedColumns)
{
   string token = SHORT_HASH(fileName + "|" + IntegerToString((int)GetTickCount()), 12);
   string tempName = fileName + ".repair_" + token + ".tmp";
   string quarantineName = fileName + ".torn_" + token + ".bak";
   if(FileIsExist(tempName) && !FileDelete(tempName)) return false;

   int source = FileOpen(fileName, FILE_READ | FILE_TXT | FILE_ANSI |
                         FILE_SHARE_READ, 0, CP_UTF8);
   int target = FileOpen(tempName, FILE_WRITE | FILE_TXT | FILE_ANSI,
                         0, CP_UTF8);
   if(source == INVALID_HANDLE || target == INVALID_HANDLE)
   {
      if(source != INVALID_HANDLE) FileClose(source);
      if(target != INVALID_HANDLE) FileClose(target);
      if(FileIsExist(tempName)) FileDelete(tempName);
      return false;
   }

   bool committedTail = C10_FileEndsWithCRLF(fileName);
   int rowIndex = 0;
   bool valid = true;
   while(!FileIsEnding(source))
   {
      string line = FileReadString(source);
      bool atEnd = FileIsEnding(source);
      if(rowIndex == 0 && line != expectedHeader)
      {
         valid = false;
         break;
      }
      if(rowIndex > 0 && atEnd && !committedTail) break;
      if(rowIndex > 0 && !C10_IsCompleteCSVRow(line, expectedColumns))
      {
         valid = false;
         break;
      }
      if(FileWriteString(target, line + "\r\n") <= 0)
      {
         valid = false;
         break;
      }
      rowIndex++;
   }
   FileFlush(target);
   FileClose(source);
   FileClose(target);

   if(!valid || rowIndex <= 0)
   {
      FileDelete(tempName);
      return false;
   }
   if(!FileMove(fileName, 0, quarantineName, 0))
   {
      FileDelete(tempName);
      return false;
   }
   if(!FileMove(tempName, 0, fileName, 0))
   {
      bool rollback = FileMove(quarantineName, 0, fileName, 0);
      if(FileIsExist(tempName)) FileDelete(tempName);
      if(!rollback)
         Print("[C10][TAIL_REPAIR_ROLLBACK_FAILED] File=", fileName,
               " Preserved=", quarantineName,
               " TradingAuthority=UNCHANGED");
      return false;
   }

   bool tornAfter = false;
   if(!C10_InspectLedgerFile(fileName, expectedHeader, expectedColumns,
                             tornAfter) || tornAfter) return false;
   Print("[C10][TAIL_REPAIRED] File=", fileName,
         " Preserved=", quarantineName,
         " TradingAuthority=UNCHANGED");
   return true;
}

string C10_SelectLedgerFile(string prefix, string schema, datetime eventTime,
                            int rowBytes)
{
   string dayKey = C10_DayKey(eventTime);
   if(dayKey == "") return "";

   int highestPart = 0;
   long highestSize = 0;
   for(int part = 1; part <= C10_LEDGER_MAX_PARTS; part++)
   {
      string fileName = C10_LedgerFileName(prefix, schema, dayKey, part);
      long size = C10_ExistingFileSize(fileName);
      if(size < 0) return "";
      if(size > 0)
      {
         highestPart = part;
         highestSize = size;
      }
   }
   if(highestPart == 0)
      return C10_LedgerFileName(prefix, schema, dayKey, 1);
   if(highestSize + rowBytes + 2 <= C10_LEDGER_MAX_BYTES)
      return C10_LedgerFileName(prefix, schema, dayKey, highestPart);
   if(highestPart >= C10_LEDGER_MAX_PARTS) return "";
   return C10_LedgerFileName(prefix, schema, dayKey, highestPart + 1);
}

bool C10_ValidateOrCreateFile(string fileName, string expectedHeader,
                              int expectedColumns)
{
   int handle = FileOpen(fileName,
                         FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI |
                         FILE_SHARE_READ, 0, CP_UTF8);
   if(handle == INVALID_HANDLE) return false;

   long size = (long)FileSize(handle);
   if(size == 0)
   {
      if(FileWriteString(handle, expectedHeader + "\r\n") <= 0)
      {
         FileClose(handle);
         return false;
      }
      FileFlush(handle);
      FileClose(handle);
      return true;
   }

   FileClose(handle);
   bool tornTail = false;
   if(!C10_InspectLedgerFile(fileName, expectedHeader, expectedColumns,
                             tornTail)) return false;
   if(!tornTail) return true;
   return C10_RepairTornTail(fileName, expectedHeader, expectedColumns);
}

// Return 1=found, 0=absent, -1=read failure.
int C10_FileContainsEvent(string fileName, string eventID)
{
   int handle = FileOpen(fileName, FILE_READ | FILE_TXT | FILE_ANSI |
                         FILE_SHARE_READ, 0, CP_UTF8);
   if(handle == INVALID_HANDLE) return -1;
   string needle = "," + C10_CSVField(eventID) + ",";
   while(!FileIsEnding(handle))
   {
      string line = FileReadString(handle);
      if(StringFind(line, needle) >= 0)
      {
         FileClose(handle);
         return 1;
      }
   }
   FileClose(handle);
   return 0;
}

int C10_EventExistsInDay(string prefix, string schema, datetime eventTime,
                         string expectedHeader, int expectedColumns,
                         string eventID)
{
   string dayKey = C10_DayKey(eventTime);
   if(dayKey == "") return -1;
   for(int part = 1; part <= C10_LEDGER_MAX_PARTS; part++)
   {
      string fileName = C10_LedgerFileName(prefix, schema, dayKey, part);
      if(!FileIsExist(fileName)) continue;
      if(!C10_ValidateOrCreateFile(fileName, expectedHeader, expectedColumns))
         return -1;
      int found = C10_FileContainsEvent(fileName, eventID);
      if(found != 0) return found;
   }
   return 0;
}

void C10_DisableLedger(string reason)
{
   if(!g_c10_integrity_failed)
      Print("[C10][LEDGER_DISABLED] Reason=", reason,
            " TradingAuthority=UNCHANGED");
   g_c10_integrity_failed = true;
   g_c10_ledger_ready = false;
}

// Return 1=appended, 0=idempotent duplicate, -1=integrity/write failure.
int C10_AppendEvent(string prefix, string schema, string expectedHeader,
                    int expectedColumns, string eventID, datetime eventTime,
                    string csvLine)
{
   if(!g_c10_ledger_ready || g_c10_integrity_failed) return -1;
   if(eventID == "" || eventTime <= 0 || csvLine == "") return -1;
   if(!C10_IsCompleteCSVRow(csvLine, expectedColumns))
   {
      C10_DisableLedger("ROW_SHAPE_INVALID");
      return -1;
   }

   int duplicate = C10_EventExistsInDay(
      prefix, schema, eventTime, expectedHeader, expectedColumns, eventID);
   if(duplicate < 0)
   {
      C10_DisableLedger("CROSS_PART_SCAN_FAILURE");
      return -1;
   }
   if(duplicate > 0) return 0;

   string fileName = C10_SelectLedgerFile(prefix, schema, eventTime,
                                           StringLen(csvLine));
   if(fileName == "")
   {
      C10_DisableLedger("ROTATION_TARGET_UNAVAILABLE");
      return -1;
   }
   if(!C10_ValidateOrCreateFile(fileName, expectedHeader, expectedColumns))
   {
      C10_DisableLedger("SCHEMA_OR_FILE_OPEN_FAILURE:" + fileName);
      return -1;
   }
   int handle = FileOpen(fileName,
                         FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI |
                         FILE_SHARE_READ, 0, CP_UTF8);
   if(handle == INVALID_HANDLE)
   {
      C10_DisableLedger("APPEND_OPEN_FAILURE:" + fileName);
      return -1;
   }
   FileSeek(handle, 0, SEEK_END);
   uint written = FileWriteString(handle, csvLine + "\r\n");
   if(written <= 0)
   {
      FileClose(handle);
      C10_DisableLedger("APPEND_WRITE_FAILURE:" + fileName);
      return -1;
   }
   FileFlush(handle);
   FileClose(handle);
   return 1;
}

string C10_AttemptKey(string decisionID)
{
   return "C10A" + IntegerToString(StrategyID) + "I" +
          IntegerToString(InstanceID) + SHORT_HASH(decisionID, 16);
}

int C10_NextAttemptSequence(string decisionID)
{
   string key = C10_AttemptKey(decisionID);
   if(GlobalVariableCheck(key))
   {
      double prior = GlobalVariableGet(key);
      if(prior < 0 || prior > 2147483000.0) return -1;
      return (int)prior + 1;
   }
   return 1;
}

bool C10_CommitAttemptSequence(string decisionID, int attemptSeq)
{
   if(decisionID == "" || attemptSeq <= 0) return false;
   return (GlobalVariableSet(C10_AttemptKey(decisionID), attemptSeq) != 0);
}

bool C10_InitializeLedgers()
{
   g_c10_ledger_ready = false;
   g_c10_integrity_failed = false;
   g_c10_run_id = "";
   g_c10_config_fingerprint = "";
   g_c10_source_hash = "";

   if(!EnableC10StatisticsLedger)
   {
      Print("[C10][OFF] Statistics ledger disabled by input; authority unchanged");
      return true;
   }

   datetime utcNow = TimeGMT();
   if(utcNow <= 0)
   {
      C10_DisableLedger("UTC_TIME_UNAVAILABLE");
      return false;
   }
   FolderCreate(C10_LEDGER_FOLDER);

   g_c10_source_hash = C10_SOURCE_HASH;
   g_c10_config_fingerprint = C10_BuildConfigFingerprint();
   g_c10_run_id = SHORT_HASH(
      IntegerToString(AccountNumber()) + "|" + AccountServer() + "|" +
      C10_UTCText(utcNow) + "|" + IntegerToString(StrategyID) + "|" +
      IntegerToString(InstanceID), 16);

   string signalFile = C10_SelectLedgerFile("bbma_signal", C10_SIGNAL_SCHEMA,
                                             utcNow, 0);
   string outcomeFile = C10_SelectLedgerFile("bbma_outcome", C10_OUTCOME_SCHEMA,
                                              utcNow, 0);
   if(signalFile == "" || outcomeFile == "" ||
      !C10_ValidateOrCreateFile(signalFile, C10_SignalHeader(), 27) ||
      !C10_ValidateOrCreateFile(outcomeFile, C10_OutcomeHeader(), 35))
   {
      C10_DisableLedger("INITIAL_SCHEMA_OR_FILE_FAILURE");
      return false;
   }

   g_c10_ledger_ready = true;
   Print("[C10][READY] Stage=B SignalSchema=", C10_SIGNAL_SCHEMA,
         " OutcomeSchema=", C10_OUTCOME_SCHEMA,
         " RunID=", g_c10_run_id,
         " Config=", g_c10_config_fingerprint,
         " Authority=NONE");
   return true;
}

void C10_ShutdownLedgers()
{
   g_c10_ledger_ready = false;
}

void C10_WriteSignalEvent(int pairIndex, BBMA_Decision &decision)
{
   if(!EnableC10StatisticsLedger || !g_c10_ledger_ready ||
      g_c10_integrity_failed || !decision.Valid) return;
   if(pairIndex < 0 || pairIndex >= g_pair_count || decision.DecisionID == "")
   {
      C10_DisableLedger("SIGNAL_IDENTITY_UNPROVABLE");
      return;
   }

   datetime eventTime = TimeGMT();
   int attemptSeq = C10_NextAttemptSequence(decision.DecisionID);
   if(eventTime <= 0 || attemptSeq <= 0)
   {
      C10_DisableLedger("ATTEMPT_OR_TIME_UNPROVABLE");
      return;
   }

   PairState state = g_pair_states[pairIndex];
   NestedJourneyState journey = g_nested_journeys[pairIndex];
   string d1OwnerEpochID = NMJE_D1OwnerEventID(
      state.actual_symbol, state.d1_major_trend_owner);
   string m5EventID = decision.NMJEM5Refinement.Present ?
                      decision.NMJEM5Refinement.EventID : "";
   int digits = GetDigits(state.actual_symbol);
   double pipValue = GetPipValue(state.actual_symbol);
   double bid = MarketInfo(state.actual_symbol, MODE_BID);
   double ask = MarketInfo(state.actual_symbol, MODE_ASK);
   string spreadPips = "NA";
   if(pipValue > 0.0 && bid > 0.0 && ask > 0.0)
      spreadPips = DoubleToString(MathAbs(ask - bid) / pipValue, 4);

   string eventIdentity = C10_SIGNAL_SCHEMA + "|FINAL|" +
                          decision.DecisionID + "|" +
                          IntegerToString(attemptSeq) + "|" +
                          EnumToString(decision.DecisionState) + "|" +
                          EnumToString(decision.RejectionReason);
   string eventID = SHORT_HASH(eventIdentity, 16);

   string fields[27];
   fields[0]  = C10_SIGNAL_SCHEMA;
   fields[1]  = "4.75";
   fields[2]  = g_c10_source_hash;
   fields[3]  = g_c10_config_fingerprint;
   fields[4]  = g_c10_run_id;
   fields[5]  = eventID;
   fields[6]  = C10_UTCText(eventTime);
   fields[7]  = decision.DecisionID;
   fields[8]  = IntegerToString(attemptSeq);
   fields[9]  = state.actual_symbol;
   fields[10] = EnumToString(decision.Direction);
   fields[11] = EnumToString(decision.SignalType);
   fields[12] = "M15";
   fields[13] = C10_ValueOrNA(d1OwnerEpochID);
   fields[14] = C10_ValueOrNA(journey.JourneyID);
   fields[15] = C10_ValueOrNA(journey.H1Node.CanonicalEventID);
   fields[16] = C10_ValueOrNA(journey.M15Node.CanonicalEventID);
   fields[17] = C10_ValueOrNA(m5EventID);
   fields[18] = decision.NMJESnapshotPresent ?
                EnumToString(decision.NMJERelation) : "NA";
   fields[19] = EnumToString(decision.DecisionState);
   fields[20] = EnumToString(decision.RejectionReason);
   fields[21] = C10_PriceOrNA(decision.EntryPrice, digits);
   fields[22] = C10_PriceOrNA(decision.StopLoss, digits);
   fields[23] = C10_PriceOrNA(decision.TakeProfit, digits);
   fields[24] = decision.HasSLTPSourceComponent ?
                EnumToString(decision.SLTPSource) : "NA";
   fields[25] = fields[24];
   fields[26] = spreadPips;

   string csvLine = C10_BuildCSVLine(fields, 27);
   int appendResult = C10_AppendEvent(
      "bbma_signal", C10_SIGNAL_SCHEMA, C10_SignalHeader(), 27,
      eventID, eventTime, csvLine);
   if(appendResult < 0) return;
   if(!C10_CommitAttemptSequence(decision.DecisionID, attemptSeq))
   {
      C10_DisableLedger("ATTEMPT_SEQUENCE_COMMIT_FAILURE");
      return;
   }

   Print("[C10][SIGNAL] EventID=", eventID,
         " DecisionID=", decision.DecisionID,
         " AttemptSeq=", IntegerToString(attemptSeq),
         " Result=", appendResult == 1 ? "APPENDED" : "DUPLICATE_IGNORED",
         " Authority=NONE");
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

   snapshot.M5_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_M5);
   snapshot.M5_IsClosed = IsCandleClosed(snapshot.M5_CandleTime, 300);
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

double SMA(string pair, int timeframe, int period, int shift)
{
   double sum = 0;
   int count = 0;
   for(int i = 0; i < period; i++)
   {
      double price = iClose(pair, timeframe, shift + i);
      if(price > 0)
      {
         sum += price;
         count++;
      }
   }
   if(count == 0) return 0;
   return sum / count;
}

double BBMAHighMA(string pair, int timeframe, int period, int shift)
{
   if(period <= 0 || shift < 0) return 0;
   return iMA(pair, timeframe, period, 0, MODE_LWMA, PRICE_HIGH, shift);
}

double BBMALowMA(string pair, int timeframe, int period, int shift)
{
   if(period <= 0 || shift < 0) return 0;
   return iMA(pair, timeframe, period, 0, MODE_LWMA, PRICE_LOW, shift);
}

double EMA(string pair, int timeframe, int period, int shift)
{
   if(period <= 0 || shift < 0) return 0;
   return iMA(pair, timeframe, period, 0, MODE_EMA, PRICE_CLOSE, shift);
}

double StandardDeviation(string pair, int timeframe, int period, int shift)
{
   double mean = SMA(pair, timeframe, period, shift);
   if(mean == 0) return 0;
   double sum = 0;
   int count = 0;
   for(int i = 0; i < period; i++)
   {
      double price = iClose(pair, timeframe, shift + i);
      if(price > 0)
      {
         sum += MathPow(price - mean, 2);
         count++;
      }
   }
   if(count == 0) return 0;
   return MathSqrt(sum / count);
}

void CalculateBollinger(string pair, int timeframe, int shift, BollingerBand &band)
{
   double middle = SMA(pair, timeframe, BB_PERIOD, shift);
   double stdDev = StandardDeviation(pair, timeframe, BB_PERIOD, shift);
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
   data.is_valid = true;
   data.is_closed = IsCandleClosed(candleTime, GetTimeframeSeconds(timeframe));
   data.data_count = iBars(pair, timeframe);
   
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

   // F2 maturity has NO fixed candle/session expiry. MaxWaitBars_Extreme stays
   // downstream as a project component-freshness overlay only; it must not
   // erase lifecycle provenance needed by later structural stages such as F1.

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

bool TryAdvanceMHVSupersessionFromCanonicalParent(MLVData &mlv,
                                                   TimeframeData &data,
                                                   ExtremeLifecycleData &parent)
{
   // N3 single-writer invariant: M09 NEVER detects, resets, promotes or mutates
   // ExtremeLifecycleData. M08 owns the canonical parent lifecycle completely.
   if(!IsMHVParentExtremeMature(parent)) return false;
   if(parent.ConfirmationCandleTime <= 0) return false;

   datetime boundary = mlv.ParentConfirmationCandleTime;
   if(boundary <= 0) boundary = mlv.ConfirmationCandleTime;
   if(boundary <= 0) boundary = mlv.VoidCandleTime;
   if(boundary <= 0 || parent.ConfirmationCandleTime <= boundary) return false;

   MarkCanonicalMLVSuperseded(
      mlv, data,
      "Old MHV/MLV cycle superseded by newer canonical M08 reversal-confirmed parent Extreme");
   if(EntryMode == 2)
      Print("[P3M2][MLV_SUPERSEDE] MLVDir=", EnumToString(mlv.Direction),
            " NewExtremeDir=", EnumToString(parent.Direction),
            " NewConfirm=", TimeToString(parent.ConfirmationCandleTime),
            " ProcessCandle=", TimeToString(data.candle_time));
   return true;
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

      if(TryAdvanceMHVSupersessionFromCanonicalParent(mlv, data, parent))
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

      if(TryAdvanceMHVSupersessionFromCanonicalParent(mlv, data, parent))
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
      TryAdvanceMHVSupersessionFromCanonicalParent(mlv, data, parent);
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

void SetD1OwnerUnresolved(PairState &state, string reason)
{
   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   ENUM_D1_OWNER_STATE previousState = owner.State;
   ENUM_DIRECTION previousDirection = owner.Direction;
   datetime previousEpoch = owner.EpochStartCandleTime;

   owner.State = D1_OWNER_UNRESOLVED;
   owner.Direction = DIR_NONE;
   owner.SourceCandleTime = state.d1_data.candle_time;
   if(previousEpoch <= 0 || previousState != D1_OWNER_UNRESOLVED ||
      previousDirection != DIR_NONE)
      owner.EpochStartCandleTime = owner.SourceCandleTime;
   else
      owner.EpochStartCandleTime = previousEpoch;
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

   owner.IsValid = true;

   if(owner.Close1 > owner.MA50_1 && owner.MA50_1 > owner.MA50_2)
   {
      owner.State = D1_OWNER_BUY_CONFIRMED;
      owner.Direction = DIR_BUY;
      owner.Reason = "Closed D1 above MA50 with rising MA50";
   }
   else if(owner.Close1 < owner.MA50_1 && owner.MA50_1 < owner.MA50_2)
   {
      owner.State = D1_OWNER_SELL_CONFIRMED;
      owner.Direction = DIR_SELL;
      owner.Reason = "Closed D1 below MA50 with falling MA50";
   }
   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";
   }

   // N3 owner epoch is provenance only: same canonical State/Direction keeps
   // the prior epoch while a transition starts a new deterministic epoch.
   if(previousEpoch <= 0 || owner.State != previousState ||
      owner.Direction != previousDirection)
      owner.EpochStartCandleTime = owner.SourceCandleTime;
   else
      owner.EpochStartCandleTime = previousEpoch;

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

bool IsReEntryIntrinsicExpired(ReEntryData &reEntry, datetime currentCandleTime)
{
   // CORE-V2-F3: Type 1 has structural owner lifetime, not a generic candle TTL.
   if(reEntry.Type == RE_TYPE_1) return false;
   if(reEntry.StartCandleTime <= 0 || reEntry.ExpiryCandleTime <= 0) return false;
   return (currentCandleTime > reEntry.ExpiryCandleTime);
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

bool IsType1MAClusterCloseSideFailure(TimeframeData &data,
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
   reEntry.ExpiryBar = MaxWaitBars_ReEntry;
   reEntry.ExpiryCandleTime =
      reEntry.StartCandleTime + MaxWaitBars_ReEntry * data.timeframe * 60;
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
      (reEntry.Type == RE_TYPE_1 ||
       reEntry.Type1ContextState != TYPE1_CTX_NONE))
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
      return RE_STATE_NONE;
   }

   if((reEntry.State == RE_STATE_CANDIDATE || reEntry.State == RE_STATE_CONFIRMED) &&
      IsReEntryIntrinsicExpired(reEntry, data.candle_time))
   {
      reEntry.State = RE_STATE_EXPIRED;
      reEntry.IsValid = false;
      reEntry.Reason = "MaxWaitBars_ReEntry expired";
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      return RE_STATE_EXPIRED;
   }

   // Confirmed Type 1 remains structurally valid only while its owner survives.
   if(reEntry.State == RE_STATE_CONFIRMED && reEntry.Type == RE_TYPE_1)
   {
      if(IsType1MAClusterCloseSideFailure(data, direction))
      {
         ResetReEntryState(reEntry, direction, data.timeframe);
         return RE_STATE_NONE;
      }

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

      if(IsType1MAClusterCloseSideFailure(data, direction))
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
      if(reEntry.Type == RE_TYPE_1)
      {
         // Structural invalidation / ownership transfer has priority.
         if(IsType1MAClusterCloseSideFailure(data, direction))
         {
            ResetReEntryState(reEntry, direction, data.timeframe);
            return RE_STATE_NONE;
         }

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

// N3 Step-2: deterministic provenance identities. These helpers consume
// canonical owner facts only; they do not detect, score, mature or gate signals.
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
   if(pair == "" || owner.EpochStartCandleTime <= 0) return "";
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

// Issue #101 P1 schema-only deterministic M5 context identity. The helper
// consumes explicit provenance values only and is not wired into processing.
string NMJE_M5ContextEventID(string pair, ENUM_DIRECTION direction,
                             int contextCode, datetime eventStartCandleTime)
{
   if(pair == "" || eventStartCandleTime <= 0 || contextCode <= 0 ||
      (direction != DIR_BUY && direction != DIR_SELL))
      return "";
   string raw = "M5CTX|" + pair + "|" + IntegerToString(PERIOD_M5) + "|" +
                IntegerToString((int)direction) + "|" +
                IntegerToString(contextCode) + "|" +
                IntegerToString((int)eventStartCandleTime);
   return NMJE_IdentityHash(raw);
}

// Fail-closed schema validator for future recovery/materialization work.
// Present=false is the valid pre-materialization state; any present snapshot
// must carry the full immutable lineage and a canonical relation.
bool NMJE_M5LineageSnapshotValid(NMJEM5RefinementState &snapshot)
{
   if(!snapshot.Present) return true;
   if(!snapshot.Valid || !snapshot.Resolved) return false;
   if(snapshot.EventID == "" || snapshot.ParentEventID == "" ||
      snapshot.JourneyID == "" || snapshot.EventStartCandleTime <= 0 ||
      snapshot.ContextStateCode <= 0 ||
      snapshot.ClosedCandleTime <= 0 ||
      snapshot.ClosedCandleTime < snapshot.EventStartCandleTime)
      return false;
   if(snapshot.Relation != NESTED_BUILDING &&
      snapshot.Relation != NESTED_SUPPORTING &&
      snapshot.Relation != NESTED_ALIGNED &&
      snapshot.Relation != NESTED_CONFLICT &&
      snapshot.Relation != NESTED_UNRESOLVED)
      return false;
   if(snapshot.ConflictSubtype < NMJE_CONFLICT_NONE ||
      snapshot.ConflictSubtype > NMJE_CONFLICT_UNRESOLVED_PROVENANCE)
      return false;
   if(snapshot.Maturity < NMJE_MATURITY_EXTREME_DEVELOPING ||
      snapshot.Maturity > NMJE_MATURITY_REENTRY_CONFIRMED)
      return false;
   if(snapshot.Relation == NESTED_CONFLICT &&
      snapshot.ConflictSubtype == NMJE_CONFLICT_NONE)
      return false;
   return true;
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

ENUM_NMJE_CONFLICT_SUBTYPE NMJE_ClassifyConflictSubtype(
   ENUM_NESTED_RELATION relation, string reason)
{
   if(StringFind(reason, "D1_TRANSITION") >= 0 ||
      StringFind(reason, "OWNER_TRANSITION") >= 0)
      return NMJE_CONFLICT_OWNER_TRANSITION;
   if(relation == NESTED_UNRESOLVED ||
      StringFind(reason, "AMBIGUOUS") >= 0 ||
      StringFind(reason, "MISSING") >= 0 ||
      StringFind(reason, "UNAVAILABLE") >= 0 ||
      StringFind(reason, "INVALID") >= 0 ||
      StringFind(reason, "UNRESOLVED") >= 0)
      return NMJE_CONFLICT_UNRESOLVED_PROVENANCE;
   if(StringFind(reason, "CANDIDATE_RETRACEMENT") >= 0)
      return NMJE_CONFLICT_TEMPORARY_RETRACEMENT;
   if(StringFind(reason, "H4_LOCAL_OPPOSES_D1") >= 0)
      return NMJE_CONFLICT_PARENT_DIRECTION;
   if(StringFind(reason, "OPPOSES_PARENT") >= 0 ||
      StringFind(reason, "H1_RE_OPPOSES") >= 0)
      return NMJE_CONFLICT_LOCAL_CHILD_OPPOSITION;
   if(relation == NESTED_CONFLICT)
      return NMJE_CONFLICT_STRUCTURAL;
   return NMJE_CONFLICT_NONE;
}

string NMJE_ConflictSubtypeText(ENUM_NMJE_CONFLICT_SUBTYPE subtype)
{
   if(subtype == NMJE_CONFLICT_TEMPORARY_RETRACEMENT) return "TEMP_RETRACEMENT";
   if(subtype == NMJE_CONFLICT_LOCAL_CHILD_OPPOSITION) return "LOCAL_CHILD";
   if(subtype == NMJE_CONFLICT_PARENT_DIRECTION) return "PARENT_DIRECTION";
   if(subtype == NMJE_CONFLICT_OWNER_TRANSITION) return "OWNER_TRANSITION";
   if(subtype == NMJE_CONFLICT_STRUCTURAL) return "STRUCTURAL";
   if(subtype == NMJE_CONFLICT_UNRESOLVED_PROVENANCE) return "UNRESOLVED_PROVENANCE";
   return "NONE";
}

ENUM_NMJE_JOURNEY_MATURITY NMJE_ClassifyJourneyMaturity(
   PairState &state, NestedJourneyState &journey)
{
   if(journey.Relation == NESTED_UNRESOLVED)
      return NMJE_MATURITY_UNRESOLVED;
   if(journey.ConflictSubtype == NMJE_CONFLICT_OWNER_TRANSITION)
      return NMJE_MATURITY_OWNER_TRANSITION;
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
   if(journey.Relation == NESTED_CONFLICT)
      return NMJE_MATURITY_CONFLICTED;
   if(journey.ParentEventID != "" && journey.JourneyID != "")
      return NMJE_MATURITY_OWNER_ONLY;
   return NMJE_MATURITY_NONE;
}

ENUM_NMJE_JOURNEY_MATURITY NMJE_ClassifyM5Maturity(
   NMJEM5RefinementState &snapshot)
{
   if(!snapshot.Present)
   {
      if(snapshot.Reason == "M5_NO_CANONICAL_CONTEXT")
         return NMJE_MATURITY_NONE;
      if(snapshot.ConflictSubtype == NMJE_CONFLICT_UNRESOLVED_PROVENANCE)
         return NMJE_MATURITY_UNRESOLVED;
      return NMJE_MATURITY_NONE;
   }
   if(snapshot.ContextCode == NMJE_M5_CONTEXT_RE_ENTRY)
   {
      if(snapshot.ContextStateCode == RE_STATE_CONFIRMED)
         return NMJE_MATURITY_REENTRY_CONFIRMED;
      if(snapshot.ContextStateCode == RE_STATE_CANDIDATE)
         return NMJE_MATURITY_REENTRY_CANDIDATE;
      return NMJE_MATURITY_UNRESOLVED;
   }
   if(snapshot.ContextCode == NMJE_M5_CONTEXT_EXTREME)
   {
      if(snapshot.ContextStateCode == EXT_MAT_RAW)
         return NMJE_MATURITY_EXTREME_DEVELOPING;
      if(snapshot.ContextStateCode == EXT_MAT_REVERSAL_CONFIRMED ||
         snapshot.ContextStateCode == EXT_MAT_RETEST_PHASE ||
         snapshot.ContextStateCode == EXT_MAT_RETEST_READY)
         return NMJE_MATURITY_EXTREME_MATURE;
   }
   return NMJE_MATURITY_UNRESOLVED;
}

string NMJE_MaturityText(ENUM_NMJE_JOURNEY_MATURITY maturity)
{
   if(maturity == NMJE_MATURITY_OWNER_ONLY) return "OWNER_ONLY";
   if(maturity == NMJE_MATURITY_EXTREME_DEVELOPING) return "EXTREME_DEVELOPING";
   if(maturity == NMJE_MATURITY_EXTREME_MATURE) return "EXTREME_MATURE";
   if(maturity == NMJE_MATURITY_REENTRY_CANDIDATE) return "RE_CANDIDATE";
   if(maturity == NMJE_MATURITY_REENTRY_CONFIRMED) return "RE_CONFIRMED";
   if(maturity == NMJE_MATURITY_MHV_DEVELOPING) return "MHV_DEVELOPING";
   if(maturity == NMJE_MATURITY_MHV_MATURE) return "MHV_MATURE";
   if(maturity == NMJE_MATURITY_CONFLICTED) return "CONFLICTED";
   if(maturity == NMJE_MATURITY_OWNER_TRANSITION) return "OWNER_TRANSITION";
   if(maturity == NMJE_MATURITY_UNRESOLVED) return "UNRESOLVED";
   return "NONE";
}

bool NMJE_NodeSupportsDirection(NestedTFNode &node, ENUM_DIRECTION direction)
{
   return (node.Valid && node.CanonicalEventID != "" &&
           node.Direction == direction);
}

int NMJE_BuildStructureMask(NestedJourneyState &journey,
                            ENUM_DIRECTION direction)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return 0;
   int mask = 0;
   if(NMJE_NodeSupportsDirection(journey.D1Node, direction)) mask |= 1;
   if(NMJE_NodeSupportsDirection(journey.H4Node, direction)) mask |= 2;
   if(NMJE_NodeSupportsDirection(journey.H1Node, direction)) mask |= 4;
   if(NMJE_NodeSupportsDirection(journey.M15Node, direction)) mask |= 8;
   if(journey.M5Refinement.Present && journey.M5Refinement.Valid &&
      journey.M5Refinement.Resolved &&
      journey.M5Refinement.Direction == direction &&
      (journey.M5Refinement.Relation == NESTED_SUPPORTING ||
       journey.M5Refinement.Relation == NESTED_ALIGNED))
      mask |= 16;
   return mask;
}

int NMJE_CountStructureBits(int mask)
{
   int count = 0;
   int bits[5] = {1,2,4,8,16};
   for(int i = 0; i < 5; i++)
      if((mask & bits[i]) != 0) count++;
   return count;
}

void NMJE_CommitM5Refinement(NestedJourneyState &journey,
                             NMJEM5RefinementState &snapshot)
{
   snapshot.ConflictSubtype =
      NMJE_ClassifyConflictSubtype(snapshot.Relation, snapshot.Reason);
   snapshot.Maturity = NMJE_ClassifyM5Maturity(snapshot);
   journey.M5Refinement = snapshot;
}

// Issue #101 Stage-C2: materialize canonical M5 Re-Entry/Extreme context as
// immutable shadow lineage. This function only writes journey.M5Refinement;
// it never mutates candidate, rejection, ranking, risk or execution state.
void NMJE_BuildM5Refinement(PairState &state, NestedJourneyState &journey)
{
   NMJEM5RefinementState snapshot;
   ZeroMemory(snapshot);
   snapshot.Direction = DIR_NONE;
   snapshot.ContextCode = NMJE_M5_CONTEXT_NONE;
   snapshot.ContextStateCode = 0;
   snapshot.Relation = NESTED_UNRESOLVED;
   snapshot.ConflictSubtype = NMJE_CONFLICT_NONE;
   snapshot.Reason = "M5_NO_CANONICAL_CONTEXT";

   if(journey.ParentEventID == "" || journey.JourneyID == "" ||
      (journey.ParentDirection != DIR_BUY && journey.ParentDirection != DIR_SELL))
   {
      snapshot.Reason = "M5_PARENT_LINEAGE_MISSING";
      NMJE_CommitM5Refinement(journey, snapshot);
      return;
   }
   if(!state.m5_data.is_valid || !state.m5_data.is_closed ||
      state.m5_data.timeframe != PERIOD_M5 || state.m5_data.candle_time <= 0)
   {
      snapshot.Reason = "M5_CLOSED_DATA_UNAVAILABLE";
      NMJE_CommitM5Refinement(journey, snapshot);
      return;
   }

   ReEntryData selectedRE;
   ZeroMemory(selectedRE);
   bool ambiguous = false;
   bool confirmedRE = NMJE_SelectConfirmedRE(state.re_m5_buy_state,
                                               state.re_m5_sell_state,
                                               selectedRE, ambiguous);
   if(ambiguous)
   {
      snapshot.Reason = "M5_CONFIRMED_RE_AMBIGUOUS";
      NMJE_CommitM5Refinement(journey, snapshot);
      return;
   }

   bool candidateRE = false;
   if(!confirmedRE)
   {
      candidateRE = NMJE_SelectCandidateRE(state.re_m5_buy_state,
                                            state.re_m5_sell_state,
                                            selectedRE, ambiguous);
      if(ambiguous)
      {
         snapshot.Reason = "M5_CANDIDATE_RE_AMBIGUOUS";
         NMJE_CommitM5Refinement(journey, snapshot);
         return;
      }
   }

   if(confirmedRE || candidateRE)
   {
      snapshot.Direction = selectedRE.Direction;
      snapshot.ContextCode = NMJE_M5_CONTEXT_RE_ENTRY;
      snapshot.ContextStateCode = (int)selectedRE.State;
      snapshot.EventStartCandleTime = selectedRE.StartCandleTime;
      if(confirmedRE && selectedRE.Direction == journey.ParentDirection)
      {
         snapshot.Relation = NESTED_ALIGNED;
         snapshot.Reason = "M5_CONFIRMED_RE_ALIGNED";
      }
      else if(confirmedRE)
      {
         snapshot.Relation = NESTED_CONFLICT;
         snapshot.Reason = "M5_TEMPORARY_CONFIRMED_RE_OPPOSES_PARENT";
      }
      else if(selectedRE.Direction == journey.ParentDirection)
      {
         snapshot.Relation = NESTED_SUPPORTING;
         snapshot.Reason = "M5_CANDIDATE_RE_SUPPORTING";
      }
      else
      {
         snapshot.Relation = NESTED_BUILDING;
         snapshot.Reason = "M5_CANDIDATE_RETRACEMENT_BUILDING";
      }
   }
   else
   {
      bool buyExtreme = NMJE_IsExtremeActive(state.extreme_m5_buy_lifecycle);
      bool sellExtreme = NMJE_IsExtremeActive(state.extreme_m5_sell_lifecycle);
      if(buyExtreme && sellExtreme)
      {
         snapshot.Reason = "M5_EXTREME_AMBIGUOUS";
         NMJE_CommitM5Refinement(journey, snapshot);
         return;
      }
      if(!buyExtreme && !sellExtreme)
      {
         NMJE_CommitM5Refinement(journey, snapshot);
         return;
      }

      ExtremeLifecycleData selectedExtreme;
      ZeroMemory(selectedExtreme);
      if(buyExtreme) selectedExtreme = state.extreme_m5_buy_lifecycle;
      else selectedExtreme = state.extreme_m5_sell_lifecycle;

      snapshot.Direction = selectedExtreme.Direction;
      snapshot.ContextCode = NMJE_M5_CONTEXT_EXTREME;
      snapshot.ContextStateCode = (int)selectedExtreme.Maturity;
      snapshot.EventStartCandleTime = selectedExtreme.RawCandleTime;
      if(selectedExtreme.Direction == journey.ParentDirection)
      {
         snapshot.Relation = NESTED_SUPPORTING;
         snapshot.Reason = "M5_EXTREME_SUPPORTING";
      }
      else
      {
         snapshot.Relation = NESTED_CONFLICT;
         snapshot.Reason = "M5_TEMPORARY_EXTREME_OPPOSES_PARENT";
      }
   }

   snapshot.ConflictSubtype =
      NMJE_ClassifyConflictSubtype(snapshot.Relation, snapshot.Reason);
   snapshot.Present = true;
   snapshot.ParentEventID = journey.ParentEventID;
   snapshot.JourneyID = journey.JourneyID;
   snapshot.ClosedCandleTime = state.m5_data.candle_time;
   snapshot.EventID = NMJE_M5ContextEventID(state.actual_symbol,
                                             snapshot.Direction,
                                             snapshot.ContextCode,
                                             snapshot.EventStartCandleTime);
   snapshot.Valid = true;
   snapshot.Resolved = true;
   snapshot.Maturity = NMJE_ClassifyM5Maturity(snapshot);
   if(!NMJE_M5LineageSnapshotValid(snapshot))
   {
      ZeroMemory(snapshot);
      snapshot.Direction = DIR_NONE;
      snapshot.ContextCode = NMJE_M5_CONTEXT_NONE;
      snapshot.ContextStateCode = 0;
      snapshot.Relation = NESTED_UNRESOLVED;
      snapshot.ConflictSubtype = NMJE_CONFLICT_UNRESOLVED_PROVENANCE;
      snapshot.Reason = "M5_LINEAGE_INVALID";
   }
   NMJE_CommitM5Refinement(journey, snapshot);
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

// Issue #101 P8 provenance-only hysteresis. Retain an exact canonical parent
// while its event and D1 epoch still exist; never delay or suppress a decision.
bool NMJE_TryRetainPreviousParent(PairState &state,
                                  NestedJourneyState &previous,
                                  ENUM_NESTED_PARENT_KIND &kind,
                                  int &timeframe,
                                  ENUM_SIGNAL_TYPE &signalType,
                                  ENUM_DIRECTION &direction,
                                  datetime &anchor,
                                  string &eventID,
                                  string &reason)
{
   if(previous.Pair != state.actual_symbol || !previous.Valid ||
      !previous.Resolved || previous.ParentKind == NESTED_PARENT_NONE ||
      previous.ParentEventID == "" || previous.JourneyID == "")
      return false;

   NestedTFNode currentD1;
   NMJE_BuildD1Node(state, currentD1);
   if(previous.D1Node.CanonicalEventID != "" &&
      currentD1.CanonicalEventID != previous.D1Node.CanonicalEventID)
      return false;

   bool exact = false;
   ReEntryData selected;
   bool ambiguous = false;
   if(previous.ParentKind == NESTED_PARENT_H4_RE &&
      NMJE_SelectConfirmedRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous) && !ambiguous)
      exact = (NMJE_ReEntryEventID(state.actual_symbol, selected) ==
               previous.ParentEventID);
   else if(previous.ParentKind == NESTED_PARENT_H4_OWNER)
      exact = (NMJE_H4OwnerEventID(state.actual_symbol,
                                   state.h4_direction_owner) ==
               previous.ParentEventID);
   else if(previous.ParentKind == NESTED_PARENT_D1_RE &&
           NMJE_SelectConfirmedRE(state.re_d1_buy_state,
                                  state.re_d1_sell_state,
                                  selected, ambiguous) && !ambiguous)
      exact = (NMJE_ReEntryEventID(state.actual_symbol, selected) ==
               previous.ParentEventID);
   else if(previous.ParentKind == NESTED_PARENT_D1_OWNER)
      exact = (NMJE_D1OwnerEventID(state.actual_symbol,
                                   state.d1_major_trend_owner) ==
               previous.ParentEventID);
   if(!exact) return false;

   kind = previous.ParentKind;
   timeframe = previous.ParentTimeframe;
   signalType = previous.ParentSignal;
   direction = previous.ParentDirection;
   anchor = previous.ParentCandleTime;
   eventID = previous.ParentEventID;
   reason = "PREVIOUS_CANONICAL_PARENT_RETAINED";
   return true;
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
                           int timeframe, ENUM_SIGNAL_TYPE signalType,
                           ENUM_DIRECTION direction, datetime anchor)
{
   return pair + "|" + NMJE_ParentText(kind) + "|" +
          IntegerToString(timeframe) + "|" + EnumToString(signalType) + "|" +
          NMJE_DirText(direction) + "|" + IntegerToString((int)anchor);
}

string NMJE_EventPhaseText(ENUM_NMJE_EVENT_PHASE phase)
{
   if(phase == NMJE_EVENT_PHASE_FIRST) return "FIRST";
   if(phase == NMJE_EVENT_PHASE_CONTINUATION) return "CONTINUATION";
   if(phase == NMJE_EVENT_PHASE_NEW_JOURNEY) return "NEW_JOURNEY";
   return "UNRESOLVED";
}

string NMJEEventPhaseGVBase(string pair)
{
   return "BBXP|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|P" + SHORT_HASH(pair) + "|";
}

bool LoadNMJEEventPhaseCheckpoint(string pair, bool &hadParent,
                                  string &journeyHash,
                                  string &parentEventHash,
                                  string &d1EventHash,
                                  ENUM_NMJE_EVENT_PHASE &phase,
                                  datetime &updateCandle)
{
   hadParent = false;
   journeyHash = "";
   parentEventHash = "";
   d1EventHash = "";
   phase = NMJE_EVENT_PHASE_UNRESOLVED;
   updateCandle = 0;
   if(pair == "") return false;

   string base = NMJEEventPhaseGVBase(pair);
   if(!GlobalVariableCheck(base + "V") ||
      !GlobalVariableCheck(base + "H") ||
      !GlobalVariableCheck(base + "F") ||
      !GlobalVariableCheck(base + "T"))
      return false;
   if((int)GlobalVariableGet(base + "V") != 1) return false;
   hadParent = (GlobalVariableGet(base + "H") > 0.5);
   phase = (ENUM_NMJE_EVENT_PHASE)((int)GlobalVariableGet(base + "F"));
   updateCandle = (datetime)((int)GlobalVariableGet(base + "T"));
   if(updateCandle <= 0 || phase < NMJE_EVENT_PHASE_UNRESOLVED ||
      phase > NMJE_EVENT_PHASE_NEW_JOURNEY)
      return false;
   if(!hadParent) return true;

   if(!NMJELoadHex16(base, "J", journeyHash) ||
      !NMJELoadHex16(base, "P", parentEventHash) ||
      !NMJELoadHex16(base, "D", d1EventHash))
      return false;
   return (StringLen(journeyHash) == 16 &&
           StringLen(parentEventHash) == 16 &&
           StringLen(d1EventHash) == 16);
}

bool SaveNMJEEventPhaseCheckpoint(string pair, bool hasParent,
                                  string journeyHash,
                                  string parentEventHash,
                                  string d1EventHash,
                                  ENUM_NMJE_EVENT_PHASE phase,
                                  datetime updateCandle)
{
   if(pair == "" || updateCandle <= 0 ||
      phase < NMJE_EVENT_PHASE_UNRESOLVED ||
      phase > NMJE_EVENT_PHASE_NEW_JOURNEY)
      return false;
   if(hasParent &&
      (StringLen(journeyHash) != 16 ||
       StringLen(parentEventHash) != 16 ||
       StringLen(d1EventHash) != 16))
      return false;

   string base = NMJEEventPhaseGVBase(pair);
   GlobalVariableDel(base + "V");
   if(GlobalVariableSet(base + "H", hasParent ? 1.0 : 0.0) == 0) return false;
   if(GlobalVariableSet(base + "F", (double)phase) == 0) return false;
   if(GlobalVariableSet(base + "T", (double)updateCandle) == 0) return false;
   if(hasParent &&
      (!NMJEStoreHex16(base, "J", journeyHash) ||
       !NMJEStoreHex16(base, "P", parentEventHash) ||
       !NMJEStoreHex16(base, "D", d1EventHash)))
      return false;
   if(GlobalVariableSet(base + "V", 1.0) == 0) return false;
   GlobalVariablesFlush();
   return true;
}

void UpdateNestedJourneyObservation(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;

   NestedJourneyState previousJourney = g_nested_journeys[pairIndex];
   NestedJourneyState journey;
   ZeroMemory(journey);
   journey.Pair = g_pair_states[pairIndex].actual_symbol;
   journey.Relation = NESTED_NOT_APPLICABLE;
   journey.ConflictSubtype = NMJE_CONFLICT_NONE;
   journey.Maturity = NMJE_MATURITY_NONE;
   journey.EventPhase = NMJE_EVENT_PHASE_UNRESOLVED;
   journey.ParentKind = NESTED_PARENT_NONE;
   journey.ParentSignal = SIGNAL_NONE;
   journey.ParentDirection = DIR_NONE;
   journey.StrategicDirection = DIR_NONE;
   journey.UpdateCandleTime = g_pair_states[pairIndex].m15_data.candle_time;
   journey.Reason = "NO_ACTIVE_JOURNEY";
   journey.ParentSelectionReason = "NO_PARENT_SELECTED";
   NMJE_CaptureD1OpportunityOverlay(g_pair_states[pairIndex], journey);

   NMJE_BuildD1Node(g_pair_states[pairIndex], journey.D1Node);
   NMJE_BuildH4Node(g_pair_states[pairIndex], journey.H4Node);
   NMJE_BuildH1Node(g_pair_states[pairIndex], journey.H1Node);
   NMJE_BuildM15Node(g_pair_states[pairIndex], journey.M15Node);

   bool priorPhaseHadParent = false;
   string priorJourneyHash = "";
   string priorParentEventHash = "";
   string priorD1EventHash = "";
   ENUM_NMJE_EVENT_PHASE priorEventPhase = NMJE_EVENT_PHASE_UNRESOLVED;
   datetime priorPhaseUpdateCandle = 0;
   bool priorPhaseKnown = LoadNMJEEventPhaseCheckpoint(
      journey.Pair, priorPhaseHadParent, priorJourneyHash,
      priorParentEventHash, priorD1EventHash, priorEventPhase,
      priorPhaseUpdateCandle);

   ENUM_D1_OWNER_STATE d1State = g_pair_states[pairIndex].d1_major_trend_owner.State;
   if(d1State == D1_OWNER_BUY_CONFIRMED || d1State == D1_OWNER_SELL_CONFIRMED)
      journey.StrategicDirection = g_pair_states[pairIndex].d1_major_trend_owner.Direction;

   if(d1State == D1_OWNER_UNRESOLVED)
   {
      journey.Relation = NESTED_UNRESOLVED;
      journey.Reason = "D1_OWNER_UNRESOLVED";
      journey.ConflictSubtype =
         NMJE_ClassifyConflictSubtype(journey.Relation, journey.Reason);
      journey.Maturity =
         NMJE_ClassifyJourneyMaturity(g_pair_states[pairIndex], journey);
      journey.EventPhaseCheckpointDurable = SaveNMJEEventPhaseCheckpoint(
         journey.Pair, false, "", "", "", journey.EventPhase,
         journey.UpdateCandleTime);
      g_nested_journeys[pairIndex] = journey;
      NMJE_PrintCoverageOverlay(journey);
      Print("[N1-NMJE] ", journey.Pair, " REL=UNRESOLVED P=NONE J=- D1=", journey.D1Node.Label,
            " H4=", journey.H4Node.Label, " H1=", journey.H1Node.Label,
            " M15=", journey.M15Node.Label, " R=", journey.Reason);
      return;
   }

   ENUM_NESTED_PARENT_KIND parentKind;
   int parentTF = 0;
   ENUM_SIGNAL_TYPE parentSignal = SIGNAL_NONE;
   ENUM_DIRECTION parentDirection = DIR_NONE;
   datetime parentAnchor = 0;
   string parentEventID = "";
   string parentReason = "";
   bool hadPreviousParent =
      (previousJourney.Pair == journey.Pair && previousJourney.Valid &&
       previousJourney.ParentKind != NESTED_PARENT_NONE &&
       previousJourney.ParentEventID != "" && previousJourney.JourneyID != "");
   bool parentRetained = NMJE_TryRetainPreviousParent(
      g_pair_states[pairIndex], previousJourney, parentKind, parentTF,
      parentSignal, parentDirection, parentAnchor, parentEventID, parentReason);
   bool hasParent = parentRetained;
   if(!hasParent)
      hasParent = NMJE_ResolveParent(g_pair_states[pairIndex], parentKind, parentTF,
                                     parentSignal, parentDirection, parentAnchor,
                                     parentEventID, parentReason);
   journey.ParentRetained = parentRetained;
   journey.ParentSelectionReason = parentRetained
      ? "PREVIOUS_CANONICAL_PARENT_RETAINED"
      : (hasParent
         ? (hadPreviousParent ? "CANONICAL_PARENT_TRANSITION" : "CANONICAL_PARENT_SELECTED")
         : (hadPreviousParent ? "PREVIOUS_PARENT_INVALID_NO_REPLACEMENT" : "NO_PARENT_SELECTED"));

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
      journey.ConflictSubtype =
         NMJE_ClassifyConflictSubtype(journey.Relation, journey.Reason);
      journey.Maturity =
         NMJE_ClassifyJourneyMaturity(g_pair_states[pairIndex], journey);
      journey.EventPhaseCheckpointDurable = SaveNMJEEventPhaseCheckpoint(
         journey.Pair, false, "", "", "", journey.EventPhase,
         journey.UpdateCandleTime);
      g_nested_journeys[pairIndex] = journey;
      NMJE_PrintCoverageOverlay(journey);
      Print("[N1-NMJE] ", journey.Pair, " REL=", NMJE_RelationText(journey.Relation),
            " P=NONE J=- D1=", journey.D1Node.Label, " H4=", journey.H4Node.Label,
            " H1=", journey.H1Node.Label, " M15=", journey.M15Node.Label,
            " PSEL=", journey.ParentSelectionReason,
            " R=", journey.Reason);
      return;
   }

   journey.ParentKind = parentKind;
   journey.ParentTimeframe = parentTF;
   journey.ParentSignal = parentSignal;
   journey.ParentDirection = parentDirection;
   journey.ParentCandleTime = parentAnchor;
   journey.ParentEventID = parentEventID;
   journey.JourneyID = NMJE_BuildJourneyID(journey.Pair, parentKind, parentTF,
                                            parentSignal, parentDirection, parentAnchor);
   journey.Valid = true;
   journey.Resolved = true;

   string currentJourneyHash = SHORT_HASH(journey.JourneyID);
   string currentParentEventHash = journey.ParentEventID;
   string currentD1EventHash = journey.D1Node.CanonicalEventID;
   bool currentPhaseIdentityValid =
      (StringLen(currentJourneyHash) == 16 &&
       StringLen(currentParentEventHash) == 16 &&
       StringLen(currentD1EventHash) == 16);
   bool samePriorIdentity =
      (currentPhaseIdentityValid && priorPhaseHadParent &&
       priorJourneyHash == currentJourneyHash &&
       priorParentEventHash == currentParentEventHash &&
       priorD1EventHash == currentD1EventHash);
   if(priorPhaseKnown && currentPhaseIdentityValid)
   {
      if(priorPhaseUpdateCandle == journey.UpdateCandleTime)
         journey.EventPhase = samePriorIdentity
            ? priorEventPhase : NMJE_EVENT_PHASE_UNRESOLVED;
      else if(priorPhaseUpdateCandle < journey.UpdateCandleTime)
      {
         if(!priorPhaseHadParent)
            journey.EventPhase = NMJE_EVENT_PHASE_FIRST;
         else if(samePriorIdentity)
            journey.EventPhase = NMJE_EVENT_PHASE_CONTINUATION;
         else
            journey.EventPhase = NMJE_EVENT_PHASE_NEW_JOURNEY;
      }
   }
   journey.EventPhaseCheckpointDurable = SaveNMJEEventPhaseCheckpoint(
      journey.Pair, true, currentJourneyHash, currentParentEventHash,
      currentD1EventHash, journey.EventPhase, journey.UpdateCandleTime);

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

   journey.ConflictSubtype =
      NMJE_ClassifyConflictSubtype(journey.Relation, journey.Reason);
   journey.Maturity =
      NMJE_ClassifyJourneyMaturity(g_pair_states[pairIndex], journey);
   // Stage-C2 binds M5 only after immutable parent and journey identities are
   // resolved. Its relation is diagnostic and cannot modify the 4-TF result.
   NMJE_BuildM5Refinement(g_pair_states[pairIndex], journey);
   g_nested_journeys[pairIndex] = journey;
   NMJE_PrintCoverageOverlay(journey);
   Print("[N1-NMJE] ", journey.Pair,
         " REL=", NMJE_RelationText(journey.Relation),
         " SUB=", NMJE_ConflictSubtypeText(journey.ConflictSubtype),
         " MAT=", NMJE_MaturityText(journey.Maturity),
         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " PRETAIN=", journey.ParentRetained ? "Y" : "N",
         " PSEL=", journey.ParentSelectionReason,
         " PHASE=", NMJE_EventPhaseText(journey.EventPhase),
         " PDUR=", journey.EventPhaseCheckpointDurable ? "Y" : "N",
         " PE=", (journey.ParentEventID == "" ? "-" : journey.ParentEventID),
         " J=", journey.JourneyID,
         " D1=", journey.D1Node.Label, "#", (journey.D1Node.CanonicalEventID == "" ? "-" : journey.D1Node.CanonicalEventID),
         " H4=", journey.H4Node.Label, "#", (journey.H4Node.CanonicalEventID == "" ? "-" : journey.H4Node.CanonicalEventID),
         " H1=", journey.H1Node.Label, "#", (journey.H1Node.CanonicalEventID == "" ? "-" : journey.H1Node.CanonicalEventID),
         " M15=", journey.M15Node.Label, "#", (journey.M15Node.CanonicalEventID == "" ? "-" : journey.M15Node.CanonicalEventID),
         " R=", journey.Reason);
   Print("[NMJE-M5-SHADOW] ", journey.Pair,
         " PRESENT=", (journey.M5Refinement.Present ? "Y" : "N"),
         " REL=", NMJE_RelationText(journey.M5Refinement.Relation),
         " SUB=", NMJE_ConflictSubtypeText(journey.M5Refinement.ConflictSubtype),
         " MAT=", NMJE_MaturityText(journey.M5Refinement.Maturity),
         " DIR=", NMJE_DirText(journey.M5Refinement.Direction),
         " CTX=", IntegerToString(journey.M5Refinement.ContextCode),
         " E=", (journey.M5Refinement.EventID == "" ? "-" : journey.M5Refinement.EventID),
         " PE=", (journey.M5Refinement.ParentEventID == "" ? "-" : journey.M5Refinement.ParentEventID),
         " J=", (journey.M5Refinement.JourneyID == "" ? "-" : journey.M5Refinement.JourneyID),
         " R=", journey.M5Refinement.Reason);
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
         " PE=", (journey.ParentEventID == "" ? "-" : journey.ParentEventID),
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
      return (candidate.SequenceType == SIGNAL_RE_ENTRY ||
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
   if(reEntry.ExpiryCandleTime > 0 && reEntry.ExpiryCandleTime < g_processing_time) return;

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
   candidate.Expiry = reEntry.ExpiryCandleTime;
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
   if(reEntry.ExpiryCandleTime > 0 && g_processing_time > reEntry.ExpiryCandleTime) return false;
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

datetime MinPositiveExpiry(datetime a, datetime b)
{
   if(a <= 0) return b;
   if(b <= 0) return a;
   return MathMin(a, b);
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
   datetime expiry = 0;

   if(h1Fresh)
   {
      SetOpportunityREComponent(candidate.Components[componentCount], h1);
      componentCount++;
      expiry = MinPositiveExpiry(expiry, h1.ExpiryCandleTime);
   }

   // Same-cycle M15 is folded into the same cluster when H4 confirms lineage.
   if(m15Fresh && h4Aligned)
   {
      SetOpportunityREComponent(candidate.Components[componentCount], m15);
      componentCount++;
      expiry = MinPositiveExpiry(expiry, m15.ExpiryCandleTime);
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
   candidate.Expiry = expiry;
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
   return 0;
}

// N3 Step-4 shadow phase: freeze provenance only. This helper must never
// decide eligibility or mutate canonical owner state.
bool FreezeNMJEShadowSnapshot(PairState &pairState, BBMA_Decision &decision)
{
   decision.NMJEJourneyID = "";
   decision.NMJEParentEventID = "";
   decision.NMJEParentRetained = false;
   decision.NMJEParentSelectionReason = "";
   decision.NMJEEventPhase = NMJE_EVENT_PHASE_UNRESOLVED;
   decision.NMJEEventPhaseCheckpointDurable = false;
   decision.NMJERelation = NESTED_NOT_APPLICABLE;
   decision.NMJEConflictSubtype = NMJE_CONFLICT_NONE;
   decision.NMJEMaturity = NMJE_MATURITY_NONE;
   decision.NMJEUpdateCandleTime = 0;
   decision.NMJESnapshotPresent = false;
   decision.NMJEStructureMask = 0;
   decision.NMJEStructureCount = 0;
   ZeroMemory(decision.NMJEM5Refinement);
   decision.NMJEM5Refinement.Direction = DIR_NONE;
   decision.NMJEM5Refinement.Relation = NESTED_UNRESOLVED;

   int pairIndex = -1;
   for(int i = 0; i < g_pair_count; i++)
   {
      if(g_pair_states[i].actual_symbol == pairState.actual_symbol)
      {
         pairIndex = i;
         break;
      }
   }
   if(pairIndex < 0) return false;

   NestedJourneyState journey = g_nested_journeys[pairIndex];
   if(journey.Pair != pairState.actual_symbol || journey.UpdateCandleTime <= 0)
      return false;

   decision.NMJEJourneyID = journey.JourneyID;
   decision.NMJEParentEventID = journey.ParentEventID;
   decision.NMJEParentRetained = journey.ParentRetained;
   decision.NMJEParentSelectionReason = journey.ParentSelectionReason;
   decision.NMJEEventPhase = journey.EventPhase;
   decision.NMJEEventPhaseCheckpointDurable =
      journey.EventPhaseCheckpointDurable;
   decision.NMJERelation = journey.Relation;
   decision.NMJEConflictSubtype = journey.ConflictSubtype;
   decision.NMJEMaturity = journey.Maturity;
   decision.NMJEUpdateCandleTime = journey.UpdateCandleTime;
   decision.NMJESnapshotPresent = true;
   decision.NMJEM5Refinement = journey.M5Refinement;
   decision.NMJEStructureMask =
      NMJE_BuildStructureMask(journey, decision.Direction);
   decision.NMJEStructureCount =
      NMJE_CountStructureBits(decision.NMJEStructureMask);
   return true;
}

bool ValidateNMJEShadowSnapshot(int pairIndex, BBMA_Decision &decision,
                                string &reason)
{
   reason = "";
   if(pairIndex < 0 || pairIndex >= g_pair_count)
   {
      reason = "PAIR_INDEX_INVALID";
      return false;
   }
   if(!decision.NMJESnapshotPresent)
   {
      reason = "SNAPSHOT_MISSING";
      return false;
   }

   NestedJourneyState current = g_nested_journeys[pairIndex];
   if(current.Pair != decision.Pair)
   {
      reason = "PAIR_MISMATCH";
      return false;
   }
   if(current.UpdateCandleTime != decision.NMJEUpdateCandleTime)
   {
      reason = "UPDATE_CANDLE_MISMATCH";
      return false;
   }
   if(current.JourneyID != decision.NMJEJourneyID)
   {
      reason = "JOURNEY_ID_MISMATCH";
      return false;
   }
   if(current.ParentEventID != decision.NMJEParentEventID)
   {
      reason = "PARENT_EVENT_ID_MISMATCH";
      return false;
   }
   if(current.Relation != decision.NMJERelation)
   {
      reason = "RELATION_MISMATCH";
      return false;
   }
   if(current.ParentRetained != decision.NMJEParentRetained ||
      current.ParentSelectionReason != decision.NMJEParentSelectionReason)
   {
      reason = "PARENT_STABILITY_METADATA_MISMATCH";
      return false;
   }
   if(current.EventPhase != decision.NMJEEventPhase ||
      current.EventPhaseCheckpointDurable !=
         decision.NMJEEventPhaseCheckpointDurable)
   {
      reason = "EVENT_PHASE_METADATA_MISMATCH";
      return false;
   }
   if(current.ConflictSubtype != decision.NMJEConflictSubtype)
   {
      reason = "CONFLICT_SUBTYPE_MISMATCH";
      return false;
   }
   if(current.Maturity != decision.NMJEMaturity)
   {
      reason = "MATURITY_MISMATCH";
      return false;
   }
   int currentStructureMask =
      NMJE_BuildStructureMask(current, decision.Direction);
   if(currentStructureMask != decision.NMJEStructureMask ||
      NMJE_CountStructureBits(currentStructureMask) != decision.NMJEStructureCount)
   {
      reason = "STRUCTURE_DENSITY_MISMATCH";
      return false;
   }
   NMJEM5RefinementState frozenM5 = decision.NMJEM5Refinement;
   NMJEM5RefinementState currentM5 = current.M5Refinement;
   if(frozenM5.Present != currentM5.Present)
   {
      reason = "M5_PRESENCE_MISMATCH";
      return false;
   }
   if(frozenM5.Present)
   {
      if(!NMJE_M5LineageSnapshotValid(frozenM5) ||
         !NMJE_M5LineageSnapshotValid(currentM5))
      {
         reason = "M5_LINEAGE_INVALID";
         return false;
      }
      if(frozenM5.EventID != currentM5.EventID ||
         frozenM5.ParentEventID != currentM5.ParentEventID ||
         frozenM5.JourneyID != currentM5.JourneyID ||
         frozenM5.Direction != currentM5.Direction ||
         frozenM5.ContextCode != currentM5.ContextCode ||
         frozenM5.ContextStateCode != currentM5.ContextStateCode ||
         frozenM5.EventStartCandleTime != currentM5.EventStartCandleTime ||
         frozenM5.ClosedCandleTime != currentM5.ClosedCandleTime ||
         frozenM5.Relation != currentM5.Relation ||
         frozenM5.ConflictSubtype != currentM5.ConflictSubtype ||
         frozenM5.Maturity != currentM5.Maturity ||
         frozenM5.Reason != currentM5.Reason)
      {
         reason = "M5_SNAPSHOT_MISMATCH";
         return false;
      }
   }
   return true;
}

string NMJE_EntryDisplacementText(ENUM_NMJE_ENTRY_DISPLACEMENT classification)
{
   if(classification == NMJE_DISPLACEMENT_FLAT) return "FLAT";
   if(classification == NMJE_DISPLACEMENT_FAVORABLE) return "FAVORABLE";
   if(classification == NMJE_DISPLACEMENT_ADVERSE) return "ADVERSE";
   return "UNRESOLVED";
}

bool BuildNMJEShadowAttribution(BBMA_Decision &decision,
                                double brokerExecutionPrice,
                                double pointSize,
                                NMJEShadowAttributionState &attribution)
{
   ZeroMemory(attribution);
   attribution.Relation = NESTED_NOT_APPLICABLE;
   attribution.M5Relation = NESTED_UNRESOLVED;
   attribution.M5Direction = DIR_NONE;
   attribution.EntryDisplacementClass = NMJE_DISPLACEMENT_UNRESOLVED;
   if(!decision.NMJESnapshotPresent || decision.NMJEJourneyID == "" ||
      decision.NMJEParentEventID == "")
      return false;

   attribution.JourneyHash = SHORT_HASH(decision.NMJEJourneyID);
   attribution.ParentEventHash = SHORT_HASH(decision.NMJEParentEventID);
   attribution.ParentRetained = decision.NMJEParentRetained;
   attribution.ParentSelectionReasonHash =
      SHORT_HASH(decision.NMJEParentSelectionReason);
   attribution.EventPhase = decision.NMJEEventPhase;
   attribution.EventPhaseCheckpointDurable =
      decision.NMJEEventPhaseCheckpointDurable;
   if(StringLen(attribution.JourneyHash) != 16 ||
      StringLen(attribution.ParentEventHash) != 16)
      return false;
   if(StringLen(attribution.ParentSelectionReasonHash) != 16)
      return false;
   if(attribution.EventPhase < NMJE_EVENT_PHASE_UNRESOLVED ||
      attribution.EventPhase > NMJE_EVENT_PHASE_NEW_JOURNEY)
      return false;

   attribution.Present = true;
   attribution.Relation = decision.NMJERelation;
   attribution.ConflictSubtype = decision.NMJEConflictSubtype;
   attribution.Maturity = decision.NMJEMaturity;
   attribution.StructureMask = decision.NMJEStructureMask;
   attribution.StructureCount = decision.NMJEStructureCount;
   attribution.RequirementCompleteness = decision.NMJERequirementCompleteness;
   attribution.SequenceCompleteness = decision.NMJESequenceCompleteness;

   // P10 is post-selection/post-execution research telemetry only. Directional
   // positive means price moved farther in the trade direction.
   double pipValue = GetPipValue(decision.Pair);
   if(decision.NMJEEntryDisplacementSourcePresent &&
      decision.NMJESourceConfirmationPrice > 0.0 &&
      decision.NMJEStructuralAnchorPrice > 0.0 &&
      decision.EntryPrice > 0.0 && brokerExecutionPrice > 0.0 &&
      pointSize > 0.0 && pipValue > 0.0 &&
      (decision.Direction == DIR_BUY || decision.Direction == DIR_SELL))
   {
      double directionSign = (decision.Direction == DIR_BUY) ? 1.0 : -1.0;
      double validationToExecution =
         directionSign * (brokerExecutionPrice - decision.EntryPrice);
      attribution.EntryDisplacementPresent = true;
      attribution.SourceConfirmationPrice = decision.NMJESourceConfirmationPrice;
      attribution.ValidationEntryPrice = decision.EntryPrice;
      attribution.BrokerExecutionPrice = brokerExecutionPrice;
      attribution.StructuralAnchorPrice = decision.NMJEStructuralAnchorPrice;
      attribution.ConfirmationToValidationPips =
         directionSign * (decision.EntryPrice -
                          decision.NMJESourceConfirmationPrice) / pipValue;
      attribution.ValidationToExecutionPips = validationToExecution / pipValue;
      attribution.ExecutionFromAnchorPips =
         directionSign * (brokerExecutionPrice -
                          decision.NMJEStructuralAnchorPrice) / pipValue;
      if(MathAbs(validationToExecution) <= pointSize * 0.5)
         attribution.EntryDisplacementClass = NMJE_DISPLACEMENT_FLAT;
      else if(validationToExecution < 0.0)
         attribution.EntryDisplacementClass = NMJE_DISPLACEMENT_FAVORABLE;
      else
         attribution.EntryDisplacementClass = NMJE_DISPLACEMENT_ADVERSE;
   }

   NMJEM5RefinementState m5 = decision.NMJEM5Refinement;
   if(m5.Present && NMJE_M5LineageSnapshotValid(m5))
   {
      attribution.M5Present = true;
      attribution.M5EventHash = SHORT_HASH(m5.EventID);
      attribution.M5Relation = m5.Relation;
      attribution.M5ConflictSubtype = m5.ConflictSubtype;
      attribution.M5Maturity = m5.Maturity;
      attribution.M5Direction = m5.Direction;
      attribution.M5ContextCode = m5.ContextCode;
      attribution.M5ContextStateCode = m5.ContextStateCode;
      attribution.M5EventStartCandleTime = m5.EventStartCandleTime;
      attribution.M5ClosedCandleTime = m5.ClosedCandleTime;
      attribution.M5ReasonHash = SHORT_HASH(m5.Reason);
      if(StringLen(attribution.M5EventHash) != 16 ||
         StringLen(attribution.M5ReasonHash) != 16)
      {
         ZeroMemory(attribution);
         attribution.Relation = NESTED_NOT_APPLICABLE;
         attribution.M5Relation = NESTED_UNRESOLVED;
         attribution.M5Direction = DIR_NONE;
         return false;
      }
   }
   return true;
}

string NMJEAttributionGVBase(int ticket)
{
   return "BBXA|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(ticket) + "|";
}

bool NMJEStoreHex16(string base, string prefix, string value)
{
   if(StringLen(value) != 16) return false;
   for(int i = 0; i < 4; i++)
   {
      double part = Hex4ToNumber(StringSubstr(value, i * 4, 4));
      if(part < 0 || GlobalVariableSet(base + prefix + IntegerToString(i), part) == 0)
         return false;
   }
   return true;
}

bool NMJELoadHex16(string base, string prefix, string &value)
{
   value = "";
   for(int i = 0; i < 4; i++)
   {
      string key = base + prefix + IntegerToString(i);
      if(!GlobalVariableCheck(key)) return false;
      string part = NumberToHex4(GlobalVariableGet(key));
      if(part == "") return false;
      value += part;
   }
   return (StringLen(value) == 16);
}

bool LoadNMJEShadowAttribution(TradeInfo &info)
{
   ZeroMemory(info.nmje_attribution);
   info.nmje_attribution.Relation = NESTED_NOT_APPLICABLE;
   info.nmje_attribution.M5Relation = NESTED_UNRESOLVED;
   info.nmje_attribution.M5Direction = DIR_NONE;
   info.nmje_attribution.EntryDisplacementClass = NMJE_DISPLACEMENT_UNRESOLVED;
   info.nmje_attribution.EventPhase = NMJE_EVENT_PHASE_UNRESOLVED;
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0 ||
      StringLen(info.execution_hash) != 16)
      return false;

   string base = NMJEAttributionGVBase(info.ticket);
   string fixedKeys[16] = {"V","M","O","R","C","JM","PR","M5","MC","M5C","M5M","M5S","SM","SC","RQ","SQ"};
   for(int i = 0; i < 16; i++)
      if(!GlobalVariableCheck(base + fixedKeys[i])) return false;
   int attributionVersion = (int)GlobalVariableGet(base + "V");
   if((attributionVersion != 1 && attributionVersion != 2 &&
       attributionVersion != 3) ||
      (int)GlobalVariableGet(base + "M") != info.magic_number ||
      (datetime)((int)GlobalVariableGet(base + "O")) != info.open_time)
      return false;

   string storedExecutionHash = "";
   if(!NMJELoadHex16(base, "X", storedExecutionHash) ||
      storedExecutionHash != info.execution_hash)
      return false;
   if(!NMJELoadHex16(base, "J", info.nmje_attribution.JourneyHash) ||
      !NMJELoadHex16(base, "P", info.nmje_attribution.ParentEventHash) ||
      !NMJELoadHex16(base, "A", info.nmje_attribution.ParentSelectionReasonHash))
      return false;
   info.nmje_attribution.ParentRetained =
      (GlobalVariableGet(base + "PR") > 0.5);

   info.nmje_attribution.Relation =
      (ENUM_NESTED_RELATION)((int)GlobalVariableGet(base + "R"));
   info.nmje_attribution.ConflictSubtype =
      (ENUM_NMJE_CONFLICT_SUBTYPE)((int)GlobalVariableGet(base + "C"));
   info.nmje_attribution.Maturity =
      (ENUM_NMJE_JOURNEY_MATURITY)((int)GlobalVariableGet(base + "JM"));
   info.nmje_attribution.StructureMask = (int)GlobalVariableGet(base + "SM");
   info.nmje_attribution.StructureCount = (int)GlobalVariableGet(base + "SC");
   info.nmje_attribution.RequirementCompleteness = (int)GlobalVariableGet(base + "RQ");
   info.nmje_attribution.SequenceCompleteness = (int)GlobalVariableGet(base + "SQ");
   if(info.nmje_attribution.Relation < NESTED_BUILDING ||
      info.nmje_attribution.Relation > NESTED_UNRESOLVED ||
      info.nmje_attribution.ConflictSubtype < NMJE_CONFLICT_NONE ||
      info.nmje_attribution.ConflictSubtype > NMJE_CONFLICT_UNRESOLVED_PROVENANCE ||
      (info.nmje_attribution.Relation == NESTED_CONFLICT &&
       info.nmje_attribution.ConflictSubtype == NMJE_CONFLICT_NONE) ||
      info.nmje_attribution.Maturity < NMJE_MATURITY_OWNER_ONLY ||
      info.nmje_attribution.Maturity > NMJE_MATURITY_UNRESOLVED ||
      info.nmje_attribution.StructureMask < 0 ||
      info.nmje_attribution.StructureMask > 31 ||
      info.nmje_attribution.StructureCount < 0 ||
      info.nmje_attribution.StructureCount > 5 ||
      NMJE_CountStructureBits(info.nmje_attribution.StructureMask) !=
         info.nmje_attribution.StructureCount ||
      info.nmje_attribution.RequirementCompleteness < 0 ||
      info.nmje_attribution.SequenceCompleteness < 0)
      return false;

   info.nmje_attribution.M5Present = (GlobalVariableGet(base + "M5") > 0.5);
   info.nmje_attribution.M5ContextCode = (int)GlobalVariableGet(base + "MC");
   info.nmje_attribution.M5ConflictSubtype =
      (ENUM_NMJE_CONFLICT_SUBTYPE)((int)GlobalVariableGet(base + "M5C"));
   info.nmje_attribution.M5Maturity =
      (ENUM_NMJE_JOURNEY_MATURITY)((int)GlobalVariableGet(base + "M5M"));
   info.nmje_attribution.M5ContextStateCode =
      (int)GlobalVariableGet(base + "M5S");
   if(info.nmje_attribution.M5Present)
   {
      string m5Keys[4] = {"MR","MD","MS","MT"};
      for(int k = 0; k < 4; k++)
         if(!GlobalVariableCheck(base + m5Keys[k])) return false;
      if(!NMJELoadHex16(base, "E", info.nmje_attribution.M5EventHash) ||
         !NMJELoadHex16(base, "Q", info.nmje_attribution.M5ReasonHash))
         return false;
      info.nmje_attribution.M5Relation =
         (ENUM_NESTED_RELATION)((int)GlobalVariableGet(base + "MR"));
      info.nmje_attribution.M5Direction =
         (ENUM_DIRECTION)((int)GlobalVariableGet(base + "MD"));
      info.nmje_attribution.M5EventStartCandleTime =
         (datetime)((int)GlobalVariableGet(base + "MS"));
      info.nmje_attribution.M5ClosedCandleTime =
         (datetime)((int)GlobalVariableGet(base + "MT"));
      if(info.nmje_attribution.M5Relation < NESTED_BUILDING ||
         info.nmje_attribution.M5Relation > NESTED_UNRESOLVED ||
         info.nmje_attribution.M5ConflictSubtype < NMJE_CONFLICT_NONE ||
         info.nmje_attribution.M5ConflictSubtype > NMJE_CONFLICT_UNRESOLVED_PROVENANCE ||
         (info.nmje_attribution.M5Relation == NESTED_CONFLICT &&
          info.nmje_attribution.M5ConflictSubtype == NMJE_CONFLICT_NONE) ||
         info.nmje_attribution.M5Maturity < NMJE_MATURITY_EXTREME_DEVELOPING ||
         info.nmje_attribution.M5Maturity > NMJE_MATURITY_REENTRY_CONFIRMED ||
         (info.nmje_attribution.M5Direction != DIR_BUY &&
          info.nmje_attribution.M5Direction != DIR_SELL) ||
         info.nmje_attribution.M5ContextCode <= NMJE_M5_CONTEXT_NONE ||
         info.nmje_attribution.M5ContextStateCode <= 0 ||
         info.nmje_attribution.M5EventStartCandleTime <= 0 ||
         info.nmje_attribution.M5ClosedCandleTime <
            info.nmje_attribution.M5EventStartCandleTime)
         return false;
   }

   // Version 1 remains readable for in-flight P4-P8 research records. Version
   // 2 adds P10 only; missing P10 data never changes live recovery state.
   if(attributionVersion >= 2)
   {
      string p10Keys[9] = {"DP","DC","SP","VP","EP","SA","CV","VE","EA"};
      for(int p10 = 0; p10 < 9; p10++)
         if(!GlobalVariableCheck(base + p10Keys[p10])) return false;
      info.nmje_attribution.EntryDisplacementPresent =
         (GlobalVariableGet(base + "DP") > 0.5);
      info.nmje_attribution.EntryDisplacementClass =
         (ENUM_NMJE_ENTRY_DISPLACEMENT)((int)GlobalVariableGet(base + "DC"));
      info.nmje_attribution.SourceConfirmationPrice = GlobalVariableGet(base + "SP");
      info.nmje_attribution.ValidationEntryPrice = GlobalVariableGet(base + "VP");
      info.nmje_attribution.BrokerExecutionPrice = GlobalVariableGet(base + "EP");
      info.nmje_attribution.StructuralAnchorPrice = GlobalVariableGet(base + "SA");
      info.nmje_attribution.ConfirmationToValidationPips = GlobalVariableGet(base + "CV");
      info.nmje_attribution.ValidationToExecutionPips = GlobalVariableGet(base + "VE");
      info.nmje_attribution.ExecutionFromAnchorPips = GlobalVariableGet(base + "EA");
      if(info.nmje_attribution.EntryDisplacementPresent &&
         (info.nmje_attribution.EntryDisplacementClass < NMJE_DISPLACEMENT_FLAT ||
          info.nmje_attribution.EntryDisplacementClass > NMJE_DISPLACEMENT_ADVERSE ||
          info.nmje_attribution.SourceConfirmationPrice <= 0.0 ||
          info.nmje_attribution.ValidationEntryPrice <= 0.0 ||
          info.nmje_attribution.BrokerExecutionPrice <= 0.0 ||
          info.nmje_attribution.StructuralAnchorPrice <= 0.0))
         return false;
   }

   if(attributionVersion >= 3)
   {
      if(!GlobalVariableCheck(base + "F") ||
         !GlobalVariableCheck(base + "FD"))
         return false;
      info.nmje_attribution.EventPhase =
         (ENUM_NMJE_EVENT_PHASE)((int)GlobalVariableGet(base + "F"));
      info.nmje_attribution.EventPhaseCheckpointDurable =
         (GlobalVariableGet(base + "FD") > 0.5);
      if(info.nmje_attribution.EventPhase < NMJE_EVENT_PHASE_UNRESOLVED ||
         info.nmje_attribution.EventPhase > NMJE_EVENT_PHASE_NEW_JOURNEY)
         return false;
   }

   info.nmje_attribution.Present = true;
   info.nmje_attribution.Durable = true;
   return true;
}

bool SaveNMJEShadowAttribution(TradeInfo &info)
{
   NMJEShadowAttributionState a = info.nmje_attribution;
   if(!a.Present || info.ticket <= 0 || info.magic_number <= 0 ||
      info.open_time <= 0 || StringLen(info.execution_hash) != 16 ||
      StringLen(a.JourneyHash) != 16 || StringLen(a.ParentEventHash) != 16 ||
      StringLen(a.ParentSelectionReasonHash) != 16)
      return false;
   if(a.EventPhase < NMJE_EVENT_PHASE_UNRESOLVED ||
      a.EventPhase > NMJE_EVENT_PHASE_NEW_JOURNEY)
      return false;
   if(a.EntryDisplacementPresent &&
      (a.EntryDisplacementClass < NMJE_DISPLACEMENT_FLAT ||
       a.EntryDisplacementClass > NMJE_DISPLACEMENT_ADVERSE ||
       a.SourceConfirmationPrice <= 0.0 || a.ValidationEntryPrice <= 0.0 ||
       a.BrokerExecutionPrice <= 0.0 || a.StructuralAnchorPrice <= 0.0))
      return false;

   string base = NMJEAttributionGVBase(info.ticket);
   GlobalVariableDel(base + "V");
   if(GlobalVariableSet(base + "M", (double)info.magic_number) == 0) return false;
   if(GlobalVariableSet(base + "O", (double)info.open_time) == 0) return false;
   if(GlobalVariableSet(base + "R", (double)a.Relation) == 0) return false;
   if(GlobalVariableSet(base + "C", (double)a.ConflictSubtype) == 0) return false;
   if(GlobalVariableSet(base + "JM", (double)a.Maturity) == 0) return false;
   if(GlobalVariableSet(base + "PR", a.ParentRetained ? 1.0 : 0.0) == 0) return false;
   if(GlobalVariableSet(base + "M5", a.M5Present ? 1.0 : 0.0) == 0) return false;
   if(GlobalVariableSet(base + "MC", (double)a.M5ContextCode) == 0) return false;
   if(GlobalVariableSet(base + "M5C", (double)a.M5ConflictSubtype) == 0) return false;
   if(GlobalVariableSet(base + "M5M", (double)a.M5Maturity) == 0) return false;
   if(GlobalVariableSet(base + "M5S", (double)a.M5ContextStateCode) == 0) return false;
   if(GlobalVariableSet(base + "SM", (double)a.StructureMask) == 0) return false;
   if(GlobalVariableSet(base + "SC", (double)a.StructureCount) == 0) return false;
   if(GlobalVariableSet(base + "RQ", (double)a.RequirementCompleteness) == 0) return false;
   if(GlobalVariableSet(base + "SQ", (double)a.SequenceCompleteness) == 0) return false;
   if(GlobalVariableSet(base + "DP", a.EntryDisplacementPresent ? 1.0 : 0.0) == 0) return false;
   if(GlobalVariableSet(base + "DC", (double)a.EntryDisplacementClass) == 0) return false;
   if(GlobalVariableSet(base + "SP", a.SourceConfirmationPrice) == 0) return false;
   if(GlobalVariableSet(base + "VP", a.ValidationEntryPrice) == 0) return false;
   if(GlobalVariableSet(base + "EP", a.BrokerExecutionPrice) == 0) return false;
   if(GlobalVariableSet(base + "SA", a.StructuralAnchorPrice) == 0) return false;
   if(GlobalVariableSet(base + "CV", a.ConfirmationToValidationPips) == 0) return false;
   if(GlobalVariableSet(base + "VE", a.ValidationToExecutionPips) == 0) return false;
   if(GlobalVariableSet(base + "EA", a.ExecutionFromAnchorPips) == 0) return false;
   if(GlobalVariableSet(base + "F", (double)a.EventPhase) == 0) return false;
   if(GlobalVariableSet(base + "FD", a.EventPhaseCheckpointDurable ? 1.0 : 0.0) == 0) return false;
   if(!NMJEStoreHex16(base, "X", info.execution_hash) ||
      !NMJEStoreHex16(base, "J", a.JourneyHash) ||
      !NMJEStoreHex16(base, "P", a.ParentEventHash) ||
      !NMJEStoreHex16(base, "A", a.ParentSelectionReasonHash))
      return false;
   if(a.M5Present)
   {
      if(StringLen(a.M5EventHash) != 16 || StringLen(a.M5ReasonHash) != 16)
         return false;
      if(GlobalVariableSet(base + "MR", (double)a.M5Relation) == 0) return false;
      if(GlobalVariableSet(base + "MD", (double)a.M5Direction) == 0) return false;
      if(GlobalVariableSet(base + "MS", (double)a.M5EventStartCandleTime) == 0) return false;
      if(GlobalVariableSet(base + "MT", (double)a.M5ClosedCandleTime) == 0) return false;
      if(!NMJEStoreHex16(base, "E", a.M5EventHash) ||
         !NMJEStoreHex16(base, "Q", a.M5ReasonHash))
         return false;
   }
   if(GlobalVariableSet(base + "V", 3.0) == 0) return false;
   GlobalVariablesFlush();

   TradeInfo verify;
   ZeroMemory(verify);
   verify.ticket = info.ticket;
   verify.magic_number = info.magic_number;
   verify.open_time = info.open_time;
   verify.execution_hash = info.execution_hash;
   if(!LoadNMJEShadowAttribution(verify)) return false;
   info.nmje_attribution.Durable = true;
   return (verify.nmje_attribution.JourneyHash == a.JourneyHash &&
           verify.nmje_attribution.ParentEventHash == a.ParentEventHash &&
           verify.nmje_attribution.ParentRetained == a.ParentRetained &&
           verify.nmje_attribution.ParentSelectionReasonHash == a.ParentSelectionReasonHash &&
           verify.nmje_attribution.Relation == a.Relation &&
           verify.nmje_attribution.ConflictSubtype == a.ConflictSubtype &&
           verify.nmje_attribution.Maturity == a.Maturity &&
           verify.nmje_attribution.StructureMask == a.StructureMask &&
           verify.nmje_attribution.StructureCount == a.StructureCount &&
           verify.nmje_attribution.RequirementCompleteness == a.RequirementCompleteness &&
           verify.nmje_attribution.SequenceCompleteness == a.SequenceCompleteness &&
           verify.nmje_attribution.EventPhase == a.EventPhase &&
           verify.nmje_attribution.EventPhaseCheckpointDurable ==
              a.EventPhaseCheckpointDurable &&
           verify.nmje_attribution.EntryDisplacementPresent == a.EntryDisplacementPresent &&
           (!a.EntryDisplacementPresent ||
            (verify.nmje_attribution.EntryDisplacementClass == a.EntryDisplacementClass &&
             verify.nmje_attribution.SourceConfirmationPrice == a.SourceConfirmationPrice &&
             verify.nmje_attribution.ValidationEntryPrice == a.ValidationEntryPrice &&
             verify.nmje_attribution.BrokerExecutionPrice == a.BrokerExecutionPrice &&
             verify.nmje_attribution.StructuralAnchorPrice == a.StructuralAnchorPrice &&
             verify.nmje_attribution.ConfirmationToValidationPips == a.ConfirmationToValidationPips &&
             verify.nmje_attribution.ValidationToExecutionPips == a.ValidationToExecutionPips &&
             verify.nmje_attribution.ExecutionFromAnchorPips == a.ExecutionFromAnchorPips)) &&
           verify.nmje_attribution.M5Present == a.M5Present &&
           (!a.M5Present ||
            (verify.nmje_attribution.M5EventHash == a.M5EventHash &&
             verify.nmje_attribution.M5ReasonHash == a.M5ReasonHash &&
             verify.nmje_attribution.M5Relation == a.M5Relation &&
             verify.nmje_attribution.M5ConflictSubtype == a.M5ConflictSubtype &&
             verify.nmje_attribution.M5Maturity == a.M5Maturity &&
             verify.nmje_attribution.M5Direction == a.M5Direction &&
             verify.nmje_attribution.M5ContextCode == a.M5ContextCode &&
             verify.nmje_attribution.M5ContextStateCode == a.M5ContextStateCode &&
             verify.nmje_attribution.M5EventStartCandleTime == a.M5EventStartCandleTime &&
             verify.nmje_attribution.M5ClosedCandleTime == a.M5ClosedCandleTime)));
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

   if(EntryMode == 1 && (buyCount > 0 || sellCount > 0))
      Print("[P3M1][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));
   if(EntryMode == 2 && (buyCount > 0 || sellCount > 0))
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
   decision.NMJERequirementCompleteness = selected.RequirementCompleteness;
   decision.NMJESequenceCompleteness = selected.SequenceCompleteness;
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

   // Shadow-only: absence/mismatch is diagnostic and MUST NOT alter selection.
   FreezeNMJEShadowSnapshot(pairState, decision);

   decision.DecisionID = GenerateDecisionID(decision.Pair, decision.CandleTime,
                                             decision.Direction,
                                             decision.SignalType,
                                             decision.SequenceHash);
   if(EntryMode == 1)
      Print("[P3M1][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " D1State=", EnumToString(decision.D1OwnerState),
            " D1Candle=", TimeToString(decision.D1OwnerCandleTime),
            " Candle=", TimeToString(decision.CandleTime),
            " DecisionID=", decision.DecisionID);
   if(EntryMode == 2)
      Print("[P3M2][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " D1State=", EnumToString(decision.D1OwnerState),
            " D1Candle=", TimeToString(decision.D1OwnerCandleTime),
            " Candle=", TimeToString(decision.CandleTime),
            " Components=", decision.ComponentCount,
            " DecisionID=", decision.DecisionID);
}

//+------------------------------------------------------------------+
//| MODULE 16: CONFLICT & INVALIDATION ENGINE                        |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsExtremeStateExpired(Signal &extreme, datetime currentTime)
{
   if(extreme.CandleTime <= 0 || extreme.Timeframe <= 0)
      return false;

   datetime expiry = extreme.CandleTime +
                     (MaxWaitBars_Extreme * extreme.Timeframe * 60);
   return (currentTime > expiry);
}

void UpdatePersistentExtremeState(Signal &matureExtreme, Signal &state)
{
   // M08 lifecycle owns RAW/reversal/retest/invalidation semantics. M16 keeps
   // only the existing project component-freshness overlay.
   if(!matureExtreme.Valid)
   {
      ZeroMemory(state);
      return;
   }

   state = matureExtreme;
   if(IsExtremeStateExpired(state, g_processing_time))
   {
      state.Valid = false;
      state.Reason = "Extreme component expired by timeframe-aware project window";
   }
}

bool IsPersistentExtremeComponentValid(PairState &pairState,
                                       ComponentIdentity &component,
                                       bool &expired)
{
   expired = false;
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

   if(IsExtremeStateExpired(state, g_processing_time))
   {
      expired = true;
      return false;
   }

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

   if(reEntry.ExpiryCandleTime > 0 && g_processing_time > reEntry.ExpiryCandleTime)
   {
      expired = true;
      return false;
   }

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

   // N3 shadow comparison only. No rejection is permitted from this result.
   string nmjeShadowReason = "";
   bool nmjeShadowMatch = ValidateNMJEShadowSnapshot(pairIndex, decision,
                                                      nmjeShadowReason);
   if(DebugLevel >= DBG_SIGNAL)
      Print("[N3-NMJE-SHADOW][M16] Pair=", decision.Pair,
            " DecisionID=", decision.DecisionID,
            " Match=", nmjeShadowMatch ? "Y" : "N",
            " Relation=", NMJE_RelationText(decision.NMJERelation),
            " Subtype=", NMJE_ConflictSubtypeText(decision.NMJEConflictSubtype),
            " Maturity=", NMJE_MaturityText(decision.NMJEMaturity),
            " StructureMask=", IntegerToString(decision.NMJEStructureMask),
            " StructureCount=", IntegerToString(decision.NMJEStructureCount),
            " Req=", IntegerToString(decision.NMJERequirementCompleteness),
            " Seq=", IntegerToString(decision.NMJESequenceCompleteness),
            " Journey=", decision.NMJEJourneyID == "" ? "-" : decision.NMJEJourneyID,
            " ParentEvent=", decision.NMJEParentEventID == "" ? "-" : decision.NMJEParentEventID,
            " ParentRetained=", decision.NMJEParentRetained ? "Y" : "N",
            " ParentSelection=", decision.NMJEParentSelectionReason,
            " Reason=", nmjeShadowMatch ? "MATCH" : nmjeShadowReason);

   decision.DecisionState = DEC_VALIDATED;
   decision.RejectionReason = REJ_NONE;
   if(EntryMode == 1)
      Print("[P3M1][M16_PASS] DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Candle=", TimeToString(decision.CandleTime));
   if(EntryMode == 2)
      Print("[P3M2][M16_PASS] DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Candle=", TimeToString(decision.CandleTime));
}

//+------------------------------------------------------------------+
//| MODULE 17: SL/TP VALIDATION                                      |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool IsApprovedSLTPSourceComponent(BBMA_Decision &decision,
                                   ComponentIdentity &source)
{
   if(!decision.HasSLTPSourceComponent) return false;
   if(source.ComponentType != SIGNAL_RE_ENTRY) return false;
   if(source.Direction != decision.Direction) return false;
   if(source.CandleTime <= 0) return false;

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
                                        double &confirmationWick,
                                        double &sourceConfirmationPrice)
{
   anchor = 0.0;
   startTime = 0;
   confirmationTime = 0;
   confirmationWick = 0.0;
   sourceConfirmationPrice = 0.0;

   ReEntryData reEntry;
   if(!ResolveMatchingReEntryLifecycle(pair, source, reEntry)) return false;

   startTime = reEntry.StartCandleTime;
   confirmationTime = reEntry.ConfirmationCandle;
   sourceConfirmationPrice = reEntry.EntryPrice;
   if(sourceConfirmationPrice <= 0.0) return false;

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
   decision.NMJEEntryDisplacementSourcePresent = false;
   decision.NMJESourceConfirmationPrice = 0.0;
   decision.NMJEStructuralAnchorPrice = 0.0;
   if(!IsApprovedSLTPSourceComponent(decision,
                                     decision.SLTPSourceComponent))
      return false;

   bool d1TPWLifecycle = IsD1TPWLifecycleIdentity(decision);
   if(d1TPWLifecycle && !EnableD1TPWLifecycle)
      return false; // never execute EXTREME_TPW with the legacy RE outer-BB TP
   d1TPWLifecycle = d1TPWLifecycle && EnableD1TPWLifecycle;
   bool c044Lifecycle = EnableC044Lifecycle && !d1TPWLifecycle;
   bool targetlessLifecycle = (d1TPWLifecycle || c044Lifecycle);

   double structuralAnchor = 0.0;
   datetime structuralStart = 0;
   datetime structuralConfirmation = 0;
   double confirmationWick = 0.0;
   double sourceConfirmationPrice = 0.0;
   double destination = 0.0;
   if(!ResolveSourceOwnedStructuralAnchor(decision.Pair,
                                          decision.SLTPSourceComponent,
                                          decision.Direction,
                                          structuralAnchor,
                                          structuralStart,
                                          structuralConfirmation,
                                          confirmationWick,
                                          sourceConfirmationPrice))
      return false;

   // C044 is intentionally fail-safe gated OFF until M23/M24 lifecycle support
   // is complete. While OFF, preserve the v4.52 static destination exactly.
   if(!targetlessLifecycle)
   {
      if(!ResolveApprovedBBDestination(decision.Pair,
                                       decision.SLTPSourceComponent,
                                       decision.Direction,
                                       destination))
         return false;

      if(decision.Direction == DIR_BUY && destination <= decision.EntryPrice)
         return false;
      if(decision.Direction == DIR_SELL && destination >= decision.EntryPrice)
         return false;
   }

   if(snapshot.Point <= 0.0 || decision.EntryPrice <= 0.0) return false;

   double safetyBuffer = snapshot.Point;
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
   decision.NMJEEntryDisplacementSourcePresent = true;
   decision.NMJESourceConfirmationPrice = sourceConfirmationPrice;
   decision.NMJEStructuralAnchorPrice = structuralAnchor;

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
            " D1TPW=", decision.D1TPWLifecycleManaged ? "Y" : "N");
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

      // Targetless lifecycle has no deterministic reward coordinate.
      // Never manufacture one merely to satisfy an explicitly enabled MinRR.
      if(MinRRRatio > 0.0)
      {
         rejection = REJ_INVALID_RR;
         return false;
      }

      double closePrice = GetDirectionalClosePrice(snapshot, decision.Direction);
      double minDistance = snapshot.StopLevel * snapshot.Point;
      if(closePrice <= 0.0)
      {
         rejection = REJ_MARKET_PRICE_INVALID;
         return false;
      }
      if(minDistance > 0.0 && MathAbs(decision.StopLoss - closePrice) < minDistance)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

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

   double closePrice = GetDirectionalClosePrice(snapshot, decision.Direction);
   double minDistance = snapshot.StopLevel * snapshot.Point;
   if(closePrice <= 0.0)
   {
      rejection = REJ_MARKET_PRICE_INVALID;
      return false;
   }

   if(minDistance > 0.0)
   {
      if(MathAbs(decision.StopLoss - closePrice) < minDistance)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }
      if(MathAbs(decision.TakeProfit - closePrice) < minDistance)
      {
         rejection = REJ_INVALID_TP;
         return false;
      }
   }

   decision.StopLossPoints = slDistance / snapshot.Point;
   return true;
}

bool ValidateStopLevel(double price, string pair, ENUM_DIRECTION direction)
{
   int stopLevel = GetStopLevel(pair);
   double point = GetPointSize(pair);
   if(stopLevel <= 0) return true;
   if(point <= 0.0) return false;

   double minDist = stopLevel * point;
   double currentPrice = (direction == DIR_BUY)
      ? MarketInfo(pair, MODE_BID)
      : (direction == DIR_SELL ? MarketInfo(pair, MODE_ASK) : 0.0);
   if(currentPrice <= 0.0) return false;
   return (MathAbs(price - currentPrice) >= minDist);
}

bool ValidateFreezeLevel(double price, string pair, ENUM_DIRECTION direction)
{
   int freezeLevel = GetFreezeLevel(pair);
   double point = GetPointSize(pair);
   if(freezeLevel <= 0) return true;
   if(point <= 0.0) return false;

   double minDist = freezeLevel * point;
   double currentPrice = (direction == DIR_BUY)
      ? MarketInfo(pair, MODE_BID)
      : (direction == DIR_SELL ? MarketInfo(pair, MODE_ASK) : 0.0);
   if(currentPrice <= 0.0) return false;
   return (MathAbs(price - currentPrice) >= minDist);
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

double CalculateBasketLossPercent_EA()
{
   double floatingLoss = 0;
   
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
      {
         if(OrderCloseTime() != 0) continue;
         double profit = OrderProfit() + OrderSwap() + OrderCommission();
         if(profit < 0)
            floatingLoss += MathAbs(profit);
      }
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

   double basketLoss = CalculateBasketLossPercent_EA();
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

bool IsLiveEAOwnedPortfolioTrade(int monitoredIndex)
{
   if(monitoredIndex < 0 || monitoredIndex >= g_monitored_count) return false;
   if(!OrderSelect(g_monitored_trades[monitoredIndex].ticket, SELECT_BY_TICKET)) return false;
   if(OrderCloseTime() != 0) return false;

   int pairIdx = FindPairStateIndex(g_monitored_trades[monitoredIndex].pair);
   if(pairIdx < 0) return false;

   int expectedMagic = g_pair_states[pairIdx].magic_number;
   if(expectedMagic <= 0) return false;
   if(g_monitored_trades[monitoredIndex].magic_number != expectedMagic) return false;
   if(OrderMagicNumber() != expectedMagic) return false;
   return true;
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
      if(!IsLiveEAOwnedPortfolioTrade(i)) continue;

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
      if(IsLiveEAOwnedPortfolioTrade(i)) count++;
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
   if(g_portfolio_emergency_close_requested)
   {
      if(BrokerConfirmsNoLiveEAOwnedOrders())
         g_portfolio_emergency_close_requested = false;
      return;
   }

   if(BasketLossPercent > 0 && CalculateBasketLossPercent_EA() >= BasketLossPercent)
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
         if(!IsLiveEAOwnedPortfolioTrade(i)) continue;
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
         if(!IsLiveEAOwnedPortfolioTrade(i)) continue;
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

   Print("[N2-NMJE-OUT] PAIR=", info.pair,
         " TICKET=", IntegerToString(info.ticket),
         " DID=", decisionToken,
         " DIDH=", decisionHash,
         " NET=", DoubleToString(netProfit, 8),
         " CLOSE=", IntegerToString((int)OrderCloseTime()),
         " REC=", EnumToString(info.recovery_state));
   Print("[NMJE-P4-OUT] PAIR=", info.pair,
         " TICKET=", IntegerToString(info.ticket),
         " DIDH=", decisionHash,
         " ATTR=", info.nmje_attribution.Present ? "Y" : "N",
         " DUR=", info.nmje_attribution.Durable ? "Y" : "N",
         " JH=", info.nmje_attribution.JourneyHash == "" ? "-" : info.nmje_attribution.JourneyHash,
         " PH=", info.nmje_attribution.ParentEventHash == "" ? "-" : info.nmje_attribution.ParentEventHash,
         " PR=", info.nmje_attribution.ParentRetained ? "Y" : "N",
         " PAH=", info.nmje_attribution.ParentSelectionReasonHash == "" ? "-" : info.nmje_attribution.ParentSelectionReasonHash,
         " REL=", NMJE_RelationText(info.nmje_attribution.Relation),
         " SUB=", NMJE_ConflictSubtypeText(info.nmje_attribution.ConflictSubtype),
         " MAT=", NMJE_MaturityText(info.nmje_attribution.Maturity),
         " M5=", info.nmje_attribution.M5Present ? "Y" : "N",
         " M5E=", info.nmje_attribution.M5EventHash == "" ? "-" : info.nmje_attribution.M5EventHash,
         " M5REL=", NMJE_RelationText(info.nmje_attribution.M5Relation),
         " M5SUB=", NMJE_ConflictSubtypeText(info.nmje_attribution.M5ConflictSubtype),
         " M5MAT=", NMJE_MaturityText(info.nmje_attribution.M5Maturity),
         " M5DIR=", NMJE_DirText(info.nmje_attribution.M5Direction),
         " M5CTX=", IntegerToString(info.nmje_attribution.M5ContextCode),
         " M5RH=", info.nmje_attribution.M5ReasonHash == "" ? "-" : info.nmje_attribution.M5ReasonHash,
         " SM=", IntegerToString(info.nmje_attribution.StructureMask),
         " SC=", IntegerToString(info.nmje_attribution.StructureCount),
         " RQ=", IntegerToString(info.nmje_attribution.RequirementCompleteness),
         " SQ=", IntegerToString(info.nmje_attribution.SequenceCompleteness),
         " NET=", DoubleToString(netProfit, 8),
         " CLOSE=", IntegerToString((int)OrderCloseTime()));
   Print("[NMJE-P10-OUT] PAIR=", info.pair,
         " TICKET=", IntegerToString(info.ticket),
         " DIDH=", decisionHash,
         " ATTR=", info.nmje_attribution.EntryDisplacementPresent ? "Y" : "N",
         " PHASE=", NMJE_EventPhaseText(info.nmje_attribution.EventPhase),
         " FDUR=", info.nmje_attribution.EventPhaseCheckpointDurable ? "Y" : "N",
         " DISP=", NMJE_EntryDisplacementText(info.nmje_attribution.EntryDisplacementClass),
         " SRC=", DoubleToString(info.nmje_attribution.SourceConfirmationPrice, info.digits),
         " VAL=", DoubleToString(info.nmje_attribution.ValidationEntryPrice, info.digits),
         " EXEC=", DoubleToString(info.nmje_attribution.BrokerExecutionPrice, info.digits),
         " ANCH=", DoubleToString(info.nmje_attribution.StructuralAnchorPrice, info.digits),
         " CVP=", DoubleToString(info.nmje_attribution.ConfirmationToValidationPips, 4),
         " VEP=", DoubleToString(info.nmje_attribution.ValidationToExecutionPips, 4),
         " EAP=", DoubleToString(info.nmje_attribution.ExecutionFromAnchorPips, 4),
         " NET=", DoubleToString(netProfit, 8),
         " CLOSE=", IntegerToString((int)OrderCloseTime()));
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
         ZeroMemory(info);
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
         BuildNMJEShadowAttribution(decision, OrderOpenPrice(), snapshot.Point,
                                    info.nmje_attribution);

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

         bool nmjeAttributionPersisted = false;
         if(info.nmje_attribution.Present && info.execution_hash != "")
         {
            nmjeAttributionPersisted = SaveNMJEShadowAttribution(info);
            if(!nmjeAttributionPersisted)
               Log(DBG_ERROR, "NMJE shadow attribution persistence failed ticket=" +
                   IntegerToString(ticket));
         }

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
         Print("[NMJE-P4-OPEN] Ticket=", IntegerToString(ticket),
               " DIDH=", info.execution_hash == "" ? "-" : info.execution_hash,
               " ATTR=", info.nmje_attribution.Present ? "Y" : "N",
               " DUR=", nmjeAttributionPersisted ? "Y" : "N",
               " JH=", info.nmje_attribution.JourneyHash == "" ? "-" : info.nmje_attribution.JourneyHash,
               " DISP=", NMJE_EntryDisplacementText(info.nmje_attribution.EntryDisplacementClass),
               " PHASE=", NMJE_EventPhaseText(info.nmje_attribution.EventPhase),
               " M5=", info.nmje_attribution.M5Present ? "Y" : "N");
         
         AddToMonitoredTrades(info);
         
         decision.DecisionState = DEC_EXECUTED;
         MarkDecisionExecuted(decision.DecisionID, ticket);
         decision.DecisionState = DEC_EXECUTED;
         decision.RejectionReason = REJ_NONE;
         if(EntryMode == 1)
            Print("[P3M1][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(OrderOpenTime()));
         if(EntryMode == 2)
            Print("[P3M2][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(OrderOpenTime()));
         return;
      }

      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_AMBIGUOUS_RESULT;
      return;
   }

   decision.DecisionState = DEC_REJECTED;
   if(ticket == -2)
      decision.RejectionReason = REJ_AMBIGUOUS_RESULT;
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

bool IsC044DirectionSideOuterBBTest(TimeframeData &data,
                                    ENUM_DIRECTION direction)
{
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0 ||
      data.high <= 0.0 || data.low <= 0.0 ||
      data.bollinger[0] <= 0.0 || data.bollinger[2] <= 0.0)
      return false;

   if(direction == DIR_BUY)
      return (data.high >= data.bollinger[0]);
   if(direction == DIR_SELL)
      return (data.low <= data.bollinger[2]);
   return false;
}

bool FreezeC044Lifecycle(TradeInfo &info, string reason)
{
   if(!info.c044_lifecycle_managed) return false;

   info.c044_state = C044_LIFE_FROZEN;
   info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
   info.c044_exit_reason = C044_EXIT_NONE;
   info.c044_exit_latched_candle = 0;
   if(!SaveC044Checkpoint(info))
      Log(DBG_ERROR, "C044 freeze checkpoint failed ticket=" + IntegerToString(info.ticket));

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
         info.c044_state = C044_LIFE_WAIT_OUTER_TEST;
         info.c044_exit_reason = C044_EXIT_NONE;
         info.c044_exit_latched_candle = 0;
      }
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "WAIT_NEXT_REENTRY_CHECKPOINT_FAILED");
      return true;
   }

   if(info.c044_state != C044_LIFE_WAIT_OUTER_TEST)
      return FreezeC044Lifecycle(info, "UNEXPECTED_OWNER_EVENT_STATE");

   if(candleTime <= info.c044_epoch_anchor_candle)
   {
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "EPOCH_BOUNDARY_CHECKPOINT_FAILED");
      return true;
   }

   if(!IsC044DirectionSideOuterBBTest(data, info.direction))
   {
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "WAIT_OUTER_TEST_CHECKPOINT_FAILED");
      return true;
   }

   bool momentum = DetectCSM(pair, info.c044_owner_timeframe,
                             info.direction, shift);
   if(momentum)
   {
      info.c044_state = C044_LIFE_WAIT_NEXT_REENTRY;
      info.c044_exit_reason = C044_EXIT_NONE;
      info.c044_exit_latched_candle = 0;
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "MOMENTUM_HOLD_CHECKPOINT_FAILED");
      return true;
   }

   if(!LatchC044Exit(info, C044_EXIT_FAILED_MOMENTUM, candleTime))
      return FreezeC044Lifecycle(info, "FAILED_MOMENTUM_LATCH_FAILED");
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

bool LatchC044Exit(TradeInfo &info, ENUM_C044_EXIT_REASON reason, datetime candleTime)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return false;
   if(reason == C044_EXIT_NONE || candleTime <= 0) return false;

   if(info.c044_state == C044_LIFE_EXIT_LATCHED)
      return (info.c044_exit_reason == reason);

   if(info.c044_state != C044_LIFE_WAIT_OUTER_TEST &&
      info.c044_state != C044_LIFE_WAIT_NEXT_REENTRY)
      return false;

   info.c044_state = C044_LIFE_EXIT_LATCHED;
   info.c044_exit_reason = reason;
   info.c044_exit_latched_candle = candleTime;
   if(!SaveC044Checkpoint(info))
      Log(DBG_ERROR, "C044 latch checkpoint failed ticket=" + IntegerToString(info.ticket));
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
         g_monitored_trades[i].recovery_state == REC_IDENTITY_MISSING_FROZEN)
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
   info.d1_tpw_cycle_hash = "";
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

bool D1TPWCheckpointExists(TradeInfo &info)
{
   if(info.ticket <= 0) return false;
   string base = D1TPWCheckpointBase(info);
   if(!GlobalVariableCheck(base + "V") ||
      (int)GlobalVariableGet(base + "V") != 2)
      return false;
   string keys[8] = {"D","X","LP","L","XL","F","OT","MG"};
   for(int i = 0; i < 8; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   string pairHash, cycleHash, executionHash;
   if(!NMJELoadHex16(base, "P", pairHash) ||
      !NMJELoadHex16(base, "C", cycleHash) ||
      !NMJELoadHex16(base, "E", executionHash))
      return false;
   return true;
}

void ClearD1TPWCheckpoint(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = D1TPWCheckpointBase(info);
   if(GlobalVariableCheck(base + "V")) GlobalVariableDel(base + "V");
   string keys[8] = {"D","X","LP","L","XL","F","OT","MG"};
   for(int i = 0; i < 8; i++)
      if(GlobalVariableCheck(base + keys[i])) GlobalVariableDel(base + keys[i]);
   for(int part = 0; part < 4; part++)
   {
      string suffix = IntegerToString(part);
      if(GlobalVariableCheck(base + "P" + suffix)) GlobalVariableDel(base + "P" + suffix);
      if(GlobalVariableCheck(base + "C" + suffix)) GlobalVariableDel(base + "C" + suffix);
      if(GlobalVariableCheck(base + "E" + suffix)) GlobalVariableDel(base + "E" + suffix);
   }
   GlobalVariablesFlush();
}

bool SaveD1TPWCheckpoint(TradeInfo &info)
{
   if(!info.d1_tpw_lifecycle_managed || info.ticket <= 0 ||
      info.magic_number <= 0 || info.open_time <= 0 ||
      info.pair == "" || StringLen(info.d1_tpw_cycle_hash) != 16 ||
      StringLen(info.execution_hash) != 16 ||
      (info.direction != DIR_BUY && info.direction != DIR_SELL) ||
      info.d1_tpw_extreme_candle <= 0 ||
      info.d1_tpw_last_processed_d1_candle < info.d1_tpw_extreme_candle ||
      (info.d1_tpw_frozen && info.d1_tpw_exit_latched))
      return false;

   string base = D1TPWCheckpointBase(info);
   if(GlobalVariableCheck(base + "V") && !GlobalVariableDel(base + "V"))
      return false;
   if(GlobalVariableSet(base + "D", (double)info.direction) == 0) return false;
   if(GlobalVariableSet(base + "X", (double)info.d1_tpw_extreme_candle) == 0) return false;
   if(GlobalVariableSet(base + "LP", (double)info.d1_tpw_last_processed_d1_candle) == 0) return false;
   if(GlobalVariableSet(base + "L", info.d1_tpw_exit_latched ? 1.0 : 0.0) == 0) return false;
   if(GlobalVariableSet(base + "XL", (double)info.d1_tpw_exit_latched_candle) == 0) return false;
   if(GlobalVariableSet(base + "F", info.d1_tpw_frozen ? 1.0 : 0.0) == 0) return false;
   if(GlobalVariableSet(base + "OT", (double)info.open_time) == 0) return false;
   if(GlobalVariableSet(base + "MG", (double)info.magic_number) == 0) return false;
   string pairHash = SHORT_HASH(info.pair, 16);
   if(!NMJEStoreHex16(base, "P", pairHash) ||
      !NMJEStoreHex16(base, "C", info.d1_tpw_cycle_hash) ||
      !NMJEStoreHex16(base, "E", info.execution_hash))
      return false;
   // V is the commit marker. A torn write is never considered recoverable.
   if(GlobalVariableSet(base + "V", 2.0) == 0) return false;
   GlobalVariablesFlush();
   return D1TPWCheckpointExists(info);
}

bool LoadD1TPWCheckpoint(TradeInfo &info)
{
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0) return false;
   if(!D1TPWCheckpointExists(info)) return false;

   string base = D1TPWCheckpointBase(info);
   ENUM_DIRECTION direction = (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   datetime extremeCandle = (datetime)((int)GlobalVariableGet(base + "X"));
   datetime lastProcessed = (datetime)((int)GlobalVariableGet(base + "LP"));
   bool latched = (GlobalVariableGet(base + "L") > 0.5);
   datetime exitCandle = (datetime)((int)GlobalVariableGet(base + "XL"));
   bool frozen = (GlobalVariableGet(base + "F") > 0.5);
   datetime openTime = (datetime)((int)GlobalVariableGet(base + "OT"));
   int magic = (int)GlobalVariableGet(base + "MG");
   string pairHash, cycleHash, executionHash;
   if(!NMJELoadHex16(base, "P", pairHash) ||
      !NMJELoadHex16(base, "C", cycleHash) ||
      !NMJELoadHex16(base, "E", executionHash))
      return false;

   if(direction != info.direction || magic != info.magic_number ||
      openTime != info.open_time || extremeCandle <= 0 ||
      lastProcessed < extremeCandle || (latched && exitCandle <= 0) ||
      (!latched && exitCandle != 0) || (frozen && latched) ||
      pairHash != SHORT_HASH(info.pair, 16) || cycleHash == "" ||
      executionHash == "" || executionHash != info.execution_hash)
      return false;

   int extremeShift = iBarShift(info.pair, PERIOD_D1, extremeCandle, true);
   int cursorShift = iBarShift(info.pair, PERIOD_D1, lastProcessed, true);
   if(extremeShift < 1 || cursorShift < 1 ||
      iTime(info.pair, PERIOD_D1, extremeShift) != extremeCandle ||
      iTime(info.pair, PERIOD_D1, cursorShift) != lastProcessed)
      return false;

   ResetD1TPWTradeState(info);
   info.d1_tpw_lifecycle_managed = true;
   info.d1_tpw_cycle_hash = cycleHash;
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
      decision.D1OpportunityDirection != decision.Direction ||
      StringLen(decision.D1OpportunityCycleID) != 16)
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
   info.d1_tpw_cycle_hash = decision.D1OpportunityCycleID;
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
   ZeroMemory(info.c044_replay_reentry);
   ZeroMemory(info.c044_replay_extreme_buy);
   ZeroMemory(info.c044_replay_extreme_sell);
}

bool IsValidC044OwnerTimeframe(int timeframe)
{
   return (timeframe == PERIOD_M15 || timeframe == PERIOD_H1 ||
           timeframe == PERIOD_H4 || timeframe == PERIOD_D1);
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
   info.c044_state = C044_LIFE_WAIT_OUTER_TEST;
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

void ClearC044ReplaySeed(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = C044ReplayGVBase(info);
   if(GlobalVariableCheck(base + "V")) GlobalVariableDel(base + "V");
   for(int i = 0; i < 20; i++)
      if(GlobalVariableCheck(C044ReplayGVKey(base, "R", i)))
         GlobalVariableDel(C044ReplayGVKey(base, "R", i));
   for(int j = 0; j < 19; j++)
   {
      if(GlobalVariableCheck(C044ReplayGVKey(base, "B", j)))
         GlobalVariableDel(C044ReplayGVKey(base, "B", j));
      if(GlobalVariableCheck(C044ReplayGVKey(base, "S", j)))
         GlobalVariableDel(C044ReplayGVKey(base, "S", j));
   }
}

bool SaveC044ReplaySeed(TradeInfo &info)
{
   if(!info.c044_replay_seed_valid || info.ticket <= 0) return false;
   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   string base = C044ReplayGVBase(info);
   GlobalVariableSet(base + "V", 1.0);

   GlobalVariableSet(C044ReplayGVKey(base,"R",0),  (double)info.c044_replay_reentry.Type);
   GlobalVariableSet(C044ReplayGVKey(base,"R",1),  (double)info.c044_replay_reentry.State);
   GlobalVariableSet(C044ReplayGVKey(base,"R",2),  (double)info.c044_replay_reentry.Direction);
   GlobalVariableSet(C044ReplayGVKey(base,"R",3),  (double)info.c044_replay_reentry.Timeframe);
   GlobalVariableSet(C044ReplayGVKey(base,"R",4),  (double)info.c044_replay_reentry.StartBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",5),  (double)info.c044_replay_reentry.StartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",6),  (double)info.c044_replay_reentry.LastUpdateBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",7),  (double)info.c044_replay_reentry.LastUpdateCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",8),  (double)info.c044_replay_reentry.ConfirmationBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",9),  (double)info.c044_replay_reentry.ConfirmationCandle);
   GlobalVariableSet(C044ReplayGVKey(base,"R",10), (double)info.c044_replay_reentry.ExpiryBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",11), (double)info.c044_replay_reentry.ExpiryCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",12), (double)info.c044_replay_reentry.MinCandlesRequired);
   GlobalVariableSet(C044ReplayGVKey(base,"R",13), (double)info.c044_replay_reentry.QualifyingCandles);
   GlobalVariableSet(C044ReplayGVKey(base,"R",14), (double)info.c044_replay_reentry.Type1ContextState);
   GlobalVariableSet(C044ReplayGVKey(base,"R",15), (double)info.c044_replay_reentry.Type1OwnerSignal);
   GlobalVariableSet(C044ReplayGVKey(base,"R",16), (double)info.c044_replay_reentry.Type1OwnerCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",17), (double)info.c044_replay_reentry.Type1RangingStartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",18), info.c044_replay_reentry.Type1PreviousClose);
   GlobalVariableSet(C044ReplayGVKey(base,"R",19), info.c044_replay_reentry.IsValid ? 1.0 : 0.0);

   ExtremeLifecycleData buy = info.c044_replay_extreme_buy;
   ExtremeLifecycleData sell = info.c044_replay_extreme_sell;
   GlobalVariableSet(C044ReplayGVKey(base,"B",0),  (double)buy.Maturity);
   GlobalVariableSet(C044ReplayGVKey(base,"B",1),  (double)buy.Direction);
   GlobalVariableSet(C044ReplayGVKey(base,"B",2),  (double)buy.Timeframe);
   GlobalVariableSet(C044ReplayGVKey(base,"B",3),  (double)buy.RawBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",4),  (double)buy.RawCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",5),  (double)buy.ConfirmationBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",6),  (double)buy.ConfirmationCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",7),  buy.ConfirmationClose);
   GlobalVariableSet(C044ReplayGVKey(base,"B",8),  (double)buy.LastUpdateBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",9),  (double)buy.LastUpdateCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",10), buy.PreviousClose);
   GlobalVariableSet(C044ReplayGVKey(base,"B",11), buy.ProvisionalBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"B",12), buy.FrozenBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"B",13), buy.RelevantMA5);
   GlobalVariableSet(C044ReplayGVKey(base,"B",14), (double)buy.RetestStartBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",15), (double)buy.RetestStartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",16), (double)buy.RetestCompletionBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",17), (double)buy.RetestCompletionCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",18), buy.IsValid ? 1.0 : 0.0);

   GlobalVariableSet(C044ReplayGVKey(base,"S",0),  (double)sell.Maturity);
   GlobalVariableSet(C044ReplayGVKey(base,"S",1),  (double)sell.Direction);
   GlobalVariableSet(C044ReplayGVKey(base,"S",2),  (double)sell.Timeframe);
   GlobalVariableSet(C044ReplayGVKey(base,"S",3),  (double)sell.RawBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",4),  (double)sell.RawCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",5),  (double)sell.ConfirmationBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",6),  (double)sell.ConfirmationCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",7),  sell.ConfirmationClose);
   GlobalVariableSet(C044ReplayGVKey(base,"S",8),  (double)sell.LastUpdateBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",9),  (double)sell.LastUpdateCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",10), sell.PreviousClose);
   GlobalVariableSet(C044ReplayGVKey(base,"S",11), sell.ProvisionalBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"S",12), sell.FrozenBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"S",13), sell.RelevantMA5);
   GlobalVariableSet(C044ReplayGVKey(base,"S",14), (double)sell.RetestStartBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",15), (double)sell.RetestStartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",16), (double)sell.RetestCompletionBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",17), (double)sell.RetestCompletionCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",18), sell.IsValid ? 1.0 : 0.0);
   return true;
}

bool ReadC044ReplayGV(string base, string group, int index, double &value)
{
   string key = C044ReplayGVKey(base, group, index);
   if(!GlobalVariableCheck(key)) return false;
   value = GlobalVariableGet(key);
   return true;
}

bool LoadC044ReplaySeed(TradeInfo &info)
{
   string base = C044ReplayGVBase(info);
   if(!GlobalVariableCheck(base + "V") ||
      (int)GlobalVariableGet(base + "V") != 1)
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
   ClearC044ReplaySeed(info);
}

bool SaveC044Checkpoint(TradeInfo &info)
{
   if(!info.c044_lifecycle_managed || info.ticket <= 0 ||
      info.magic_number <= 0 || info.open_time <= 0 ||
      (info.direction != DIR_BUY && info.direction != DIR_SELL) ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe) ||
      info.c044_owner_reentry_candle <= 0 || info.c044_epoch_anchor_candle <= 0 ||
      info.c044_last_processed_owner_candle <= 0 ||
      info.c044_state == C044_LIFE_NONE)
      return false;

   if(info.c044_state != C044_LIFE_FROZEN &&
      (!info.c044_replay_seed_valid || !SaveC044ReplaySeed(info)))
      return false;

   string base = C044CheckpointBase(info);
   GlobalVariableSet(base + "D",  (double)info.direction);
   GlobalVariableSet(base + "TF", (double)info.c044_owner_timeframe);
   GlobalVariableSet(base + "OR", (double)info.c044_owner_reentry_candle);
   GlobalVariableSet(base + "EP", (double)info.c044_epoch_anchor_candle);
   GlobalVariableSet(base + "LP", (double)info.c044_last_processed_owner_candle);
   GlobalVariableSet(base + "ST", (double)info.c044_state);
   GlobalVariableSet(base + "XR", (double)info.c044_exit_reason);
   GlobalVariableSet(base + "XL", (double)info.c044_exit_latched_candle);
   GlobalVariableSet(base + "OT", (double)info.open_time);
   GlobalVariableSet(base + "MG", (double)info.magic_number);
   GlobalVariablesFlush();

   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   return true;
}

bool LoadC044Checkpoint(TradeInfo &info)
{
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0) return false;
   string base = C044CheckpointBase(info);
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
   if(state != C044_LIFE_WAIT_OUTER_TEST &&
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
   return LoadC044ReplaySeed(info);
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
      ZeroMemory(info);
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
      // P4 recovery is research-only. Missing/corrupt attribution never
      // freezes, rejects, closes or otherwise changes the live trade.
      bool nmjeAttributionRecovered = LoadNMJEShadowAttribution(info);
      if(DebugLevel >= DBG_SIGNAL)
         Print("[NMJE-P4-RECOVER] Ticket=", IntegerToString(info.ticket),
               " DIDH=", info.execution_hash == "" ? "-" : info.execution_hash,
               " ATTR=", nmjeAttributionRecovered ? "Y" : "N");

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

      AddToMonitoredTrades(info);

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
   g_dashboard_snapshot += "=== BBMA EA V4.75 C10 Audit Ledger Stage B ===\n";
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

   Print("[D1-10A] ", pair,
         " D1=", D10D1(g_pair_states[pairIndex].d1_major_trend_owner.State),
         " H4=", D10H4(g_pair_states[pairIndex].h4_direction_owner.State,
                       g_pair_states[pairIndex].h4_direction_owner.Direction),
         " F=", finalCandidate);

   Print("[D1-10B] ", pair,
         " RE H1=", D10RE(g_pair_states[pairIndex].re_h1_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_h1_sell_state.State),
         " H4=", D10RE(g_pair_states[pairIndex].re_h4_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_h4_sell_state.State),
         " D1=", D10RE(g_pair_states[pairIndex].re_d1_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_d1_sell_state.State),
         " M15=", D10RE(g_pair_states[pairIndex].re_m15_buy_state.State), "/",
                      D10RE(g_pair_states[pairIndex].re_m15_sell_state.State),
         " OPP=", D1OpportunityFamilyText(g_pair_states[pairIndex].d1_opportunity.Family), "/",
                    D10Dir(g_pair_states[pairIndex].d1_opportunity.Direction), "/",
                    (g_pair_states[pairIndex].d1_opportunity.Active ? "Y" : "N"));

   Print("[D1-10C] ", pair,
         " X H1=", D10EXT(g_pair_states[pairIndex].extreme_h1_buy_lifecycle.Maturity), "/",
                    D10EXT(g_pair_states[pairIndex].extreme_h1_sell_lifecycle.Maturity),
         " H4=", D10EXT(g_pair_states[pairIndex].extreme_h4_buy_lifecycle.Maturity), "/",
                    D10EXT(g_pair_states[pairIndex].extreme_h4_sell_lifecycle.Maturity),
         " M15=", D10MLV(g_pair_states[pairIndex].mlv_buy_state.State), "/",
                     D10MLV(g_pair_states[pairIndex].mlv_sell_state.State));
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
   // NMJE v2 Stage-C1: latest closed M5 data is sampled only inside this
   // existing M15-driven ProcessPair cycle. It has no processing authority.
   GetDataForTimeframe(actual, PERIOD_M5, g_pair_states[pairIndex].tf_snapshot.M5_CandleTime,
                       g_pair_states[pairIndex].m5_data);

   // D1-01: classify strategic D1/MA50 owner from fully closed D1 data.
   // Producer only in this step; M15/M16 consumption is intentionally later.
   UpdateD1MajorTrendOwner(actual, g_pair_states[pairIndex]);

   // H4 owner is persistent across neutral H4 candles and changes only on
   // source-valid authoritative H4 direction/momentum events.
   UpdateRuntimeH4DirectionalOwner(pairIndex);

   BollingerBand d1Band, h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band, m5Band;
   ZeroMemory(d1Band); ZeroMemory(h1Band); ZeroMemory(h1PrevBand);
   ZeroMemory(h4Band); ZeroMemory(h4PrevBand); ZeroMemory(m15Band); ZeroMemory(m5Band);

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

   m5Band.TOP_BB = g_pair_states[pairIndex].m5_data.bollinger[0];
   m5Band.MID_BB = g_pair_states[pairIndex].m5_data.bollinger[1];
   m5Band.LOW_BB = g_pair_states[pairIndex].m5_data.bollinger[2];
   m5Band.Width = m5Band.TOP_BB - m5Band.LOW_BB;
   m5Band.State = BB_NONE;

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

   // Issue #101 Stage-C2: canonical M5 Extreme lifecycle advances only when
   // this M15-driven cycle runs. The state is shadow context, never a signal.
   bool m5RawBuyExtreme = DetectExtreme(actual, DIR_BUY,
                                         g_pair_states[pairIndex].m5_data, m5Band);
   bool m5RawSellExtreme = DetectExtreme(actual, DIR_SELL,
                                          g_pair_states[pairIndex].m5_data, m5Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5_buy_lifecycle,
                          actual, DIR_BUY, g_pair_states[pairIndex].m5_data,
                          m5Band, m5RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5_sell_lifecycle,
                          actual, DIR_SELL, g_pair_states[pairIndex].m5_data,
                          m5Band, m5RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_m5_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_m5_sell_lifecycle,
                                      g_pair_states[pairIndex].m5_data);

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

   for(int dirIdx = 0; dirIdx < 2; dirIdx++)
   {
      ENUM_DIRECTION direction = (dirIdx == 0) ? DIR_BUY : DIR_SELL;

      Signal h1ExtremeSnapshot, h4ExtremeSnapshot, m15MHVSnapshot, m15CSDSnapshot;
      Signal m15ECSDSnapshot, m15CSMSnapshot;
      ZeroMemory(h1ExtremeSnapshot); ZeroMemory(h4ExtremeSnapshot);
      ZeroMemory(m15MHVSnapshot); ZeroMemory(m15CSDSnapshot);
      ZeroMemory(m15ECSDSnapshot); ZeroMemory(m15CSMSnapshot);

      Signal detectedH1Extreme, detectedH4Extreme;
      ZeroMemory(detectedH1Extreme); ZeroMemory(detectedH4Extreme);
      if(direction == DIR_BUY)
      {
         detectedH1Extreme = resolvedH1BuyExtreme;
         detectedH4Extreme = resolvedH4BuyExtreme;
      }
      else
      {
         detectedH1Extreme = resolvedH1SellExtreme;
         detectedH4Extreme = resolvedH4SellExtreme;
      }

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
         ExportCanonicalMHVSignal(g_pair_states[pairIndex].mlv_buy_state,
                                  m15MHVSnapshot);

         UpdateReEntryState(g_pair_states[pairIndex].re_h1_buy_state, actual, direction,
                            g_pair_states[pairIndex].h1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_h4_buy_state, actual, direction,
                            g_pair_states[pairIndex].h4_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_d1_buy_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m15_buy_state, actual, direction,
                            g_pair_states[pairIndex].m15_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m5_buy_state, actual, direction,
                            g_pair_states[pairIndex].m5_data);
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
         ExportCanonicalMHVSignal(g_pair_states[pairIndex].mlv_sell_state,
                                  m15MHVSnapshot);

         UpdateReEntryState(g_pair_states[pairIndex].re_h1_sell_state, actual, direction,
                            g_pair_states[pairIndex].h1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_h4_sell_state, actual, direction,
                            g_pair_states[pairIndex].h4_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_d1_sell_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m15_sell_state, actual, direction,
                            g_pair_states[pairIndex].m15_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m5_sell_state, actual, direction,
                            g_pair_states[pairIndex].m5_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
         NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);
      }

      if(direction == DIR_BUY)
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;
      else
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;

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

      if(direction == DIR_BUY)
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;
      else
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;
      h4_extreme = h4ExtremeSnapshot;

      ComponentSet rem, rre, ree;
      BuildPossibleCombinations(rem, rre, ree, h4_reEntry, extreme, mlv,
                                d1_reEntry, h4_extreme);
      
      ValidatedSequenceCandidate reEntryCandidate;
      BuildConfirmedReEntryCandidate(
         reEntry, g_pair_states[pairIndex].h4_direction_owner, reEntryCandidate);
      AppendValidatedCandidate(reEntryCandidate, allCandidates, allCandidateCount);

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

   // N1/N2 relationship observation remains descriptive; D1O execution uses
   // the separately owned/frozen D1 opportunity identity, not NESTED_RELATION.
   UpdateNestedJourneyObservation(pairIndex);

   BBMA_Decision decision;
   OppositeConflictPackage conflict;
   ZeroMemory(decision);
   ZeroMemory(conflict);
   decision.Pair = actual;

   PriorityEngine_Atomic(allCandidates, allCandidateCount,
                         g_pair_states[pairIndex], decision, conflict);

   // D1-07: M16 may only consume an actual M15-created decision.
   // ZeroMemory() leaves enum value 0 (= DEC_CREATED), so state alone is not
   // sufficient to prove that M15 selected/froze a decision.
   if(decision.Valid && decision.DecisionState == DEC_CREATED)
   {
      InvalidationEngine_Atomic(pairIndex, decision, conflict);
   }

   if(decision.DecisionState == DEC_VALIDATED)
   {
      // N2-01 shadow metadata only; execution path remains unchanged.
      NMJE_PrintValidatedDecisionShadow(pairIndex, decision);
      RunEntryPreflightAndExecute(decision, actual);
   }

   if(EntryMode == 2 && decision.Valid)
   {
      // C10 Stage B is evidence-only. It consumes the already-final decision
      // after preflight and cannot mutate candidate or execution authority.
      C10_WriteSignalEvent(pairIndex, decision);
      Print("[P3M2][DECISION_FINAL] Pair=", actual,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " State=", EnumToString(decision.DecisionState),
            " Reason=", EnumToString(decision.RejectionReason),
            " DecisionID=", decision.DecisionID);
   }

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

   if(g_portfolio_emergency_close_requested) return;
   
   if(g_is_scanning) return;
   g_is_scanning = true;
   
   g_processing_time = GetProcessingTime();
   
   for(int i = 0; i < g_pair_count; i++)
   {
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
   g_timer_registered = false;
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

   // Audit-only C10 failure disables evidence writing but never changes EA
   // strategy/execution state. The input remains OFF by default.
   C10_InitializeLedgers();

   ResetLastError();
   if(!EventSetTimer(1))
   {
      int timerError = GetLastError();
      if(IsTesting() && timerError == TESTER_FUNCTION_NOT_ALLOWED)
      {
         Print("[C3TIMER][TESTER_FALLBACK] EventSetTimer unavailable, error=",
               IntegerToString(timerError), "; OnTick remains the processing driver");
      }
      else
      {
         g_is_initialized = false;
         Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));
         return INIT_FAILED;
      }
   }
   else
      g_timer_registered = true;
   
   Log(DBG_FULL, "BBMA EA V4.75 C10 Audit Ledger Stage B initialized successfully");
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| EXPERT DEINITIALIZATION FUNCTION                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   if(g_timer_registered)
      EventKillTimer();
   g_timer_registered = false;

   C10_ShutdownLedgers();

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

