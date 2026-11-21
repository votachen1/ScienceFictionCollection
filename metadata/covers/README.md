# 封面目錄與命名

[返回元資訊說明](../README.md)

封面以“作者／作品／版本”歸檔。檔案名說明實際用途或已確認的版次，不再使用來源平臺編號、作品ID或雜湊作為圖片檔案名。來源編號、ISBN、原圖摘要、當前圖片摘要及權利說明保留在 [catalog.json](catalog.json) 中。

## 當前目錄

```text
covers/
  works/<作者slug>/<作品名稱slug>/<版本說明>.webp
  journals/<刊物slug>/<年份>/issue-<期號>-<版本說明>.webp
  catalog.json
  title-aliases.json
  README.md
```

例如：

```text
works/liu-cixin/三體/reference-edition.webp
works/arthur-c-clarke/2061-太空漫遊/2019-zh-cn-epub-cover.webp
works/orson-scott-card/死者代言人/zh-cn-epub-cover.webp
works/orson-scott-card/死者代言人/reference-edition.webp
works/philip-k-dick/the-variable-man/1953-09-original-magazine.webp
journals/science-fiction-world/2026/issue-05-zh-cn-epub.webp
```

作品目錄採用可讀書名；同一作品的不同格式、譯本或參考封面放在一起。期刊目錄中的 `issue-05` 表示第5期，不推測為5月刊。期號補零便於按檔案名排列，清單中的期號仍使用整數。

## 版本說明

| 名稱 | 含義 |
| --- | --- |
| `reference-edition` | 出版參考版封面，不能據此認定與正文的譯本或紙本版次一致 |
| `1895-reference-edition` | 已有來源支援1895年參考封面，不以正文原作年份代替封面版次 |
| `zh-cn-epub-cover`、`zh-tw-epub-cover`、`en-epub-cover` | 對應所收錄EPUB版本的封面，語言標記來自該正文版本 |
| `2019-zh-cn-epub-cover` | 已明確登記2019年中文版本的EPUB封面 |
| `上冊-zh-cn-epub-cover` | 上冊EPUB的封面，卷冊資訊作為版本說明保留 |
| `1953-09-original-magazine` | 原作首發刊期的封面素材，不冒充獨立單行本封面 |

只有有來源依據的年份、語言或卷冊資訊才進入版本名；未知資訊不推測補寫。同一張封面若服務於多個版本，只儲存一份，由各自清單明確引用；共享參考封面不表示這些正文版本相同。

## 清單與維護

- 各作者作品清單、期刊分期清單中的 `cover` 是當前使用關係；檔案路徑相對於 metadata。
- `catalog.json` 的 `entries` 按 `bookId` 儲存匹配記錄，`asset` 指向當前圖片；`source` 保留來源編號、原始連結、ISBN、版本與權利資訊。
- `sha256` 是當前WebP圖片摘要，`sourceSha256` 是原始圖像摘要；重新命名不改變這些摘要。
- `assetVersion` 記錄可讀版本名，`storage` 統計當前圖片數量與位元組數；舊批次壓縮統計儲存在 `historicalCompressionBatch`，不冒充本次遷移統計。
- `title-aliases.json` 只用於書名檢索，不生成封面圖片。

新增圖片先按上述結構命名，再登記來源和作品引用。刪除圖片前，以現有小說和期刊清單的 `cover` 引用確定是否仍在使用；引用中的圖片保留，未引用的舊圖、示例圖及其廢棄生成附件可以清理。沒有封面的作品使用閱讀器內的即時繪製邏輯，不需要存放示例圖片。

2026年10月21日共遷移76張在用封面，刪除3張未引用示例WebP及其3份SVG，並移除只用於這些示例的生成指令碼和舊說明檔案。在用圖片未重編碼，78個閱讀檔案繼續使用這些封面。逐項舊路徑、新路徑、摘要與清理原因見 [封面整理記錄](../acquisition/cover-organization-2026-10-21.json)；其中舊路徑只用於歷史追溯，不表示檔案仍應存在。
