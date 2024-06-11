function Reader(input)
	local document

	document = pandoc.Pandoc(pandoc.structure.make_sections({
		pandoc.Str("first section"),
		pandoc.Str("second section"),
		pandoc.Str("third section"),
	}))

	return document
end
