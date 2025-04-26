Here’s a clean, organized **Markdown file** based on everything you wrote. I’ve slightly polished the formatting to make it easier for an LLM (or any agent) to understand the context properly:

---

# SQL Expert Context and Instructions

## 📚 Table Descriptions

### Table: neptune-3dd81.saved_tables.user_trades

- **Purpose**:
  **Purpose**: Tracks weekly user-level trading performance, capital movement, and behavioral signals (churn, reactivation).  
  **Key Metrics**: Returns, capital, charges, churn status, P&L percentages.

- **Columns**:

| Column Name             | Description                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| ACCOUNT_ID              | Unique identifier for the user's account                                                                  |
| IDENTIFIER_WEEK         | Unique weekly identifier                                                                                  |
| IDENTIFIER_MONTH        | Monthly identifier                                                                                        |
| IDENTIFIER_YEAR         | Yearly identifier                                                                                         |
| WEEK_START_DATE         | Week start date (string)                                                                                  |
| WEEK_END_DATE           | Week end date (string)                                                                                    |
| MONTH_START_DATE        | Start date of the month                                                                                   |
| TRADE_WEEK_NUM          | Week number in a trading calendar                                                                         |
| TRADE_WEEK_INDEX        | Index for sorting or tracking sequence                                                                    |
| TRADES                  | Number of trades                                                                                          |
| CAPITAL                 | User's capital during the week                                                                            |
| PREV_CAPITAL            | Capital in the previous week                                                                              |
| CARD_PNL                | Gross returns (before charges)                                                                            |
| PNL_WITHOUT_CHARGES     | Returns without transaction costs                                                                         |
| NET_PNL                 | Net returns (after charges)                                                                               |
| CHARGES                 | Total charges (brokerage, platform)                                                                       |
| CARD_PNL_PERCENTAGE     | CARD_PNL as % of CAPITAL (Ideal Returns which user should have received in this week based on Trade Card) |
| USERS_PNL_PERCENTAGE    | PNL as % of CAPITAL (before charges)                                                                      |
| USERS_NETPNL_PERCENTAGE | PNL as % of CAPITAL (after charges)                                                                       |
| USERS_CURRENT_WEEK      | Current active week for the user                                                                          |
| USERS_ACTIVATED_WEEK    | Activation week of the user                                                                               |
| CLIENT_CODE             | External client identifier                                                                                |
| CLIENT_NAME             | Name of the user                                                                                          |
| BROKER                  | Broker used for trading                                                                                   |
| FIRST_TRADE_FLAG        | 1 if it’s user’s first week of trading                                                                    |
| LAST_TRADE_FLAG         | 1 if it’s the user’s last trade week                                                                      |
| REJOINED_FLAG           | 1 if user rejoined after a gap                                                                            |
| CHURN_FLAG              | 1 if user has churned                                                                                     |
| REACTIVATION_FLAG       | 1 if user has been reactivated                                                                            |
| NEW_CAPITAL             | New capital added this week                                                                               |
| ADDED_CAPITAL           | Capital added this week                                                                                   |
| REJOINED_CAPITAL        | Capital rejoined after inactivity                                                                         |
| DROPPED_CAPITAL         | Capital removed before churn                                                                              |
| CHURNED_CAPITAL         | Capital marked as churned                                                                                 |

---

### Table: neptune-3dd81.automation_user_pnl.weekly_data

**Purpose**: Captures weekly bundle and strategy-level performance metrics for users.  
**Key Metrics**: Strategy returns, capital allocation, charges, success rate.

- **Columns**:
  | Column Name | Description |
  |-------------------------|-------------|
  | ACCOUNT_ID | User's account identifier |
  | BUNDLE_NAME | Name of the bundle |
  | STRATEGY | Trading strategy name within a bundle |
  | CAPITAL | Capital allocated to this strategy |
  | CARDPNL | Ideal PNL user should have received based on Trade Cards |
  | CARDPNL_PERC | CARDPNL as a % of CAPITAL |
  | NETPNL | Net P&L after charges |
  | NETPNL_PERC | NETPNL as a % of CAPITAL |
  | CHARGES | Charges incurred for the strategy |
  | CHARGES_PERC | CHARGES as a % of CAPITAL |
  | TRADES | Number of trades executed |
  | TRADE_START_DATE | Week start date |
  | TRADE_MONTH | Month of trade activity |
  | ORDER_SUCCESS_RATE | Order success ratio |
  | NAME | Strategy name |
  | MULTIPLIER_CHANGE | Change in quantity multiplier |
  | EXECUTION_TIME | Time taken to execute trades |
  | CLIENT_ID | Alternate client identifier |
  | IN_HOUSE_ACCOUNT | Flag if internal account |
  | STATUS | Trading status |
  | SERVER_ID | Server executing strategy |
  | AWP | Average Weekly Performance |
  | BACKTESTPNL | Backtested performance |
  | BACKTESTPNL_PERC | Backtested P&L percentage |

---

## 🔗 Relationships

- `ACCOUNT_ID` links both tables.
- Each `BUNDLE_NAME` in `user_trades` maps to 4 `STRATEGY` rows.
- Weekly granularity is based on `WEEK_START_DATE`; monthly via `TRADE_MONTH`.
- To adjust `WEEK_START_DATE` to Friday:

```sql
DATE_ADD(PARSE_DATE('%Y-%m-%d', week_start_date), INTERVAL 4 DAY)
```

---

## 🎯 Metric Use Cases (Agent Thinking Guide)

| Use Case                  | Table         | Key Columns                                                                |
| ------------------------- | ------------- | -------------------------------------------------------------------------- |
| User Returns (Mean & P50) | `user_trades` | `USERS_NETPNL_PERCENTAGE`, `CLIENT_CODE`, `WEEK_START_DATE`                |
| Strategy-Level Returns    | `weekly_data` | `BUNDLE_NAME`, `STRATEGY`, `NETPNL_PERC`, `TRADE_MONTH`                    |
| Retention by Month        | `weekly_data` | `ACCOUNT_ID`, `ONBOARDED_MONTH`, `CHURN_FLAG`, `WEEK_START_DATE`           |
| Capital Growth            | `weekly_data` | `ACCOUNT_ID`, `CAPITAL`, `NEW_CAPITAL`, `ADDED_CAPITAL`, `WEEK_START_DATE` |
| High Volatility Users     | `user_trades` | `ACCOUNT_ID`, `USERS_NETPNL_PERCENTAGE`, `CARD_PNL_PERCENTAGE`             |

---

## 🧠 SQL Writing Instructions

1. **Clarify the Metric**  
   Expand the user's prompt by correctly mapping it to a use case above.

2. **Suggest SQL**  
   Return only the SQL query in a single line that:

   - Uses BigQuery syntax.
   - Convert date from the user question to the format YYYY-MM-DD and make the queries.
   - Quotes table names (backticks).
   - Uses the columns exactly from the shared schema.
   - Adjust week_start_date to Friday as shown in the relationship section.
   - Use date columns as exactly given in the examples
   - **No** aggregation, **only** column selection.

3. **Response Format**  
   Always return the output in this structure:

```json
{
  "sql": "SQL query here",
  "conversation": "Elaborated conversation here"
}
```

> **Note**: No extra markdown, no extra text, just the JSON object with `sql` and `conversation`.

---

# ✅ Example SQL Queries

### 1. User Returns (Mean & P50)

**Question**: What is the returns and median returns from October 2024 to March 2025?

**SQL**:

```sql
select account_id, client_code, DATE_ADD(PARSE_DATE('%Y-%m-%d', week_start_date), INTERVAL 4 DAY) as week_dt, DATE(CAST(SUBSTR(IDENTIFIER_MONTH, 2, 2) AS INT64) + 2000, CAST(SUBSTR(IDENTIFIER_MONTH, 5, 2) AS INT64), 1) as trade_month, users_netpnl_percentage from `neptune-3dd81.saved_tables.user_trades` where DATE_ADD(PARSE_DATE('%Y-%m-%d', week_start_date), INTERVAL 4 DAY) between date('2024-10-01') and date('2025-03-31')
```

---

### 2. Strategy-Level Returns

**Question**: What is the bundle level median returns for the strategies in the bundle 'Nova' from August 2024 to October 2024?

**SQL**:

```sql
select distinct bundle_name, strategy, account_id, client_id, trade_month, DATE_ADD(PARSE_DATE('%Y-%m-%d', week_start_date), INTERVAL 4 DAY) as week_dt, cardpnl_perc, netpnl_perc from `neptune-3dd81.automation_user_pnl.weekly_data` where strategy is not null and trade_start_date >= date('2024-07-28') and DATE_ADD(PARSE_DATE('%Y-%m-%d', week_start_date), INTERVAL 4 DAY) between date('2024-08-01') and date('2024-10-31') and left(lower(bundle_name),4) like '%nova%'
```

---

Would you also like me to create a downloadable `.md` file for this so you can directly upload/use it? 📄  
(Just say the word!)
