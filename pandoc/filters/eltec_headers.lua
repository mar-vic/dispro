local logging = require("logging")
local stack = require("simple_stack")

local headers = Stack:Create()

-- function Header(h)
-- 	if headers:getn() == 0 then
-- 		headers:push(h)
-- 		return { "<div type='chapter'><head>", pandoc.Inlines(h.content), "</head>" }
-- 	elseif h.level <= headers:peek().level then
-- 		local closingTags = ""
-- 		while headers:peek() and h.level <= headers:peek().level do
-- 			headers:pop(1)
-- 			closingTags = closingTags .. "</div>"
-- 		end
-- 		headers:push(h)
-- 		return { closingTags .. "<div type='chapter'><head>", pandoc.Inlines(h.content), "</head>" }
-- 	else
-- 		headers:push(h)
-- 		return { "<div type='chapter'><head>", Writer.Inlines(h.content), "</head>" }
-- 	end
-- end

headcount = {
	Header = function(h)
		if headers:getn() == 0 then
			headers:push(h)
		elseif h.level <= headers:peek().level then
			while headers:peek() and h.level <= headers:peek().level do
				headers:pop(1)
			end
			headers:push(h)
		else
			headers:push(h)
		end
	end,
}

function Pandoc(el)
  logging.temp(el)
	el.blocks:walk(headcount)
	el.meta.unclosed_chapters = {}
	-- logging.temp(headers:getn())
	while headers:getn() > 0 do
		table.insert(el.meta.unclosed_chapters, pandoc.utils.stringify(headers:pop()))
	end
	return el
end
