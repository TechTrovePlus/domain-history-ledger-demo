let lastSearchedDomain = null;

const searchBtn = document.getElementById("searchBtn");
const timelineBtn = document.getElementById("timelineBtn");
const resultDiv = document.getElementById("result");
const timelineDiv = document.getElementById("timeline");

async function searchDomain() {
  const domain = document.getElementById("domainInput").value.trim();
  const analysisConsole = document.getElementById("analysisConsole");
  const consoleLogs = document.getElementById("consoleLogs");
  const analysisStatus = document.getElementById("analysisStatus");

  if (!domain) {
    resultDiv.innerHTML = `<div class="result UNKNOWN">Please enter a domain to search.</div>`;
    return;
  }

  lastSearchedDomain = domain;

  // Reset UI
  resultDiv.innerHTML = "";
  timelineDiv.innerHTML = "";
  timelineBtn.style.display = "none";
  searchBtn.disabled = true;

  // Setup Console
  analysisConsole.style.display = "block";
  consoleLogs.innerHTML = "";
  analysisStatus.innerText = "Initializing scan...";

  try {
    const response = await fetch(
      `http://localhost:5000/search?domain=${domain}`
    );
    const data = await response.json();

    // Stream logs with a small delay for visual effect
    if (data.processing_logs) {
      for (const log of data.processing_logs) {
        const logEl = document.createElement("div");
        logEl.className = `log-entry ${log.status}`;
        logEl.innerHTML = `<span class="log-icon"></span> ${log.step}`;
        consoleLogs.appendChild(logEl);

        // Auto-scroll console
        consoleLogs.scrollTop = consoleLogs.scrollHeight;

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 400));
      }
    }

    analysisStatus.innerText = "Scan complete.";
    await new Promise(resolve => setTimeout(resolve, 300));

    resultDiv.className = `result ${data.status}`;

    let proofHtml = "";
    if (data.blockchain_proof) {
      proofHtml = `
        <div class="proof-card">
          <strong>Blockchain Verification</strong>
          <div><span class="label">Integrity Hash:</span> ${data.blockchain_proof.integrity_hash}</div>
          <div style="margin-top: 8px;"><span class="label">Transaction ID:</span> ${data.blockchain_proof.transaction}</div>
        </div>
      `;
    }

    resultDiv.innerHTML = `
      <div class="status-badge">${data.status}</div>
      <div class="label">Current Status</div>
      <div class="value">${data.status}</div>
      
      <div class="label">Analysis Reason</div>
      <div class="value" style="font-size: 1rem; color: var(--text-muted);">${data.reason}</div>
      
      ${proofHtml}
    `;

    timelineBtn.style.display = "block";

  } catch (err) {
    analysisStatus.innerText = "Scan failed.";
    resultDiv.innerHTML = `<div class="result RED">Error connecting to the DNS Guard backend. Please ensure the server is running.</div>`;
  } finally {
    searchBtn.disabled = false;
  }
}

async function loadTimeline() {
  if (!lastSearchedDomain) return;

  timelineDiv.innerHTML = `<div class="loading"><div class="spinner"></div></div>`;
  timelineBtn.disabled = true;

  try {
    const response = await fetch(
      `http://localhost:5000/timeline?domain=${lastSearchedDomain}`
    );
    const data = await response.json();

    if (!data.events || data.events.length === 0) {
      timelineDiv.innerHTML = `<div class="result UNKNOWN">No historical events recorded for this domain.</div>`;
      return;
    }

    timelineDiv.innerHTML = `<h3 class="timeline-header">Domain History Ledger</h3>`;

    data.events.forEach(event => {
      let proofHtml = "";
      if (event.blockchain_proof) {
        proofHtml = `
          <div class="proof-card">
            <strong>Block Proof</strong>
            <div style="font-size: 0.75rem; overflow-wrap: break-word;">${event.blockchain_proof.integrity_hash}</div>
          </div>
        `;
      }

      timelineDiv.innerHTML += `
        <div class="timeline-event ${event.event_type}">
          <div class="event-date">${event.date}</div>
          <div class="event-type">${event.event_type.replace('_', ' ')}</div>
          <div class="event-desc">${event.description}</div>
          ${proofHtml}
        </div>
      `;
    });

  } catch (err) {
    timelineDiv.innerHTML = `<div class="result RED">Failed to retrieve timeline data.</div>`;
  } finally {
    timelineBtn.disabled = false;
    timelineBtn.style.display = "none"; // Hide after loading to keep UI clean, or keep it if you want to allow refresh
  }
}

// Allow Enter key to trigger search
document.getElementById("domainInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    searchDomain();
  }
});
