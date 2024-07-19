local logging = require("logging")
local inspect = require("inspect")
local SLAXML = require("slaxml")
local xml2lua = require("xml2lua")
--Uses a handler that converts the XML to a Lua table
local handler = require("xmlhandler.tree")

-- local template = pandoc.template
-- logging.temp("Return value of pandoc.template", template.default("eltec"))

function Writer(doc, opts)
	local filter = {
		-- CodeBlock = function(cb)
		-- 	-- only modify, if code block has no attributes
		-- 	if cb.attr == pandoc.Attr() then
		-- 		local delimited = "```\n" .. cb.text .. "\n```"
		-- 		return pandoc.RawBlock("markdown", delimited)
		-- 	end
		-- end,
	}

	local result = pandoc.write(doc:walk(filter), opts)
	logging.temp("Result", result)

	-- logging.temp(result)

	return pandoc.write(doc:walk(filter), "gfm", opts)
end

Template = pandoc.template.default("eltec")
-- function Template()
-- 	return (pandoc.template.default("eltec"))
-- end
