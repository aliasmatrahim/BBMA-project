//+------------------------------------------------------------------+
//|                                           BBMA_PROFESSIONAL_EA.mq4 |
//|                                    Version 4.5.1 - PATCHED 2.1    |
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
#property copyright "BBMA Professional EA"
#property link      "https://www.bbmaea.com"
#property version   "4.51"
#property strict

//+------------------------------------------------------------------+
//| MODULE 01: HEADER & INPUTS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

//--- INPUTS
input int      EntryMode                          = 2;          // EntryMode: 1=RE_ENTRY_ONLY, 2=ALL_VALIDATED_BBMA_ENTRIES
input int      TradeLockMode                      = 0;          // TradeLockMode: 0=OFF, 1=SAME_DIRECTION, 2=ONE_POSITION
input int      MaxWaitBars_Extreme                = 5;          // MaxWaitBars_Extreme
input int      MaxWaitBars_MLV                    = 5;          // MaxWaitBars_MLV
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
input string   PairList                           = "EURUSD,GBPUSD,USDJPY"; // PairList
input int      MaxActivePair                      = 5;          // MaxActivePair
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
#define PAIR_ID_MAX             20
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
   SIGNAL_REVERSAL,
   SIGNAL_CONTINUATION,
   SIGNAL_MAJOR_REVERSAL
};

enum ENUM_DIRECTION { DIR_NONE, DIR_BUY, DIR_SELL };

enum ENUM_BB_STATE { BB_NONE, BB_SQUEEZE, BB_EXPANDING, BB_CONTRACTING, BB_FLAT };

enum ENUM_MLV_STATE { MLV_NONE, MLV_CANDIDATE, MLV_CONFIRMED, MLV_VOID, MLV_EXPIRED };

enum ENUM_RE_TYPE { RE_NONE, RE_TYPE_1, RE_TYPE_2, RE_TYPE_3_CSM, RE_TYPE_4_CSD };

enum ENUM_RE_STATE { RE_STATE_NONE, RE_STATE_CANDIDATE, RE_STATE_CONFIRMED, RE_STATE_EXPIRED };

enum ENUM_EXTREME_TYPE { EXT_NONE, EXT_SIDEWAYS, EXT_WITH_MOMENTUM, EXT_WITHOUT_MOMENTUM };

enum ENUM_SIGNAL_LEVEL { LEVEL_NONE, LEVEL_D, LEVEL_C, LEVEL_B, LEVEL_A, LEVEL_A_PLUS };

enum ENUM_PRIORITY_TIER { TIER_NONE, TIER_C, TIER_B, TIER_A, TIER_A_PLUS };

enum ENUM_TRADE_LOCK { LOCK_OFF, LOCK_SAME_DIRECTION, LOCK_ONE_POSITION };

enum ENUM_SIGNAL_MODE { MODE_SAFE, MODE_NORMAL, MODE_AGGRESSIVE, MODE_MANUAL };

enum ENUM_CYCLE_STATE { CYCLE_NONE, CYCLE_WAITING, CYCLE_EXTREME, CYCLE_MHV, 
                        CYCLE_MLV, CYCLE_CSD, CYCLE_RE_ENTRY, CYCLE_COMPLETE, CYCLE_INVALID };

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
                           REC_IDENTITY_HASH_ONLY };

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

struct MLVData
{
   ENUM_MLV_STATE       State;
   ENUM_DIRECTION       Direction;
   string               PatternType;
   string               Reason;
   string               PatternID;
   double               Candle1;
   double               Candle2;
   double               Candle3;
   double               Level1;
   double               Level2;
   double               Neckline;
   int                  StartBar;
   datetime             StartCandleTime;
   int                  LastUpdateBar;
   datetime             LastUpdateCandleTime;
   int                  ConfirmationBar;
   datetime             ConfirmationCandleTime;
   int                  VoidBar;
   int                  ExpiryBar;
   datetime             ExpiryCandleTime;
   bool                 IsValid;
   double               StrengthScore;
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
   bool                 IsValid;
   double               StrengthScore;
   string               Reason;
};

struct SignalMemory
{
   ENUM_SIGNAL_TYPE     Extreme;
   ENUM_SIGNAL_TYPE     MHV;
   ENUM_SIGNAL_TYPE     CSD;
   ENUM_SIGNAL_TYPE     ECSD;
   ENUM_SIGNAL_TYPE     CSM;
   ENUM_SIGNAL_TYPE     REM;
   ENUM_SIGNAL_TYPE     RRE;
   ENUM_SIGNAL_TYPE     REE;
   ENUM_SIGNAL_TYPE     MLV;
   ENUM_SIGNAL_TYPE     ReEntry;
   ENUM_CYCLE_STATE     CycleState;
   ENUM_DIRECTION       Direction;
   ENUM_EXTREME_TYPE    ExtremeType;
   datetime             CycleStartBar;
   datetime             CycleStartCandleTime;
   datetime             LastUpdateBar;
   bool                 IsValid;
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
   double               prev_ema50;
   double               current_ema50;
   double               prev_daily_ema50;
   double               current_daily_ema50;
   SignalMemory         buy_signal_memory;
   SignalMemory         sell_signal_memory;
   // M16 persistent validity overlay for source-detected Extremes.
   // M08 remains the detector; M16 owns temporal invalidation/expiry only.
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

struct TradeRequest
{
   string               pair;
   ENUM_DIRECTION       direction;
   ENUM_SIGNAL_TYPE     signal_type;
   string               comment;
   double               lot;
   double               entry_price;
   double               stop_loss;
   double               take_profit;
   int                  magic_number;
   int                  priority;
   datetime             candle_time;
   double               point;
   int                  digits;
   int                  stop_level;
   int                  freeze_level;
   string               DecisionID;
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

struct OrderResult
{
   int                  ticket;
   bool                 success;
   int                  error;
   bool                 ambiguous;
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

struct ExecutionSnapshot
{
   string               DecisionID;
   string               Pair;
   ENUM_DIRECTION       Direction;
   ENUM_SIGNAL_TYPE     SignalType;
   ENUM_PRIORITY_TIER   PriorityTier;
   double               IntendedEntryPrice;
   double               DecisionStopLoss;
   double               DecisionTakeProfit;
   double               Lot;
   datetime             CandleTime;
   double               CurrentBid;
   double               CurrentAsk;
   double               IntendedExecutionPrice;
   int                  MagicNumber;
   double               IntendedRiskPriceDistance;
   double               FrozenAllowedDeviation;
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
   string base = RemoveSuffix(symbol);
   for(int i = 0; i < SymbolsTotal(true); i++)
   {
      string name = SymbolName(i, true);
      if(StringFind(name, base) == 0)
         return name;
   }
   return symbol;
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

double NormalizePrice(double price, string pair)
{
   int digits = GetDigits(pair);
   return NormalizeDouble(price, digits);
}

double NormalizeLot(double lot, string pair)
{
   int digits = GetLotDigits(pair);
   return NormalizeDouble(RoundDownToLotStep(lot, pair), digits);
}

double RoundToLotStep(double lot, string pair)
{
   double step = GetLotStep(pair);
   if(step <= 0) return lot;
   return MathFloor(lot / step + 0.5) * step;
}

double RoundDownToLotStep(double lot, string pair)
{
   double step = GetLotStep(pair);
   if(step <= 0) return lot;
   return MathFloor(lot / step) * step;
}

bool ValidatePrice(double price, string pair)
{
   if(price <= 0) return false;
   double point = GetPointSize(pair);
   if(point <= 0) return false;
   return true;
}

bool IsSymbolAllowed(string symbol)
{
   return SymbolSelect(symbol, true);
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

int GetTolerance(string pair)
{
   return (int)MarketInfo(pair, MODE_SPREAD);
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
   int hash = 0;
   for(int i = 0; i < StringLen(clean); i++)
   {
      hash = hash * 31 + StringGetChar(clean, i);
   }
   hash = MathAbs(hash);
   return PAIR_ID_MIN + (hash % (PAIR_ID_MAX - PAIR_ID_MIN + 1));
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

string FormatNumber(double number, int decimals)
{
   return DoubleToString(number, decimals);
}

void RefreshPrices()
{
   RefreshRates();
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

PairState GetPairState(string pair)
{
   int idx = FindPairStateIndex(pair);
   if(idx >= 0 && idx < g_pair_count)
      return g_pair_states[idx];
   PairState empty;
   InitPairState(empty);
   return empty;
}

void StorePairState(PairState &state)
{
   int idx = FindPairStateIndex(state.base_symbol);
   if(idx >= 0 && idx < g_pair_count)
      g_pair_states[idx] = state;
}

void InitPairState(PairState &state)
{
   state.base_symbol = "";
   state.actual_symbol = "";
   state.pair_id = 0;
   state.point = 0;
   state.tick_value = 0;
   state.tick_size_price = 0;
   state.min_lot = 0;
   state.max_lot = 0;
   state.lot_step = 0;
   state.lot_digits = 2;
   state.cent_factor = 1;
   state.digits = 5;
   state.stop_level = 0;
   state.freeze_level = 0;
   state.is_cent_account = false;
   state.pair_enabled = false;
   state.is_processing = false;
   state.last_3_count = 0;
   state.last_5_count = 0;
   state.last_20_count = 0;
   ZeroMemory(state.mlv_buy_state);
   ZeroMemory(state.mlv_sell_state);
   state.mlv_buy_state.State = MLV_NONE;
   state.mlv_buy_state.Direction = DIR_BUY;
   state.mlv_sell_state.State = MLV_NONE;
   state.mlv_sell_state.Direction = DIR_SELL;
   ZeroMemory(state.re_h1_buy_state);
   ZeroMemory(state.re_h1_sell_state);
   ZeroMemory(state.re_h4_buy_state);
   ZeroMemory(state.re_h4_sell_state);
   ZeroMemory(state.re_d1_buy_state);
   ZeroMemory(state.re_d1_sell_state);
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
   state.trade_count = 0;
   state.magic_number = 0;
   state.broker_retry_count = 0;
   state.broker_spec_valid = false;
   ZeroMemory(state.extreme_h1_buy_state);
   ZeroMemory(state.extreme_h1_sell_state);
   ZeroMemory(state.extreme_h4_buy_state);
   ZeroMemory(state.extreme_h4_sell_state);
}

void CopyPairState(PairState &dest, PairState &src)
{
   dest = src;
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

void CopyTimeframeData(TimeframeData &dest, TimeframeData &src)
{
   dest = src;
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

   // Executed rows are idempotency tombstones and must never be removed by the
   // generic size cleanup. Remove only non-executed rows, oldest first.
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

   // If executed tombstones alone exceed SIGNAL_HISTORY_MAX, preserve them.
   // Correct duplicate prevention takes precedence over a soft history-size cap.
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

datetime GetCandleTimeFromBarIndex(string pair, int timeframe, int shift)
{
   return iTime(pair, timeframe, shift);
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

datetime GetExpiryTime(Signal &signal, int maxWaitBars)
{
   int seconds = GetTimeframeSeconds(signal.Timeframe);
   return signal.CandleTime + (maxWaitBars * seconds);
}

datetime GetGlobalExpiryTime(datetime cycleStartTime)
{
   return cycleStartTime + (MaxWaitBars_Global * 900);
}

datetime GetCombinedExpiry(datetime combinationStartTime)
{
   return combinationStartTime + (MaxWaitBars_Combined * 900);
}

datetime GetEffectiveExpiry(datetime individual, datetime combined, datetime global)
{
   datetime min = individual;
   if(combined < min) min = combined;
   if(global < min) min = global;
   return min;
}

double GetEffectiveMaxLot(string pair)
{
   double brokerMax = GetMaxLot(pair);
   if(MaxAutoLot < brokerMax)
      return MaxAutoLot;
   return brokerMax;
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
   // Combination identity must include the BBMA setup type and each component TF.
   // SL/TP source is deliberately excluded: M13 is a collector, not an SL/TP owner.
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

   // UPSERT by full DecisionID or stable execution hash.
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

   // A successful execution may occur before any ordinary history row exists.
   // Create the tombstone immediately so the same DecisionID cannot execute
   // again later in the same terminal session after the position has closed.
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
   // Restart idempotency is execution-hash based. Scan BOTH open and historical
   // EA orders so an already-executed decision cannot be recreated after restart
   // merely because its position has already closed.
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

// FIX 3 & 4: Create comment with C: for candle time
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

// FIX 3 & 4: Parse comment with full fields including C:
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
      else if(key == "C") candleTime = StringToTime(value);  // FIX 3: Parse actual candle time
      else if(key == "P") pair = value;
      else if(key == "D") direction = (ENUM_DIRECTION)StringToInteger(value);
      else if(key == "T") signalType = (ENUM_SIGNAL_TYPE)StringToInteger(value);
      else if(key == "E") intendedEntry = StringToDouble(value);
      else if(key == "S") intendedSL = StringToDouble(value);
      else if(key == "L") intendedLot = StringToDouble(value);
      else if(key == "R") intendedRisk = StringToDouble(value);
      else if(key == "Q") sequenceHash = value;
   }
   // Full parsing is metadata only. Recovery identity is H:, because brokers may
   // truncate later fields and Q: stores a hash of SequenceHash, not the original
   // SequenceHash required to reconstruct the exact original DecisionID.
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

double ConvertSpreadToPoints(string pair, double spreadPips)
{
   int digits = GetDigits(pair);
   int multiplier = (digits == 5 || digits == 3) ? 10 : 1;
   return spreadPips * multiplier;
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
   // Close-price SMA is retained for Bollinger calculations only.
   // BBMA MA5/10 High/Low must use the source-defined LWMA applied price.
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
   // Source setting: Exponential MA applied to Close. Using MT4 iMA avoids
   // the previous custom recurrence being evaluated newest-to-oldest.
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
   // BBMA source settings:
   // MA5/10 High = Linear Weighted applied to High.
   // MA5/10 Low  = Linear Weighted applied to Low.
   // MA50        = Exponential applied to Close.
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

void CreateCandleFromData(TimeframeData &data, Candle &candle)
{
   candle.Open = data.open;
   candle.High = data.high;
   candle.Low = data.low;
   candle.Close = data.close;
   candle.Time = data.candle_time;
   candle.Index = data.barIndex;
   candle.Type = 0;
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

double AverageBodySize(string pair, int timeframe, int count, int shift)
{
   double sum = 0;
   int total = 0;
   for(int i = 0; i < count; i++)
   {
      double open = iOpen(pair, timeframe, shift + i);
      double close = iClose(pair, timeframe, shift + i);
      if(open > 0 && close > 0)
      {
         sum += MathAbs(close - open);
         total++;
      }
   }
   if(total == 0) return 0;
   return sum / total;
}

double GetHighestHigh3(string pair, int timeframe, int shift)
{
   return GetHighestHigh(pair, timeframe, 3, shift);
}

double GetLowestLow3(string pair, int timeframe, int shift)
{
   return GetLowestLow(pair, timeframe, 3, shift);
}

//+------------------------------------------------------------------+
//| MODULE 07: BB SHAPE ENGINE                                       |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

ENUM_BB_STATE DetectBBState(BollingerBand &current, BollingerBand &previous)
{
   if(current.Width <= 0 || previous.Width <= 0) return BB_NONE;
   
   double widthRatio = current.Width / previous.Width;
   
   if(widthRatio < 0.9)
      return BB_SQUEEZE;
   else if(widthRatio > 1.1)
      return BB_EXPANDING;
   else if(widthRatio >= 0.9 && widthRatio <= 1.1)
      return BB_CONTRACTING;
   return BB_FLAT;
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
   
   current.State = DetectBBState(current, previous);
   return (current.State != BB_NONE);
}

int CalculateBollingerArray(string pair, int timeframe, int period, int count, double &result[])
{
   if(count < 0) count = 0;
   ArrayResize(result, count);
   for(int i = 0; i < count; i++)
   {
      result[i] = SMA(pair, timeframe, period, i);
   }
   return count;
}

string GetBBStateString(ENUM_BB_STATE state)
{
   switch(state)
   {
      case BB_SQUEEZE: return "SQUEEZE";
      case BB_EXPANDING: return "EXPANDING";
      case BB_CONTRACTING: return "CONTRACTING";
      case BB_FLAT: return "FLAT";
      default: return "NONE";
   }
}

//+------------------------------------------------------------------+
//| MODULE 08: EXTREME DETECTOR                                      |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool DetectExtreme(string pair, ENUM_DIRECTION direction, TimeframeData &data, BollingerBand &band)
{
   if(!data.is_valid || !data.is_closed) return false;
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   // M08 detects the BBMA Extreme SIGNAL only. A detected Extreme is not
   // automatically an execution-eligible standalone entry. The source requires
   // reversal-candle confirmation and identifies the retest candle as the
   // standalone Extreme entry point; that entry-eligibility contract is handled
   // separately from raw signal detection.
   if(direction == DIR_SELL)
   {
      double ma5High = data.ma[0];
      double ma10High = data.ma[1];
      if(ma5High <= 0 || ma10High <= 0) return false;

      // Source contract: SELL Extreme forms when MA5 or MA5/10 High is
      // outside the TOP BB. A candle close outside TOP BB makes it VOID.
      bool maOutside = (ma5High > band.TOP_BB || ma10High > band.TOP_BB);
      if(!maOutside) return false;
      if(data.close > band.TOP_BB) return false;
      return true;
   }

   double ma5Low = data.ma[2];
   double ma10Low = data.ma[3];
   if(ma5Low <= 0 || ma10Low <= 0) return false;

   // Source contract: BUY Extreme forms when MA5 or MA5/10 Low is
   // outside the LOW BB. A candle close outside LOW BB makes it VOID.
   bool maOutside = (ma5Low < band.LOW_BB || ma10Low < band.LOW_BB);
   if(!maOutside) return false;
   if(data.close < band.LOW_BB) return false;
   return true;
}

void BuildSLTP_Extreme(ENUM_DIRECTION direction, double entryPrice, 
                       double &sl, double &tp, double &slPoints)
{
   double point = GetPointSize(Symbol());
   double slDistance = MaxSLPips * point / 10;
   
   if(direction == DIR_BUY)
   {
      sl = entryPrice - slDistance;
      tp = entryPrice + slDistance * MinRRRatio;
   }
   else if(direction == DIR_SELL)
   {
      sl = entryPrice + slDistance;
      tp = entryPrice - slDistance * MinRRRatio;
   }
   slPoints = MathAbs(entryPrice - sl);
}

//+------------------------------------------------------------------+
//| MODULE 09: MHV & MLV STATE ENGINE                                |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

bool DetectMHV(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!data.is_valid || !data.is_closed) return false;
   if(data.ma[0] <= 0 || data.ma[2] <= 0) return false;
   
   if(direction == DIR_BUY)
   {
      double ma5_high = data.ma[0];
      if(data.close > ma5_high)
      {
         double prev_ma5_high = BBMAHighMA(pair, data.timeframe, MA5_HIGH_PERIOD, data.barIndex + 1);
         if(prev_ma5_high > 0 && ma5_high > prev_ma5_high)
            return true;
      }
   }
   else if(direction == DIR_SELL)
   {
      double ma5_low = data.ma[2];
      if(data.close < ma5_low)
      {
         double prev_ma5_low = BBMALowMA(pair, data.timeframe, MA5_LOW_PERIOD, data.barIndex + 1);
         if(prev_ma5_low > 0 && ma5_low < prev_ma5_low)
            return true;
      }
   }
   return false;
}

void ResetMLVState(MLVData &mlv, ENUM_DIRECTION direction)
{
   ZeroMemory(mlv);
   mlv.State = MLV_NONE;
   mlv.Direction = direction;
}

void MarkMLVVoid(MLVData &mlv, datetime voidCandleTime, int voidBar, string reason)
{
   if(mlv.State == MLV_NONE || mlv.State == MLV_EXPIRED) return;
   mlv.State = MLV_VOID;
   mlv.IsValid = false;
   mlv.VoidBar = voidBar;
   mlv.LastUpdateBar = voidBar;
   mlv.LastUpdateCandleTime = voidCandleTime;
   mlv.Reason = reason;
}

bool IsMLVIntrinsicExpired(MLVData &mlv, datetime currentCandleTime)
{
   if(mlv.StartCandleTime <= 0 || mlv.ExpiryCandleTime <= 0) return false;
   return (currentCandleTime > mlv.ExpiryCandleTime);
}

ENUM_MLV_STATE DetectMLV_State(MLVData &mlv, string pair,
                               ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableMLVStateEngine) return MLV_NONE;
   if(direction != DIR_BUY && direction != DIR_SELL) return MLV_NONE;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return mlv.State;
   
   // A terminal state is kept for one completed processing candle, then released
   // so the same pair+direction slot can detect a new independent MLV pattern.
   if((mlv.State == MLV_VOID || mlv.State == MLV_EXPIRED) &&
      mlv.LastUpdateCandleTime > 0 && data.candle_time > mlv.LastUpdateCandleTime)
   {
      ResetMLVState(mlv, direction);
   }
   
   // Each persistent slot is direction-owned. Never let a BUY update mutate SELL state.
   if(mlv.State != MLV_NONE && mlv.Direction != direction)
      return mlv.State;
   
   if((mlv.State == MLV_CANDIDATE || mlv.State == MLV_CONFIRMED) &&
      IsMLVIntrinsicExpired(mlv, data.candle_time))
   {
      mlv.State = MLV_EXPIRED;
      mlv.IsValid = false;
      mlv.Reason = "MaxWaitBars_MLV expired";
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      return MLV_EXPIRED;
   }
   
   if(mlv.State == MLV_NONE)
   {
      double point = GetPointSize(pair);
      if(point <= 0 || data.barIndex < 1) return MLV_NONE;
      
      double currentLevel = 0;
      double previousLevel = 0;
      string patternType = "";
      
      if(direction == DIR_SELL)
      {
         currentLevel = data.high;
         previousLevel = iHigh(pair, data.timeframe, data.barIndex + 2);
         patternType = "DoubleTop";
      }
      else
      {
         currentLevel = data.low;
         previousLevel = iLow(pair, data.timeframe, data.barIndex + 2);
         patternType = "DoubleBottom";
      }
      
      if(currentLevel <= 0 || previousLevel <= 0) return MLV_NONE;
      if(MathAbs(currentLevel - previousLevel) >= point * 10) return MLV_NONE;
      
      mlv.State = MLV_CANDIDATE;
      mlv.Direction = direction;
      mlv.PatternType = patternType;
      mlv.Level1 = currentLevel;
      mlv.Level2 = previousLevel;
      mlv.Neckline = (direction == DIR_SELL)
                     ? (mlv.Level1 + mlv.Level2) / 2 - point * 5
                     : (mlv.Level1 + mlv.Level2) / 2 + point * 5;
      mlv.StartBar = data.barIndex;
      mlv.StartCandleTime = data.candle_time;
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.ExpiryBar = MaxWaitBars_MLV;
      mlv.ExpiryCandleTime = mlv.StartCandleTime + MaxWaitBars_MLV * data.timeframe * 60;
      mlv.PatternID = patternType + "_" + TimeToString(mlv.StartCandleTime);
      mlv.IsValid = false;
      mlv.Reason = "Awaiting confirmation";
      return MLV_CANDIDATE;
   }
   
   if(mlv.State == MLV_CANDIDATE)
   {
      // Confirmation must occur on a later closed M15 candle, never on the
      // same candle that created the candidate.
      if(data.candle_time <= mlv.StartCandleTime) return MLV_CANDIDATE;
      
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      
      bool confirmed = false;
      if(direction == DIR_SELL)
         confirmed = (data.close > 0 && data.close < mlv.Neckline);
      else
         confirmed = (data.close > 0 && data.close > mlv.Neckline);
      
      if(confirmed)
      {
         mlv.State = MLV_CONFIRMED;
         mlv.ConfirmationBar = data.barIndex;
         mlv.ConfirmationCandleTime = data.candle_time;
         mlv.IsValid = true;
         mlv.Reason = "Confirmed";
         return MLV_CONFIRMED;
      }
      return MLV_CANDIDATE;
   }
   
   if(mlv.State == MLV_CONFIRMED)
   {
      mlv.IsValid = true;
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
   }
   
   return mlv.State;
}

bool DetectMLVPattern(string pair, int timeframe, ENUM_DIRECTION direction,
                      MLVData &mlv, datetime candleTime)
{
   TimeframeData data;
   InitTimeframeData(data);
   GetDataForTimeframe(pair, timeframe, candleTime, data);
   if(!data.is_valid || !data.is_closed) return false;
   return DetectMLV_State(mlv, pair, direction, data) == MLV_CONFIRMED;
}

bool IsMLVPatternStillValid(MLVData &mlv, datetime currentTime)
{
   if(mlv.State != MLV_CONFIRMED) return false;
   if(!mlv.IsValid) return false;
   if(mlv.ExpiryCandleTime <= 0) return false;
   return currentTime <= mlv.ExpiryCandleTime;
}

void GetMLVEntry(MLVData &mlv, ENUM_DIRECTION direction, 
                 double &entry, double &sl, double &tp, double &slPoints)
{
   double point = GetPointSize(Symbol());
   double slDistance = MaxSLPips * point / 10;
   
   if(direction == DIR_BUY)
   {
      entry = mlv.Level2 + point * 5;
      sl = mlv.Level1 - slDistance;
      tp = entry + slDistance * MinRRRatio;
   }
   else if(direction == DIR_SELL)
   {
      entry = mlv.Level2 - point * 5;
      sl = mlv.Level1 + slDistance;
      tp = entry - slDistance * MinRRRatio;
   }
   slPoints = MathAbs(entry - sl);
}

//+------------------------------------------------------------------+
//| MODULE 10: CSM, CSD, eCSD                                        |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

bool IsReversalCandle(Candle &candle)
{
   double body = MathAbs(candle.Close - candle.Open);
   double range = candle.High - candle.Low;
   if(range <= 0) return false;
   return (body / range) > 0.6;
}

bool IsCandleCloseOutsideBB(Candle &candle, BollingerBand &band)
{
   if(candle.Close <= 0 || band.MID_BB <= 0) return false;
   return (candle.Close > band.TOP_BB || candle.Close < band.LOW_BB);
}

bool IsCandleCloseInsideBB(Candle &candle, BollingerBand &band)
{
   if(candle.Close <= 0 || band.MID_BB <= 0) return false;
   return (candle.Close >= band.LOW_BB && candle.Close <= band.TOP_BB);
}

bool IsCandleCloseAbove(Candle &candle, double level)
{
   return candle.Close > level;
}

bool IsCandleCloseBelow(Candle &candle, double level)
{
   return candle.Close < level;
}

bool IsCandleCloseNear(Candle &candle, double level, string pair)
{
   double point = GetPointSize(pair);
   return MathAbs(candle.Close - level) < point * 5;
}

bool IsDoubleTopPattern(Candle &candle1, Candle &candle2, double tolerance)
{
   if(candle1.High <= 0 || candle2.High <= 0) return false;
   return MathAbs(candle1.High - candle2.High) < tolerance;
}

bool IsDoubleBottomPattern(Candle &candle1, Candle &candle2, double tolerance)
{
   if(candle1.Low <= 0 || candle2.Low <= 0) return false;
   return MathAbs(candle1.Low - candle2.Low) < tolerance;
}

bool HasRecentCSD(SignalMemory &memory, int bars)
{
   return (memory.CSD != SIGNAL_NONE);
}

bool HasRecentCSM(SignalMemory &memory, int bars)
{
   return (memory.CSM != SIGNAL_NONE);
}

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

   // Source: a candle close outside TOP/LOW BB while BB is vertical marks
   // directional MOMENTUM. The reference also describes expanding BB as
   // momentum getting stronger.
   //
   // Operational encoding of "BB vertical":
   // - BB width is increasing versus the previous closed candle; and
   // - MID BB is moving in the same direction as the momentum.
   // No arbitrary percentage threshold is added.
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

   // Source: eCSD crosses MA5/10; CSD crosses MA5/10 AND MID BB.
   // Operational encoding: "crosses" means the CLOSED candle body spans
   // each required line from open to close. Wick-only touches do not count.
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

   // Source: eCSD is the early direction candle that crosses MA5/10,
   // without requiring the MID BB cross that distinguishes a full CSD.
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

void BuildSLTP_CSD(ENUM_DIRECTION direction, double entryPrice,
                   double &sl, double &tp, double &slPoints)
{
   double point = GetPointSize(Symbol());
   double slDistance = MaxSLPips * point / 10;
   
   if(direction == DIR_BUY)
   {
      sl = entryPrice - slDistance;
      tp = entryPrice + slDistance * MinRRRatio;
   }
   else if(direction == DIR_SELL)
   {
      sl = entryPrice + slDistance;
      tp = entryPrice - slDistance * MinRRRatio;
   }
   slPoints = MathAbs(entryPrice - sl);
}

//+------------------------------------------------------------------+
//| MODULE 11: TREND FUNCTIONS                                       |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

int GetTrend(string pair, int timeframe, int shift)
{
   double ema50 = EMA(pair, timeframe, EMA50_PERIOD, shift);
   double close = iClose(pair, timeframe, shift);
   if(close <= 0 || ema50 <= 0) return 0;
   if(close > ema50) return 1;
   if(close < ema50) return -1;
   return 0;
}

double GetTrendFromMA50(string pair, int timeframe, int shift)
{
   return EMA(pair, timeframe, EMA50_PERIOD, shift);
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

   // BBMA source law: BUY uses MA5/10 Low; SELL uses MA5/10 High.
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
      // Market finds MA5/10 Low and candle closes above the support cluster.
      return (data.low <= MathMax(ma5, ma10) &&
              data.close >= ma5 && data.close >= ma10);
   }

   // Market finds MA5/10 High and candle closes below the resistance cluster.
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

bool DetectReEntry_Type1(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type1) return false;
   if(!data.is_valid || !data.is_closed) return false;

   // Source: Re-Entry Type 1 is made when price finds the relevant
   // MA5/10 High (SELL) or MA5/10 Low (BUY), with CS closing on the
   // resistance/support side of the cluster. No EMA50-cross rule is stated.
   return HasReEntryMAClusterTouch(data, direction);
}

bool DetectReEntry_Type2(string pair, ENUM_DIRECTION direction, TimeframeData &data,
                         bool &mostPowerful)
{
   mostPowerful = false;
   if(!EnableRE_Type2) return false;
   if(!data.is_valid || !data.is_closed || data.bollinger[1] <= 0) return false;

   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;

   // Source: Powerful Re-Entry = MA5/10 and MID BB meet/collide.
   // Existing project IsNear() is used only as numerical collision tolerance;
   // it is not a new BBMA strategy condition.
   bool powerful = IsNear(ma5, data.bollinger[1], pair) &&
                   IsNear(ma10, data.bollinger[1], pair);
   if(!powerful) return false;

   // Source: Most Powerful Re-Entry also includes MA50 in the collision.
   mostPowerful = (data.ma[4] > 0 && IsNear(data.ma[4], data.bollinger[1], pair));
   return true;
}

bool DetectReEntry_Type3(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type3) return false;
   if(!data.is_valid || !data.is_closed) return false;

   // Type 3 candidate begins only after a source-valid CSM has formed.
   // The later retrace to MA5 or MA50 is handled by the persistent lifecycle.
   return DetectCSM(pair, data.timeframe, direction, data.barIndex);
}

bool DetectReEntry_Type4(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type4) return false;
   if(!data.is_valid || !data.is_closed) return false;

   MovingAverage ma;
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];

   BollingerBand band;
   ZeroMemory(band);
   band.TOP_BB = data.bollinger[0];
   band.MID_BB = data.bollinger[1];
   band.LOW_BB = data.bollinger[2];
   band.Width = band.TOP_BB - band.LOW_BB;

   // Type 4 candidate begins when CSD appears. The later gyration/retrace
   // toward MA5/10 is handled by the persistent lifecycle below.
   return DetectCSD(pair, data.timeframe, direction, data.barIndex, ma, band);
}

ENUM_RE_TYPE DetectReEntry_Master(string pair, ENUM_DIRECTION direction,
                                  TimeframeData &data, bool &mostPowerful)
{
   mostPowerful = false;

   // Preserve existing detector precedence; Step 3B changes source semantics,
   // not cross-type priority policy.
   if(DetectReEntry_Type2(pair, direction, data, mostPowerful)) return RE_TYPE_2;
   if(DetectReEntry_Type1(pair, direction, data)) return RE_TYPE_1;
   if(DetectReEntry_Type3(pair, direction, data)) return RE_TYPE_3_CSM;
   if(DetectReEntry_Type4(pair, direction, data)) return RE_TYPE_4_CSD;
   return RE_NONE;
}

void ResetReEntryState(ReEntryData &reEntry, ENUM_DIRECTION direction, int timeframe)
{
   ZeroMemory(reEntry);
   reEntry.Type = RE_NONE;
   reEntry.State = RE_STATE_NONE;
   reEntry.Direction = direction;
   reEntry.Timeframe = timeframe;
}

bool IsReEntryIntrinsicExpired(ReEntryData &reEntry, datetime currentCandleTime)
{
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
   reEntry.EntryCandle = data.candle_time;
   reEntry.EntryPrice = data.close;
   reEntry.IsValid = true;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   SetReEntrySnapshotLevels(reEntry, data);
   reEntry.Reason = reason;
}

ENUM_RE_STATE UpdateReEntryState(ReEntryData &reEntry, string pair,
                                 ENUM_DIRECTION direction, TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return RE_STATE_NONE;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return reEntry.State;

   // EXPIRED is retained for one completed timeframe candle before reuse.
   if(reEntry.State == RE_STATE_EXPIRED &&
      reEntry.LastUpdateCandleTime > 0 &&
      data.candle_time > reEntry.LastUpdateCandleTime)
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
   }

   // One slot is owned by one timeframe + direction.
   if(reEntry.State != RE_STATE_NONE &&
      (reEntry.Direction != direction || reEntry.Timeframe != data.timeframe))
      return reEntry.State;

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

   if(reEntry.State == RE_STATE_NONE)
   {
      bool mostPowerful = false;
      ENUM_RE_TYPE detectedType = DetectReEntry_Master(pair, direction, data, mostPowerful);
      if(detectedType == RE_NONE) return RE_STATE_NONE;

      reEntry.Type = detectedType;
      reEntry.Direction = direction;
      reEntry.Timeframe = data.timeframe;
      reEntry.EntryPrice = 0;
      reEntry.EntryCandle = 0;
      reEntry.StartBar = data.barIndex;
      reEntry.StartCandleTime = data.candle_time;
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      reEntry.ConfirmationBar = 0;
      reEntry.ConfirmationCandle = 0;
      reEntry.ExpiryBar = MaxWaitBars_ReEntry;
      reEntry.ExpiryCandleTime =
         reEntry.StartCandleTime + MaxWaitBars_ReEntry * data.timeframe * 60;
      reEntry.IsValid = false;
      SetReEntrySnapshotLevels(reEntry, data);

      // Type 1 source contains no separate precursor/confirmation stage:
      // the relevant MA5/10 touch on a CLOSED candle is the Re-Entry setup.
      if(detectedType == RE_TYPE_1)
      {
         reEntry.MinCandlesRequired = 1;
         reEntry.QualifyingCandles = 1;
         ConfirmReEntryState(reEntry, data,
            (direction == DIR_BUY)
            ? "Type1 confirmed: MA5/10 Low support touch"
            : "Type1 confirmed: MA5/10 High resistance touch");
         return RE_STATE_CONFIRMED;
      }

      reEntry.State = RE_STATE_CANDIDATE;
      reEntry.QualifyingCandles = 1;

      if(detectedType == RE_TYPE_2)
      {
         // Operational encoding of the source phrase "minimum of 3 candles per TF":
         // three DISTINCT consecutive closed candles must retain the MA5/10 + MID BB
         // collision. This interpretation is explicit and must not be silently changed.
         reEntry.MinCandlesRequired = 3;
         reEntry.Reason = mostPowerful
                          ? "Type2 candidate: MA5/10 + MID BB + MA50 collision (1/3)"
                          : "Type2 candidate: MA5/10 + MID BB collision (1/3)";
      }
      else if(detectedType == RE_TYPE_3_CSM)
      {
         reEntry.MinCandlesRequired = 1;
         reEntry.Reason = "Type3 candidate: CSM formed; awaiting retrace to MA5 or MA50";
      }
      else if(detectedType == RE_TYPE_4_CSD)
      {
         reEntry.MinCandlesRequired = 1;
         reEntry.Reason = "Type4 candidate: CSD formed; awaiting retrace to MA5/10";
      }

      return RE_STATE_CANDIDATE;
   }

   if(reEntry.State == RE_STATE_CANDIDATE)
   {
      // M15 is the sole orchestration clock, but one H1/H4/D1 snapshot can be
      // observed repeatedly. Lifecycle advances only on a NEW closed candle of
      // the candidate's own timeframe.
      if(data.candle_time <= reEntry.LastUpdateCandleTime) return RE_STATE_CANDIDATE;

      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      SetReEntrySnapshotLevels(reEntry, data);

      if(reEntry.Type == RE_TYPE_2)
      {
         bool mostPowerful = false;
         if(!DetectReEntry_Type2(pair, direction, data, mostPowerful))
         {
            // Three-candle Type 2 confluence must remain continuous.
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

         // General BBMA Re-Entry law still requires the market to find the
         // relevant MA5/10 entry cluster; line confluence alone is not a raw entry.
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

void BuildReEntrySignal(ENUM_RE_TYPE type, ENUM_DIRECTION direction, double entryPrice,
                        double &sl, double &tp, double &slPoints)
{
   double point = GetPointSize(Symbol());
   double slDistance = MaxSLPips * point / 10;
   
   if(direction == DIR_BUY)
   {
      sl = entryPrice - slDistance;
      tp = entryPrice + slDistance * MinRRRatio;
   }
   else if(direction == DIR_SELL)
   {
      sl = entryPrice + slDistance;
      tp = entryPrice - slDistance * MinRRRatio;
   }
   slPoints = MathAbs(entryPrice - sl);
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
   // M13 is a pure collector. Detector/state-engine ownership remains in
   // M08/M09/M10/M12; M13 only copies immutable per-cycle snapshots.
   extreme = h1_extreme_snapshot;
   mhv = m15_mhv_snapshot;
   mlv = m15_mlv_snapshot;
   csd = m15_csd_snapshot;
   ecsd = m15_ecsd_snapshot;
   csm = m15_csm_snapshot;
   reEntry = h1_reEntry_snapshot;

   // A full CSD mechanically also crosses MA5/10, so the same closed candle may
   // satisfy the simpler eCSD predicate. Source classification gives CSD the
   // stronger identity because it additionally crosses MID BB. Do not count the
   // same candle as two independent confirmations.
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
   return (mlv.State == MLV_CONFIRMED &&
           mlv.IsValid &&
           mlv.Direction != DIR_NONE &&
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
   set.SLTPSource = SIGNAL_NONE; // SL/TP ownership is downstream, never M13.
   set.SequenceHash = GenerateSequenceHash(set);
}

void BuildPossibleCombinations(ComponentSet &rem, ComponentSet &rre, ComponentSet &ree,
                               Signal &h4_reEntry, Signal &h1_extreme, MLVData &m15_mlv,
                               Signal &d1_reEntry, Signal &h4_extreme)
{
   ZeroMemory(rem);
   ZeroMemory(rre);
   ZeroMemory(ree);

   // Source row available in this project: H4 Re-Entry + H1 Extreme + M15 MLV.
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

   // Source row available in this project: D1 Re-Entry + H4 Re-Entry + H1 Extreme.
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

   // Source row available in this project: D1 Re-Entry + H4 Extreme + H1 Extreme.
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

   // Source-locked project rows from the REM/RRE/REE BBMA table.
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

   // M14 validates only. M13 does not own SL/TP and the supplied source does
   // not define a priority tier among REM/RRE/REE. Those policies remain
   // downstream responsibilities and must not be invented here.
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

   // REM/RRE/REE are multi-timeframe combinations, not a universal
   // Comp1 < Comp2 < Comp3 chronological sequence. M13 supplies components
   // that coexist as valid owner snapshots in the current processing cycle.
   // M14 validates identity, exact TF signature and direction consistency only.
   // Expiry/freshness policy remains downstream and must use owner-aware data.
   if(!ValidateCombinationSignature(set) ||
      !ValidateDirectionConsistency(set))
   {
      candidate.Valid = false;
      return;
   }

   PopulateValidatedCombination(set, candidate);
}

datetime CheckEffectiveExpiry(datetime individual, datetime combined, datetime global)
{
   return GetEffectiveExpiry(individual, combined, global);
}

//+------------------------------------------------------------------+
//| MODULE 15: PRIORITY ENGINE (FINAL SIGNAL AUTHORITY)              |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsEntryModeCandidateAllowed(ValidatedSequenceCandidate &candidate)
{
   if(EntryMode == 1) // RE_ENTRY_ONLY
      return (candidate.SequenceType == SIGNAL_RE_ENTRY);

   if(EntryMode == 2) // ALL_VALIDATED_BBMA_ENTRIES
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

   // Candidates are rebuilt atomically on every closed M15 processing cycle.
   // Persistent validity belongs to the owner module. A non-zero Expiry here is
   // used only when the owner exported an explicit expiry (e.g. Re-Entry).
   if(candidate.Expiry > 0 && candidate.Expiry < g_processing_time) return false;
   return true;
}

void BuildConfirmedReEntryCandidate(ReEntryData &reEntry,
                                    ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);

   // M12 is the sole Re-Entry lifecycle owner. M15 only normalizes an already
   // confirmed snapshot into the common final-authority candidate format.
   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return;
   if(reEntry.Direction != DIR_BUY && reEntry.Direction != DIR_SELL) return;
   if(reEntry.Timeframe != PERIOD_H1) return;
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
   // This is deterministic bookkeeping, NOT a BBMA quality ranking.
   // When several same-direction entries are simultaneously valid, use the
   // freshest current-cycle representation. No REM/RRE/REE superiority is invented.
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

   // M15 is the final direction authority. Opposite validated opportunities are
   // resolved atomically. The supplied BBMA source does not define a universal
   // tie-break rule between simultaneous BUY and SELL setups, so no trade is
   // preferred by invention.
   if(buyCount > 0 && sellCount > 0)
   {
      conflict.Exists = true;
      conflict.ConflictType = CONFLICT_DIRECTION_VIOLATION;
      conflict.ConflictReason = "Opposite validated BBMA entries coexist";
      conflict.FrozenSnapshotTime = g_processing_time;
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
}

//+------------------------------------------------------------------+
//| MODULE 16: CONFLICT & INVALIDATION ENGINE                        |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsExtremeStateExpired(Signal &extreme, datetime currentTime)
{
   // Expiry and invalidation are different states. Invalid/VOID-by-CSM must not
   // be mislabeled as time expiry.
   if(extreme.CandleTime <= 0 || extreme.Timeframe <= 0)
      return false;

   datetime expiry = extreme.CandleTime +
                     (MaxWaitBars_Extreme * extreme.Timeframe * 60);
   return (currentTime > expiry);
}

void UpdatePersistentExtremeState(Signal &detectedExtreme, Signal &csmSnapshot,
                                  Signal &state)
{
   // M08 remains the detector. M16 only stores validity identity and applies
   // temporal invalidation/expiry to that already-detected Extreme.
   if(detectedExtreme.Valid)
   {
      if(!state.Valid || detectedExtreme.CandleTime >= state.CandleTime)
         state = detectedExtreme;
   }

   if(state.Valid && IsExtremeStateExpired(state, g_processing_time))
   {
      state.Valid = false;
      state.Reason = "Extreme expired by timeframe-aware project window";
   }

   // Source rule: an Extreme is no longer valid in the presence of CSM.
   // Operational encoding: a later CLOSED CSM on the same timeframe invalidates
   // the stored Extreme. Direction is deliberately not used as an extra source rule.
   if(state.Valid && csmSnapshot.Valid &&
      csmSnapshot.Type == SIGNAL_CSM &&
      csmSnapshot.Timeframe == state.Timeframe &&
      csmSnapshot.CandleTime > state.CandleTime)
   {
      state.Valid = false;
      state.Reason = "Extreme invalidated by later same-TF CSM";
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

   if(mlv.ExpiryCandleTime > 0 && g_processing_time > mlv.ExpiryCandleTime)
   {
      expired = true;
      return false;
   }

   return (mlv.State == MLV_CONFIRMED &&
           mlv.IsValid &&
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

   // Step 6 normally produces no DEC_CREATED decision when opposite validated
   // BUY and SELL coexist. Keep this guard for any future conflict package that
   // reaches M16 together with a created decision.
   if(conflict.Exists &&
      (conflict.ConflictType == CONFLICT_DIRECTION_VIOLATION ||
       conflict.BreaksSequence))
   {
      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_OPPOSITE_SIGNAL;
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

   // Explicit candidate expiry is carried only when an owner supplies one
   // (currently standalone confirmed Re-Entry). No generic M15 multiplier here.
   if(decision.CandidateExpiry > 0 && g_processing_time > decision.CandidateExpiry)
   {
      decision.DecisionState = DEC_EXPIRED;
      decision.RejectionReason = REJ_EXPIRED;
      return;
   }

   decision.DecisionState = DEC_VALIDATED;
   decision.RejectionReason = REJ_NONE;
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
   if(shift < 1) return -1; // source must remain a fully closed candle

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
   // Step 8C implements the approved Step 8B mapping only. It does not create
   // new detector logic, fixed-pip targets, RR-derived targets or higher-TF TP2/TP3.
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

   // EA_SAFETY: one broker point beyond the exact closed source candle wick.
   // This buffer is engineering protection and must not be represented as a
   // PDF Oma Ally rule.
   double safetyBuffer = snapshot.Point;
   double structuralSL = (decision.Direction == DIR_BUY)
      ? wickAnchor - safetyBuffer
      : wickAnchor + safetyBuffer;

   // A crossed/stale BB destination must not be replaced by another target.
   if(decision.Direction == DIR_BUY && destination <= decision.EntryPrice)
      return false;
   if(decision.Direction == DIR_SELL && destination >= decision.EntryPrice)
      return false;

   decision.StopLoss = structuralSL;
   decision.TakeProfit = destination;
   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;
   return true;
}

double GetDirectionalClosePrice(RiskValidationSnapshot &snapshot, ENUM_DIRECTION direction)
{
   // MT4 market positions close/trigger on BID for BUY and ASK for SELL.
   if(direction == DIR_BUY) return snapshot.Bid;
   if(direction == DIR_SELL) return snapshot.Ask;
   return 0.0;
}

bool ResolveExecutionReferencePrice(BBMA_Decision &decision, RiskValidationSnapshot &snapshot)
{
   // This is broker execution geometry, not a new BBMA strategy entry rule.
   // BUY market execution references ASK; SELL references BID.
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
   // Step 8 is deliberately fail-closed. The supplied BBMA PDF gives an
   // Extreme SL placement example but no deterministic TP formula, and it does
   // not define a complete SL/TP pair for the currently executable confirmed
   // Re-Entry / REM / RRE / REE candidates. Legacy MaxSL/MinRR builders are
   // therefore not accepted as BBMA source resolution.
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

   // MaxSLPips is a project risk cap only; it must never manufacture the SL.
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

   // MinRRRatio is also a rejection filter only; it never manufactures TP.
   if(MinRRRatio > 0.0 && (tpDistance / slDistance) < MinRRRatio)
   {
      rejection = REJ_INVALID_RR;
      return false;
   }

   // StopLevel is measured from the side that closes/triggers the market order:
   // BID for BUY positions, ASK for SELL positions.
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

   // P0 Step 9: M18 is observability only. M15 is the final entry authority.
   // The previous weights and unconditional BBShape/MultiTF bonuses were not
   // source-backed BBMA rules and could imply a false quality hierarchy.
   if(!decision.Valid) return result;

   result.ScoreBreakdown = "LABEL_ONLY|Type:" + EnumToString(decision.SignalType) +
                           "|Direction:" + EnumToString(decision.Direction) + "|";

   if(decision.HasSLTPSourceComponent)
      result.ScoreBreakdown += "SourceTF:" +
                               IntegerToString(decision.SLTPSourceComponent.Timeframe) + "|";

   // Numeric quality score is deliberately neutral. It cannot rank, gate,
   // invalidate or change any BBMA decision.
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

double CalculateBasketProfitPercent_EA()
{
   double floatingProfit = 0;
   
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
      {
         if(OrderCloseTime() != 0) continue;
         double profit = OrderProfit() + OrderSwap() + OrderCommission();
         if(profit > 0)
            floatingProfit += profit;
      }
   }
   
   if(g_protection_reference_equity <= 0) return 0;
   return floatingProfit / g_protection_reference_equity * 100;
}

double CalculateTotalRisk(string pair, double newLot, double newEntry, double newSL,
                          RiskValidationSnapshot &snapshot, bool &valid)
{
   valid = true;
   double totalRisk = 0;

   // MaxTotalRiskPercent is an EA-wide cap, not a same-pair cap. Existing open
   // trades must be measured using their own symbol tick value/tick size.
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(!OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
         continue;
      if(OrderCloseTime() != 0)
         continue;

      if(g_monitored_trades[i].remaining_lot <= 0)
         continue;

      double riskDistance = MathAbs(g_monitored_trades[i].entry_price -
                                    g_monitored_trades[i].current_sl);

      if(riskDistance <= 0)
         continue; // breakeven / zero-distance protected position

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

   // MaxSpreadPips is expressed in pips. Use the project pip-price helper so
   // 4/5-digit and 2/3-digit broker quoting are handled coherently.
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

   // If current EA portfolio state is already beyond a hard limit, no new trade
   // may be admitted. M20 only rejects; it never modifies M15-M17 payload.
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

void ManagePortfolio()
{
   // M20 owns portfolio protection state, not broker close execution.
   // Once basket-loss protection trips, latch the request until all EA-owned
   // monitored positions are actually closed by M23. This prevents partial-close
   // failures from silently clearing protection on a later tick.
   if(g_portfolio_emergency_close_requested)
   {
      if(CountLiveEAOwnedPortfolioTrades() == 0)
         g_portfolio_emergency_close_requested = false;
      return;
   }

   if(BasketLossPercent > 0 && CalculateBasketLossPercent_EA() >= BasketLossPercent)
      g_portfolio_emergency_close_requested = true;

   // BasketProfitPercent is intentionally NOT an execution trigger. M17 owns the
   // approved BBMA TP destination; M20 must not invent an alternate basket TP.
}

//+------------------------------------------------------------------+
//| MODULE 21: MONEY MANAGEMENT                                      |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

double NormalizeLotDownFromSnapshot(double lot, RiskValidationSnapshot &snapshot)
{
   if(lot <= 0 || snapshot.LotStep <= 0 || snapshot.LotDigits < 0)
      return 0;

   // Risk sizing must never round UP because that can exceed AutoLotPercent.
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

   // M21 is sizing-only. It consumes the final M17 Entry/SL and may not repair,
   // clamp, replace or reinterpret either value.
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

   // The risk snapshot is frozen for this decision. Reject a mismatched payload
   // instead of mixing a later broker/account state with the approved M17 values.
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

      // Use the same frozen equity snapshot that downstream M19 validates.
      // Calling AccountEquity() here made lot sizing tick-dependent and non-atomic.
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

      // MaxAutoLot is an AutoLot-only user cap; broker MaxLot comes from the
      // same frozen snapshot. Do not re-query live broker data during sizing.
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

      // FixedLot is explicit user intent. Do not silently normalize or clamp it;
      // an invalid broker step/min/max setting must fail closed.
      if(!IsValidSnapshotLotStep(lot, snapshot))
      {
         valid = false;
         return 0;
      }

      return lot;
   }

   // Unknown MMMode must never silently fall through to FixedLot.
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

   // MT4/brokers may truncate OrderComment(). The stable execution identity is
   // intentionally placed at the beginning of CreateOrderComment(): BBMA|H:<16-hex>.
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
      for(int i = 0; i < g_monitored_count; i++)
      {
         if(!IsLiveEAOwnedPortfolioTrade(i)) continue;
         if(g_monitored_trades[i].pair == pair &&
            g_monitored_trades[i].direction == decision.Direction)
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
   // Return codes:
   //  >0 = confirmed ticket (newly returned or reconciled existing order)
   //  -1 = definite broker/execution failure
   //  -2 = ambiguous result; DO NOT resend automatically
   //  -3 = execution price moved beyond frozen deviation
   if(MaxRetry <= 0 || pair == "" || lot <= 0 || stopLoss <= 0 || takeProfit <= 0 ||
      magicNumber <= 0 || decisionID == "")
      return -1;

   int retry = 0;
   while(retry < MaxRetry)
   {
      // Idempotency guard BEFORE every possible send. If an earlier attempt was
      // accepted but the terminal did not receive a definitive success result,
      // reconcile it instead of creating a duplicate position.
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
         // Reconcile once using stable decision identity. If the order is not
         // observable yet, the result is genuinely ambiguous. Never resend here:
         // the broker may have accepted the first request and expose it later.
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
   // Capacity is verified before broker execution. Compact only tickets that the
   // broker definitively reports as closed; transient selection failures remain
   // reserved fail-closed so a possibly live owned order is never forgotten.
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

   // M22 must never repair or recreate the immutable M15-M17 payload.
   if(pair == "" || decision.Pair != pair || decision.DecisionID == "" ||
      decision.Direction == DIR_NONE || decision.EntryPrice <= 0 ||
      decision.StopLoss <= 0 || decision.TakeProfit <= 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_DECISION_STATE;
      return;
   }
   
   // M22 is execution-only. Lot sizing belongs to M21, live risk filtering to
   // M19, and prospective portfolio/protection gating to M20. M27 invokes those
   // owners exactly once before entering M22. Never repeat them here.
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
   
   int existingTicket = FindExistingExecutionTicket(pair,
                           (decision.Direction == DIR_BUY) ? OP_BUY : OP_SELL,
                           magic, decision.DecisionID);
   if(existingTicket > 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_DUPLICATE;
      return;
   }

   // Fail BEFORE OrderSend if lifecycle ownership cannot be registered safely.
   // This guarantees that any broker order opened by M22 has a monitored slot
   // available for M19/M20/M23 ownership and emergency management.
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
   
   // FIX 3: Pass candle time to comment
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
         info.recovery_state = REC_NORMAL;
         
         AddToMonitoredTrades(info);
         
         decision.DecisionState = DEC_EXECUTED;
         MarkDecisionExecuted(decision.DecisionID, ticket);
         decision.DecisionState = DEC_EXECUTED;
         decision.RejectionReason = REJ_NONE;
         return;
      }

      // A ticket was identified but cannot be selected/reconciled now. Treat this
      // as ambiguous rather than sending another order on the same decision.
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

   // One frozen execution/risk snapshot for this decision. Strategy semantics
   // are already frozen by the closed-M15 M15/M16/M17 path; only broker/account
   // conditions are live here.
   RiskValidationSnapshot snapshot;
   BuildRiskValidationSnapshot(pair, decision, snapshot);

   // M17: resolve/validate the source-owned BBMA destination and protective SL.
   ENUM_REJECTION_REASON sltpRejection = REJ_NONE;
   if(!ValidateSLTP(decision, snapshot, sltpRejection))
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = (sltpRejection != REJ_NONE) ?
                                 sltpRejection : REJ_SLTP_UNRESOLVED;
      return false;
   }

   // M21 must precede M19 because prospective total-risk requires the proposed
   // frozen lot. M21 may size only; it cannot change Entry/SL/TP/direction.
   bool lotValid = true;
   double lot = CalculateLotSize(decision, snapshot, lotValid);
   if(!lotValid || lot <= 0)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_LOT;
      return false;
   }

   // M19: live risk filter only.
   RiskStatus riskStatus = CheckRiskBeforeTrade(decision, snapshot, lot);
   if(!riskStatus.allowed)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = (riskStatus.rejection_reason != REJ_NONE) ?
                                 riskStatus.rejection_reason : REJ_TOTAL_RISK;
      return false;
   }

   // M20: final prospective portfolio/protection gate. While emergency
   // liquidation is latched, no new order may be admitted even if floating loss
   // has temporarily fallen below the original basket-loss trigger.
   if(g_portfolio_emergency_close_requested)
   {
      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_BASKET_LOSS;
      return false;
   }

   FinalPortfolioGuard(decision);
   if(decision.DecisionState != DEC_VALIDATED) return false;

   // M22: immutable execution only. No re-sizing, re-risking or strategy repair.
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

      // Revalidate live EA ownership before any lifecycle action.
      int pairIdx = FindPairStateIndex(OrderSymbol());
      if(pairIdx < 0) continue;
      int expectedMagic = g_pair_states[pairIdx].magic_number;
      if(expectedMagic <= 0 || OrderMagicNumber() != expectedMagic ||
         g_monitored_trades[i].magic_number != expectedMagic)
         continue;

      string pair = OrderSymbol();
      double bid = MarketInfo(pair, MODE_BID);
      double ask = MarketInfo(pair, MODE_ASK);

      // Keep monitored state synchronized with broker state only. M23 must not
      // manufacture a new SL/TP or lot policy.
      g_monitored_trades[i].entry_price = OrderOpenPrice();
      g_monitored_trades[i].current_sl = OrderStopLoss();
      g_monitored_trades[i].current_tp = OrderTakeProfit();
      g_monitored_trades[i].lot = OrderLots();
      g_monitored_trades[i].remaining_lot = OrderLots();
      
      if(g_monitored_trades[i].recovery_state == REC_CORRUPTED ||
         g_monitored_trades[i].recovery_state == REC_RECOVERY_INVALID)
      {
         Log(DBG_ERROR, "Trade " + IntegerToString(g_monitored_trades[i].ticket) + 
             " corrupted, frozen: " + EnumToString(g_monitored_trades[i].recovery_state));
         continue;
      }

      // M20 emergency basket-loss protection is the only active M23 broker-side
      // lifecycle close policy at this stage. Keep the request latched in M20 so
      // a failed close is retried on a later tick. No partial close is allowed.
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

      // Normal exit is broker-side SL/TP already supplied by M17->M22.
      // No 1R partial close, breakeven migration, trailing stop, TP2/TP3, or
      // synthetic manual TP close is permitted here.
   }
   
   g_is_managing_trade = false;
}

//+------------------------------------------------------------------+
//| MODULE 24: RECOVERY ENGINE                                       |
//| LEVEL: EXPERT                                                    |
//+------------------------------------------------------------------+

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
      string executionHash;
      if(!ExtractExecutionHash(comment, executionHash))
      {
         Log(DBG_ERROR, "EA-owned order missing execution hash ticket=" +
             IntegerToString(OrderTicket()));
         continue;
      }

      ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;
      string decisionHash, parsedPair, sequenceHash;
      ENUM_DIRECTION parsedDirection = DIR_NONE;
      ENUM_SIGNAL_TYPE signalType = SIGNAL_NONE;
      double intendedEntry, intendedSL, intendedLot, intendedRisk;
      datetime candleTime = 0;

      bool fullMetadata = ParseOrderCommentFull(comment, decisionHash, parsedPair,
                                                 parsedDirection, signalType,
                                                 intendedEntry, intendedSL,
                                                 intendedLot, intendedRisk,
                                                 sequenceHash, candleTime);

      // Comment metadata may be truncated, but if present it must agree with live
      // broker ownership/direction and H: execution identity. Never let parsed
      // comment fields override the selected live order.
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
         
         // Never fabricate a full DecisionID from lossy comment metadata.
         info.decision_id = "";
         info.execution_hash = executionHash;
         info.sequence_hash_short = sequenceHash;

         // Recovery preserves broker-side Entry/SL/TP/lot exactly. A valid live
         // BBMA market order must still have directionally sane protective levels.
         bool geometryValid = (info.initial_entry_price > 0 &&
                               info.initial_stop_loss > 0 &&
                               info.initial_take_profit > 0);
         if(geometryValid && liveDirection == DIR_BUY)
            geometryValid = (info.initial_stop_loss < info.initial_entry_price &&
                             info.initial_entry_price < info.initial_take_profit);
         else if(geometryValid && liveDirection == DIR_SELL)
            geometryValid = (info.initial_take_profit < info.initial_entry_price &&
                             info.initial_entry_price < info.initial_stop_loss);

         double currentLot = OrderLots();
         if(!geometryValid || currentLot <= 0 || !IsValidLotStep(currentLot, pair))
         {
            info.recovery_state = REC_RECOVERY_INVALID;
         }
         else if(fullMetadata && intendedLot > 0 && currentLot > intendedLot + 0.0000001)
         {
            info.recovery_state = REC_CORRUPTED;
         }
         else if(fullMetadata && intendedLot > 0 && currentLot < intendedLot - 0.0000001)
         {
            // Legacy/manual external reduction is preserved as live state; never
            // infer permission for another partial close or restore the old lot.
            info.recovery_state = REC_PARTIAL_INFERRED;
            info.remaining_lot = currentLot;
         }
         else if(fullMetadata)
         {
            info.recovery_state = REC_NORMAL;
         }
         else
         {
            // Stable H: identity + exact live EA ownership are enough for safe
            // monitoring and emergency liquidation, but not for reconstructing
            // strategy metadata that the broker comment no longer contains.
            info.recovery_state = REC_IDENTITY_HASH_ONLY;
         }

         // Step 14 removed breakeven/partial-management authority. Recovery must
         // not infer or reactivate those deprecated lifecycle policies.
         info.partial_closed = false;
         info.partial_available = false;
         info.partial_attempted = false;
         info.breakeven_set = false;
         info.be_attempted = false;

         AddToMonitoredTrades(info);

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
   // M25 is display-only. It may render already-owned state but must never mutate
   // strategy, risk, recovery, order or lifecycle state.
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

   // Locked Entry Mode contract: only the two source-governed meanings are valid.
   if(EntryMode < 1 || EntryMode > 2) return false;

   // SignalMode no longer gates M15 entry authority. Arbitrary SAFE/NORMAL/
   // AGGRESSIVE tier ranking is not part of the supplied BBMA source.
   return true;
}

bool ValidatePairIDCollision()
{
   int usedIDs[MAX_PAIRS];
   ArrayInitialize(usedIDs, 0);
   
   for(int i = 0; i < g_pair_count; i++)
   {
      int pid = g_pair_states[i].pair_id;
      if(pid < PAIR_ID_MIN || pid > PAIR_ID_MAX)
      {
         g_pair_states[i].pair_enabled = false;
         Log(DBG_ERROR, "PairID out of range for " + g_pair_names[i]);
         return false;
      }
      if(usedIDs[pid - PAIR_ID_MIN] > 0)
      {
         g_pair_states[i].pair_enabled = false;
         Log(DBG_ERROR, "PairID collision for " + g_pair_names[i] + 
             " with " + g_pair_names[usedIDs[pid - PAIR_ID_MIN] - 1]);
         return false;
      }
      usedIDs[pid - PAIR_ID_MIN] = i + 1;
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
      
      string actual = FindActualSymbol(pair);
      if(actual == "")
      {
         Log(DBG_ERROR, "Symbol not found: " + pair);
         continue;
      }
      
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
         g_pair_states[g_pair_count].pair_enabled = true;
      else
         g_pair_states[g_pair_count].pair_enabled = false;
      
      g_pair_states[g_pair_count].is_cent_account = DetectCentAccount();
      g_pair_states[g_pair_count].cent_factor = GetCentFactor();
      
      g_processed_candle_time[g_pair_count] = 0;
      g_pair_count++;
   }
}

int InitializeEA()
{
   // Explicitly enter a non-operational state until ALL ownership, recovery and
   // protection initialization has completed successfully.
   g_is_initialized = false;
   g_is_scanning = false;
   g_is_managing_trade = false;
   g_terminal_connected = IsTerminalConnected();
   g_portfolio_emergency_close_requested = false;
   g_processing_time = GetProcessingTime();

   InitBrokerInfo();
   LoadPairs();
   if(g_pair_count == 0)
   {
      Log(DBG_ERROR, "No valid pairs loaded");
      return INIT_FAILED;
   }
   
   if(!ValidatePairIDCollision())
   {
      Log(DBG_ERROR, "PairID collision detected");
      return INIT_PARAMETERS_INCORRECT;
   }
   if(!ValidateMagicCollision())
   {
      Log(DBG_ERROR, "Magic collision detected");
      return INIT_PARAMETERS_INCORRECT;
   }
   
   ArrayResize(g_global_signal_history, 0);
   g_global_signal_count = 0;
   g_monitored_count = 0;

   // M19 drawdown contract is explicitly equity-based. Using balance here would
   // create a false restart drawdown baseline whenever recovered positions are
   // already floating in profit/loss.
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

   // Pair/symbol/magic ownership is already validated above. Only now may M24
   // rebuild execution tombstones and monitored live-order state.
   RebuildExecutionHistory();
   RecoverExistingOrders();

   // Recovery must not implicitly re-arm an old in-memory emergency latch. The
   // live M20 protection engine will evaluate the recovered portfolio from current
   // broker state and latch again deterministically when required.
   g_portfolio_emergency_close_requested = false;

   g_is_initialized = true;
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

   // Numeric BB snapshots exist regardless of whether BB shape classification is enabled.
   // M06 owns the values; M27 only routes the frozen snapshots to signal owners.
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

   // M16 temporal Extreme invalidation needs the presence of a later CSM on the
   // same timeframe. The source does not qualify that invalidation by CSM direction,
   // so build one H1/H4 CSM presence snapshot before the BUY/SELL candidate loop.
   Signal h1AnyCSMSnapshot, h4AnyCSMSnapshot;
   ZeroMemory(h1AnyCSMSnapshot); ZeroMemory(h4AnyCSMSnapshot);

   int h1ShiftForCSM = g_pair_states[pairIndex].h1_data.barIndex;
   if(DetectCSM(actual, PERIOD_H1, DIR_BUY, h1ShiftForCSM) ||
      DetectCSM(actual, PERIOD_H1, DIR_SELL, h1ShiftForCSM))
   {
      h1AnyCSMSnapshot.Type = SIGNAL_CSM;
      h1AnyCSMSnapshot.Valid = true;
      h1AnyCSMSnapshot.Timeframe = PERIOD_H1;
      h1AnyCSMSnapshot.BarIndex = h1ShiftForCSM;
      h1AnyCSMSnapshot.CandleTime = g_pair_states[pairIndex].h1_data.candle_time;
      h1AnyCSMSnapshot.Timestamp = h1AnyCSMSnapshot.CandleTime;
      h1AnyCSMSnapshot.Close = g_pair_states[pairIndex].h1_data.close;
   }

   int h4ShiftForCSM = g_pair_states[pairIndex].h4_data.barIndex;
   if(DetectCSM(actual, PERIOD_H4, DIR_BUY, h4ShiftForCSM) ||
      DetectCSM(actual, PERIOD_H4, DIR_SELL, h4ShiftForCSM))
   {
      h4AnyCSMSnapshot.Type = SIGNAL_CSM;
      h4AnyCSMSnapshot.Valid = true;
      h4AnyCSMSnapshot.Timeframe = PERIOD_H4;
      h4AnyCSMSnapshot.BarIndex = h4ShiftForCSM;
      h4AnyCSMSnapshot.CandleTime = g_pair_states[pairIndex].h4_data.candle_time;
      h4AnyCSMSnapshot.Timestamp = h4AnyCSMSnapshot.CandleTime;
      h4AnyCSMSnapshot.Close = g_pair_states[pairIndex].h4_data.close;
   }

   // Both directions are collected first. M15 receives one atomic pair-level pool
   // and is called exactly once after BUY and SELL owner snapshots are complete.
   ValidatedSequenceCandidate allCandidates[];
   int allCandidateCount = 0;

   for(int dirIdx = 0; dirIdx < 2; dirIdx++)
   {
      ENUM_DIRECTION direction = (dirIdx == 0) ? DIR_BUY : DIR_SELL;

      // Signal-owner outputs. M27 orchestrates detector/state-engine calls once;
      // M13 receives only immutable copies of these cycle snapshots.
      Signal h1ExtremeSnapshot, h4ExtremeSnapshot, m15MHVSnapshot, m15CSDSnapshot;
      Signal m15ECSDSnapshot, m15CSMSnapshot;
      ZeroMemory(h1ExtremeSnapshot); ZeroMemory(h4ExtremeSnapshot);
      ZeroMemory(m15MHVSnapshot); ZeroMemory(m15CSDSnapshot);
      ZeroMemory(m15ECSDSnapshot); ZeroMemory(m15CSMSnapshot);

      Signal detectedH1Extreme, detectedH4Extreme;
      ZeroMemory(detectedH1Extreme); ZeroMemory(detectedH4Extreme);

      if(DetectExtreme(actual, direction, g_pair_states[pairIndex].h1_data, h1Band))
      {
         detectedH1Extreme.Type = SIGNAL_EXTREME;
         detectedH1Extreme.Direction = direction;
         detectedH1Extreme.Valid = true;
         detectedH1Extreme.Timeframe = PERIOD_H1;
         detectedH1Extreme.BarIndex = g_pair_states[pairIndex].h1_data.barIndex;
         detectedH1Extreme.CandleTime = g_pair_states[pairIndex].h1_data.candle_time;
         detectedH1Extreme.Timestamp = detectedH1Extreme.CandleTime;
         detectedH1Extreme.Close = g_pair_states[pairIndex].h1_data.close;
      }

      if(DetectMHV(actual, direction, g_pair_states[pairIndex].m15_data))
      {
         m15MHVSnapshot.Type = SIGNAL_MHV;
         m15MHVSnapshot.Direction = direction;
         m15MHVSnapshot.Valid = true;
         m15MHVSnapshot.Timeframe = PERIOD_M15;
         m15MHVSnapshot.BarIndex = g_pair_states[pairIndex].m15_data.barIndex;
         m15MHVSnapshot.CandleTime = g_pair_states[pairIndex].m15_data.candle_time;
         m15MHVSnapshot.Timestamp = m15MHVSnapshot.CandleTime;
         m15MHVSnapshot.Close = g_pair_states[pairIndex].m15_data.close;
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
         DetectMLV_State(g_pair_states[pairIndex].mlv_buy_state, actual, direction,
                         g_pair_states[pairIndex].m15_data);
         mlvSnapshot = g_pair_states[pairIndex].mlv_buy_state;

         UpdateReEntryState(g_pair_states[pairIndex].re_h1_buy_state, actual, direction,
                            g_pair_states[pairIndex].h1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_h4_buy_state, actual, direction,
                            g_pair_states[pairIndex].h4_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_d1_buy_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_buy_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_buy_state;
      }
      else
      {
         DetectMLV_State(g_pair_states[pairIndex].mlv_sell_state, actual, direction,
                         g_pair_states[pairIndex].m15_data);
         mlvSnapshot = g_pair_states[pairIndex].mlv_sell_state;

         UpdateReEntryState(g_pair_states[pairIndex].re_h1_sell_state, actual, direction,
                            g_pair_states[pairIndex].h1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_h4_sell_state, actual, direction,
                            g_pair_states[pairIndex].h4_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_d1_sell_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
      }

      // M16 applies temporal validity over M08's raw Extreme detector output.
      // CSM invalidation is evaluated on the same timeframe as the stored Extreme.
      if(direction == DIR_BUY)
      {
         UpdatePersistentExtremeState(detectedH1Extreme, h1AnyCSMSnapshot,
                                      g_pair_states[pairIndex].extreme_h1_buy_state);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;
      }
      else
      {
         UpdatePersistentExtremeState(detectedH1Extreme, h1AnyCSMSnapshot,
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

      if(DetectExtreme(actual, direction, g_pair_states[pairIndex].h4_data, h4Band))
      {
         detectedH4Extreme.Type = SIGNAL_EXTREME;
         detectedH4Extreme.Direction = direction;
         detectedH4Extreme.Valid = true;
         detectedH4Extreme.Timeframe = PERIOD_H4;
         detectedH4Extreme.BarIndex = g_pair_states[pairIndex].h4_data.barIndex;
         detectedH4Extreme.CandleTime = g_pair_states[pairIndex].h4_data.candle_time;
         detectedH4Extreme.Timestamp = detectedH4Extreme.CandleTime;
         detectedH4Extreme.Close = g_pair_states[pairIndex].h4_data.close;
      }

      if(direction == DIR_BUY)
      {
         UpdatePersistentExtremeState(detectedH4Extreme, h4AnyCSMSnapshot,
                                      g_pair_states[pairIndex].extreme_h4_buy_state);
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;
      }
      else
      {
         UpdatePersistentExtremeState(detectedH4Extreme, h4AnyCSMSnapshot,
                                      g_pair_states[pairIndex].extreme_h4_sell_state);
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;
      }
      h4_extreme = h4ExtremeSnapshot;

      ComponentSet rem, rre, ree;
      BuildPossibleCombinations(rem, rre, ree, h4_reEntry, extreme, mlv,
                                d1_reEntry, h4_extreme);
      
      // Standalone Re-Entry eligibility is normalized from the authoritative H1
      // M12 lifecycle snapshot. H4/D1 Re-Entry remain higher-TF combination context.
      ValidatedSequenceCandidate reEntryCandidate;
      BuildConfirmedReEntryCandidate(reEntry, reEntryCandidate);
      AppendValidatedCandidate(reEntryCandidate, allCandidates, allCandidateCount);

      // M14 validates only the three source-defined REM/RRE/REE rows.
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

   // FINAL pair-level authority: exactly one M15 pass after both directions exist.
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

   // Live lifecycle/protection always runs before any new strategy scan.
   ManagePortfolio();
   ManagePositions();

   // Emergency liquidation is an exclusive portfolio state. Do not scan or
   // admit new entries while M20's latch remains active.
   if(g_portfolio_emergency_close_requested) return;
   
   if(g_is_scanning) return;
   g_is_scanning = true;
   
   g_processing_time = GetProcessingTime();
   
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      if(g_pair_states[i].is_processing) continue;
      if(IsNewCandle(g_pair_names[i], i))
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
   
   Log(DBG_FULL, "BBMA Professional EA V4.5.1 initialized successfully");
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| EXPERT DEINITIALIZATION FUNCTION                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   // Stop all local orchestration first. Do NOT erase execution-hash/tombstone
   // semantics here; restart recovery reconstructs them from broker history.
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
   
   ManagePositions();
   
   CleanupSignalHistoryEntries();
   CleanupGlobalSignalHistory();
   
   datetime todayStart = GetTodayStart();
   if(todayStart > g_last_reset_date)
   {
      // Keep daily reset consistent with the M19 equity-drawdown contract.
      double resetEquity = AccountEquity();
      if(resetEquity > 0)
         g_protection_reference_equity = resetEquity;
      g_last_reset_date = todayStart;
      g_last_daily_profit = 0;
      Log(DBG_FULL, "Daily reset: protection reference = " + DoubleToString(g_protection_reference_equity, 2));
   }
   
   g_processing_time = GetProcessingTime();
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      if(g_pair_states[i].is_processing) continue;
      if(IsNewCandle(g_pair_names[i], i))
      {
         ProcessPair(i);
      }
   }
   
   if(g_dashboard_needs_update)
   {
      UpdateDashboard();
      g_dashboard_needs_update = false;
   }
}

//+------------------------------------------------------------------+
//| END OF EXPERT ADVISOR                                            |
//+------------------------------------------------------------------+