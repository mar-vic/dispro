local logging = require("logging")

local function get_document_id(lan, pub_date)
	return lan .. pub_date .. pandoc.Inlines(tostring(math.random(1000)))
end

local function get_time_slot(pub_date)
	if pub_date < 1859 then
		return "T1"
	elseif pub_date < 1879 then
		return "T2"
	elseif pub_date < 1899 then
		return "T3"
	else
		return "T4"
	end
end

-- TODO: write functions to calculate word count, page count and size and add calculate values to metadata
-- word count implementation: https://pandoc.org/lua-filters.html#counting-words-in-a-document

function Meta(m)
	m.documentId = get_document_id(m.language, m.srced.pub_date)

	local year = tonumber(pandoc.utils.stringify(m.srced.pub_date))
	if year then
		m.time_slot = get_time_slot(year)
	end
	return m
end
