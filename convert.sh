#!/bin/bash

# 用法：bash convert.sh [檔案或目錄 ...]
# 預設遞迴處理當前目錄的 *.txt；僅將嚴格可逆的 GBK 轉為 UTF-8。
# 已是 UTF-8 的檔案保持原樣；無法解碼的檔案報錯且不覆蓋。
set -euo pipefail

exec python3 - "$@" <<'PY'
import os
import stat
import sys
import tempfile
from pathlib import Path


def find_text_files(path):
    if path.is_symlink():
        return
    if path.is_dir():
        for child in sorted(path.iterdir()):
            if not child.name.startswith('.'):
                yield from find_text_files(child)
    elif path.is_file():
        if path.suffix.lower() == '.txt':
            yield path
    else:
        raise ValueError(f'路徑不存在或不是普通檔案：{path}')


def convert(path):
    original = path.read_bytes()
    try:
        original.decode('utf-8')
        return False
    except UnicodeDecodeError:
        pass

    # 嚴格解碼，不忽略錯誤、不替換字元、不規範化換行。
    text = original.decode('gbk')
    if text.encode('gbk') != original:
        raise ValueError('GBK 編碼無法逐位元組還原，已跳過')
    converted = text.encode('utf-8')
    if converted.decode('utf-8').encode('gbk') != original:
        raise ValueError('轉換校驗失敗，已跳過')

    mode = stat.S_IMODE(path.stat().st_mode)
    # 每個檔案使用獨立的臨時檔案；只有寫入和校驗成功才原子替換。
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.convert-', delete=False) as file:
        temporary = Path(file.name)
        try:
            file.write(converted)
            file.flush()
            os.fsync(file.fileno())
            os.fchmod(file.fileno(), mode)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        if temporary.read_bytes() != converted:
            raise ValueError('臨時檔案校驗失敗，原檔案保持不變')
        if path.read_bytes() != original:
            raise ValueError('處理期間原檔案發生變化，已取消替換')
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'[已轉換] {path}')
    return True


converted_count = 0
skipped_count = 0
errors = 0
seen = set()
for argument in sys.argv[1:] or ['.']:
    try:
        for path in find_text_files(Path(argument)):
            key = path.resolve()
            if key in seen:
                continue
            seen.add(key)
            try:
                if convert(path):
                    converted_count += 1
                else:
                    skipped_count += 1
            except (OSError, UnicodeError, ValueError) as error:
                errors += 1
                print(f'[失敗，保留原檔案] {path}: {error}', file=sys.stderr)
    except (OSError, ValueError) as error:
        errors += 1
        print(f'[失敗] {argument}: {error}', file=sys.stderr)

print(f'完成：轉換 {converted_count}，跳過 UTF-8 檔案 {skipped_count}，失敗 {errors}。')
sys.exit(1 if errors else 0)
PY
