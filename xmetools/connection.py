import paramiko


def exec_command(command):
    ssh = ssh_conn()
    _, stdout, _ = ssh.exec_command(command)
    content = stdout.read().decode()
    ssh.close()
    return content

def ssh_conn(hostname='192.168.2.17', port=22, username='xzadudu179', password='0404xzadudu'):
    # 创建 SSH 客户端
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    # 自动添加远程主机的 SSH 密钥（防止第一次连接时提示）
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接到远程主机
    ssh.connect(hostname, port, username, password)
    return ssh

def get_file(path: str, local_dir="."):
    ssh = ssh_conn()
    sftp = ssh.open_sftp()
    # 下载远程文件到本地
    path.replace("\\", "/")
    if path.startswith("~"):
        path = "/home/xzadudu179" + path[1:]
    print(path)
    remote_path = path  # 远程文件路径
    local_path = (local_dir + "/").replace("//", "/") + path.split("/")[-1]    # 本地保存路径
    # print("stat:", sftp.stat(remote_path))
    sftp.get(remote_path, local_path)
    # print(f"文件下载成功: {remote_path} 到 {local_path}")
    # 关闭会话
    sftp.close()
    ssh.close()
    return local_path

def list_files(path):
    return exec_command(f'ls {path}').split()

# get_file('~/Desktop/Server/1.20_mods_202501/Server/crash-reports/crash-2025-01-19_06.38.36-server.txt')