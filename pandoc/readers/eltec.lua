local logging = require("logging")
local inspect = require("inspect")
local SLAXML = require("slaxml")

function generate_pandoc_ast(xml)
	-- A stack used to construct pandoc's AST
	local index = 0
	local stack = {}

	-- pushes an item on top of the stack
	local push = function(item)
		index = index + 1
		stack[index] = item
	end

	-- removes the item from top of the stack
	local pop = function()
		local popped = table.remove(stack, index)
		index = index - 1
		return popped
	end

	-- gets the item on top of the stack
	local peek = function()
		return stack[index]
	end

	-- gets a parent of the item on top of the stack
	local peekAhead = function(lvl)
		if not lvl then
			return stack[index - 1]
		end
		if index - lvl < 1 then
			lvl = 1
		end
		return stack[index - lvl]
	end

	-- tests wether a tag is present somewhere in stack
	-- (i.e., if a tag on top is a child of given tag
	local isInStack = function(tagName)
		for _, item in ipairs(stack) do
			if item.tagName == tagName then
				return true
			end
		end
		return false
	end

	local inspectStack = function(message, log_level)
		if not message then
			message = "inspecting stack"
		else
			message = "inspecting stack (" .. message .. ")"
		end
		if not log_level or not logging[log_level] then
			log_level = "temp"
		end

		logging[log_level]("\n\n\n<<" .. string.upper(message) .. ">>")
		for i = index, 1, -1 do
			logging[log_level](
				"\n\n  STACK LVL " .. i .. " (<" .. string.upper(stack[i].tagName) .. ">)",
				stack[i].panFrag
			)
		end
	end

	local splitCamelCase = function(s)
		local words = {}
		while true do
			local pos = string.find(string.sub(s, 2), "%u")
			if pos then
				table.insert(words, string.sub(s, 1, pos))
				s = string.sub(s, pos + 1)
			else
				table.insert(words, s)
				break
			end
		end
		s = ""
		for i, val in pairs(words) do
			if i > 1 then
				s = s .. " " .. val
			else
				s = s .. val
			end
		end
		return string.upper(string.sub(s, 1, 1)) .. string.sub(s, 2)
	end

	local sourceDescTags = {
		author = true,
		title = true,
		publisher = true,
		pubPlace = true,
		date = true,
	}

	-- For storing the resulting pandoc AST
	local document

	-- For indexing notes
	local noteCounter = 0

	local headLvl = 1

	-- Table with parsing instructions for relevant elements encountered the eltec file
	local parsingInstructions = {
		TEI = {
			onstart = function()
				-- Create blocks to store the elements of the whole document
				-- and push them onto the stack
				push({ tagName = "TEI", panFrag = pandoc.Blocks({}) })
			end,
			onclose = function()
				--
				document = pandoc.Pandoc(pop().panFrag)
			end,
		},
		sourceDesc = {
			onstart = function()
				push({ tagName = "sourceDesc", panFrag = pandoc.Blocks({}) })
			end,
			onclose = function()
				-- Pops the paragraphs containing source description and encloses them
				-- within horizontal rules
				local paragraphs = pop().panFrag
				pandoc.List.insert(paragraphs, 1, pandoc.HorizontalRule())
				pandoc.List.insert(paragraphs, pandoc.HorizontalRule())

				-- adds paragraphs to the document (i.e., blocks representing <TEI>)
				pandoc.List.extend(peek().panFrag, paragraphs)
			end,
		},
		bibl = {
			onstart = function()
				if peek().tagName == "sourceDesc" then
					push({ tagName = "bibl", panFrag = pandoc.Blocks({}) })
				end
			end,
			onclose = function()
				local paragraphs = pop().panFrag
				pandoc.List.extend(peek().panFrag, paragraphs)
			end,
			onattribute = function(name, value)
				if name == "type" then
					-- pandoc.List.insert(peek().panFrag, pandoc.Strong(string.upper(value) .. ":"))
					pandoc.List.insert(peek().panFrag, pandoc.Strong(string.upper(splitCamelCase(value))))
				end
			end,
		},
		author = {
			onstart = function()
				if peek().tagName == "bibl" then
					push({
						tagName = "author",
						panFrag = pandoc.Para({
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Strong("Author:"),
						}),
					})
				end
			end,
			onclose = function()
				if peek().tagName == "author" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
			ontext = function(text)
				if isInStack("bibl") and peek().tagName == "author" then
					pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
				end
			end,
		},
		title = {
			onstart = function()
				if peek().tagName == "bibl" then
					push({
						tagName = "title",
						panFrag = pandoc.Para({
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Strong("Title:"),
						}),
					})
				end
			end,
			onclose = function()
				if peek().tagName == "title" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
			ontext = function(text)
				if isInStack("bibl") and peek().tagName == "title" then
					pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
				end
			end,
		},
		publisher = {
			onstart = function()
				if peek().tagName == "bibl" then
					push({
						tagName = "publisher",
						panFrag = pandoc.Para({
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Strong("Publisher:"),
						}),
					})
				end
			end,
			onclose = function()
				if peek().tagName == "publisher" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
			ontext = function(text)
				if isInStack("bibl") and peek().tagName == "publisher" then
					pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
				end
			end,
		},
		pubPlace = {
			onstart = function()
				if peek().tagName == "bibl" then
					push({
						tagName = "pubPlace",
						panFrag = pandoc.Para({
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Strong("Publication place:"),
						}),
					})
				end
			end,
			onclose = function()
				if peek().tagName == "pubPlace" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
			ontext = function(text)
				if isInStack("bibl") and peek().tagName == "pubPlace" then
					pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
				end
			end,
		},
		date = {
			onstart = function()
				if peek().tagName == "bibl" then
					push({
						tagName = "date",
						panFrag = pandoc.Para({
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Space(),
							pandoc.Strong("Publication date:"),
						}),
					})
				end
			end,
			onclose = function()
				if peek().tagName == "date" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
			ontext = function(text)
				if isInStack("bibl") and peek().tagName == "date" then
					pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
				end
			end,
		},
		text = {
			onstart = function()
				push({ tagName = "text", panFrag = pandoc.Blocks({}) })
			end,
			onclose = function()
				if peek().tagName == "text" then
					local blocks = pop().panFrag
					pandoc.List.extend(peek().panFrag, blocks)
				end
			end,
		},
		front = {
			onstart = function()
				push({ tagName = "front", panFrag = pandoc.Blocks({}) })
			end,
			onclose = function()
				if peek().tagName == "front" then
					local blocks = pop().panFrag
					pandoc.List.extend(peek().panFrag, blocks)
				end
			end,
		},
		body = {
			onstart = function()
				push({ tagName = "body", panFrag = pandoc.Blocks({}) })
			end,
			onclose = function()
				if peek().tagName == "body" then
					local blocks = pop().panFrag
					pandoc.List.extend(peek().panFrag, blocks)
				end
			end,
		},
		back = {
			onstart = function()
				push({ tagName = "back", panFrag = pandoc.Blocks({}) })
			end,
			onclose = function()
				if peek().tagName == "back" then
					local blocks = pop().panFrag
					pandoc.List.extend(peek().panFrag, blocks)
				end
			end,
		},
		p = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "p", panFrag = pandoc.Para(pandoc.Str("")) })
				end
			end,
			onclose = function()
				if peek().tagName == "p" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
			ontext = function(text)
				if peek().tagName == "p" then
					if not peek().panFrag.content[2] and peek().panFrag.content[1] == pandoc.Str("") then
						-- If no content was added to paragraph yet
						peek().panFrag.content[1] = pandoc.Str(text)
					else
						-- all addition content is processed here
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
					end
				end
			end,
		},
		emph = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "emph", panFrag = pandoc.Emph("") })
				end
			end,
			onclose = function()
				if peek().tagName == "emph" then
					local emphasizedContent = pop().panFrag
					if
						emphasizedContent
						and peek().panFrag.content[2]
						and peek().panFrag.content[1] == pandoc.Str("")
					then
						-- If no content was added to the block yet
						peek().panFrag.content[2] = emphasizedContent
					else
						-- all additional content is processed here
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" "))
						pandoc.List.insert(peek().panFrag.content, emphasizedContent)
					end
				end
			end,
			ontext = function(text)
				if peek().tagName == "emph" then
					if not peek().panFrag.content[2] and not peek().panFrag.content[1] then
						peek().panFrag.content[1] = pandoc.Str(text)
					else
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
					end
				end
			end,
		},
		hi = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "hi", panFrag = pandoc.Emph("") })
				end
			end,
			onclose = function()
				if peek().tagName == "hi" then
					local emphasizedContent = pop().panFrag
					if
						emphasizedContent
						and peek().panFrag.content[2]
						and peek().panFrag.content[1] == pandoc.Str("")
					then
						-- If no content was added to the block yet
						peek().panFrag.content[2] = emphasizedContent
					else
						-- all additional content is processed here
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" "))
						pandoc.List.insert(peek().panFrag.content, emphasizedContent)
					end
				end
			end,
			ontext = function(text)
				if peek().tagName == "hi" then
					if not peek().panFrag.content[2] and not peek().panFrag.content[1] then
						peek().panFrag.content[1] = pandoc.Str(text)
					else
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
					end
				end
			end,
		},
		foreign = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "foreign", panFrag = pandoc.Emph("") })
				end
			end,
			onclose = function()
				if peek().tagName == "foreign" then
					local emphasizedContent = pop().panFrag
					if
						emphasizedContent
						and peek().panFrag.content[2]
						and peek().panFrag.content[1] == pandoc.Str("")
					then
						-- If no content was added to the block yet
						peek().panFrag.content[2] = emphasizedContent
					else
						-- all additional content is processed here
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" "))
						pandoc.List.insert(peek().panFrag.content, emphasizedContent)
					end
				end
			end,
			ontext = function(text)
				if peek().tagName == "foreign" then
					if not peek().panFrag.content[2] and not peek().panFrag.content[1] then
						peek().panFrag.content[1] = pandoc.Str(text)
					else
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
					end
				end
			end,
		},
		milestone = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "milestone", panFrag = pandoc.Para(pandoc.Str("* * * *")) })
				end
			end,
			onclose = function()
				if peek().tagName == "milestone" then
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, paragraph)
					end
				end
			end,
		},
		gap = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "gap", panFrag = pandoc.Para(pandoc.Str("")) })
				end
			end,
			onattribute = function(name, value)
				if name == "unit" then
					peek().panFrag.content[1] = pandoc.Str(
						"A material ("
							.. value
							.. ") has been omitted in a transcription, whether for editorial reasons, as part of sampling practice, or because the material is illegible, invisible, or inaudible"
					)
				end
			end,
			onclose = function()
				if peek().tagName == "gap" then
					if peek().panFrag.content[1] == pandoc.Str("") then
						peek().panFrag.content[1] = pandoc.Strong(
							"A material has been omitted in a transcription, whether for editorial reasons, as part of sampling practice, or because the material is illegible, invisible, or inaudible"
						)
					end
					local paragraph = pop().panFrag
					if paragraph then
						pandoc.List.insert(peek().panFrag, pandoc.HorizontalRule())
						pandoc.List.insert(peek().panFrag, paragraph)
						pandoc.List.insert(peek().panFrag, pandoc.HorizontalRule())
					end
				end
			end,
		},
		div = {
			onstart = function()
				if isInStack("body") then
					headLvl = headLvl + 1
				end
				if isInStack("back") then
					push({ tagName = "div" })
				end
			end,
			onattribute = function(name, value)
				if isInStack("back") and peek().tagName == "div" and name == "type" and value == "notes" then
					peek().panFrag = pandoc.OrderedList({})
				end
			end,
			onclose = function()
				if isInStack("body") then
					headLvl = headLvl - 1
				end
				if peek().tagName == "div" then
					local panFrag = pop().panFrag
					if panFrag then
						pandoc.List.insert(peek().panFrag, pandoc.Header(2, "Authorial Notes"))
						pandoc.List.insert(peek().panFrag, panFrag)
					end
				end
			end,
		},
		head = {
			onstart = function()
				if isInStack("text") then
					push({ tagName = "head", panFrag = pandoc.Header(headLvl, pandoc.Str("")) })
				end
			end,
			ontext = function(text)
				if peek().tagName == "head" then
					if not peek().panFrag.content[2] and peek().panFrag.content[1] == pandoc.Str("") then
						-- If no content was added to paragraph yet
						peek().panFrag.content[1] = pandoc.Str(text)
					else
						-- all addition contentl is processed here
						pandoc.List.insert(peek().panFrag.content, pandoc.Str(" " .. text))
					end
				end
			end,
			onclose = function()
				if peek().tagName == "head" then
					local heading = pop().panFrag
					if heading then
						pandoc.List.insert(peek().panFrag, heading)
					end
				end
			end,
		},
		ref = {
			onstart = function()
				noteCounter = noteCounter + 1
			end,
			onclose = function()
				pandoc.List.insert(peek().panFrag.content, pandoc.Superscript(pandoc.Str(noteCounter)))
			end,
		},
		note = {
			onstart = function()
				if isInStack("back") and peek().tagName == "div" and peek().panFrag then
					push({ tagName = "note", panFrag = pandoc.Inlines({}) })
				end
			end,
			ontext = function(text)
				if peek().tagName == "note" then
					if not peek().panFrag[1] then
						-- If no content was added to paragraph yet
						peek().panFrag[1] = pandoc.Str(text)
					else
						-- all addition contentl is processed here
						pandoc.List.insert(peek().panFrag, pandoc.Str(" " .. text))
					end
				end
			end,
			onclose = function()
				if peek().tagName == "note" then
					local note = pop().panFrag
					pandoc.List.insert(peek().panFrag.content, note)
				end
			end,
		},
	}

	local newParser = SLAXML:parser({
		startElement = function(name, nsUri, nsPrefix)
			if parsingInstructions[name] then
				parsingInstructions[name].onstart()
			end
		end,
		attribute = function(name, value, nsURI, nsPrefix)
			local instructions = parsingInstructions[peek().tagName]
			if instructions and instructions.onattribute then
				instructions.onattribute(name, value)
			end
		end,
		text = function(text, cdata)
			local instructions = parsingInstructions[peek().tagName]
			if instructions and instructions.ontext then
				instructions.ontext(text)
			end
		end,
		closeElement = function(name, nsUri, nsPrefix)
			if parsingInstructions[name] then
				parsingInstructions[name].onclose()
			end
		end,
	})

	-- defining parser behaviour
	local parser = SLAXML:parser({
		startElement = function(name, nsUri, nsPrefix)
			-- Encountering <TEI
			if name == "TEI" then -- When <TEI is encountered do the following
				push({
					tagName = name,
					panFrag = pandoc.Blocks({}),
				})
			elseif name == "sourceDesc" then
				push({ tagName = name, panFrag = pandoc.Blocks({}) })
			-- Encountering <author, <title, <publisher, <pubPlace, <date within <sourceDesc>
			elseif sourceDescTags[name] and peek().tagName == "sourceDesc" then
				push({ tagName = name })
			elseif name == "text" then
				push({
					tagName = name,
					panFrag = pandoc.Blocks({}),
				})
			-- Encountering <p, <head or <l within <text>
			elseif isInStack("text") and (name == "p" or name == "head" or name == "l") then
				push({ tagName = name })
			elseif isInStack("text") and name == "milestone" then
				pandoc.List.insert(peek().panFrag, pandoc.Para(pandoc.Str("* * * * *")))
			elseif isInStack("text") and name == "ref" then
				noteCounter = noteCounter + 1
				pandoc.List.insert(peek().panFrag.content, pandoc.Superscript(pandoc.Str(noteCounter)))
			elseif isInStack("text") and name == "back" then
				push({
					tagName = name,
				})
			elseif isInStack("back") and name == "note" then
				top = peek()
				if not top.panFrag then
					top.panFrag = pandoc.OrderedList({})
				end
				push({
					tagName = name,
				})
			end
		end,

		text = function(text, cdata) -- extracts text encountered within specified tag
			-- Integrating the text into the item on top of the stack

			-- Just human readable translations of tags wihtin <sourceDesc
			niceSrcDescTagNames = {
				author = "Author",
				title = "Title",
				publisher = "Publisher",
				pubPlace = "Publishing place",
				date = "Date of publication",
			}

			local top = peek()

			-- Encountering text within <author, <title, <publisher, <pubPlace, <date
			if isInStack("sourceDesc") and sourceDescTags[top.tagName] then
				top.panFrag = pandoc.Inlines({
					pandoc.Strong(niceSrcDescTagNames[top.tagName] .. ":"),
					pandoc.Str(" " .. text),
				})
			-- Encountering text within <p>'s  or <l>'s within <text>
			elseif isInStack("text") and (top.tagName == "p" or top.tagName == "l") then
				if not top.panFrag then
					top.panFrag = pandoc.Para(text)
				else
					pandoc.List.insert(top.panFrag.content, pandoc.Space())
					pandoc.List.insert(top.panFrag.content, text)
				end
			-- Encountering text within <head>'s
			elseif isInStack("text") and top.tagName == "head" then
				top.panFrag = pandoc.Header(1, text)
			elseif isInStack("text") and top.tagName == "note" then
				if not top.panFrag then
					top.panFrag = pandoc.Inlines({
						pandoc.Str(text),
					})
				else
					pandoc.List.insert(top.panFrag.content, pandoc.Space())
					pandoc.List.insert(top.panFrag.content, text)
				end
				pandoc.List.insert(top.panFrag, text)
			end
		end,

		closeElement = function(name, nsURI)
			-- Integrating sourceDesc elements
			if sourceDescTags[name] and peekAhead() and peekAhead().tagName == "sourceDesc" then
				-- pops the stack and creates the paragraph
				local p = pandoc.Para(pop().panFrag)

				-- adds the paragraph to the item added to the stack previously
				-- (i.e., the representation of sourceDesc)
				pandoc.List.insert(peek().panFrag, p)
			-- Integrating rest of the elements
			elseif name == "sourceDesc" then
				-- Creates blocks of paragraphs presenting data about the source
				local blocks = pandoc.Blocks(pop().panFrag)
				pandoc.List.insert(blocks, 1, pandoc.HorizontalRule())
				pandoc.List.insert(blocks, pandoc.HorizontalRule())

				-- adds paragraphs to the item added to the stack previously
				-- (i.e., the represention of TEI element)
				pandoc.List.extend(peek().panFrag, blocks)
			elseif isInStack("text") and name == "p" and peek().tagName == "p" then
				local para = pop().panFrag
				if not para then
					para = pandoc.Para(pandoc.Str(""))
				end
				pandoc.List.extend(peek().panFrag, pandoc.Blocks({ para }))
			elseif isInStack("text") and name == "l" and peek().tagName == "l" then
				local para = pop().panFrag
				if not para then
					para = pandoc.Para(pandoc.Str(""))
				end
				pandoc.List.extend(peek().panFrag, pandoc.Blocks({ para }))
			elseif isInStack("text") and name == "head" and peek().tagName == "head" then
				local para = pop().panFrag
				if not para then
					para = pandoc.Para(pandoc.Str(""))
				end
				pandoc.List.extend(peek().panFrag, pandoc.Blocks({ para }))
			elseif name == "note" and peek().tagName == "note" then
				local note = pop().panFrag
				if note then
					pandoc.List.insert(peek().panFrag.content, note)
				end
			elseif name == "back" and peek().tagName == "back" then
				local notes = pop().panFrag
				if notes then
					pandoc.List.insert(peek().panFrag, pandoc.Header(1, pandoc.Str("Notes")))
					pandoc.List.insert(peek().panFrag, notes)
				end
			elseif name == "text" and peek().tagName == "text" then
				local blocks = pop().panFrag
				pandoc.List.extend(peek().panFrag, blocks)
			elseif name == "TEI" then
				document = pandoc.Pandoc(pop().panFrag)
			end
		end,
	})

	-- runs the parser
	newParser:parse(xml, { stripWhitespace = true })

	return document
end

function Reader(input)
	-- local ws = splitCamelCase("")
	-- print(ws)
	local document = generate_pandoc_ast(tostring(input))

	return document
end
