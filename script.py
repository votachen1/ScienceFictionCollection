import os
import json
from urllib.parse import quote
import re
import stat
import tempfile
from pathlib import Path

HEADER = """# 科幻小說作品集

## 貢獻者 Contributors

[![Contributors](https://contrib.rocks/image?repo=VeejaLiu/ScienceFictionCollection)](https://github.com/VeejaLiu/ScienceFictionCollection/graphs/contributors)

## 作者

"""


SIZE_UNIT = ["B", "KB", "MB", "GB"]


def get_file_size(file_path):
    unit_level = 0
    file_size = os.path.getsize(file_path)
    for i in range(3):
        if file_size > 1000:
            unit_level += 1
            file_size = file_size / 1000
        else:
            break
    return str(round(file_size, 2)) + SIZE_UNIT[unit_level]


def add_books_from_directory(path, indent_level=0):
    """遞迴生成目錄內容；不跟隨符號連結或收錄隱藏檔案。"""
    markdown = ""
    indent = " " * 2 * indent_level  # 生成縮排

    directories = []
    files = []

    for entry in os.scandir(path):
        if entry.name.startswith('.') or entry.is_symlink():
            continue
        if entry.is_dir():
            directories.append(entry.name)
        elif entry.is_file():
            files.append(entry.name)

    # 先寫目錄，再寫檔案
    for directory in sorted(directories):
        markdown += f"{indent}- {directory}\n"
        markdown += add_books_from_directory(os.path.join(path, directory), indent_level + 1)
    for file in sorted(files):
        book_size = get_file_size(os.path.join(path, file))
        missing_note = " **（空檔案，正文缺失）**" if os.path.getsize(os.path.join(path, file)) == 0 else ""
        markdown += f"{indent}- {file} _[{book_size}]_{missing_note}\n"
    return markdown


def author_directories(root):
    periodical_directories = {item['directory'] for item in periodical_records(root)}
    return sorted(path.name for path in root.iterdir()
                  if path.is_dir() and not path.is_symlink()
                  and re.match(r'^\d{3} - .+', path.name)
                  and path.name not in periodical_directories)


def periodical_records(root):
    manifest = root / 'metadata' / 'periodicals.json'
    return json.loads(manifest.read_text(encoding='utf-8'))['periodicals'] if manifest.exists() else []


def periodical_index(root):
    records = periodical_records(root)
    if not records:
        return ''
    return '\n## 期刊\n\n' + ''.join(f"- [{item['name']}]({quote(item['directory'], safe='')}/)\n" for item in records)


def generate_readme(root):
    metadata_file = root / 'metadata' / 'authors.json'
    records = json.loads(metadata_file.read_text(encoding='utf-8'))['authors'] if metadata_file.exists() else []
    by_directory = {author['directory']: author for author in records}
    markdown = HEADER
    for directory in author_directories(root):
        author = by_directory.get(directory)
        name = author['name'] if author else directory
        english = author.get('names', {}).get('en') if author else None
        if english and english != name:
            name += f' · {english}'
        markdown += f"- [{name}]({quote(directory, safe='')}/)\n"
    markdown += periodical_index(root) + '\n## 作品\n\n' + generate_work_list(root)
    return markdown + """
## 更多

[線上閱讀](https://veejaliu.github.io/ScienceFictionCollection-Web/) · [專案說明](docs/PROJECT.md) · [授權範圍](LICENSE-SCOPE.md) · [Web 倉庫](https://github.com/VeejaLiu/ScienceFictionCollection-Web)

## Star History

[![Star History Chart](https://star-history.dera.page/svg?repos=VeejaLiu/ScienceFictionCollection&type=Date)](https://star-history.dera.page/#VeejaLiu/ScienceFictionCollection&Date)
"""


def generate_catalog(root):
    authors = author_directories(root)
    markdown = '# 完整作品目錄\n\n[返回倉庫首頁](README.md) · [線上閱讀](https://veejaliu.github.io/ScienceFictionCollection-Web/)\n\n由 `script.py` 根據目錄和檔案大小生成，不讀取小說正文。\n\n## 作者索引\n\n'
    for author in authors:
        anchor = re.sub(r'[^\w\s-]', '', author.lower()).strip()
        anchor = re.sub(r'\s+', '-', anchor)
        markdown += f"- [{author}](#{anchor})\n"
    return markdown + periodical_index(root) + '\n## 作品\n\n' + generate_work_list(root)


def generate_work_list(root):
    markdown = ''
    for author in author_directories(root):
        markdown += f"### {author.rstrip()}\n"
        markdown += add_books_from_directory(root / author)
    for periodical in periodical_records(root):
        markdown += f"### 期刊：{periodical['name']}\n"
        markdown += add_books_from_directory(root / periodical['directory'])
    return markdown


def write_document(target, text):
    content = text.encode('utf-8')
    if target.exists() and target.read_bytes() == content:
        print(f'{target.name} 已是最新。')
        return
    mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o644
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.readme-', delete=False) as file:
        temporary = Path(file.name)
        try:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
            os.fchmod(file.fileno(), mode)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'{target.name} 已更新。')


def main():
    root = Path(__file__).resolve().parent
    write_document(root / 'README.md', generate_readme(root))
    write_document(root / 'CATALOG.md', generate_catalog(root))


if __name__ == '__main__':
    main()
