import streamlit as st
import streamlit.components.v1 as components
import json

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Galaxy Maze Explorer",
    page_icon="🌌",
    layout="wide",
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a0033 0%, #0a0014 60%, #000000 100%);
        color: #e0d0ff;
    }
    h1 { 
        color: #c084fc !important; 
        text-shadow: 0 0 20px #7c3aed, 0 0 40px #4c1d95;
        font-family: 'Trebuchet MS', sans-serif;
    }
    /* Styling Sidebar agar senada dengan tema galaksi */
    [data-testid="stSidebar"] {
        background-color: #120022 !important;
        border-right: 1px solid #4c1d95;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR PENGATURAN (Mirip temen kamu)
# =========================================================
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan Simulasi")
    st.markdown("Atur mode dan jalankan animasi labirin di sini.")
    
    # Mode Selector
    st.markdown("### 📍 Mode Klik Peta")
    click_mode = st.radio(
        "Pilih objek yang ingin dipindahkan:",
        ("Start (Astronot)", "Target (UFO)"),
        help="Setelah memilih, klik kotak kosong di peta untuk memindahkannya."
    )
    
    st.markdown("---")
    
    # Tombol Algoritma
    st.markdown("### 🚀 Jalankan Algoritma")
    col1, col2 = st.columns(2)
    with col1:
        btn_bfs = st.button("🔵 BFS", use_container_width=True)
    with col2:
        btn_dfs = st.button("🔴 DFS", use_container_width=True)
        
    st.markdown("---")
    
    # Kontrol Animasi
    st.markdown("### 🎮 Kontrol Animasi")
    col3, col4 = st.columns(2)
    with col3:
        btn_back = st.button("⏮️ Mundur", use_container_width=True)
    with col4:
        btn_forward = st.button("⏭️ Maju", use_container_width=True)
        
    col5, col6 = st.columns(2)
    with col5:
        btn_play = st.button("▶️ Play", use_container_width=True)
    with col6:
        btn_stop = st.button("⏸️ Jeda", use_container_width=True)
        
    btn_reset = st.button("🔄 Ulang Animasi", use_container_width=True)
    
    st.markdown("---")
    
    # Slider Kecepatan
    st.markdown("### ⏱️ Kecepatan Animasi")
    speed_val = st.slider("Pilih kecepatan (ms):", min_value=10, max_value=1000, value=200, step=10)

# =========================================================
# DATA LABIRIN (10x10 / Grid 21x21)
# =========================================================
maze_raw = """
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 1 1 0 1
1 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 1 0 0 0 1
1 1 1 0 1 0 1 1 1 0 1 1 1 0 1 0 1 0 1 1 1
1 0 0 0 1 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 1
1 0 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 0 1
1 0 1 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 1
1 0 1 0 1 1 1 1 1 0 1 1 1 0 1 1 1 0 1 1 1
1 0 0 0 1 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1
1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1 1 1 0 1
1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 1
1 0 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1 0 1
1 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 1 0 1
1 0 1 0 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1
1 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1
1 1 1 0 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1
1 0 0 0 1 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 1
1 0 1 1 1 1 1 0 1 1 1 1 1 0 1 0 1 1 1 1 1
1 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""

rows = [line.strip().split() for line in maze_raw.strip().split("\n")]
maze = [[int(x) for x in row] for row in rows]
maze_json = json.dumps(maze)

# =========================================================
# HTML + JS (UI Labirin & Panel Kanan)
# =========================================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: transparent; /* Transparan agar menyatu dengan Streamlit */
            font-family: 'Trebuchet MS', sans-serif;
            color: #e0d0ff;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding-top: 10px;
        }}
        .main-wrapper {{
            display: flex;
            gap: 20px;
            background: rgba(20, 0, 40, 0.8);
            padding: 20px;
            border-radius: 20px;
            border: 1px solid #7c3aed;
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.4);
        }}
        .left-panel {{ text-align: center; }}
        canvas {{
            background-color: #150025;
            border-radius: 15px;
            border: 2px solid #4c1d95;
            box-shadow: inset 0 0 25px #2a0a4a;
            cursor: crosshair;
        }}
        
        /* CSS UNTUK PANEL KANAN (DATA & KESIMPULAN) */
        .right-panel {{
            width: 320px; 
            background: rgba(40, 10, 80, 0.6);
            padding: 15px;
            border-radius: 15px;
            border: 1px solid #4c1d95;
            font-size: 14px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 520px; 
            overflow-y: auto; 
        }}
        .right-panel::-webkit-scrollbar {{ width: 8px; }}
        .right-panel::-webkit-scrollbar-track {{ background: rgba(0, 0, 0, 0.2); border-radius: 10px; }}
        .right-panel::-webkit-scrollbar-thumb {{ background: #7c3aed; border-radius: 10px; }}
        .right-panel::-webkit-scrollbar-thumb:hover {{ background: #c084fc; }}

        .stat-box {{
            padding: 10px;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
        }}
        .stat-box h4 {{ margin: 0 0 5px 0; }}
        .bfs-color {{ color: #38bdf8; }}
        .dfs-color {{ color: #f472b6; }}
        .legend {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 12px;}}
        .dot {{ width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }}
        
        .desc-box {{
            background: rgba(0, 0, 0, 0.4); 
            padding: 12px; 
            border-radius: 8px;
            font-size: 12px;
            line-height: 1.5;
            border-left: 4px solid #c084fc;
            display: none; 
        }}
        .desc-box h4 {{ margin: 0 0 8px 0; font-size: 13px; }}
        .desc-box b {{ color: #fff; }}
        
        .conclusion-box {{
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid #10b981;
            padding: 12px; 
            border-radius: 8px;
            font-size: 12px;
            line-height: 1.5;
            color: #d1fae5;
            display: none;
        }}
        .conclusion-box h4 {{ margin: 0 0 8px 0; font-size: 13px; color: #10b981; }}
        .conclusion-box ul {{ margin: 5px 0 0 0; padding-left: 18px; }}
        .conclusion-box li {{ margin-bottom: 5px; }}
        
        .instruction {{
            text-align: center; 
            color: #a78bfa; 
            font-style: italic; 
            font-size: 13px;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="main-wrapper">
        <div class="left-panel">
            <canvas id="mazeCanvas" width="500" height="500"></canvas>
            <div class="instruction" style="margin-top: 10px;">
                💡 <b>Mode Aktif:</b> <span id="activeModeText">📍 Start (Astronot)</span>
            </div>
        </div>

        <div class="right-panel">
            <h3 style="margin-top:0; color:#c084fc; text-align:center;">📊 Panel Data</h3>
            
            <div class="stat-box">
                <h4 class="bfs-color">🔵 BFS</h4>
                <div id="bfsStats">Menunggu simulasi...</div>
            </div>

            <div class="stat-box">
                <h4 class="dfs-color">🔴 DFS</h4>
                <div id="dfsStats">Menunggu simulasi...</div>
            </div>

            <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px;">
                <h4 style="margin: 0 0 8px 0; font-size: 13px;">Legenda:</h4>
                <div class="legend"><div class="dot" style="background:#38bdf8;"></div> Jalur Aktif (BFS)</div>
                <div class="legend"><div class="dot" style="background:#f472b6;"></div> Jalur Aktif (DFS)</div>
                <div class="legend"><div class="dot" style="background:#4c1d95;"></div> Jejak Buntu (Mundur)</div>
                <div class="legend"><div class="dot" style="background:#10b981;"></div> Rute Sukses</div>
            </div>

            <div id="descBox" class="desc-box">
                <h4 id="descTitle" style="margin-top:0;">🧠 Teori Dasar</h4>
                <div id="descContent"></div>
            </div>

            <div id="conclusionBox" class="conclusion-box">
                <h4>🎉 Kesimpulan & Perbandingan</h4>
                <div id="conclusionContent"></div>
            </div>
            
            <div id="instructionText" class="instruction">
                Pilih algoritma di panel kiri untuk memulai.
            </div>
        </div>
    </div>

    <script>
        const maze = {maze_json};
        const rows = maze.length;
        const cols = maze[0].length;
        const cellSize = 500 / cols;
        
        const canvas = document.getElementById('mazeCanvas');
        const ctx = canvas.getContext('2d');

        let START = [1, 0];
        let TARGET = [rows - 2, cols - 1];

        let history = []; 
        let currentFrame = 0;
        let currentAlgo = '';
        let playInterval = null;
        let speedMs = {speed_val}; // Diambil dari Streamlit sidebar
        let clickMode = 'START';

        // Menangkap event klik dari Streamlit Sidebar
        window.addEventListener('message', (event) => {{
            const data = event.data;
            if (data.type === 'streamlit:setComponentValue') {{
                // Ignored, using click events via buttons
            }}
        }});

        // Fungsi untuk menerima perintah dari Streamlit
        function handleStreamlitAction(action) {{
            if (action === 'MODE_START') {{
                clickMode = 'START';
                document.getElementById('activeModeText').innerHTML = '📍 Start (Astronot)';
            }} else if (action === 'MODE_TARGET') {{
                clickMode = 'TARGET';
                document.getElementById('activeModeText').innerHTML = '🎯 Target (UFO)';
            }} else if (action === 'BFS') {{
                generateHistory('BFS');
            }} else if (action === 'DFS') {{
                generateHistory('DFS');
            }} else if (action === 'PLAY') {{
                if (history.length > 0 && !playInterval) {{
                    playInterval = setInterval(() => {{
                        if (currentFrame < history.length - 1) {{
                            currentFrame++;
                            renderFrame();
                        }} else {{
                            clearInterval(playInterval);
                            playInterval = null;
                        }}
                    }}, speedMs);
                }}
            }} else if (action === 'STOP') {{
                clearInterval(playInterval); 
                playInterval = null;
            }} else if (action === 'BACK') {{
                clearInterval(playInterval); playInterval = null;
                if (currentFrame > 0) {{ currentFrame--; renderFrame(); }}
            }} else if (action === 'FORWARD') {{
                clearInterval(playInterval); playInterval = null;
                if (currentFrame < history.length - 1) {{ currentFrame++; renderFrame(); }}
            }} else if (action === 'RESET') {{
                clearInterval(playInterval); playInterval = null;
                if (history.length > 0) {{
                    currentFrame = 0;
                    renderFrame();
                }}
            }}
        }}

        function drawEmoji(emoji, r, c, sizeMultiplier = 1) {{
            ctx.font = `${{cellSize * sizeMultiplier}}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(emoji, c * cellSize + cellSize/2, r * cellSize + cellSize/2);
        }}

        function drawBaseMap() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let r = 0; r < rows; r++) {{
                for (let c = 0; c < cols; c++) {{
                    if (maze[r][c] === 1) {{
                        ctx.fillStyle = '#2a0a4a';
                        ctx.beginPath(); ctx.roundRect(c * cellSize, r * cellSize, cellSize, cellSize, 2); ctx.fill();
                    }} else {{
                        ctx.fillStyle = '#3b1d63';
                        ctx.beginPath(); ctx.arc(c * cellSize + cellSize/2, r * cellSize + cellSize/2, cellSize/6, 0, Math.PI*2); ctx.fill();
                    }}
                }}
            }}
            drawEmoji("👨‍🚀", START[0], START[1], 0.8);
            drawEmoji("🛸", TARGET[0], TARGET[1], 0.8);
        }}

        function renderFrame() {{
            if (history.length === 0) return;
            
            const state = history[currentFrame];
            drawBaseMap();

            let isSuccess = false;
            if (currentFrame === history.length - 1) {{
                if (state.path[state.path.length-1][0] === TARGET[0] && state.path[state.path.length-1][1] === TARGET[1]) {{
                    isSuccess = true;
                }}
            }}

            for (let v of state.visited) {{
                let isInPath = state.path.some(p => p[0] === v[0] && p[1] === v[1]);
                if (!isInPath) {{
                    ctx.fillStyle = '#4c1d95'; 
                    ctx.beginPath();
                    ctx.arc(v[1] * cellSize + cellSize/2, v[0] * cellSize + cellSize/2, cellSize/4, 0, Math.PI*2);
                    ctx.fill();
                }}
            }}

            if (state.path.length > 1) {{
                ctx.beginPath();
                ctx.strokeStyle = isSuccess ? '#10b981' : (currentAlgo === 'BFS' ? '#38bdf8' : '#f472b6');
                ctx.lineWidth = cellSize * 0.5;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.shadowBlur = 15;
                ctx.shadowColor = ctx.strokeStyle;

                ctx.moveTo(state.path[0][1] * cellSize + cellSize/2, state.path[0][0] * cellSize + cellSize/2);
                for (let i = 1; i < state.path.length; i++) {{
                    ctx.lineTo(state.path[i][1] * cellSize + cellSize/2, state.path[i][0] * cellSize + cellSize/2);
                    ctx.stroke(); 
                    ctx.beginPath();
                    ctx.moveTo(state.path[i][1] * cellSize + cellSize/2, state.path[i][0] * cellSize + cellSize/2);
                }}
                ctx.shadowBlur = 0;
            }}

            if (state.current) {{
                drawEmoji("👾", state.current[0], state.current[1], 0.8);
            }}

            ctx.font = `${{cellSize * 0.3}}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#ffffff'; 
            ctx.shadowBlur = 2;
            ctx.shadowColor = '#000000';
            
            for (let i = 0; i < state.visited.length; i++) {{
                let v = state.visited[i];
                let num = i + 1; 
                let textX = v[1] * cellSize + cellSize/2;
                let textY = v[0] * cellSize + cellSize/2;
                
                if (cellSize > 15) {{
                    ctx.fillText(num, textX, textY);
                }}
            }}
            ctx.shadowBlur = 0;

            const stepText = `Langkah: ${{currentFrame + 1}} / ${{history.length}}`;
            const visitedText = `Titik diperiksa: ${{state.visited.length}}`;
            if (currentAlgo === 'BFS') {{
                document.getElementById('bfsStats').innerHTML = `${{visitedText}}<br>${{stepText}}`;
            }} else {{
                document.getElementById('dfsStats').innerHTML = `${{visitedText}}<br>${{stepText}}`;
            }}

            const conclusionBox = document.getElementById('conclusionBox');
            if (isSuccess) {{
                conclusionBox.style.display = 'block';
                
                let content = `<b>${{currentAlgo}} Berhasil!</b><br>`;
                content += `Rute ditemukan dengan <b>${{state.path.length}}</b> langkah, mengeksplorasi <b>${{state.visited.length}}</b> titik.<br><br>`;
                content += `<b>Perbandingan Konsep:</b><ul>`;
                
                if (currentAlgo === 'BFS') {{
                    content += `<li><b>BFS (Sekarang):</b> Rute dijamin paling pendek karena menyebar rata per lapisan, meski harus memeriksa banyak titik.</li>`;
                    content += `<li><b>DFS (Pembanding):</b> Menyusuri satu lorong sampai buntu baru mundur. Bisa saja memeriksa lebih sedikit titik jika beruntung, tapi rutenya belum tentu sependek BFS.</li>`;
                }} else {{
                    content += `<li><b>DFS (Sekarang):</b> Menyusuri lorong sampai buntu. Berhasil menemukan rute, namun rute ini belum tentu yang terpendek karena tidak memeriksa semua alternatif.</li>`;
                    content += `<li><b>BFS (Pembanding):</b> Akan menyebar rata dan menjamin rute terpendek. Jika BFS dijalankan, ia mungkin memeriksa lebih banyak titik, tapi pasti menemukan jalur dengan langkah paling sedikit.</li>`;
                }}
                content += `</ul>`;
                document.getElementById('conclusionContent').innerHTML = content;
            }} else {{
                conclusionBox.style.display = 'none';
            }}
        }}

        function getNeighbors(r, c) {{
            let nbs = [];
            const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
            for (let d of dirs) {{
                let nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] === 0) {{
                    nbs.push([nr, nc]);
                }}
            }}
            return nbs.sort((a, b) => a[0] === b[0] ? a[1] - b[1] : a[0] - b[0]); 
        }}

        function generateHistory(algo) {{
            clearInterval(playInterval); playInterval = null;
            history = [];
            currentFrame = 0;
            currentAlgo = algo;

            document.getElementById('instructionText').style.display = 'none';
            document.getElementById('conclusionBox').style.display = 'none';
            
            const descBox = document.getElementById('descBox');
            const descTitle = document.getElementById('descTitle');
            const descContent = document.getElementById('descContent');
            
            descBox.style.display = 'block';
            descBox.style.borderLeftColor = algo === 'BFS' ? '#38bdf8' : '#f472b6';
            descTitle.style.color = algo === 'BFS' ? '#38bdf8' : '#f472b6';
            
            if (algo === 'BFS') {{
                descTitle.innerHTML = "🔵 Teori BFS";
                descContent.innerHTML = "<b>BFS (Breadth):</b> Menyebar rata seperti air. <i>Dijamin menemukan rute terpendek</i>, tapi memeriksa banyak titik.";
            }} else {{
                descTitle.innerHTML = "🔴 Teori DFS";
                descContent.innerHTML = "<b>DFS (Depth):</b> Menyusuri satu jalur sampai buntu baru mundur. <i>Tidak menjamin terpendek</i>, tapi bisa lebih cepat jika beruntung.";
            }}

            if (algo === 'BFS') {{
                let queue = [[START, [START]]];
                let vis = new Set();
                while (queue.length > 0) {{
                    let [curr, p] = queue.shift();
                    let key = curr.join(',');
                    if (vis.has(key)) continue;
                    vis.add(key);
                    history.push({{ current: curr, path: p, visited: Array.from(vis).map(s => s.split(',').map(Number)) }});
                    
                    if (curr[0] === TARGET[0] && curr[1] === TARGET[1]) break;

                    for (let nb of getNeighbors(curr[0], curr[1])) {{
                        if (!vis.has(nb.join(','))) queue.push([nb, [...p, nb]]);
                    }}
                }}
            }} else {{
                let stack = [[START, [START]]];
                let vis = new Set();
                while (stack.length > 0) {{
                    let [curr, p] = stack.pop();
                    let key = curr.join(',');
                    if (vis.has(key)) continue;
                    vis.add(key);
                    history.push({{ current: curr, path: p, visited: Array.from(vis).map(s => s.split(',').map(Number)) }});

                    if (curr[0] === TARGET[0] && curr[1] === TARGET[1]) break;

                    let nbs = getNeighbors(curr[0], curr[1]).reverse();
                    for (let nb of nbs) {{
                        if (!vis.has(nb.join(','))) stack.push([nb, [...p, nb]]);
                    }}
                }}
            }}
            renderFrame();
        }}

        canvas.addEventListener('click', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const c = Math.floor(x / cellSize);
            const r = Math.floor(y / cellSize);

            if (r >= 0 && r < rows && c >= 0 && c < cols && maze[r][c] === 0) {{
                if (clickMode === 'START') {{
                    if (r === TARGET[0] && c === TARGET[1]) return;
                    START = [r, c];
                }} else {{
                    if (r === START[0] && c === START[1]) return;
                    TARGET = [r, c];
                }}
                
                history = []; 
                currentFrame = 0;
                drawBaseMap();
                document.getElementById('descBox').style.display = 'none';
                document.getElementById('conclusionBox').style.display = 'none';
                document.getElementById('instructionText').style.display = 'block';
                document.getElementById('bfsStats').innerHTML = 'Menunggu simulasi...';
                document.getElementById('dfsStats').innerHTML = 'Menunggu simulasi...';
            }}
        }});

        drawBaseMap();
    </script>
</body>
</html>
"""

# =========================================================
# MENGHUBUNGKAN SIDEBAR KE DALAM HTML/JS
# =========================================================
# Kita menggunakan trik query param / session state untuk mengirim perintah ke iframe HTML
# Karena components.html tidak bisa langsung mendengar klik streamlit, 
# kita inject script JS yang otomatis terpanggil saat tombol diklik.

# Menyiapkan instruksi berdasarkan tombol yang diklik
action_script = ""
if btn_bfs: action_script = "handleStreamlitAction('BFS');"
elif btn_dfs: action_script = "handleStreamlitAction('DFS');"
elif btn_play: action_script = "handleStreamlitAction('PLAY');"
elif btn_stop: action_script = "handleStreamlitAction('STOP');"
elif btn_back: action_script = "handleStreamlitAction('BACK');"
elif btn_forward: action_script = "handleStreamlitAction('FORWARD');"
elif btn_reset: action_script = "handleStreamlitAction('RESET');"

if click_mode == "Start (Astronot)":
    action_script += "handleStreamlitAction('MODE_START');"
else:
    action_script += "handleStreamlitAction('MODE_TARGET');"

# Suntikkan script ke dalam HTML jika ada aksi
if action_script:
    html_code = html_code.replace("drawBaseMap();", f"drawBaseMap();\n        {action_script}")

# Perhatikan bagian ini: height disesuaikan agar pas
components.html(html_code, height=600)
