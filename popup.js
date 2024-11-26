let isCancelled = false; // Flag to check if the process is cancelled

document.getElementById("downloadImages").addEventListener("click", async () => {
  isCancelled = false; // Reset the flag
  const status = document.getElementById("status");
  status.textContent = "Downloading images...";

  try {
    // Get the URL of the current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const webpageUrl = tab.url;

    // Send POST request to FastAPI server
    const response = await fetch("http://127.0.0.1:8000/download-images/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({ webpage_url: webpageUrl })
    });

    if (isCancelled) {
      status.textContent = "Download cancelled.";
      return;
    }

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = "images.zip";
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      if (!isCancelled) {
        status.textContent = "Download complete!";
      }
    } else {
      status.textContent = "Failed to download images.";
    }
  } catch (error) {
    console.error("Error:", error);
    status.textContent = "Error occurred. Check the console.";
  }
});

document.getElementById("cancelProcess").addEventListener("click", () => {
  isCancelled = true;
  const status = document.getElementById("status");
  status.textContent = "Download process cancelled by user.";
});
