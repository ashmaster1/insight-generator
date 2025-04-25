# TAP Orders with Deviation

I need a retool script as output returns the list of orders executed in
TAP along with the deviation.

## Data Sources

1. TAP Orders
Source: Bigquery
Project: neptune-3dd81
Dataset: tap_orders
Table: tap_orders_raw_latest
The datastructure of the row is like this.,
```
field,type
document_name,STRING
document_id,STRING
timestamp,TIMESTAMP
event_id,STRING
operation,STRING
data,STRING
old_data,STRING
```
The data field contains the actual order data. The sample order data looks like this.,
```json
{
  "CancelRejectReason": "",
  "ChasingLimitEnabled": true,
  "CumulativeQuantity": 150,
  "ExchangeTransactTime": {
    "_seconds": 1745215562,
    "_nanoseconds": 0
  },
  "LastUpdateDateTime": {
    "_seconds": 1745215566,
    "_nanoseconds": 0
  },
  "LeavesQuantity": 0,
  "OrderAverageTradedPrice": "34.90",
  "OrderGeneratedDateTime": {
    "_seconds": 1745215562,
    "_nanoseconds": 0
  },
  "OrderPrice": 34.5,
  "OrderQuantity": 150,
  "OrderSide": "SELL",
  "OrderStatus": "Filled",
  "OrderTerminalStatusTime": 1745215568923286000,
  "OrderType": "Limit",
  "OrderUniqueIdentifier": "RL6yNABjoWU=",
  "TradingSymbol": "NIFTY 24APR2025 PE 23700",
  "clientCode": "VIJI1010",
  "description": "Order placed successfully for user",
  "epochTime": 1745215568923786000,
  "instanceName": "aef-trade--automation--service-v3--19--0-6pkr",
  "orderForceExecuted": false,
  "orderId": 1211035081,
  "orderInitiatedAt": "2025-04-21T06:06:02.679573468Z",
  "orderLifecycleStatus": "COMPLETED",
  "orderModificationCount": 1,
  "orderRequest": {
    "broker": "XTS",
    "exchangeInstrumentID": 79510,
    "expiry": "24APR25",
    "limitPrice": 34.2,
    "limitPriceBufferPercentage": 0.02,
    "ltp": 34.900001525878906,
    "option_type": "PE",
    "orderQuantity": 150,
    "orderSide": "SELL",
    "orderToOrderKeyRelation": "signalTradeUserOrder:SiaVIBsqZCuAI1vfw6J1:signal:fl6D508FmLCMCPF8mxfg:0f4aabf0-4b99-4613-8326-565e82b2c246:8WIEBkZXzHO7gG9c71Hf:ZsLziYklJJnh0ZL0oAHy:NIFTY25APR23700PE:RL6yNABjoWU=",
    "orderUniqueIdentifier": "RL6yNABjoWU=",
    "signalPayloadSymbol": "NIFTY25APR23700PE",
    "stopPrice": 0,
    "symbol": "NIFTY24APR2025PE23700"
  },
  "orderSource": "WS",
  "placeOrderResponseElapseTime": 10,
  "placeOrderResponseTime": 1745215562689755400,
  "releaseName": "TAP-GA",
  "retryCount": 0,
  "serverIdentifier": "6",
  "signalId": "signal:fl6D508FmLCMCPF8mxfg:0f4aabf0-4b99-4613-8326-565e82b2c246:8WIEBkZXzHO7gG9c71Hf",
  "status": "TAP:OE:PM:0002",
  "strategyId": "SiaVIBsqZCuAI1vfw6J1",
  "updatedAt": {
    "_seconds": 1745215568,
    "_nanoseconds": 944517000
  },
  "userInfo": {
    "brokerName": "XTS",
    "clientCode": "VIJI1010",
    "multiplier": 2,
    "rootKey": "strategyId:SiaVIBsqZCuAI1vfw6J1:accountId:ZsLziYklJJnh0ZL0oAHy"
  }
}
```

2. TAP Signals
Source: Bigquery
Project: neptune-3dd81
Dataset: tap_signals
Table: tap_signals_raw_latest
The datastructure of the row is like this.,
```
field,type
document_name,STRING
document_id,STRING
timestamp,TIMESTAMP
event_id,STRING
operation,STRING
data,STRING
old_data,STRING
```
The data field contains the actual signal data. The sample signal data looks like this.,
```json
{
  "generatedAt": 1745222692689,
  "instanceName": "aef-trade--automation--service-v3--19--0-svmc",
  "receivedAt": 1745222693946613200,
  "releaseName": "TAP-GA",
  "serverIdentifier": "3",
  "signalSignature": "signal:5d62cdcb7949ab1bf573834a7e888faabb0832c810685f97d46e77cbac9ce1c6",
  "strategyId": "JPDy55mGd24Px6wLPxU1",
  "tapStatus": "INITIATED",
  "timestamp": {
    "_seconds": 1745222693,
    "_nanoseconds": 0
  },
  "triggerActions": [
    {
      "entry": 0.1,
      "exited": false,
      "id": "action-id-0",
      "ltp": 1.4,
      "meta": {
        "expiry": "24APR25",
        "option_type": "PE",
        "quantity": 75
      },
      "pnl": 50,
      "symbol": "NIFTY25APR20350PE",
      "timestamp": "2025-04-21T08:04:53.784Z",
      "type": "S",
      "updatedAt": "2025-04-21T08:04:53.784Z"
    },
    {
      "entry": 0.1,
      "exited": false,
      "id": "action-id-1",
      "ltp": 1.4,
      "meta": {
        "expiry": "24APR25",
        "option_type": "PE",
        "quantity": 75
      },
      "pnl": 50,
      "symbol": "NIFTY25APR20350PE",
      "timestamp": "2025-04-21T08:04:53.784Z",
      "type": "B",
      "updatedAt": "2025-04-21T08:04:53.784Z"
    }
  ],
  "updatedAt": {
    "_seconds": 1745222693,
    "_nanoseconds": 993954000
  }
}
```

3. Accounts
Source: Bigquery
Project: neptune-3dd81
Dataset: saved_tables
Table: accounts_latest
The datastructure of the row is like this.,
```
field,type
document_id,STRING
data,STRING
timestamp,TIMESTAMP
```
The data field contains the actual signal data. The sample signal data looks like this.,
```json
{
  "blazeStatus": "CRM_BATCH",
  "broker": "IIFL",
  "brokerageInfo": {
    "aaaBrokerage": 10.5,
    "transactionalBrokerage": 10.5
  },
  "brokerageMismatch": true,
  "clientCode": "92839603",
  "createdAt": {
    "_seconds": 1715241424,
    "_nanoseconds": 217000000
  },
  "currentCapital": 4032193.04,
  "currentPledgedAmount": 3396676,
  "dob": {
    "_seconds": 743040000,
    "_nanoseconds": 0
  },
  "email": "mariafraji@gmail.com",
  "franchiseCode": "F434O",
  "id": "Rzz3x4ojbUpk6hwEw2WJ",
  "isCdcMigrated": true,
  "isCdcReceived": true,
  "isXTSTokenGenerated": true,
  "joinedAt": {
    "_seconds": 1714694400,
    "_nanoseconds": 0
  },
  "location": "KERALA",
  "marginInfo": {
    "cashCollateral": 1707863.634,
    "liquidCash": 635516.6702999999,
    "nonCashCollateral": 1688812.7357,
    "updatedAt": {
      "_seconds": 1745291533,
      "_nanoseconds": 149940000
    }
  },
  "marketfeedUserId": "fE8xdGh4TkWy9nVrRHBmoKuWEi52",
  "metadata": {
    "activationStage": "ACTIVATED",
    "nickname": "Maria",
    "pnlAggregatedTill": "Y25W15",
    "tradeStartWeek": "Y24W20"
  },
  "mobile": "8547510068",
  "name": "Maria Fraji Francis",
  "note": "",
  "pan": "ABHPF0183F",
  "permissions": [
    "HoldingsPermission"
  ],
  "pledgeRatioReadyToTakeRisk": false,
  "pledgeRatioRiskTill": null,
  "pledgeRatioStatus": "Healthy",
  "pnl": 247947.58596586104,
  "pnlCharges": 196488.43733999995,
  "pnlIdealPercentage": 7.715320931210456,
  "pnlStrategyPnL": 825011.0004448891,
  "pnlSyncedTill": {
    "_seconds": 1744884008,
    "_nanoseconds": 872000000
  },
  "pnlWeeks": 41,
  "pnlWeightedCapital": 3591951.2195121953,
  "pnlWithoutCharges": 444436.02330586076,
  "startDate": {
    "_seconds": 1714694400,
    "_nanoseconds": 0
  },
  "status": "ACTIVE",
  "stoxxoServerId": "sYX9bpcuc6RC0W7Z5dbk",
  "strategyAllocated": true,
  "strategyAllocatedCapital": 3900000,
  "strategyCapital": 3900000,
  "syncedAt": {
    "_seconds": 1714694400,
    "_nanoseconds": 0
  },
  "tncDocumentId": "DID240509135504736SS19MJ6LLN2PG6",
  "tncSigned": true,
  "type": "PUBLIC",
  "updatedAt": {
    "_seconds": 1745319663,
    "_nanoseconds": 821000000
  },
  "vendor": "TAP",
  "whatsappNumber": "917907353781",
}
```

4. Strategies
Source: Firestore
Project: neptune-3dd81
Collection: strategies
The datastructure of the row is like this.,
```json
{
    "strategyId": "0nND6BgM7mFiyl8Kk0bU",
    "name": "Delta",
}
```


In the retool, Bigquery, Firestore Tables are added as data sources.

## Logic
Fetch TAP orders from Bigquery and identify the deviation between the First User's LTP and the rest of the users's LTP. I want to identify the deviation in the following formats.,
1. Simple Price difference
2. Percentage difference
3. Percentile value based on deviation, higher the deviation, higher the percentile. SELL and BUY orders are to classified separately

Identification of order's signal is to be done by joining the TAP Orders and TAP Signals tables. Here the first user is derived separately for the buy order and sell order. For either buy or sell order the first user is the one with the lowest orderInitaitedAt field value. So for each signalId, the lowest buy order with orderInitaitedAt is the first buy and the lowest sell order with orderInitiatiedAt is the first sell and that is what we use to compare deviation for both buy and sell legs.

For deviation calculation:
- For BUY orders: Deviation = Current Order Price - First BUY Order LTP
- For SELL orders: Deviation = First SELL Order LTP - Current Order Price

Percentile calculation should be done at 5 intervals (p0, p5, p10, p15... p95) plus p99 and p100, with percentiles calculated separately for each signal.

The results should be returned only for orders which have "Filled" order status. To get the strategy name, we need to map the strategyId in the tap signal to the strategyId in the strategy document in firestore.

For the signalPublishedAt timestamp, we need to use the timestamp in the data field of the BigQuery record (specifically the receivedAt field), not the timestamp column. This timestamp should be displayed in IST (UTC+5:30) format.

For each order, there will be a clientCode which need to be mapped with the accounts table in bigquery to identify if the user belongs to CDC_1 or CDC_2. In the accounts table if isCdcMigrated is true the it's CDC_2, else it's CDC_1.

## Input
The script should use today's date for testing purposes. All price fields should be converted to float during fetching from orders to make it easier to operate later.

## Output
The output should have the following rows.,
```
Strategy Name,
Signal ID,
Signal Publish Time,
Client Code,
CDC,
Order Side,
Trading Symbol,
Initiated At,
Exchange Transact Time,
Elapsed Time,
Signal to Exchange,
Quantity,
Traded Price,
Limit Price,
LTP,
Signal LTP,
Deviation in Price
Deviation in Percentage
Deviation in Percentile,
ID,
Order ID,
Release Name,
Retry Count,
Modification Count,
Server Identifier,
Order Source
```
create an sql query for this