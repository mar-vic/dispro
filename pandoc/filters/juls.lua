-- pandoc filter for dealing with juls annotations in .docx files
local logging = require("logging")

local noteContents = nil
local headCleaned = false

function Str(s)
  if s.text == "#POZ#" then
    logging.temp("Poggers, I have encountered a note!!!!!")
    noteContents = ""
    return pandoc.Str("")
  elseif s.text == "#-POZ#" then
    local note = pandoc.Note(noteContents)
    noteContents = nil
    return note
  elseif noteContents then
    noteContents = noteContents .. s.text
    return pandoc.Str("")
  else
    return s
  end
end

function Space(spc)
  if noteContents then
    noteContents = noteContents .. " "
    return pandoc.Str("")
  else
    return spc
  end
end
