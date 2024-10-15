local logging = require("logging")

function Meta(m)
	if m.date == nil then
		print("Setting date to: " .. os.date("%B %e, %Y"))
		m.date = pandoc.Str(os.date("%B %e, %Y"))
		logging.temp(m)
		return m
	end
end
