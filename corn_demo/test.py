import subprocess
script = "/root/CropGPT/iCREPCP-main/corn_demo/predict.py"
input_file = "/root/CropGPT/iCREPCP-main/corn_demo/example1.txt"
parameter1 = "BJ"
parameter2 = "DLL"
command = f"python {script} {input_file} --diquname {parameter1} --name {parameter2}"
print(command)
# command = f"python predict.py example1.txt --diquname BJ --name DLL"
# 在命令行中执行命令
result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# 打印命令执行后的标准输出
print(result.stdout)