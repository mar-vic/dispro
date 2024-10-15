local logging = require("logging")
local inspect = require("inspect")
local SLAXML = require("slaxdom")
-- local xml2lua = require("xml2lua")
--Uses a handler that converts the XML to a Lua table
-- local handler = require("xmlhandler.tree")

local function generateDocumentId(doc)
	-- @xml:id values must be unique across the corpus, preferably short, and valid XML names
	-- recommended format: xxxyyyyd where xxx is ISO 639-3 language code, yyyy the year of publication, and d an extra digit for disambiguation
	-- logging.temp(doc.meta.printSource.pubDate[1])
	local documentId = pandoc.MetaInlines({ pandoc.MetaString("SLK") })
	if doc.meta.printSource and doc.meta.printSource.pubDate then
		pandoc.List.extend(documentId, doc.meta.printSource.pubDate)
	elseif doc.meta.firstEdition and doc.meta.firstEdition.pubDate then
		pandoc.List.extend(documentId, doc.meta.firstEdition.pubDate)
	else
		pandoc.List.insert(documentId, pandoc.MetaString("0000"))
	end
	pandoc.List.insert(documentId, pandoc.MetaString(os.time()))
	return documentId
end

local function calculateExtent(doc)
	-- page and volume counts are optional; wordcount is mandatory
	-- figures must be supplied without punctuation or spaces
	local wordCount = pandoc.MetaInlines({ pandoc.MetaString("0") })
	local pageCount = pandoc.MetaInlines({ pandoc.MetaString("0") })
	return wordCount, pageCount
end

local function getSizeCategory(doc)
	-- word count excluding header and all markup
	-- short (10-50k) | medium (50-100k) | long (>100k)
	return pandoc.MetaInlines({ pandoc.MetaString("short") })
end

local function getTimeSlot(doc)
	-- date first published as a book
	-- T1 (1840-1859) | T2 (1860-1879) | T3 (1880-1899) | T4 (1900-1920)
	return pandoc.MetaInlines({ pandoc.MetaString("T1") })
end

function Writer(doc, opts)
	-- derived metadata setup
	doc.meta.documentId = generateDocumentId(doc)
	doc.meta.wordCount, doc.meta.pageCount = calculateExtent(doc)
	doc.meta.size = getSizeCategory(doc)
	doc.meta.timeSlot = getTimeSlot(doc)

	local filter = {
		Para = function(p)
			return pandoc.Inlines("xml", "<p></p>")
		end,
	}

	-- print(logging.temp(doc.meta))
	local xml = pandoc.write(doc:walk(filter), nil, opts)
	-- Using SLAXML for xml linting
	-- local dom = SLAXML:dom(xml, { stripWhitespace = true, simple = true })
	-- xml = SLAXML:xml(dom, { indent = 2, sort = true })
	return xml
end

Writer = pandoc.scaffolding.Writer

Writer.Pandoc = function(doc)
	doc.meta.documentId = generateDocumentId(doc)
	doc.meta.wordCount, doc.meta.pageCount = calculateExtent(doc)
	doc.meta.size = getSizeCategory(doc)
	doc.meta.timeSlot = getTimeSlot(doc)

	local d = Writer.Blocks(doc.blocks)

	-- print(logging.temp(doc.meta))

	return d
end

local function sanitized(s)
	s = string.gsub(s, "&", "&amp")

	local escCharsMap = {}
	escCharsMap['"'] = "&quot"
	escCharsMap["'"] = "&apos"
	escCharsMap["<"] = "&lt"
	escCharsMap[">"] = "&gt"

	for escapeC, escapedC in pairs(escCharsMap) do
		s = string.gsub(s, escapeC, escapedC)
	end

	return s
end

authorialNotes = {}

-- Rendering functions for block elements
-- ======================================

Writer.Block.BlockQuote = function(bq)
	return { "<quote>", Writer.Blocks(bq.content), "</quote>" }
end

Writer.Block.BulletList = function(bl)
	local listItems = {}
	table.insert(listItems, "<p>")
	for idx, item in pairs(bl.content) do
		table.insert(listItems, Writer.Inline("- "))
		table.insert(listItems, Writer.Blocks(item))
		table.insert(listItems, pandoc.layout.cr)
	end
	table.insert(listItems, "<p>")
	return listItems
end

Writer.Block.CodeBlock = function(cb)
	return { "<p>", sanitized(cb.text), "</p>" }
end

Writer.Block.DefinitionList = function(dl)
	local definitions = {}
	for i, definition in pairs(dl.content) do
		-- logging.temp(Writer.Inlines(item[1]))
		table.insert(definitions, "<p>")
		table.insert(definitions, Writer.Inlines(definition[1]))
		table.insert(definitions, Writer.Inline(": "))
		for j, definiens in pairs(definition[2]) do
			table.insert(definitions, Writer.Inlines(definiens[1].content))
			if j < #definition[2] then
				table.insert(definitions, Writer.Inline(" / "))
			end
		end
		table.insert(definitions, "</p>")
	end
	return definitions
end

Writer.Block.Div = function(d)
	local type = d.attr.attributes.type
	if type then
		return { "<div type='" .. type .. "'>", Writer.Blocks(d.content), "</div>" }
	end
	return { "<div>", Writer.Blocks(d.content), "</div" }
end

Writer.Block.Figure = function(d)
	return { "<!-- a figure in the original has been omitted--><gap unit='figure'/>" }
end

Writer.Block.Header = function(h)
	return { "<head>", Writer.Inlines(h.content), "</head>" }
end

Writer.Block.HorizontalRule = function(hr)
	return { "<milestone unit='subchapter' rend='stars'/>" }
end

Writer.Block.LineBlock = function(lb)
	local lines = {}
	for idx, line in pairs(lb.content) do
		table.insert(lines, "<l>")
		table.insert(lines, Writer.Inlines(line))
		table.insert(lines, "</l>")
		table.insert(lines, pandoc.layout.cr)
	end
	return lines
end

Writer.Block.OrderedList = function(ol)
	local listItems = {}
	table.insert(listItems, "<p>")
	for idx, item in pairs(ol.content) do
		table.insert(listItems, Writer.Inline(idx .. ". "))
		table.insert(listItems, Writer.Blocks(item))
		table.insert(listItems, pandoc.layout.cr)
	end
	table.insert(listItems, "</p>")
	return listItems
end

Writer.Block.Para = function(p)
	return { "<p>", Writer.Inlines(p.content), "</p>" }
end

Writer.Block.Plain = function(p)
	return { Writer.Inlines(p.content) }
end

Writer.Block.RawBlock = function(rb)
	return { "<p>", "```{=", rb.format, "}", pandoc.layout.cr, sanitized(rb.text), pandoc.layout.cr, "```", "</p>" }
end

Writer.Block.Table = function(t)
	return { "<!-- a table in the original has been omitted--><gap unit='table'/>" }
end

-- Rendering functions for inline elements
-- =======================================

Writer.Inline.Cite = function(c)
	local citations = {}
	table.insert(citations, "<label>")
	for idx, citation in pairs(c.citations) do
		table.insert(
			citations,
			Writer.Inlines(citation.prefix) .. " " .. citation.id .. Writer.Inlines(citation.suffix)
		)
		-- Several citations are seprated by semicolons
		if idx < #c.citations then
			table.insert(citations, ";")
		end
	end
	table.insert(citations, "</label>")
	return citations
end

Writer.Inline.Code = function(c)
	return { "`", sanitized(c.text), "`" }
end

Writer.Inline.Emph = function(e)
	return { "<emph>", Writer.Inlines(e.content), "</emph>" }
end

Writer.Inline.Image = function(i)
	return { "<!-- a picture in the original has been omitted--><gap unit='graphic'/>" }
end

Writer.Inline.LineBreak = function(lb)
	return pandoc.layout.cr
end

Writer.Inline.Link = function(l)
	return Writer.Inlines(l.content)
end

Writer.Inline.Math = function(m)
	return "<!-- math symbols in the original have been omitted--><gap unit='math' />"
end

Writer.Inline.Note = function(l)
	-- TODO: <div type="notes"> rendering according to: https://distantreading.github.io/Training/Budapest/encodingGuide-2.html#(13)
	local noteId = "#N" .. #authorialNotes + 1
	table.insert(authorialNotes, { "<note xml:id='" .. noteId .. "'>", Writer.Blocks(l.content), "</note>" })
	return "<ref target='" .. noteId .. "'/>"
end

Writer.Inline.Quoted = function(q)
	if q.quotetype == "DoubleQuote" then
		return { "“", Writer.Inlines(q.content), "”" }
	else
		return { "‘", Writer.Inlines(q.content), "’" }
	end
end

Writer.Inline.RawInline = function(ri)
	return sanitized(ri.text)
end

Writer.Inline.SmallCaps = function(sc)
	return Writer.Inlines(sc.content)
end

Writer.Inline.SoftBreak = function(sb)
	return ""
end

Writer.Inline.Space = function(s)
	return " "
end

Writer.Inline.SoftBreak = function(sb)
	return ""
end

Writer.Inline.Space = function(s)
	return pandoc.layout.space
end

Writer.Inline.Span = function(s)
	return Writer.Inlines(s.content)
end

Writer.Inline.Str = function(s)
	return sanitized(s.text)
end

Writer.Inline.Strikeout = function(s)
	return { "<hi>", Writer.Inlines(s.content), "</hi>" }
end

Writer.Inline.Strong = function(s)
	return { "<hi>", Writer.Inlines(s.content), "</hi>" }
end

Writer.Inline.Subscript = function(s)
	return { "<hi>", Writer.Inlines(s.content), "</hi>" }
end

Writer.Inline.Superscript = function(s)
	return { "<hi>", Writer.Inlines(s.content), "</hi>" }
end
