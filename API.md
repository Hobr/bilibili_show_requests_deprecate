# 会员购API

记录一下会员购下单api的参数, 以便后续更新

参考:

- 实名 <https://show.bilibili.com/platform/detail.html?id=71951>
- 选座+实名 <https://show.bilibili.com/platform/detail.html?id=71951>
- 非实名 <https://show.bilibili.com/platform/detail.html?id=72099>
- 纸质票+非实名 <https://show.bilibili.com/platform/detail.html?id=72271>
- 选择日期+非实名 <https://show.bilibili.com/platform/detail.html?id=71519>

## 返回值的基本构成

```json
{
  "errno": 0,// 错误码
  "errtag": 0,
  "msg": "",// 错误信息
  "data": {}// 返回数据
}
```

下文将不重复解释以上内容

## 项目完整信息

### 请求

- URL: ``https://show.bilibili.com/api/ticket/project/get``
- Method: GET
- Params:
  - version: 134
  - id: {project_id}
- Example: <https://show.bilibili.com/api/ticket/project/get?version=134&id=71951>

### 返回

```json

```

## token获取

### 请求

- URL: ``https://show.bilibili.com/api/ticket/order/prepare``
- Method: POST
- Params:
  - count: {count}
  - order_type: 1
  - project_id: {project_id}
  - screen_id: {screen_id}
  - sku_id: {sku_id}
  - token: ""

### 返回

```json

```

## 订单完整信息

### 请求

- URL: ``https://show.bilibili.com/api/ticket/order/confirmInfo``
- Method: GET
- Params:
  - token: {token}
  - voucher: ""
- Example: <https://show.bilibili.com/api/ticket/order/confirmInfo?token=wGRWFGYAARkPAAHmjQEAAQAF1vY.&voucher=>

### 返回

```json

```

## 购买人信息

### 请求

- URL: ``https://show.bilibili.com/api/ticket/buyer/list``
- Method: GET
- Params:
  - is_default: ""
  - project_id: {project_id}
- Example: <https://show.bilibili.com/api/ticket/buyer/list?is_default&projectId=71951>

### 返回

```json

```

## 下单

### 请求

- URL: ``https://show.bilibili.com/api/ticket/order/createV2``
- Method: POST
- Params:
  - buyer_info: (list){buyer_info}
  - count: {count}
  - deviceId: ""
  - order_type: 1
  - pay_money: {pay_money}
  - project_id: {project_id}
  - screen_id: {screen_id}
  - sku_id: {sku_id}
  - timestamp: ""
  - token: {token}

### 返回

```json

```

## 订单状态创建

### 请求

- URL: ``https://show.bilibili.com/api/ticket/order/createstatus``
- Method: GET
- Params:
  - token: {order_token}
  - timestamp: ""
- Example: <https://show.bilibili.com/api/ticket/order/createstatus?token=0693eb804082c07c3b8b1fe6f99baf90&timestamp=1683362919630>

### 返回

```json

```

## 订单状态查询

### 请求

- URL: ``https://show.bilibili.com/api/ticket/order/info``
- Method: GET
- Params:
  - order_id: {order_id}
  - timestamp: ""
- Example: <https://show.bilibili.com/api/ticket/order/info?order_id=4007620767596999&timestamp=1683362919723>

### 返回

```json

```
