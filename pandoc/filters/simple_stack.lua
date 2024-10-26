-- Stack Table
-- Uses a table as stack, use <table>:push(value) and <table>:pop()
-- Lua 5.1 compatible

local logging = require("logging")

-- GLOBAL
Stack = {}

-- Create a Table with stack functions
function Stack:Create()
	-- stack table
	local t = {}
	-- entry table
	t._et = {}

	-- push a value on to the stack
	function t:push(...)
		if ... then
			local targs = { ... }
			-- add values
			for _, v in ipairs(targs) do
				table.insert(self._et, v)
			end
		end
	end

	-- pop a value from the stack
	function t:pop(num)
		-- get num values from stack
		local num = num or 1

		-- return table
		local entries = {}

		-- get values into entries
		for i = 1, num do
			-- get last entry
			if #self._et ~= 0 then
				table.insert(entries, self._et[#self._et])
				-- remove last value
				table.remove(self._et)
			else
				break
			end
		end
		-- return unpacked entries
		return table.unpack(entries)
	end

	-- Get a value from top of the stack without removing it
	function t:peek()
		return self._et[#self._et]
	end

	-- get entries
	function t:getn()
		return #self._et
	end

	-- list values
	function t:list()
		for i, v in pairs(self._et) do
			print(i, v)
		end
	end
	return t
end

-- s = Stack:Create()
-- s:push(3, 4, 5, 6)
-- print(s:getn())
-- print(s:list())
-- s:pop()
-- s:pop()
-- s:pop()
-- s:pop()
-- print(s:peek())
-- print(s:pop(1))
-- print(s:pop(1))
-- print(s:pop(1))
-- print(s:pop(1))
-- print(s:pop(1))
-- print(s:pop(1))

-- CHILLCODE™
