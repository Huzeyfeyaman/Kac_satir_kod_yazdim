import os
import json
from pathlib import Path
from colorama import Fore, Style, init
from typing import TextIO

# Terminal renkleri için başlatma
init()

# Yazılım dillerine göre dosya uzantıları
LANGUAGE_EXTENSIONS = {
    'Python': ['.py'],
    'JavaScript': ['.js'],
    'C++': ['.cpp', '.h'],
    'Java': ['.java'],
    'HTML': ['.html', '.htm'],
    'CSS': ['.css'],
    'Ruby': ['.rb'],
    'PHP': ['.php'],
    'C#': ['.cs'],
    'Go': ['.go'],
    'R': ['.r'],
    'SQL': ['.sql'],
    'Shell': ['.sh']
}


def count_lines(file_path: str) -> int:
    try:
        with open(file_path, 'r', errors='ignore') as file:
            return sum(1 for _ in file)
    except Exception as e:
        print(f"{Fore.RED}Hata: {file_path} okunamadı ({e}){Style.RESET_ALL}")
        return 0


def get_file_size(file_path: str) -> int:
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"{Fore.RED}Hata: {file_path} boyutu alınamadı ({e}){Style.RESET_ALL}")
        return 0


def detect_language(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    for language, extensions in LANGUAGE_EXTENSIONS.items():
        if ext in extensions:
            return language
    return 'Unknown'


def scan_directory(directory: str) -> dict:
    result = {}
    for root, _, files in os.walk(directory):
        for file in files:
            lang = detect_language(file)
            full_path = os.path.join(root, file)
            line_count = count_lines(full_path)
            file_size = get_file_size(full_path)

            if lang in result:
                result[lang]['files'].append({'path': full_path, 'lines': line_count, 'size': file_size})
                result[lang]['total_lines'] += line_count
                result[lang]['total_size'] += file_size
            else:
                result[lang] = {
                    'files': [{'path': full_path, 'lines': line_count, 'size': file_size}],
                    'total_lines': line_count,
                    'total_size': file_size
                }
    return result


def save_results_to_json(results: dict, output_file: str) -> None:
    with open(str(output_file), 'w', encoding='utf-8') as f:  # Ensure correct type hinting
        json.dump(results, f, indent=4, ensure_ascii=False)


def main() -> None:
    directory = input(f"{Fore.YELLOW}Taranacak dizini girin: {Style.RESET_ALL}")
    if not os.path.isdir(directory):
        print(f"{Fore.RED}Hata: Geçersiz dizin!{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Taranıyor: {directory}{Style.RESET_ALL}")
    scan_results = scan_directory(directory)
    output_file = str(Path(directory) / 'scan_results.json')
    save_results_to_json(scan_results, output_file)

    for lang, data in scan_results.items():
        print(f"{Fore.GREEN}{lang}:{Style.RESET_ALL}")
        print(f"  {Fore.BLUE}Toplam Dosya Sayısı:{Style.RESET_ALL} {len(data['files'])}")
        print(f"  {Fore.MAGENTA}Toplam Satır Sayısı:{Style.RESET_ALL} {data['total_lines']}")
        print(f"  {Fore.YELLOW}Toplam Boyut (KB):{Style.RESET_ALL} {data['total_size'] / 1024:.2f}")

    print(f"{Fore.CYAN}Sonuçlar kaydedildi: {output_file}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
