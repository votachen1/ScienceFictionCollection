[返回倉庫首頁](../README.md) · [完整作品目錄](../CATALOG.md)

# 科幻小說作品集

收集科幻小說原文，並集中維護線上閱讀所需的作者、作品與版本元資訊。

**[線上閱讀](https://veejaliu.github.io/ScienceFictionCollection-Web/)** · **[閱讀器 Web 倉庫](https://github.com/VeejaLiu/ScienceFictionCollection-Web)** · **[元資訊維護指南](../metadata/README.md)**

## 兩個倉庫的分工

| 專案 | 負責內容 |
| --- | --- |
| [ScienceFictionCollection](https://github.com/VeejaLiu/ScienceFictionCollection)（本倉庫） | 作者與系列目錄中的小說原文，以及 `metadata/` 中的姓名、簡介、語言版本、頭像和封面 |
| [ScienceFictionCollection-Web](https://github.com/VeejaLiu/ScienceFictionCollection-Web) | 書架與列表、線上閱讀、語言與版本切換、閱讀進度、SEO 和 GitHub Pages 釋出 |

當前登記 **17 位作者、1種期刊、224組小說作品、2期期刊、228個閱讀檔案**。網頁透過 metadata 中的 `directory`、`path` 繫結檔案，內部 ID 保持穩定，對外使用可讀的 slug。截至2026年10月18日，已逐項核對全部作品檔案，累計修正30個年份標註、1個版本名稱，並將誤署名阿西莫夫的《被遺忘的世界》節寫本按原作歸入柯南·道爾目錄；不同譯本和版本均保留。[核對來源、年份口徑及5個待核條目](../metadata/publication-years/verification.json) 單獨登記，[本輪8項追查記錄](../metadata/publication-years/follow-up-2026-10-18.json) 包括已查明事實和未決原因。

《創世紀》的空檔案尚未補入正文：已登記[番茄小說官方合集目錄](https://fanqienovel.com/page/7363514084773350462)及版權頁，但平臺篇目與2004—2005年原刊尚未比對，也未查到可再分發的開放許可文字。目錄明確標註正文缺失；其餘待核條目保留原狀。

## 線上閱讀與語言版本

閱讀器支援簡體中文、繁體中文、英文、法語、德語、俄語、日語和韓語介面。介面翻譯不等於正文翻譯：當前正文以中文為主，簡繁體按檔案登記；《火星紀事》EPUB 已核對為繁體。其他語言版本需要收錄真實檔案，並透過相同的 `workId` 關聯。

每本書優先選擇當前介面語言，其次英文，最後選擇一個已有語言版本；書架、列表與閱讀頁均保留版本切換。TXT/Markdown 開啟後按需載入正文並儲存本機閱讀進度；EPUB 支援瀏覽器內閱讀、目錄跳轉、翻頁和位置恢復；PDF 提供原始檔案入口。目錄及網站構建只讀取元資訊和圖片，不批次讀取或打包小說正文。

## 元資訊與圖片

- `metadata/authors.json`：作者 ID、slug、真實目錄、多語言姓名、簡介和資料來源。
- `metadata/books/<作者slug>.json`：檔案 ID、作品 `workId`、slug、正文路徑、語言、格式、系列和封面。
- `metadata/avatars/`、`metadata/covers/`：WebP 頭像和封面；頭像最長邊 160 畫素，封面不超過 600 × 900 畫素。
- [封面整理清單](../metadata/covers/catalog.json)：現有228條閱讀檔案記錄，其中78條引用76張封面；圖片按作者、作品、版本歸檔，期刊按刊名、年份、期號歸檔。來源編號、版本說明和圖片摘要保留在清單中；未引用的舊示例圖已清理，沒有封面的作品由閱讀器即時繪製替代圖。

## 維護與更新

在本倉庫根目錄執行：

```bash
python3 metadata/sync.py
python3 metadata/sync.py --check
python3 script.py
```

作者清單由 `authors.json` 的 `booksFile` 明確指定，例如 `books/liu-cixin.json`；ID保留在JSON內容中。同步指令碼只讀取檔案名、路徑和檔案大小，保留已有元資訊欄位；移動檔案時先更新 `path`，保留檔案 ID、作品 `workId` 和 slug。新增作者或翻譯版本的欄位說明見 [metadata/README.md](../metadata/README.md)。

README 首頁與完整作品目錄由 `script.py` 自動生成；本說明文件單獨維護。

2026年10月21日新增的使用者檔案包括太空漫遊四部曲拆分EPUB、《2061》TXT、《海中山》及《科幻世界》2026年第5、6期，新增7組作品、8份檔案；來源、廣告清理及完整性核對見 [元資訊維護指南](../metadata/README.md#本輪使用者提供的小說與期刊2026年10月21日)。期刊在獨立的“期刊”分類中按刊名、年份及期號登記，保留整期文章署名。

Web 主分支更新後由 GitHub Actions 自動釋出。僅修改本倉庫元資訊時，在 [Web 的 Pages 釋出工作流](https://github.com/VeejaLiu/ScienceFictionCollection-Web/actions/workflows/pages.yml) 選擇 **Run workflow** 即可重新構建網站；釋出會讀取本倉庫 `master` 的 metadata，正文則在閱讀時從本倉庫按需獲取。

## 來源與權利記錄

詳見 [授權範圍](../LICENSE-SCOPE.md)；現有 [MIT LICENSE](../LICENSE) 保留原文。

小說正文、作者頭像、出版社封面與應用程式碼分別保留各自的權利歸屬。書目或封面來源連結不代表獲得開放許可；封面出處與版本匹配說明見整理清單，閱讀器自有程式碼及第三方素材的授權記錄見 [Web 倉庫說明](https://github.com/VeejaLiu/ScienceFictionCollection-Web/blob/master/docs/PROJECT.md#上游來源與應用授權)。

## Star History

[![Star History Chart](https://star-history.dera.page/svg?repos=VeejaLiu/ScienceFictionCollection&type=Date)](https://star-history.dera.page/#VeejaLiu/ScienceFictionCollection&Date)
