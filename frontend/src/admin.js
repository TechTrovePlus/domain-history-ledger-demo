// admin.js - Management Logic
const currentWaves = { registrar: 1, abuse: 1 };

async function openSidebar(side) {
    const sidebar = side === 'left' ? document.getElementById("sidebarLeft") : document.getElementById("sidebarRight");
    const feedType = side === 'left' ? 'registrar' : 'abuse';

    await switchWave(feedType, currentWaves[feedType]);

    sidebar.classList.add("open");
    document.getElementById("overlay").classList.add("visible");
}

async function switchWave(type, num) {
    currentWaves[type] = num;
    const editor = type === 'registrar' ? document.getElementById("jsonEditorLeft") : document.getElementById("jsonEditorRight");

    // Update Tabs UI
    document.querySelectorAll(`.sidebar.${type === 'registrar' ? 'left' : 'right'} .wave-tab`).forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(`tab_${type}_${num}`).classList.add('active');

    // Fetch current feed data
    try {
        const response = await fetch(`http://localhost:5000/api/feed/${type}/${num}`);
        const data = await response.json();
        editor.value = JSON.stringify(data, null, 2);
    } catch (err) {
        editor.value = "Error loading feed data.";
    }
}

function closeSidebars() {
    document.getElementById("sidebarLeft").classList.remove("open");
    document.getElementById("sidebarRight").classList.remove("open");
    document.getElementById("overlay").classList.remove("visible");
}

async function saveFeed(type) {
    const editor = type === 'registrar' ? document.getElementById("jsonEditorLeft") : document.getElementById("jsonEditorRight");
    const num = currentWaves[type];
    try {
        const data = JSON.parse(editor.value);
        const response = await fetch(`http://localhost:5000/api/feed/${type}/${num}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        alert(result.message);
    } catch (err) {
        alert("Invalid JSON format or Server Error");
    }
}

async function triggerIngest(type) {
    const analysisConsole = document.getElementById("analysisConsole");
    const consoleLogs = document.getElementById("consoleLogs");
    const analysisStatus = document.getElementById("analysisStatus");
    const num = currentWaves[type];
    const waveId = `${type}_${num}`;

    analysisConsole.style.display = "block";
    analysisStatus.innerText = "Processing ingestion cycle...";

    const logEl = document.createElement("div");
    logEl.className = "log-entry info";
    logEl.innerHTML = `<span class="log-icon"></span> Initiating injection for: ${waveId.replace('_', ' ')}...`;
    consoleLogs.appendChild(logEl);

    try {
        const response = await fetch(`http://localhost:5000/api/system/ingest/${waveId}`, { method: 'POST' });
        const result = await response.json();

        if (result.status === "error") throw new Error(result.message);

        const successEl = document.createElement("div");
        successEl.className = "log-entry success";
        successEl.innerHTML = `<span class="log-icon"></span> ${result.message}`;
        consoleLogs.appendChild(successEl);

        closeSidebars();
    } catch (err) {
        const errorEl = document.createElement("div");
        errorEl.className = "log-entry warning";
        errorEl.innerHTML = `<span class="log-icon"></span> Error: ${err.message}`;
        consoleLogs.appendChild(errorEl);
    }
}

async function resetSystem() {
    if (!confirm("Are you sure? This will wipe the entire reputation database. YOU CANNOT UNDO THIS.")) return;

    try {
        const response = await fetch('http://localhost:5000/api/system/reset', { method: 'POST' });
        const result = await response.json();
        alert(result.message);

        // Clear the logs
        const consoleLogs = document.getElementById("consoleLogs");
        if (consoleLogs) consoleLogs.innerHTML = "";

    } catch (err) {
        alert("System reset failed.");
    }
}
