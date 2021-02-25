-- filename: UART SeNsors

local function init()
	-- called once when model is loaded
	sources = {}
	local file = io.open('/SCRIPTS/MIXES/sources.txt', 'r')
	local char = '\r'
	-- loop until end of file ('') is reached
	while char ~= '' do
		-- reset temporary src
		local src = ''
		-- skip all carriage return and new line characters
		while char == '\r' or char == '\n' do
			char = io.read(file, 1)
		end
		-- append characters to src until the next carriage return or new line
		while char ~= '\r' and char ~= '\n' and char ~= '' do
			src = src .. char
			char = io.read(file, 1)
		end
		-- append src to sources
		table.insert(sources, src)
	end
	io.close(file)
end

local function run()
	-- called periodically
	packet = ''
	for i,src in ipairs(sources) do
		packet = packet .. src .. '\x03' .. getValue(src) ..'\x03'
	end
	packet = packet .. '\n'
	serialWrite(packet)
end

return {init=init, run=run}