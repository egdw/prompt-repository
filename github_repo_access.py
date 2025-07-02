import os
import requests
from typing import List, Optional

class GitHubRepoAccess:
    def __init__(self, owner: str, repo: str):
        """初始化GitHub仓库访问类

        Args:
            owner (str): 仓库所有者的用户名
            repo (str): 仓库名称
        """
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

    def get_root_directories(self) -> List[str]:
        """获取仓库根目录下的所有目录

        Returns:
            List[str]: 目录名称列表
        """
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            contents = response.json()
            return [item["name"] for item in contents if item["type"] == "dir"]
        else:
            raise Exception(f"获取根目录失败: {response.status_code}")

    def get_txt_files_in_directory(self, directory: str) -> List[str]:
        """获取指定目录下的所有txt文件

        Args:
            directory (str): 目录名称

        Returns:
            List[str]: txt文件名称列表
        """
        url = f"{self.base_url}/{directory}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            contents = response.json()
            return [item["name"] for item in contents 
                    if item["type"] == "file" and item["name"].endswith(".txt")]
        else:
            raise Exception(f"获取目录内容失败: {response.status_code}")

    def get_file_content(self, directory: str, filename: str) -> Optional[str]:
        """获取指定文件的内容

        Args:
            directory (str): 文件所在的目录名称
            filename (str): 文件名称

        Returns:
            Optional[str]: 文件内容，如果文件不存在则返回None
        """
        url = f"{self.base_url}/{directory}/{filename}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            content = response.json()
            if content["type"] == "file":
                import base64
                return base64.b64decode(content["content"]).decode("utf-8")
        return None

# 使用示例
def main():
    # 创建GitHubRepoAccess实例
    repo_access = GitHubRepoAccess("egdw", "prompt-repository")

    try:
        # 1. 获取所有根目录
        print("获取根目录:")
        root_dirs = repo_access.get_root_directories()
        print(root_dirs)

        if root_dirs:
            # 2. 获取第一个目录下的所有txt文件
            first_dir = root_dirs[0]
            print(f"\n获取 {first_dir} 目录下的txt文件:")
            txt_files = repo_access.get_txt_files_in_directory(first_dir)
            print(txt_files)

            if txt_files:
                # 3. 获取第一个txt文件的内容
                first_file = txt_files[0]
                print(f"\n获取文件 {first_file} 的内容:")
                content = repo_access.get_file_content(first_dir, first_file)
                if content:
                    print(content)
                else:
                    print("无法获取文件内容")

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()