--When MSFS runs on same computer
--ip = "127.0.0.1",
--When MSFS runs on different computer, enter the computer's IP shown when running the python script DCS_MSFS_CONNECT
--ip = "192.168.1.100",
Network = {
	ip = "127.0.0.1",
    port = 31339
}

Config = {
    writeLog = false, -- write log txt file
    filename = "C:/Users/ME/DcsMsfsLog.txt",
    interval = 3, -- frequent updates in milliseconds
    rare = 50, -- less important updates in milliseconds
}