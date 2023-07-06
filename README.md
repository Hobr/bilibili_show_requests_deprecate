# Bilibili_show_ticket_order

> 懒得做了, api买票的大概思路都在这......selenium版左转[Hobr/cp_deprecate](https://github.com/Hobr/bilibili_show_selenium_deprecate)

Bilibili会员购抢票助手, 通过B站接口抢购目标漫展/演出, 仅适用于购买实名制电子票, 暂无适配其他票种的计划

本脚本仅供学习交流使用, 不得用于商业用途, 如有侵权请联系删除

## 使用

```bash
pip install -r requirements.txt
python api.py
```

## 模式

- API模式
  - 使用requests, 调用B站的API接口抢票
  - 效率更高, 适合开票时抢票
  - 短时间内抢不到的话有可能被风控BanIP

## 配置说明

- global 全局配置
  - init 初始化状态, 0为未初始化, 1为已初始化
  - mode 运行模式, 0为API模式, 1为浏览器模式
  - process 进程数, 1为单进程, 大于1为多线程
  - timeout 请求超时时间, 单位为秒, 调用api时使用
  - timestop 操作间隔时间, 单位为秒, 避免过快请求被风控
  - step 当前执行进度
  - url 目标商品详情页地址, 用于获取project_id
  - buyerList 购票人
  - screennum 横向场次序号, 从0开始
  - skunum 横向价格序号, 从0开始
  - fullToken 完整的token, 由firToken和secToken拼接而成
  - firToken 时间戳token, 通过api第一步获取
  - secToken 商品token
  - cookie 用户cookie

- api
  - project_id 商品id, 对应url里的'id'
  - screen_id 场次id
  - sku_id 价格id
  - buyer 处理后的购票人, 对应buyList里的'name'
  - pay_money 支付金额
  - order_token 订单token
  - order_id 订单id
  - headers 请求头

- browser
  - headless 是否无头模式, 0为否, 1为是
