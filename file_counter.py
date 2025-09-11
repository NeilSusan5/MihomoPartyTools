import os

def count_files_in_current_directory():
    """
    计算当前目录下的文件数量。
    """
    # 初始化文件计数器
    file_count = 0
    # 遍历当前目录及其所有子目录
    for _, _, files in os.walk('.'):
        # 将当前目录下的文件数量累加到计数器
        file_count += len(files)
    # 返回文件总数
    return file_count

if __name__ == "__main__":
    total_files = count_files_in_current_directory()
    print(f"当前目录下的文件总数: {total_files}")
