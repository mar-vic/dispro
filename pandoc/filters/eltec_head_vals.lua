-- pandoc filter for generating some metadata (ie, document id, wordcount and timeslot) in eltec headers

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

local function get_size(wc)
	if wc < 50000 then
		return "short"
	elseif wc < 100000 then
		return "medium"
	else
		return "long"
	end
end

words = 0

wordcount = {
	Str = function(el)
		-- we don't count a word if it's entirely punctuation:
		if el.text:match("%P") then
			words = words + 1
		end
	end,

	Code = function(el)
		_, n = el.text:gsub("%S+", "")
		words = words + n
	end,

	CodeBlock = function(el)
		_, n = el.text:gsub("%S+", "")
		words = words + n
	end,
}

function Pandoc(el)
	if not el.meta.language then
		local lan = "slk"
	end

	if not el.meta.srced or not el.meta.srced.pub_date then
		local pub_date = ""
	end

	el.meta.documentId = get_document_id(el.meta.language, el.meta.srced.pub_date)

	-- skip metadata, just count body:
	el.blocks:walk(wordcount)
	el.meta.words = tostring(words)

  local year
  -- TODO: the value should be used only in case, if there is no firsted.pub_date
  if el.meta.firsted and el.meta.firsted.pub_date then
    year = tonumber(pandoc.utils.stringify(el.meta.firsted.pub_date ))
  else
    year = tonumber(pandoc.utils.stringify(el.meta.srced.pub_date))
  end
	if year then
		el.meta.time_slot = get_time_slot(year)
	end

	el.meta.size = get_size(words)

	el.meta.creation_date = os.date("%Y-%m-%d")

	-- logging.temp(el)
	return el
end
