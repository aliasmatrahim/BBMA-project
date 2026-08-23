//+------------------------------------------------------------------+
//|                                           BBMA_EA.mq4 |
//|                                    Version 4.5.1 - P3-M2-07 OPPOSITE GUARD    |
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
#property version   "4.51"
#property description "P3-M2-07 Cycle Direction Guard"
#property strict

//+------------------------------------------------------------------+
//| MODULE 01: HEADER & INPUTS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

//--- INPUTS
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
#define MAX_PAIRS               20
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

enum ENUM_EXTREME_TYPE { EXT_NONE, EXT_SIDEWAYS, EXT_WITH_MOMENTUM, EXT_WITHOUT_MOMENTUM };

enum ENUM_EXTREME_MATURITY
{
   EXT_MAT_NONE,
   EXT_MAT_RAW,
   EXT_MAT_REVERSAL_CONFIRMED,
   EXT_MAT_RETEST_PHASE,
   EXT_MAT_RETEST_READY,
   EXT_MAT_VOID
};

enum ENUM_SIGNAL_LEVEL { LEVEL_NONE, LEVEL_D, LEVEL_C, LEVEL_B, LEVEL_A, LEVEL_A_PLUS };

enum ENUM_PRIORITY_TIER { TIER_NONE, TIER_C, TIER_B, TIER_A, TIER_A_PLUS };

enum ENUM_TRADE_LOCK { LOCK_OFF, LOCK_SAME_DIRECTION, LOCK_ONE_POSITION };

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

enum ENUM_DEBUG_LEVEL { DBG_OFF, DBG_ERROR, DBG_SIGNAL, DBG_TRADE, DBG_FULL };

enum ENUM_RECOVERY_STATE { REC_NORMAL, REC_CORRUPTED, REC_RECOVERY_INVALID, REC_PARTIAL_INFERRED,
                           REC_IDENTITY_HASH_ONLY, REC_IDENTITY_MISSING_FROZEN };

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
   
   // MUTABLE LIFECYCLE
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
   H4DirectionalOwner   h4_direction_owner;
   double               prev_ema50;
   double               current_ema50;
   double               prev_daily_ema50;
   double               current_daily_ema50;
   // F2 source-aligned Extreme maturity lifecycle.
   ExtremeLifecycleData extreme_h1_buy_lifecycle;
   ExtremeLifecycleData extreme_h1_sell_lifecycle;
   ExtremeLifecycleData extreme_h4_buy_lifecycle;
   ExtremeLifecycleData extreme_h4_sell_lifecycle;
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
datetime             g_processed_candle_time[MAX_PAIRS];
int                  g_pair_count;

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

//--- Manual mode
ENUM_PRIORITY_TIER   g_manual_priority_tiers[];

//--- Dashboard
string               g_dashboard_snapshot;
bool                 g_dashboard_needs_update;

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

   state.h4_direction_owner.State = H4_OWNER_RECOVERY_UNRESOLVED;
   state.h4_direction_owner.Direction = DIR_NONE;
   state.h4_direction_owner.SourceSignal = SIGNAL_NONE;
   state.h4_direction_owner.LastAdvanceSignal = SIGNAL_NONE;
   state.h4_direction_owner.IsValid = false;
   state.h4_direction_owner.RecoveryComplete = false;
   state.h4_direction_owner.RecoveredFromCheckpoint = false;
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

         string executionHash;
         if(!ExtractExecutionHash(OrderComment(), executionHash)) continue;

         ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;
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
   string hash = SHORT_HASH(decisionID);
   string seqHash = SHORT_HASH(sequenceHash);
   return "BBMA|H:" + hash + "|C:" + TimeToString(candleTime) + "|P:" + pair + 
          "|D:" + IntegerToString(direction) + "|T:" + IntegerToString(signalType) + 
          "|E:" + DoubleToString(intendedEntry, 5) + "|S:" + DoubleToString(intendedSL, 5) + 
          "|L:" + DoubleToString(intendedLot, 2) + "|R:" + DoubleToString(intendedRisk, 2) + 
          "|Q:" + seqHash;
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

   if(extreme.Maturity == EXT_MAT_VOID)
   {
      if(!rawDetected || data.candle_time <= extreme.LastUpdateCandleTime)
         return EXT_MAT_VOID;
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

datetime GetCandidateAnchorTime(ValidatedSequenceCandidate &candidate)
{
   datetime anchor = candidate.Components[0].CandleTime;
   for(int i = 1; i < 3; i++)
   {
      if(candidate.Components[i].CandleTime > anchor)
         anchor = candidate.Components[i].CandleTime;
   }
   return anchor;
}

bool ResolveSelectedSLTPSourceComponent(ValidatedSequenceCandidate &selected,
                                        ComponentIdentity &source)
{
   ZeroMemory(source);

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

void PriorityEngine_Atomic(ValidatedSequenceCandidate &candidates[], int count,
                           BBMA_Decision &decision, OppositeConflictPackage &conflict)
{
   int buyCount = 0;
   int sellCount = 0;

   for(int i = 0; i < count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      if(candidates[i].Direction == DIR_BUY) buyCount++;
      else if(candidates[i].Direction == DIR_SELL) sellCount++;
   }

   if(EntryMode == 1 && (buyCount > 0 || sellCount > 0))
      Print("[P3M1][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));

   if(buyCount > 0 && sellCount > 0)
   {
      conflict.Exists = true;
      conflict.ConflictType = CONFLICT_DIRECTION_VIOLATION;
      conflict.ConflictReason = "Opposite validated BBMA entries coexist";
      conflict.FrozenSnapshotTime = g_processing_time;
      if(EntryMode == 1)
         Print("[P3M1][M15_CONFLICT] Opposite eligible RE candidates; no winner selected");
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
      if(candidates[i].Direction != targetDirection) continue;

      if(canonicalIdx < 0 ||
         CompareCanonicalCandidates(candidates[i], candidates[canonicalIdx]) > 0)
      {
         canonicalIdx = i;
      }
   }

   if(canonicalIdx < 0) return;

   ValidatedSequenceCandidate selected = candidates[canonicalIdx];
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
      Print("[P3M1][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " Candle=", TimeToString(decision.CandleTime),
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
      Print("[P3M1][M16_PASS] DecisionID=", decision.DecisionID,
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
      return (source.Timeframe == PERIOD_H1);

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

bool ResolveSourceOwnedWickAnchor(string pair, ComponentIdentity &source,
                                  ENUM_DIRECTION direction, double &anchor)
{
   anchor = 0.0;
   int shift = ResolveClosedSourceShift(pair, source);
   if(shift < 1) return false;

   if(direction == DIR_BUY)
      anchor = iLow(pair, source.Timeframe, shift);
   else if(direction == DIR_SELL)
      anchor = iHigh(pair, source.Timeframe, shift);
   else
      return false;

   return (anchor > 0.0);
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

bool ResolveApprovedInitialSLTP(BBMA_Decision &decision,
                                RiskValidationSnapshot &snapshot)
{
   if(!IsApprovedSLTPSourceComponent(decision,
                                     decision.SLTPSourceComponent))
      return false;

   double wickAnchor = 0.0;
   double destination = 0.0;
   if(!ResolveSourceOwnedWickAnchor(decision.Pair,
                                    decision.SLTPSourceComponent,
                                    decision.Direction,
                                    wickAnchor))
      return false;

   if(!ResolveApprovedBBDestination(decision.Pair,
                                    decision.SLTPSourceComponent,
                                    decision.Direction,
                                    destination))
      return false;

   if(snapshot.Point <= 0.0 || decision.EntryPrice <= 0.0) return false;

   double safetyBuffer = snapshot.Point;
   double structuralSL = (decision.Direction == DIR_BUY)
      ? wickAnchor - safetyBuffer
      : wickAnchor + safetyBuffer;

   if(decision.Direction == DIR_BUY && destination <= decision.EntryPrice)
      return false;
   if(decision.Direction == DIR_SELL && destination >= decision.EntryPrice)
      return false;

   if(snapshot.TickSize_Price <= 0.0 || snapshot.Digits < 0) return false;

   double slTicks = structuralSL / snapshot.TickSize_Price;
   double tpTicks = destination / snapshot.TickSize_Price;
   double normalizedSL = 0.0;
   double normalizedTP = 0.0;

   if(decision.Direction == DIR_BUY)
   {
      normalizedSL = MathFloor(slTicks + 0.000000001) * snapshot.TickSize_Price;
      normalizedTP = MathFloor(tpTicks + 0.000000001) * snapshot.TickSize_Price;
   }
   else if(decision.Direction == DIR_SELL)
   {
      normalizedSL = MathCeil(slTicks - 0.000000001) * snapshot.TickSize_Price;
      normalizedTP = MathCeil(tpTicks - 0.000000001) * snapshot.TickSize_Price;
   }
   else
      return false;

   normalizedSL = NormalizeDouble(normalizedSL, snapshot.Digits);
   normalizedTP = NormalizeDouble(normalizedTP, snapshot.Digits);
   if(normalizedSL <= 0.0 || normalizedTP <= 0.0) return false;

   decision.StopLoss = normalizedSL;
   decision.TakeProfit = normalizedTP;
   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;
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
   return (decision.StopLoss > 0.0 && decision.TakeProfit > 0.0);
}

bool ValidateDirectionalSLTPGeometry(BBMA_Decision &decision)
{
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
   
   if(status.active_pairs > MaxActivePair)
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
   
   if(wouldBePairs > MaxActivePair)
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
   return (error == 135 || error == 138 || error == 128 || error == 146);
}

bool IsFatalError(int error)
{
   return (error == 130 || error == 131 || error == 134 || error == 148);
}

bool IsAmbiguousError(int error)
{
   return (error == 4 || error == 6 || error == 141);
}

int FindExistingExecutionTicket(string pair, int direction, int magicNumber,
                                string decisionID)
{
   if(pair == "" || magicNumber <= 0 || decisionID == "") return -1;

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

   // P3-M2-07 SOURCE-DERIVED CYCLE DIRECTION GUARD:
   // Multiple distinct same-direction BBMA entries may coexist, but a fresh
   // opposite-direction entry must not create BUY+SELL coexistence on the
   // same EA-owned pair while the earlier opposite position is still live.
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(!IsLiveEAOwnedPortfolioTrade(i)) continue;
      if(g_monitored_trades[i].pair != pair) continue;
      if(g_monitored_trades[i].direction != decision.Direction)
         return false;
   }
   
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
   if(MaxRetry <= 0 || pair == "" || lot <= 0 || stopLoss <= 0 || takeProfit <= 0 ||
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

void CompactMonitoredTrades()
{
   int write = 0;
   for(int i = 0; i < g_monitored_count; i++)
   {
      bool removeClosed = false;
      if(OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
         removeClosed = (OrderCloseTime() != 0);
      if(removeClosed) continue;
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

   if(pair == "" || decision.Pair != pair || decision.DecisionID == "" ||
      decision.Direction == DIR_NONE || decision.EntryPrice <= 0 ||
      decision.StopLoss <= 0 || decision.TakeProfit <= 0)
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

         string expectedExecutionHash = SHORT_HASH(decision.DecisionID);
         string persistedExecutionHash = "";
         string persistedComment = OrderComment();
         bool persistedHashFound = ExtractExecutionHash(persistedComment, persistedExecutionHash);
         bool persistedHashMatch = (persistedHashFound &&
                                    persistedExecutionHash == expectedExecutionHash);
         info.execution_hash = persistedHashMatch ? persistedExecutionHash : "";
         info.recovery_state = REC_NORMAL;

         Print("[P3S5][EXEC_ID] Ticket=", IntegerToString(ticket),
               " Pair=", pair,
               " Persist=", persistedHashMatch ? "PASS" : "FAIL",
               " HashFound=", persistedHashFound ? "Y" : "N",
               " HashMatch=", persistedHashMatch ? "Y" : "N",
               " ExpectedHash=", expectedExecutionHash,
               " PersistedHash=", persistedExecutionHash,
               " RawLen=", IntegerToString(StringLen(persistedComment)),
               " RawComment=<", persistedComment, ">");
         
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

   ProcessEntry(decision, pair, snapshot, lot);
   return (decision.DecisionState == DEC_EXECUTED);
}

//+------------------------------------------------------------------+
//| MODULE 23: POSITION MANAGEMENT (TICK-DRIVEN)                     |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

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
   }
   
   g_is_managing_trade = false;
}

//+------------------------------------------------------------------+
//| MODULE 24: RECOVERY ENGINE                                       |
//| LEVEL: EXPERT                                                    |
//+------------------------------------------------------------------+

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
      string executionHash = "";
      bool hasExecutionHash = ExtractExecutionHash(comment, executionHash);

      ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;
      string decisionHash, parsedPair, sequenceHash;
      ENUM_DIRECTION parsedDirection = DIR_NONE;
      ENUM_SIGNAL_TYPE signalType = SIGNAL_NONE;
      double intendedEntry, intendedSL, intendedLot, intendedRisk;
      datetime candleTime = 0;

      bool fullMetadata = hasExecutionHash &&
                          ParseOrderCommentFull(comment, decisionHash, parsedPair,
                                                parsedDirection, signalType,
                                                intendedEntry, intendedSL,
                                                intendedLot, intendedRisk,
                                                sequenceHash, candleTime);

      if(fullMetadata &&
         (decisionHash != executionHash || parsedPair != pair ||
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

      bool geometryValid = (info.initial_entry_price > 0 &&
                            info.initial_stop_loss > 0 &&
                            info.initial_take_profit > 0);
      if(geometryValid && liveDirection == DIR_BUY)
         geometryValid = (info.initial_stop_loss < info.initial_entry_price &&
                          info.initial_entry_price < info.initial_take_profit);
      else if(geometryValid && liveDirection == DIR_SELL)
         geometryValid = (info.initial_take_profit < info.initial_entry_price &&
                          info.initial_entry_price < info.initial_stop_loss);

      string recoveryCause = "";
      double currentLot = OrderLots();
      if(!geometryValid)
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

void BuildDashboardSnapshot()
{
   g_dashboard_snapshot = "";
   g_dashboard_snapshot += "=== BBMA EA V4.5.1 ===\n";
   g_dashboard_snapshot += "Time: " + TimeToString(TimeCurrent()) + "\n";
   g_dashboard_snapshot += "Balance: " + DoubleToString(AccountBalance(), 2) + "\n";
   g_dashboard_snapshot += "Equity: " + DoubleToString(AccountEquity(), 2) + "\n";
   g_dashboard_snapshot += "Trades: " + IntegerToString(g_monitored_count) + "\n";
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

//+------------------------------------------------------------------+
//| MODULE 26: INITIALIZATION & CLEANUP                              |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool ValidateInputParameters()
{
   if(MaxRetry <= 0) return false;
   if(Slippage < 0 || AllowedExecutionDeviation_MinPoints < 0) return false;
   if(TradeLockMode < LOCK_OFF || TradeLockMode > LOCK_ONE_POSITION) return false;
   if(MMMode != 1 && MMMode != 2) return false;
   if(MMMode == 1 && AutoLotPercent <= 0) return false;
   if(MMMode == 1 && MaxAutoLot <= 0) return false;
   if(MMMode == 2 && FixedLot <= 0) return false;

   if(MaxActivePair > MAX_PAIRS) return false;
   if(MaxTradePerPair > MAX_TRADES_PER_PAIR) return false;
   if(MaxTotalTrade > MAX_MONITORED) return false;
   if(StrategyID < STRATEGY_ID_MIN || StrategyID > STRATEGY_ID_MAX) return false;
   if(InstanceID < INSTANCE_ID_MIN || InstanceID > INSTANCE_ID_MAX) return false;
   
   string pairs[];
   SplitString(PairList, ",", pairs);
   if(ArraySize(pairs) > MAX_PAIRS) return false;

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
         " MaxActivePair=", IntegerToString(MaxActivePair));

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

   // H4 owner is persistent across neutral H4 candles and changes only on
   // source-valid authoritative H4 direction/momentum events.
   UpdateRuntimeH4DirectionalOwner(pairIndex);

   BollingerBand h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band;
   ZeroMemory(h1Band); ZeroMemory(h1PrevBand);
   ZeroMemory(h4Band); ZeroMemory(h4PrevBand); ZeroMemory(m15Band);

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

      bool h1RawExtreme = DetectExtreme(actual, direction,
                                        g_pair_states[pairIndex].h1_data, h1Band);
      if(direction == DIR_BUY)
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_buy_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h1_data, h1Band, h1RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h1_buy_lifecycle, detectedH1Extreme);
      }
      else
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_sell_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h1_data, h1Band, h1RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h1_sell_lifecycle, detectedH1Extreme);
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
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
         NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);
      }

      if(direction == DIR_BUY)
      {
         UpdatePersistentExtremeState(detectedH1Extreme,
                                      g_pair_states[pairIndex].extreme_h1_buy_state);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;
      }
      else
      {
         UpdatePersistentExtremeState(detectedH1Extreme,
                                      g_pair_states[pairIndex].extreme_h1_sell_state);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;
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

      bool h4RawExtreme = DetectExtreme(actual, direction,
                                        g_pair_states[pairIndex].h4_data, h4Band);
      if(direction == DIR_BUY)
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_buy_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h4_data, h4Band, h4RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h4_buy_lifecycle, detectedH4Extreme);
         UpdatePersistentExtremeState(detectedH4Extreme,
                                      g_pair_states[pairIndex].extreme_h4_buy_state);
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;
      }
      else
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_sell_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h4_data, h4Band, h4RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h4_sell_lifecycle, detectedH4Extreme);
         UpdatePersistentExtremeState(detectedH4Extreme,
                                      g_pair_states[pairIndex].extreme_h4_sell_state);
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;
      }
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

   BBMA_Decision decision;
   OppositeConflictPackage conflict;
   ZeroMemory(decision);
   ZeroMemory(conflict);
   decision.Pair = actual;

   PriorityEngine_Atomic(allCandidates, allCandidateCount, decision, conflict);

   if(decision.DecisionState == DEC_CREATED)
   {
      InvalidationEngine_Atomic(pairIndex, decision, conflict);
   }

   if(decision.DecisionState == DEC_VALIDATED)
      RunEntryPreflightAndExecute(decision, actual);
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
   
   Log(DBG_FULL, "BBMA Professional EA V4.5.1 initialized successfully");
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
}

//+------------------------------------------------------------------+
//| END OF EXPERT ADVISOR                                            |
//+------------------------------------------------------------------+
