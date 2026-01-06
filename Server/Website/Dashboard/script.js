async function updateWidget() {
    try {
        const response = await fetch ("../api/info");
        if (!response.ok) {
            console.error("Error" + error);
            return;
        }
        const data = await response.json();

        document.getElementById("Battery").textContent = data.battery
        document.getElementById("Battery2").textContent = data.battery
        document.getElementById("Uptime").textContent = data.uptime
        document.getElementById("IP").textContent = data.ip
        document.getElementById("Sessions").textContent = data.sessions
        document.getElementById("Temp").textContent = data.temp
        document.getElementById("CPU-Usage").textContent = data["CPU-Usage"]
        document.getElementById("RAM-Usage").textContent = data["RAM-Usage"]
    
    } catch (error) {
        console.error("Error:" + error)
    }
}

async function blink() {
    document.getElementById("blink").textContent = " "
    await new Promise(r => setTimeout(r, 500));
    document.getElementById("blink").textContent = "█"
}

updateWidget()

setInterval(blink, 1000)

setInterval(updateWidget, 30000)