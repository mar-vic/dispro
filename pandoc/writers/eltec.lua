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

local function replaceEscapeChars(s)
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

-- Rendering functions for block elements
Writer.Block.BlockQuote = function(bq)
	return { "<quote>", Writer.Blocks(bq.content), "</quote>" }
end

Writer.Block.BulletList = function(bl)
	local listItems = {}
	for idx, item in pairs(bl.content) do
		table.insert(listItems, Writer.Inline("- "))
		table.insert(listItems, Writer.Blocks(item))
		table.insert(listItems, pandoc.layout.cr)
	end
	return listItems
end

Writer.Block.HorizontalRule = function(hr)
	return { "<milestone unit='subchapter' rend='stars'/>" }
end

Writer.Block.OrderedList = function(ol)
	print("Encountered a ordered list")
	logging.temp(ol)
	local listItems = {}
	for idx, item in pairs(ol.content) do
		table.insert(listItems, Writer.Inline(idx .. ". "))
		table.insert(listItems, Writer.Blocks(item))
		table.insert(listItems, pandoc.layout.cr)
	end
	return listItems
end

Writer.Block.Para = function(p)
	return { "<p>", Writer.Inlines(p.content), "</p>" }
end

Writer.Block.Plain = function(p)
	return { Writer.Inlines(p.content) }
end

Writer.Block.Header = function(h)
	return { "<head>", Writer.Inlines(h.content), "</head>" }
end

Writer.Block.CodeBlock = function(cb)
	return { "<p>", cb.text, "</p>" }
end

-- Rendering functions for inline elements
Writer.Inline.Emph = function(e)
	return { "<emph>", Writer.Inlines(e.content), "</emph>" }
end

Writer.Inline.Str = function(s)
	return replaceEscapeChars(s.text)
end

Writer.Inline.Strong = function(s)
	return { "<hi>", Writer.Inlines(s.content), "</hi>" }
end

Writer.Inline.RawInline = function(ri)
	return replaceEscapeChars(ri.text)
end

Writer.Inline.SoftBreak = function(sb)
	return ""
end

Writer.Inline.Space = function(s)
	return pandoc.layout.space
end
