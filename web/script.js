let config = {
    user: localStorage.getItem('aio_user') || "",
    key: localStorage.getItem('aio_key') || ""
};

window.addEventListener('load', function () {
    initGauges();
    updateClock();
    setInterval(updateClock, 1000);

    if (config.user) document.getElementById('aio_user').value = config.user;
    if (config.key) document.getElementById('aio_key').value = config.key;

    if (config.user && config.key) {
        pollAdafruit();
        setInterval(pollAdafruit, 5000);
    }
});

function updateClock() {
    const now = new Date();
    const time = now.toLocaleTimeString('vi-VN', { hour12: false });
    const date = now.toLocaleDateString('vi-VN');
    const clockEl = document.getElementById('digital-clock');
    if (clockEl) clockEl.innerText = `${time} | ${date}`;
}

// ==================== ĐIỀU KHIỂN QUẠT ====================
function updateFanLabel(val) {
    document.getElementById('fan-speed-text').innerText = val;
}

async function sendFanSpeed(speed) {
    if (!config.user || !config.key) return alert("Error! Please try again");
    
    // Cập nhật giao diện ngay lập tức
    updateFanUI(speed);

    try {
        await fetch(`https://io.adafruit.com/api/v2/${config.user}/feeds/fan-speed/data`, {
            method: 'POST',
            headers: { "X-AIO-Key": config.key, "Content-Type": "application/json" },
            body: JSON.stringify({ value: speed })
        });
        console.log("Đã gửi tốc độ quạt:", speed);
    } catch (e) {
        console.error("Lỗi gửi lệnh quạt", e);
    }
}

function updateFanUI(speed) {
    const val = parseInt(speed);
    document.getElementById('fan-slider').value = val;
    document.getElementById('fan-speed-text').innerText = val;
    
    const icon = document.getElementById('fan-icon');
    if (val > 0) {
        icon.classList.add('fan-on');
        // Tốc độ quay nhanh chậm dựa trên giá trị slider
        const duration = 2 - (val / 100 * 1.8); 
        icon.style.animationDuration = duration + "s";
    } else {
        icon.classList.remove('fan-on');
    }
}

// ==================== LẤY DỮ LIỆU CLOUD ====================
async function pollAdafruit() {
    if (!config.user || !config.key) return;

    // Thêm fan-speed vào danh sách polling
    const feeds = ["temperature", "humidity", "light", "fan-speed"];
    for (let feed of feeds) {
        try {
            const url = `https://io.adafruit.com/api/v2/${config.user}/feeds/${feed}/data/last`;
            const response = await fetch(url, { headers: { "X-AIO-Key": config.key } });
            
            if (response.ok) {
                const data = await response.json();
                const val = parseFloat(data.value);
                
                if (feed === "temperature") window.gaugeTemp.refresh(val);
                if (feed === "humidity") window.gaugeHumi.refresh(val);
                if (feed === "light") window.gaugeLight.refresh(val);
                if (feed === "fan-speed") updateFanUI(val); // Cập nhật slider quạt từ Cloud
            }
        } catch (e) { console.error("Lỗi fetch feed " + feed, e); }
    }
}

// --- Các phần khác (Settings, Relay, Gauges) giữ nguyên logic cũ của bạn ---

document.getElementById('settingsForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const newUser = document.getElementById('aio_user').value.trim();
    const newKey = document.getElementById('aio_key').value.trim();
    localStorage.setItem('aio_user', newUser);
    localStorage.setItem('aio_key', newKey);
    config.user = newUser; config.key = newKey;
    alert("✅ Đã lưu cấu hình!");
    pollAdafruit();
});

function initGauges() {
    const commonConfig = { min: 0, max: 100, donut: true, pointer: false, gaugeWidthScale: 0.2, gaugeColor: "#f0f0f0", counter: true };
    window.gaugeTemp = new JustGage({ id: "gauge_temp", value: 0, ...commonConfig, symbol: "°C", levelColors: ["#00BCD4", "#FFC107", "#F44336"] });
    window.gaugeHumi = new JustGage({ id: "gauge_humi", value: 0, ...commonConfig, symbol: "%", levelColors: ["#E1F5FE", "#42A5F5", "#01579B"] });
    window.gaugeLight = new JustGage({ id: "gauge_light", value: 0, ...commonConfig, symbol: "%", levelColors: ["#333333", "#FFD700", "#FFFF00"] });
}

function showSection(id, event) {
    document.querySelectorAll('.section').forEach(sec => sec.style.display = 'none');
    const target = document.getElementById(id);
    if (target) target.style.display = (id === 'settings') ? 'flex' : 'block';
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    if (event) event.currentTarget.classList.add('active');
}

let relayList = [];
function openAddRelayDialog() { document.getElementById('addRelayDialog').style.display = 'flex'; }
function closeAddRelayDialog() { document.getElementById('addRelayDialog').style.display = 'none'; }
function saveRelay() {
    const name = document.getElementById('relayName').value;
    const gpio = document.getElementById('relayGPIO').value;
    if (name && gpio) {
        relayList.push({ id: Date.now(), name, gpio, state: false });
        renderRelays();
        closeAddRelayDialog();
    }
}
function renderRelays() {
    const container = document.getElementById('relayContainer');
    if (!container) return;
    container.innerHTML = "";
    relayList.forEach(r => {
        const card = document.createElement('div');
        card.className = 'device-card';
        card.innerHTML = `<h3>${r.name}</h3><p>GPIO: ${r.gpio}</p>
            <button class="toggle-btn ${r.state ? 'on' : ''}" onclick="toggleRelay(${r.id})">${r.state ? 'ON' : 'OFF'}</button>`;
        container.appendChild(card);
    });
}
async function toggleRelay(id) {
    const relay = relayList.find(r => r.id === id);
    if (relay && config.user && config.key) {
        relay.state = !relay.state;
        const val = relay.state ? "ON" : "OFF";
        try {
            await fetch(`https://io.adafruit.com/api/v2/${config.user}/feeds/relay/data`, {
                method: 'POST',
                headers: { "X-AIO-Key": config.key, "Content-Type": "application/json" },
                body: JSON.stringify({ value: val })
            });
            renderRelays();
        } catch (e) { console.error("Lỗi điều khiển relay", e); }
    }
}