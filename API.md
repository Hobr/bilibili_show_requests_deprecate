# 会员购API

记录一下会员购下单api的参数, 以便后续更新

参考:

- 实名+电子 <https://show.bilibili.com/platform/detail.html?id=73422>
- 选座+实名+纸质 <https://show.bilibili.com/platform/detail.html?id=71822>
- 非实名+电子 <https://show.bilibili.com/platform/detail.html?id=72125>
- 纸质票+实名 <https://show.bilibili.com/platform/detail.html?id=72421>
- 纸质+非实名 <https://show.bilibili.com/platform/detail.html?id=72911>
- 选择日期+非实名+电子 <https://show.bilibili.com/platform/detail.html?id=72287>

## response的基本构成

```json
{
  "errno": 0,// 错误码
  "errtag": 0,
  "msg": "",// 错误信息
  "data": {}// 返回数据
}
```

## project信息

### 请求

- URL: ``https://show.bilibili.com/api/ticket/project/get``
- Method: GET
- Params:
- Example:

### 返回

```json

```

## token获取

## ticket信息

## 实名购买人信息

## 订单创建

## 订单状态
