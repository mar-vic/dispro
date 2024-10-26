local stack = require("simple_stack")

local headers = Stack:Create()

function Header(h)
	if headers:getn() == 0 then
		headers:push(h)
		return { "<div type='chapter'><head>", pandoc.Inlines(h.content), "</head>" }
	elseif h.level <= headers:peek().level then
		local closingTags = ""
		while headers:peek() and h.level <= headers:peek().level do
			headers:pop(1)
			closingTags = closingTags .. "</div>"
		end
		headers:push(h)
		return { closingTags .. "<div type='chapter'><head>", pandoc.Inlines(h.content), "</head>" }
	else
		headers:push(h)
		return { "<div type='chapter'><head>", pandoc.Inlines(h.content), "</head>" }
	end
end
