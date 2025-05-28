@echo off
echo 启动GIS局放监测系统...

REM 启动局放类型识别API服务
echo 正在启动局放类型识别API服务...
start cmd /k "cd /d %~dp0pd_recognition_system && python svm_fastapi.py"

REM 等待API服务启动
echo 等待API服务启动...
timeout /t 5 /nobreak

REM 启动主程序
echo 正在启动GIS局放监测系统主程序...
start python "%~dp03_11_gis_modbusTCPGUI_v6.py"

echo 系统启动完成！