function copyToClipboard() {
    // Get the shortened URL text
    const shortUrlText = document.getElementById("short-url").innerText;

    // Create a temporary textarea element to copy from
    const tempInput = document.createElement("textarea");
    tempInput.value = shortUrlText;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    // Optionally provide user feedback
    alert("Copied to clipboard: " + shortUrlText);
}