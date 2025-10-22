# -*- coding: utf-8 -*-
import os

def count_files_in_directory(directory='.'):
    """
    计算指定目录下的文件数量。
    """
    file_count = 0
    for _, _, files in os.walk(directory):
        file_count += len(files)
    return file_count

def count_code_lines_in_file(filepath):
    """
    计算单个文件中的代码行数（忽略空行和注释）。
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        code_lines = 0
        for line in lines:
            stripped_line = line.strip()
            # 忽略空行和单行注释
            if stripped_line and not stripped_line.startswith('#'):
                code_lines += 1
        return code_lines
    except Exception:
        return 0

def count_total_code_lines(directory='.'):
    """
    计算目录中所有代码文件的总行数。
    只统计特定后缀的文件。
    """
    code_file_extensions = ['.py', '.sh', '.md']
    total_lines = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in code_file_extensions):
                filepath = os.path.join(dirpath, filename)
                total_lines += count_code_lines_in_file(filepath)
    return total_lines


if __name__ == "__main__":
    current_directory = '.'
    total_files = count_files_in_directory(current_directory)
    total_lines_of_code = count_total_code_lines(current_directory)
    
    print(f"当前目录下的文件总数: {total_files}")
    print(f"当前目录下的代码总行数 (py, sh, md): {total_lines_of_code}")
