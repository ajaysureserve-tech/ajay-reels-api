const API_KEY = 'AIzaSyBp9tuB1C-QYCSSGHgLu809PywUaXGGazk';

// Categories Data
const appCategories = {
    "Social Media": [{name: "Facebook", icon: "fab fa-facebook", color: "#1877f2"}],
    "Business & Finance": [{name: "Paytm", icon: "fas fa-wallet", color: "#00b9f1"}],
    "Dating": [{name: "Tinder", icon: "fas fa-heart", color: "#ff4458"}],
    "Health & Fitness": [{name: "HealthifyMe", icon: "fas fa-leaf", color: "#ff9800"}]
};

function handleSearch(e) {
    if (e.key === 'Enter') searchVideos();
}

function handleIconClick(query) {
    document.getElementById('ytQuery').value = query;
    searchVideos();
}

async function searchVideos() {
    let q = document.getElementById('ytQuery').value;
    document.getElementById('homeContent').style.display = 'none';
    const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q=${q}&type=video&key=${API_KEY}`);
    const data = await response.json();
    renderVideos(data.items);
}

function openAllApps() {
    const list = document.getElementById('categoryList');
    list.innerHTML = Object.keys(appCategories).map(cat => `
        <div style="margin-bottom:20px;">
            <h4 style="color:#888; margin-bottom:10px;">${cat}</h4>
            <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px;">
                ${appCategories[cat].map(app => `
                    <div style="text-align:center; font-size:12px;">
                        <i class="${app.icon}" style="font-size:25px; color:${app.color}; display:block;"></i>
                        <span>${app.name}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
    document.getElementById('appsModal').style.display = 'block';
}

function closeAllApps() { document.getElementById('appsModal').style.display = 'none'; }
