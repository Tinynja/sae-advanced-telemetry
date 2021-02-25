local function init()
	-- called once when model is loaded
	sources = {}
	local file = io.open('sources.txt', 'r')
	local src = file:read('l')
	while src ~= nil do
		table.insert(sources, src)
		src = file:read('l')
	end
end

local function background()
	-- called periodically
	packet = ''
	for i,v in ipairs(sources) do
		packet = packet .. sources[i] .. '\x03' .. getValue(sources[i]) ..'\x03'
	end
	packet = packet .. '\x04'
	serialWrite(packet)
end

return {init=init, background=background}