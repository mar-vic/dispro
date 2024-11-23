-- pandoc filter for generating some metadata (document id, wordcount and timeslot) in eltec headers

local logging = require("logging")

local notes = {}

function renderNote(el)
	local noteId = "N" .. #notes + 1
	-- table.insert(notes, "<note xml:id='" .. noteId .. "'>" .. pandoc.utils.stringify(el.content) .. "</note>")
	table.insert(notes, { id = noteId, content = pandoc.utils.stringify(el.content) })
end

function Pandoc(el)
  -- logging.temp(el)
	el.blocks:walk({ Note = renderNote })
	-- logging.temp(notes)
	if #notes > 0 then
		el.meta.notes = notes
	end
	return el
end
