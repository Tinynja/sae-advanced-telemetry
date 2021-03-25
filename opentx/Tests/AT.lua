local function init()
	setSerialBaudrate(38400)
end

local function run()
	serialWrite('AT\r\n')
end

return {init=init, run=run}