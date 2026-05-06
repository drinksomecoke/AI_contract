# TenderAlpha — Unified Government Contract Awards (UGCA)
## 字段目录 / Data Dictionary（中英对照）

> **数据集来源 / Source**：Dewey Data — TenderAlpha
> **页面链接**：<https://app.deweydata.io/data/tenderalpha/unified-government-contract-awards/unified-government-contract-awards>
> **整理依据**：Dewey 平台 Data Dictionary 截图（截至访问日期）

---

## 数据集简介 / Overview

TenderAlpha 的 **Unified Government Contract Awards (UGCA)** 是市场上覆盖范围最广的政府采购合同授予数据库，自 2010 年起累计收录 **超过 1.2 亿条** 政府合同记录，覆盖 **65+ 国家与地区**（含美国、整个 EEA、英国、加拿大、澳大利亚、巴西、印度等）。

每条记录对应一份政府授予的合同（contract award），并包含：
- 采购主体（contracting entity）的身份与联系方式
- 合同标的描述、CPV 行业代码、地理位置
- 授予日期、起止日期、合同金额（本币 + USD）
- 中标公司及其母公司信息（含上市公司 ticker 与 ISIN 映射）

**字段命名约定**：

| 前缀 | 含义 |
| --- | --- |
| `ORIGIN_*` | 数据来源标识 |
| `CONTRACTING_ENTITY_*` | 采购方（政府机构/招标方） |
| `TRANSACTION_*` / `TENDER_*` | 招标与合同本身的属性 |
| `DIRECT_AWARDEE_*` | 直接中标的公司 |
| `AWARDEE_PARENT_*` | 中标公司的母公司 |

**Value Type 说明**：`FIXED` = 数值型（含定点小数） · `TEXT` = 文本 · `DATE` = 日期 · `BOOLEAN` = 布尔

---

## 1. 数据来源标识 / Origin Identifiers

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `ORIGIN_ID` | ID of Origin | 数据来源 ID | FIXED | 100% | 1 |
| `ORIGIN` | Geographical region where the award has been procured from (US, EEA, etc.) | 该合同采购所在的地理区域（如 US、EEA 等） | TEXT | 100% | EEA Procurement |
| `EVENT_TYPE_GREEN_CONTRACT` | Indicates whether the award is an initial procurement event or a consequent transactional one. Identifies if the contract is awarded for green procurement | 标识该笔授予是初始采购事件还是后续交易事件；同时识别是否为绿色采购合同 | TEXT | <1% | — |

---

## 2. 采购方信息 / Contracting Entity

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `CONTRACTING_ENTITY_BIZPORTAL_ID` | ID of Contracting Authority | 采购方（招标机构）在 BizPortal 中的 ID | FIXED | 100% | 591321 |
| `CONTRACTING_ENTITY_NAME` | The name of the Contracting Authority that has initiated the tender | 发起本次招标的采购方名称 | TEXT | 100% | UNIVERSITY MULTIDIFILINARY… |
| `CONTRACTING_ENTITY_COUNTRY` | ISO2 country code of the Contracting Authority | 采购方所在国家的 ISO2 国家代码 | TEXT | 100% | BG |
| `CONTRACTING_ENTITY_STATE` | ISO2 state code of the Contracting Authority. [US companies and wherever applicable] | 采购方所在州/省的 ISO2 代码（主要适用于美国及其他适用情形） | TEXT | <1% | — |
| `CONTRACTING_ENTITY_LOCATION` | The city of the Contracting Authority | 采购方所在城市 | TEXT | 15% | Sofia |
| `CONTRACTING_ENTITY_ADDRESS` | Street address of the Contracting Authority | 采购方街道地址 | TEXT | 13% | st. St. George Sophia No. 1 |
| `CONTRACTING_ENTITY_POSTCODE` | Postcode of the city where the Contracting Authority is located | 采购方所在城市的邮政编码 | TEXT | 12% | 1431 |
| `CONTRACTING_ENTITY_CONTACT_POINT` | A representative of the Contracting Authority staff who is responsible for initiating the tender | 采购方负责发起本次招标的联系人 | TEXT | <1% | — |
| `CONTRACTING_ENTITY_WEBSITE` | Official website of the Contracting Authority | 采购方官方网站 | TEXT | 6% | www.alexandrovska.com |
| `CONTRACTING_ENTITY_EMAIL` | Email address of the Contracting Authority | 采购方电子邮箱 | TEXT | <1% | — |
| `CONTRACTING_ENTITY_PHONE` | Telephone number of the Contracting Authority | 采购方电话 | TEXT | <1% | — |
| `CONTRACTING_ENTITY_FAX` | Fax number of the Contracting Authority | 采购方传真号码 | TEXT | <1% | — |

---

## 3. 招标 / 合同标识 / Tender & Transaction IDs

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `TRANSACTION_BIZPORTAL_ID` | ID of Contract Award Transaction [Only for transactional feeds and wherever applicable] | 合同授予"交易"在 BizPortal 中的 ID（仅用于交易型 feed 及适用场景） | FIXED | 100% | 0 |
| `TENDER_BIZPORTAL_ID` | ID of Awarded Tender/Contract | 已授予招标/合同在 BizPortal 中的 ID | FIXED | 100% | 209599271 |

---

## 4. 招标内容与地理 / Tender Content & Geography

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `TENDER_INDUSTRY_CODES` | List of industry code as per the Common Procurement Vocabulary (CPV) | 按欧盟通用采购词汇表（CPV）划分的行业代码列表 | TEXT | 77% | 33651100-Antibacterials for… |
| `TENDER_TITLE` | Title name of the tender | 招标标题 | TEXT | 100% | Sultamicillin (Ampicillin, Sulbactam) |
| `TENDER_DESCRIPTION` | A brief description of the tendering procedure (works, goods, services) | 招标程序的简要描述（工程、货物或服务类） | TEXT | 95% | J01CR01 Sultamicillin … |
| `TENDER_FUNDING_ORIGIN_COUNTRY` | ISO2 code of origin country that provides financial resources | 提供资金的来源国家 ISO2 代码 | TEXT | 100% | BG |
| `TENDER_COUNTRY` | ISO2 country code where the work was / is performed | 合同实际履行地的国家 ISO2 代码 | TEXT | 100% | BG |
| `TENDER_STATE` | ISO2 state code in which the work was / is performed. [US companies and wherever applicable] | 合同实际履行地的州/省 ISO2 代码（主要美国适用） | TEXT | 56% | — |
| `TENDER_LOCATION` | The principal place where the work was / is performed | 合同实际履行的主要地点（城市） | TEXT | 69% | Sofia |

---

## 5. 招标关键日期 / Tender Dates

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `TENDER_DATE_OF_AWARD` | The date that a mutually binding agreement was reached | 双方达成具有约束力协议的日期（授标日） | DATE | 97% | 2026-01-12 |
| `TENDER_DATE_OF_DISPATCH` | The date on which the information becomes publicly available | 信息公开发布的日期 | DATE | 100% | 2026-01-12 |
| `TENDER_MIN_DELIVERY_DATE` | The earliest date when the information could be delivered to the Client receiving the data | 数据最早可向客户交付的日期 | DATE | 100% | 2026-01-13 |
| `TENDER_CONTRACT_START_DATE` | Date on which the contract was started. [US tenders and wherever applicable] | 合同开始执行日期（主要美国适用） | DATE | 78% | 2026-01-12 |
| `TENDER_CONTRACT_END_DATE` | Date on which the contract was finished. [US tenders and wherever applicable] | 合同结束日期（主要美国适用） | DATE | 74% | 2028-01-13 |

---

## 6. 招标金额与投标参与情况 / Tender Values & Bidding

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `TENDER_CURRENCY` | ISO3 currency code of the tender | 招标金额的 ISO3 货币代码 | TEXT | 98% | EUR |
| `TENDER_POTENTIAL_VALUE_OF_CONTRACT` | Possible maximum amount obligated for the full period of the contract | 合同整个履行期内可能的最大金额（本币） | FIXED | 98% | 54788.50 |
| `TENDER_POTENTIAL_VALUE_OF_CONTRACT_USD` | Possible maximum amount obligated for the full period of the contract in USD | 合同整个履行期内可能的最大金额（美元） | FIXED | 98% | 64053.34 |
| `TENDER_CURRENT_EVENT_AMOUNT` | Amount of the specific initial/transactional award | 当前这次具体授予/交易的金额（本币） | FIXED | 94% | 54788.50 |
| `TENDER_CURRENT_EVENT_AMOUNT_USD` | Amount of the specific initial/transactional award in USD | 当前这次具体授予/交易的金额（美元） | FIXED | 94% | 64053.34 |
| `TENDER_VALUE_OF_CONTRACT_TO_DATE` | The entire obligated amount of funds to the vendor as per the date of the event | 截至事件发生日，已向供应商承诺支付的累计金额（本币） | FIXED | 98% | 54788.50 |
| `TENDER_VALUE_OF_CONTRACT_TO_DATE_USD` | The entire obligated amount of funds in USD to the vendor as per the date of the event | 截至事件发生日，已向供应商承诺支付的累计金额（美元） | FIXED | 98% | 64053.34 |
| `TENDER_BUDGET_EXECUTION_PERCENTAGE_TO_DATE` | The percentage of the contract budget execution as per the date of the event, calculated by ratio of "Tender - Value of Contract to Date" to potential value | 截至事件发生日的合同预算执行百分比（= 截至日累计金额 / 合同潜在最大金额） | FIXED | 99% | 100.00 |
| `TENDER_BIDDERS_COUNT` | The number of other participants (bidders) who have applied for the tender | 参与该次招标的投标人数量 | FIXED | 35% | 5 |

---

## 7. 招标程序与合同类型 / Procedure & Contract Type

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `TENDER_FRAMEWORK` | An agreement between one or more business organisations | 是否为框架协议（一个或多个组织间的总括协议） | BOOLEAN | 100% | false |
| `TENDER_TYPE_OF_AUTHORITY` | Type of Contracting Authority that has initiated the tender | 发起招标的采购方机构类型 | TEXT | 11% | Body governed by public law |
| `TENDER_TYPE_OF_CONTRACT` | Contract type of the tendering procedure | 招标程序的合同类型（如 Supplies/Services/Works） | TEXT | 66% | Supplies |
| `TENDER_TYPE_OF_PROCEDURE` | Tender procedure type | 招标程序类型（如公开/限制性等） | TEXT | 71% | open |
| `TENDER_TYPE_OF_REGULATION` | Type of tendering procedure regulation | 招标程序所适用的法规类型 | TEXT | 5% | — |
| `TENDER_TYPE_OF_BID` | Type of tendering procedure bidding | 招标程序的投标方式类型 | TEXT | 6% | — |
| `TENDER_AWARD_CRITERIA` | Type of contract award criteria | 合同授予的评判标准类型（如 Price、MEAT 等） | TEXT | 18% | Price |
| `TENDER_TYPE_OF_CONTRACT_PRICING` | Payment model for a contract. Each has a different way of accounting for costs, fees, and profits | 合同付款/计价模型，决定成本、费用与利润的核算方式 | TEXT | 100% | FIRM FIXED PRICE |

---

## 8. 直接中标方 / Direct Awardee

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `DIRECT_AWARDEE_BIZPORTAL_ID` | ID of Directly awarded company | 直接中标公司在 BizPortal 中的 ID | FIXED | 100% | 8619 |
| `DIRECT_AWARDEE_NAME` | Name of the Awarded Company | 中标公司名称 | TEXT | 100% | Medex |
| `DIRECT_AWARDEE_UIC` | Unique national ID Number of the Awarded Company | 中标公司的国家统一识别码（UIC，类似工商号） | TEXT | 29% | 131268894 |
| `DIRECT_AWARDEE_VAT_NUMBER` | Tax identification number of the Awarded Company | 中标公司的增值税/税号 | TEXT | 21% | ATU36837900 |
| `DIRECT_AWARDEE_COUNTRY` | ISO2 country code of the Awarded Company | 中标公司所在国家 ISO2 代码 | TEXT | 100% | BG |
| `DIRECT_AWARDEE_STATE` | ISO2 state code of the Awarded Company. [US companies and wherever applicable] | 中标公司所在州/省 ISO2 代码（主要美国适用） | TEXT | 57% | CA |
| `DIRECT_AWARDEE_LOCATION` | The location of the Awarded Company | 中标公司所在地（城市） | TEXT | 93% | Sofia |
| `DIRECT_AWARDEE_ADDRESS` | Street address of the Awarded Company | 中标公司街道地址 | TEXT | 94% | Mladost district, residential complex… |
| `DIRECT_AWARDEE_POSTCODE` | Zip code or postal code of the Awarded Company address | 中标公司地址邮编 | TEXT | 90% | 1000 |
| `DIRECT_AWARDEE_EMAIL` | Email address of the Awarded Company | 中标公司电子邮箱 | TEXT | <1% | — |
| `DIRECT_AWARDEE_CONTACT_POINT` | A person or a department serving as the coordinator of information | 信息联络人或部门 | TEXT | <1% | — |
| `DIRECT_AWARDEE_WEBSITE` | Website of the Awarded Company | 中标公司官网 | TEXT | 42% | www.medex.bg |
| `DIRECT_AWARDEE_PHONE` | Phone number of the Awarded Company | 中标公司电话 | TEXT | <1% | — |
| `DIRECT_AWARDEE_FAX` | The fax number of the Awarded Company | 中标公司传真 | TEXT | <1% | — |
| `DIRECT_AWARDEE_LISTING_STATUS` | Values: Delisted, Unlisted, Listed | 上市状态：已退市 / 未上市 / 上市 | TEXT | 100% | Unlisted |
| `DIRECT_AWARDEE_TICKER_SYMBOL` | Ticker symbol of the awarded company. [Available for public companies only] | 中标公司股票代码（仅上市公司） | TEXT | 17% | VIG |
| `DIRECT_AWARDEE_STOCK_EXCHANGE_MIC` | Market Identifier Code of the Awarded Company's stock exchange | 中标公司所在证券交易所的 MIC 代码 | TEXT | 16% | XWBO |
| `DIRECT_AWARDEE_STOCK_EXCHANGE_NAME` | Stock exchange where the company's shares are being officially traded. [Available for public companies only] | 中标公司股票正式交易的证券交易所名称（仅上市公司） | TEXT | 16% | WIENER BOERSE AG |
| `DIRECT_AWARDEE_STOCK_EXCHANGE_COUNTRY` | ISO2 country code of the Stock exchange where the company's shares are being officially traded. [Available for public companies only] | 中标公司挂牌交易所所在国家的 ISO2 代码（仅上市公司） | TEXT | 16% | AT |
| `DIRECT_AWARDEE_ISIN_NUMBER` | An International Securities Identification Number. [Available for public companies only] | 国际证券识别码 ISIN（仅上市公司） | TEXT | 17% | AT0000908504 |
| `DIRECT_AWARDEE_AMOUNT` | It is the mutually agreed upon total contract or order value | 双方约定的合同或订单总金额（本币） | FIXED | 21% | 54788.50 |
| `DIRECT_AWARDEE_CURRENCY` | ISO3 currency code of the tender | 该笔授予的 ISO3 货币代码 | TEXT | 21% | EUR |
| `DIRECT_AWARDEE_USD_AMOUNT` | The amount of the tender in USD | 该笔授予折算为美元后的金额 | FIXED | 21% | 64053.34 |

---

## 9. 中标方母公司 / Awardee Parent

| Column Name | English Description | 中文说明 | Type | Populated | Example |
|---|---|---|---|---|---|
| `AWARDEE_PARENT_BIZPORTAL_ID` | ID of the Awarded Company's Parent. [US companies and wherever applicable] | 中标公司母公司在 BizPortal 中的 ID（主要美国适用） | FIXED | 100% | 0 |
| `AWARDEE_PARENT_NAME` | Name of the Parent Company | 母公司名称 | TEXT | 29% | ENERGOBIT HOLDING LTD |
| `AWARDEE_PARENT_UIC` | National ID Number of the Parent Company | 母公司国家统一识别码 | TEXT | 2% | M-11.339 |
| `AWARDEE_PARENT_VAT_NUMBER` | Tax identification number of the Parent Company | 母公司增值税/税号 | TEXT | 2% | ESA28599033 |
| `AWARDEE_PARENT_COUNTRY` | ISO2 country code of the Parent Company | 母公司所在国家 ISO2 代码 | TEXT | 19% | CY |
| `AWARDEE_PARENT_STATE` | ISO2 state code of the Parent Company. [US companies and wherever applicable] | 母公司所在州/省 ISO2 代码（主要美国适用） | TEXT | 5% | — |
| `AWARDEE_PARENT_LOCATION` | The location of the Parent Company | 母公司所在地（城市） | TEXT | 15% | Nicosia |
| `AWARDEE_PARENT_ADDRESS` | Street address of the Parent Company | 母公司街道地址 | TEXT | 15% | JULIA HOUSE, THEMISTOKLI DERVI 3 |
| `AWARDEE_PARENT_POSTCODE` | Zip code or postal code of the Parent Company address | 母公司地址邮编 | TEXT | 15% | 1066 |
| `AWARDEE_PARENT_EMAIL` | Email address of the Parent Company | 母公司电子邮箱 | TEXT | <1% | — |
| `AWARDEE_PARENT_CONTACT_POINT` | A person or a department serving as the coordinator of information in the Parent Company | 母公司信息联络人或部门 | TEXT | <1% | — |
| `AWARDEE_PARENT_WEBSITE` | Website of the Parent Company | 母公司官网 | TEXT | 11% | https://www.indracompany.com/ |
| `AWARDEE_PARENT_PHONE` | Phone number of the Parent Company | 母公司电话 | TEXT | <1% | — |
| `AWARDEE_PARENT_FAX` | The fax number of the Parent Company | 母公司传真 | TEXT | <1% | — |
| `AWARDEE_PARENT_LISTING_STATUS` | Values: Delisted, Unlisted, Listed | 母公司上市状态：已退市 / 未上市 / 上市 | TEXT | 29% | Unlisted |
| `AWARDEE_PARENT_TICKER_SYMBOL` | Ticker symbol. [Available for public companies only] | 母公司股票代码（仅上市公司） | TEXT | 6% | IDR |
| `AWARDEE_PARENT_STOCK_EXCHANGE_MIC` | Market Identifier Code of the Parent Company's stock exchange | 母公司所在证券交易所的 MIC 代码 | TEXT | 6% | XBAR |
| `AWARDEE_PARENT_STOCK_EXCHANGE_NAME` | Stock exchange where the company's shares are being officially traded. [Available for public companies only] | 母公司股票正式交易的证券交易所名称（仅上市公司） | TEXT | 6% | BOLSA DE BARCELONA |
| `AWARDEE_PARENT_STOCK_EXCHANGE_COUNTRY` | ISO2 country code of the Stock exchange where the company's shares are being officially traded. [Available for public companies only] | 母公司挂牌交易所所在国家的 ISO2 代码（仅上市公司） | TEXT | 6% | ES |
| `AWARDEE_PARENT_ISIN_NUMBER` | An International Securities Identification Number. [Available for public companies only] | 母公司国际证券识别码 ISIN（仅上市公司） | TEXT | 6% | ES0118594417 |

---

## 使用建议 / Usage Notes

1. **核心字段（覆盖率高，建议优先使用）**
   - 主键/标识：`TENDER_BIZPORTAL_ID`、`CONTRACTING_ENTITY_BIZPORTAL_ID`、`DIRECT_AWARDEE_BIZPORTAL_ID`
   - 内容：`TENDER_TITLE`（100%）、`TENDER_DESCRIPTION`（95%）、`TENDER_INDUSTRY_CODES`（77%）
   - 地理：`CONTRACTING_ENTITY_COUNTRY`、`TENDER_COUNTRY`、`DIRECT_AWARDEE_COUNTRY`（均 100%）
   - 金额：`TENDER_POTENTIAL_VALUE_OF_CONTRACT_USD`、`TENDER_VALUE_OF_CONTRACT_TO_DATE_USD`（均 98%，可跨国比较）
   - 时间：`TENDER_DATE_OF_AWARD`（97%）、`TENDER_DATE_OF_DISPATCH`（100%）

2. **稀疏字段（覆盖率低，使用前需谨慎）**
   - 联系方式类（email/phone/fax/contact_point）几乎都 <1%，仅适合做"是否提供联系方式"的虚拟变量。
   - `*_STATE`、`*_CONTRACT_START/END_DATE` 主要在美国合同中可用。

3. **跨实体连接思路**
   - 通过 `DIRECT_AWARDEE_BIZPORTAL_ID` ↔ `AWARDEE_PARENT_BIZPORTAL_ID` 构建公司-母公司层级。
   - 通过 `*_TICKER_SYMBOL` / `*_ISIN_NUMBER` 与股价/财报数据库连接，做政府合同 → 股价反应类研究。
   - 通过 `TENDER_INDUSTRY_CODES`（CPV）做行业聚合分析。

4. **货币与金额**
   - 同时存在本币（`*_AMOUNT` / `*_VALUE_OF_CONTRACT*`）和美元字段（`*_USD`），跨国研究建议直接使用 USD 字段。

---

*本文档基于 Dewey 平台展示的字段元数据整理，字段释义与 TenderAlpha 官方 Data Dictionary 保持一致；数据更新可能引起 Populated 比例变化。*
