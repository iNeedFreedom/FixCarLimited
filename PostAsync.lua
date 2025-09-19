local https = require("ssl.https")
local ltn12 = require("ltn12")
local cjson = require("cjson")
local mime = require("mime") -- for base64 encoding

local token = "BREADTOKEN33" -- your GitHub personal access token
local owner = "iNeedFreedom"
local repo = "FixCarLimited"
local path = "Data.js"

-- Step 1: Fetch current file SHA
local response_body = {}
local _, code = https.request{
    url = "https://api.github.com/repos/"..owner.."/"..repo.."/contents/"..path,
    method = "GET",
    headers = {
        ["Authorization"] = "token " .. token,
        ["User-Agent"] = "Lua-App"
    },
    sink = ltn12.sink.table(response_body)
}

if code ~= 200 then
    print("Failed to fetch file, code:", code)
    print(table.concat(response_body))
    return
end

local fileData = cjson.decode(table.concat(response_body))
local sha = fileData.sha

-- Step 2: Prepare new content
local newData = { CurrentCar = 2 }
local newJson = cjson.encode(newData)
local base64Content = mime.b64(newJson)

local updateBody = cjson.encode({
    message = "Update Data.js from Lua",
    content = base64Content,
    sha = sha
})

-- Step 3: Send PUT request to update file
local updateResponse = {}
local _, updateCode = https.request{
    url = "https://api.github.com/repos/"..owner.."/"..repo.."/contents/"..path,
    method = "PUT",
    headers = {
        ["Authorization"] = "token " .. token,
        ["User-Agent"] = "Lua-App",
        ["Content-Type"] = "application/json",
        ["Content-Length"] = tostring(#updateBody)
    },
    source = ltn12.source.string(updateBody),
    sink = ltn12.sink.table(updateResponse)
}

local lapis = require("lapis")
local app = lapis.Application()

app:post("/roblox", function(self)
  local data = self.params  -- Roblox JSON body will appear here
  print("Got data from Roblox:", require("cjson").encode(data))
  return { json = { status = "ok", received = data } }
end)

return app
