-- filename: UART SeNsors

local function init()
	-- called once when model is loaded
	uart_sources = {}
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
		-- figure out the identifier of the source (getting value by identifier is faster than by name)
		src = getFieldInfo(src)
		-- check if src exists
		if src ~= nil then
			-- save some memory
			src['desc'] = nil
			src['unit'] = nil
			-- append src to uart_sources
			table.insert(uart_sources, src)
		end
	end
	io.close(file)
end

local function run()
	-- called periodically
	local packet = ''
	for i,src in ipairs(uart_sources) do
		-- protocol: \x01 + [type] + \x02 + [source] + \x03 + \x01 + [type] + \x02 + [value] + \x03
		
		-- 		type :=
		-- 			s: source
		-- 			v: value
		
		-- 		\x01: start_of_heading
		-- 		\x02: start_of_text
		-- 		\x03: end_of_text
		local value = getValue(src['id'])
		if src['name'] == 'GPS' then
			-- GPS source returns a table so it requires unpacking
			value = tostring(value['lat']) .. ',' .. tostring(value['lon'])
		end
		-- Assemble the packet
		packet = packet .. '\x01' .. 's' .. '\x02' .. src['name'] .. '\x03'
		packet = packet .. '\x01' .. 'v' .. '\x02' .. value .. '\x03'
	end
	packet = packet .. '\n'
	serialWrite(packet)
end

return {init=init, run=run}