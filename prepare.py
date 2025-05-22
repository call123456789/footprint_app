import os,json
import subprocess
import sys

def install(package):
    # 检查是否已安装
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        print(f"{package} 已存在，跳过安装")
        return
    
    try:
        #使用这些命令安装库
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "--trusted-host", "files.pythonhosted.org",
            "--trusted-host", "pypi.org",
            "--trusted-host", "pypi.python.org",
            "--trusted-host", "files.pythonhosted.org:443",
            "--trusted-host", "pypi.org:443",
            "--trusted-host", "pypi.python.org:443",
            "--trusted-host", "mirrors.aliyun.com",
            "--trusted-host", "mirrors.aliyun.com:443",
            package
        ], check=True)
        print(f"{package} 已成功安装")
    except subprocess.CalledProcessError as e:
        print(f"安装 {package} 时出错: {e}")
def prepare():
    install("openai")
    install("requests")
    install("PyQt5")

def prepare2():
    list = ['江西省', '安徽省', '浙江省', '四川省', '甘肃省', '贵州省', '河南省', '青海省', '山西省', '福建省', '湖北省', '香港特别行政区', '陕西省', '澳门特别行政区', '重庆市', '台湾省', '内蒙古自治区', '宁夏回族自治区', '广东省', '江苏省', '上海市', '山东省', '黑龙江省', '吉林省', '海南省', '西藏自治区', '云南省', '广西壮族自治区', '北京市', '新疆维吾尔自治区', '辽宁省', '湖南省', '天津市', '河北省']
    for i in list:
        with open('resources/data/'+i+'.json') as f:
            dict = json.load(f)
        for j in dict:
            os.makedirs('resources/data/'+i+j, exist_ok=True)

if __name__ == "__main__":
    prepare()
    prepare2()