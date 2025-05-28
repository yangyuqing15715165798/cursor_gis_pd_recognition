import importlib.metadata
import sys

def generate_requirements(output_file='requirements.txt'):
    # 获取当前环境中的所有已安装包及其版本号
    packages = importlib.metadata.distributions()
    requirements = sorted(f"{package.metadata['Name']}=={package.version}" for package in packages)

    # 将包信息写入 requirements.txt 文件
    with open(output_file, 'w') as f:
        for req in requirements:
            f.write(req + '\n')

    print(f"Requirements have been generated and saved to {output_file}.")

if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("This script requires Python 3.8 or higher.")
    else:
        generate_requirements()

