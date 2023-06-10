# 会员购API

记录一下会员购下单api的参数, 以便后续更新

参考:

- 实名 <https://show.bilibili.com/platform/detail.html?id=73422>
- 选座+实名 <>
- 非实名 <https://show.bilibili.com/platform/detail.html?id=73404>
- 纸质票+非实名 <>
- 选择日期+非实名 <https://show.bilibili.com/platform/detail.html?id=72287>

## 返回值的基本构成

```json
{
  "errno": 0,// 错误码
  "errtag": 0,
  "msg": "",// 错误信息
  "data": {}// 返回数据
}
```

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

## 订单完整信息

## 购买人信息

## 下单

## 订单状态创建

## 订单状态查询
