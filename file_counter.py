import os

def count_files_in_current_directory():
    """
    计算当前目录下的文件数量。
    """
    file_count = 0
    for _, _, files in os.walk('.'):
        file_count += len(files)
    return file_count

if __name__ == "__main__":
    total_files = count_files_in_current_directory()
    print(f"当前目录下的文件总数: {total_files}")
