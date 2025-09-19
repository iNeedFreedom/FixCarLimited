local lapis = require("lapis")
local app = lapis.Application()

app:post("/roblox", function(self)
  local data = self.params  -- Roblox JSON body will appear here
  print("Got data from Roblox:", require("cjson").encode(data))
  return { json = { status = "ok", received = data } }
end)

return app
