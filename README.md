部署说明（README.md）
为了使脚本在每次启动时自动运行，请按照以下步骤操作：

保存脚本：将上面的 Python 代码保存为 startup_logger.py。
给予执行权限：在终端中运行以下命令，使其可执行：
        chmod +x startup_logger.py
    
创建系统服务（推荐方法）：
    创建服务单元文件：
                sudo nano /etc/systemd/system/startup-logger.service
        
    在文件中粘贴以下内容（请将 /path/to/your/startup_logger.py 替换为你实际保存脚本的完整路径）：
                [Unit]
        Description=Log startup date and IP
        After=network.target

        [Service]
        Type=oneshot
        ExecStart=/usr/bin/python3 /path/to/your/startup_logger.py
        RemainAfterExit=yes

        [Install]
        WantedBy=multi-user.target
        
    保存并关闭文件。
    重新加载 systemd 配置并启用服务：
                sudo systemctl daemon-reload
        sudo systemctl enable startup-logger.service
        
    系统将在下次启动时自动运行该脚本。

（备选方案）添加到用户启动脚本：
    如果你只想为当前用户记录，可以将脚本路径添加到 ~/.bash_profile 或 ~/.profile 文件中：
        echo "python3 /path/to/your/startup_logger.py" >> ~/.bash_profile
    

完成部署后，每次启动系统，脚本都会自动执行，并将包含时间戳、外网IP和内网IP的日志追加到 ~/.startup_log.txt 文件中。
Grnerate By Qwen
