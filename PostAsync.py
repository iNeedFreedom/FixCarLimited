import fetch from "node-fetch";

app.post("/roblox", async (req, res) => {
  const { left } = req.body;
  print(
  // Example: update file in GitHub repo
  const response = await fetch("https://github.com/repos/YOURUSER/YOURREPO/contents/data.json", {
    method: "PUT",
    headers: {
      "Authorization": "token YOUR_GITHUB_PAT",
      "Accept": "application/vnd.github.v3+json",
    },
    body: JSON.stringify({
      message: "Update data.json from Roblox",
      content: Buffer.from(JSON.stringify({ HNCTCAR_left: left }, null, 2)).toString("base64"),
      sha: "EXISTING_FILE_SHA"
    }),
  });

  const result = await response.json();
  res.json(result);
});
