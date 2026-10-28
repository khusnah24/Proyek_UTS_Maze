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

    /* ===== HEADER BANNER ===== */
    .hero-header {
        /* Background disamakan dengan tema labirin (ungu gelap) */
        background: linear-gradient(135deg, #1a0033 0%, #2a0a4a 50%, #150025 100%);
        border: 1px solid #7c3aed;
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 20px;
        box-shadow: 0 0 30px rgba(124, 58, 237, 0.25);
        display: flex;
        align-items: flex-start;
        gap: 18px;
        position: relative;
        overflow: hidden; /* Agar ulat tidak keluar */
    }

    /* Animasi Ular/Ulat Berjalan di Background Header */
    .snake-bg {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.15; /* Dibuat transparan agar teks tetap terbaca */
    }
    .snake-segment {
        position: absolute;
        width: 16px; height: 16px;
        background-color: #c084fc;
        border-radius: 50%;
        box-shadow: 0 0 10px #c084fc;
        animation: moveSnake 8s linear infinite;
    }
    /* Keyframes untuk ulat berjalan zigzag */
    @keyframes moveSnake {
        0%   { top: 10%; left: -5%; }
        15%  { top: 50%; left: 15%; }
        30%  { top: 80%; left: 30%; }
        45%  { top: 20%; left: 50%; }
        60%  { top: 70%; left: 65%; }
        75%  { top: 30%; left: 80%; }
        100% { top: 50%; left: 105%; }
    }
    /* Menunda animasi tiap segmen agar terlihat seperti ular menyambung */
    .snake-segment:nth-child(2) { animation-delay: 0.2s; }
    .snake-segment:nth-child(3) { animation-delay: 0.4s; }
    .snake-segment:nth-child(4) { animation-delay: 0.6s; }
    .snake-segment:nth-child(5) { animation-delay: 0.8s; }
    .snake-segment:nth-child(6) { animation-delay: 1.0s; }
    .snake-segment:nth-child(7) { animation-delay: 1.2s; }
    .snake-segment:nth-child(8) { animation-delay: 1.4s; }
    .snake-segment:nth-child(9) { animation-delay: 1.6s; }
    .snake-segment:nth-child(10){ animation-delay: 1.8s; }

    .hero-content {
        position: relative;
        z-index: 1; /* Agar konten di atas animasi ulat */
        display: flex;
        align-items: flex-start;
        gap: 18px;
        width: 100%;
    }

    .hero-icon {
        font-size: 42px;
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid #7c3aed;
        border-radius: 14px;
        padding: 10px 14px;
        line-height: 1;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        color: #c084fc;
        margin: 0;
        text-shadow: 0 0 20px rgba(192, 132, 252, 0.4);
        font-family: 'Trebuchet MS', sans-serif;
    }
    .hero-subtitle {
        color: #a78bfa;
        font-size: 14px;
        margin: 6px 0 12px 0;
    }
    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    /* Badge Interaktif */
    .hero-badge {
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid #7c3aed;
        color: #c084fc;
        font-size: 12px;
        padding: 6px 14px;
        border-radius: 999px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        user-select: none;
    }
    .hero-badge:hover {
        background: rgba(124, 58, 237, 0.4);
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(192, 132, 252, 0.5);
    }
    
    /* Panel Penjelasan Badge */
    .badge-explanation {
        display: none;
        width: 100%;
        margin-top: 15px;
        padding: 10px 15px;
        background: rgba(0, 0, 0, 0.4);
        border-left: 4px solid #c084fc;
        border-radius: 8px;
        font-size: 13px;
        color: #e0d0ff;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO HEADER DENGAN ULAT BERJALAN & BADGE INTERAKTIF
# =========================================================
st.components.v1.html("""
<style>
    /* Style khusus dimasukkan ke dalam iframe agar terisolasi */
    body { margin: 0; font-family: 'Trebuchet MS', sans-serif; }
    .hero-header {
        background: linear-gradient(135deg, #1a0033 0%, #2a0a4a 50%, #150025 100%);
        border: 1px solid #7c3aed;
        border-radius: 16px;
        padding: 20px 28px;
        box-shadow: 0 0 30px rgba(124, 58, 237, 0.25);
        display: flex;
        align-items: flex-start;
        position: relative;
        overflow: hidden;
    }

    /* Animasi Ular/Ulat Berjalan */
    .snake-bg {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.2;
    }
    .snake-segment {
        position: absolute;
        width: 14px; height: 14px;
        background-color: #c084fc;
        border-radius: 50%;
        box-shadow: 0 0 10px #c084fc;
        animation: moveSnake 8s linear infinite;
    }
    @keyframes moveSnake {
        0%   { top: 10%; left: -5%; }
        15%  { top: 50%; left: 15%; }
        30%  { top: 80%; left: 30%; }
        45%  { top: 20%; left: 50%; }
        60%  { top: 70%; left: 65%; }
        75%  { top: 30%; left: 80%; }
        100% { top: 50%; left: 105%; }
    }
    .snake-segment:nth-child(2) { animation-delay: 0.2s; }
    .snake-segment:nth-child(3) { animation-delay: 0.4s; }
    .snake-segment:nth-child(4) { animation-delay: 0.6s; }
    .snake-segment:nth-child(5) { animation-delay: 0.8s; }
    .snake-segment:nth-child(6) { animation-delay: 1.0s; }
    .snake-segment:nth-child(7) { animation-delay: 1.2s; }
    .snake-segment:nth-child(8) { animation-delay: 1.4s; }
    .snake-segment:nth-child(9) { animation-delay: 1.6s; }
    .snake-segment:nth-child(10){ animation-delay: 1.8s; }

    .hero-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: flex-start;
        gap: 18px;
        width: 100%;
    }

    .hero-icon {
        font-size: 42px;
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid #7c3aed;
        border-radius: 14px;
        padding: 10px 14px;
        line-height: 1;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        color: #c084fc;
        margin: 0;
        text-shadow: 0 0 20px rgba(192, 132, 252, 0.4);
    }
    .hero-subtitle {
        color: #a78bfa;
        font-size: 14px;
        margin: 6px 0 12px 0;
    }
    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    /* Badge Interaktif */
    .hero-badge {
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid #7c3aed;
        color: #c084fc;
        font-size: 12px;
        padding: 6px 14px;
        border-radius: 999px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        user-select: none;
    }
    .hero-badge:hover {
        background: rgba(124, 58, 237, 0.4);
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(192, 132, 252, 0.5);
    }
    
    /* Panel Penjelasan Badge */
    .badge-explanation {
        display: none;
        width: 100%;
        margin-top: 15px;
        padding: 10px 15px;
        background: rgba(0, 0, 0, 0.4);
        border-left: 4px solid #c084fc;
        border-radius: 8px;
        font-size: 13px;
        color: #e0d0ff;
        line-height: 1.5;
    }
</style>

<div class="hero-header">
    <!-- Animasi Ular Latar Belakang -->
    <div class="snake-bg">
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
        <div class="snake-segment"></div>
    </div>

    <div class="hero-content">
        <div class="hero-icon">🌌</div>
        <div style="width: 100%;">
            <h1 class="hero-title">Galaxy Maze Explorer</h1>
            <div class="hero-subtitle">
                Perbandingan algoritma BFS vs DFS pada labirin antariksa 21×21 — animasi langkah demi langkah
            </div>
            <div class="hero-badges">
                <div class="hero-badge" onclick="showInfo('BFS')">Algoritma BFS</div>
                <div class="hero-badge" onclick="showInfo('DFS')">Algoritma DFS</div>
                <div class="hero-badge" onclick="showInfo('Graf')">Graf Tak Berbobot</div>
                <div class="hero-badge" onclick="showInfo('Validasi')">Validasi Otomatis</div>
                <div class="hero-badge" onclick="showInfo('Grid')">Grid 21×21</div>
            </div>
            
            <!-- Tempat Penjelasan -->
            <div id="badgeExplanation" class="badge-explanation"></div>
        </div>
    </div>
</div>

<script>
    const explanations = {
        'BFS': '<b>BFS (Breadth-First Search):</b> Menjelajah graf secara melebar. Sangat cocok untuk mencari rute terpendek pada graf tak berbobot.',
        'DFS': '<b>DFS (Depth-First Search):</b> Menjelajah graf secara mendalam. Tidak menjamin rute terpendek, tapi bisa lebih hemat memori.',
        'Graf': '<b>Graf Tak Berbobot:</b> Setiap langkah/sisi memiliki bobot yang sama (1). Titik adalah sel kosong, sisi adalah jalan bersebelahan.',
        'Validasi': '<b>Validasi Otomatis:</b> Sistem memeriksa apakah jalur menembus dinding dan membuktikan BFS selalu menemukan jalur minimum.',
        'Grid': '<b>Grid 21×21:</b> Labirin berukuran 21 baris dan 21 kolom. Titik awal (Astronot) dan target (UFO) dapat dipindahkan.'
    };

    function showInfo(key) {
        const box = document.getElementById('badgeExplanation');
        if (box.style.display === 'block' && box.innerHTML === explanations[key]) {
            // Jika diklik lagi, sembunyikan
            box.style.display = 'none';
        } else {
            box.innerHTML = explanations[key];
            box.style.display = 'block';
        }
    }
</script>
""", height=260)

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
# HTML + JS LABIRIN (Sama seperti sebelumnya)
# =========================================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: transparent;
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
            margin-bottom: 15px;
            cursor: crosshair;
        }}
        .controls {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        button {{
            background: linear-gradient(135deg, #6d28d9, #9333ea);
            color: white;
            border: 1px solid #a78bfa;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 0 10px #7c3aed;
            transition: all 0.2s;
        }}
        button:hover {{
            background: linear-gradient(135deg, #7c3aed, #c084fc);
            box-shadow: 0 0 20px #c084fc;
            transform: scale(1.05);
        }}
        .slider-container {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            color: #a78bfa;
        }}
        input[type="range"] {{ accent-color: #c084fc; width: 150px; }}
        
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
            max-height: 580px; 
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

        .validation-box {{
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid #3b82f6;
            padding: 12px; 
            border-radius: 8px;
            font-size: 12px;
            line-height: 1.5;
            color: #dbeafe;
            display: none;
        }}
        .validation-box h4 {{ margin: 0 0 8px 0; font-size: 13px; color: #60a5fa; }}
        .validation-box ul {{ margin: 5px 0 0 0; padding-left: 18px; }}
        .validation-box li {{ margin-bottom: 5px; }}
        
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
            <div class="mode-selector">
                <button id="modeStart" class="mode-btn active">📍 Pindahkan Start</button>
                <button id="modeTarget" class="mode-btn">🎯 Pindahkan Target</button>
            </div>

            <canvas id="mazeCanvas" width="500" height="500"></canvas>
            
            <div class="controls">
                <button id="btnBFS">🔵 BFS</button>
                <button id="btnDFS">🔴 DFS</button>
                <button id="btnBack">⏮️ Mundur</button>
                <button id="btnPlay">▶️ Play</button>
                <button id="btnStop">⏸️ Jeda</button>
                <button id="btnForward">⏭️ Maju</button>
                <button id="btnReset">🔄 Ulang</button>
            </div>
            <div class="slider-container">
                <label>Kecepatan:</label>
                <input type="range" id="speedSlider" min="10" max="1000" value="200" step="10">
                <span id="speedValue">200 ms</span>
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

            <div id="validationBox" class="validation-box">
                <h4>🔍 Validasi Otomatis</h4>
                <div id="validationContent"></div>
            </div>

            <div id="conclusionBox" class="conclusion-box">
                <h4>🎉 Kesimpulan & Perbandingan</h4>
                <div id="conclusionContent"></div>
            </div>
            
            <div id="instructionText" class="instruction">
                Klik tombol BFS atau DFS untuk melihat perbandingan data.
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
        let speedMs = 200; 
        let clickMode = 'START';

        let resultBFS = null;
        let resultDFS = null;

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

            if (isSuccess) {{
                if (currentAlgo === 'BFS') {{
                    resultBFS = {{ pathLen: state.path.length, visited: state.visited.length, path: state.path }};
                }} else {{
                    resultDFS = {{ pathLen: state.path.length, visited: state.visited.length, path: state.path }};
                }}
                runValidation();
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

        function runValidation() {{
            const box = document.getElementById('validationBox');
            const content = document.getElementById('validationContent');
            
            if (!resultBFS && !resultDFS) {{
                box.style.display = 'none';
                return;
            }}
            
            box.style.display = 'block';
            let html = '<ul>';
            
            let wallCheck = true;
            if (resultBFS) {{
                for (let p of resultBFS.path) {{
                    if (maze[p[0]][p[1]] === 1) {{ wallCheck = false; break; }}
                }}
            }}
            if (resultDFS) {{
                for (let p of resultDFS.path) {{
                    if (maze[p[0]][p[1]] === 1) {{ wallCheck = false; break; }}
                }}
            }}
            if (wallCheck) {{
                html += '<li>✅ <b>Lintasan tidak menembus dinding</b> — semua titik pada jalur bernilai 0 (bukan dinding).</li>';
            }} else {{
                html += '<li>❌ <b>VALIDASI GAGAL</b> — lintasan menembus dinding!</li>';
            }}
            
            if (resultBFS) {{
                html += `<li>✅ <b>BFS menjamin lintasan minimum</b> pada graf tak berbobot. Panjang lintasan BFS = <b>${{resultBFS.pathLen - 1}}</b> sisi (langkah).</li>`;
            }}
            
            if (resultDFS && resultBFS) {{
                if (resultDFS.pathLen > resultBFS.pathLen) {{
                    html += `<li>⚠️ <b>DFS tidak minimum</b>: panjang DFS = <b>${{resultDFS.pathLen - 1}}</b> sisi, sedangkan BFS = <b>${{resultBFS.pathLen - 1}}</b> sisi. Selisih <b>${{resultDFS.pathLen - resultBFS.pathLen}}</b> sisi.</li>`;
                }} else if (resultDFS.pathLen === resultBFS.pathLen) {{
                    html += `<li>ℹ️ <b>DFS kebetulan sama panjang</b> dengan BFS (${{resultDFS.pathLen - 1}} sisi), tetapi ini <i>tidak dijamin</i> secara umum.</li>`;
                }}
            }} else if (resultDFS) {{
                html += `<li>ℹ️ <b>DFS belum dibandingkan</b> — jalankan BFS juga untuk memverifikasi apakah lintasan DFS minimum.</li>`;
            }}
            
            html += '</ul>';
            html += '<div style="margin-top:8px; padding-top:8px; border-top:1px dashed #3b82f6; font-size:11px; color:#93c5fd;">';
            html += '<b>Urutan tetangga yang dipakai:</b> Bawah → Atas → Kanan → Kiri (diurutkan berdasarkan baris lalu kolom). Urutan ini konsisten agar perbandingan dapat diulang.';
            html += '</div>';
            
            content.innerHTML = html;
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
                descContent.innerHTML = "<b>BFS (Breadth-First Search):</b> Menyebar rata seperti air. <i>Dijamin menemukan rute terpendek</i> pada graf tak berbobot karena memeriksa semua simpul pada level yang sama sebelum lanjut ke level berikutnya.";
            }} else {{
                descTitle.innerHTML = "🔴 Teori DFS";
                descContent.innerHTML = "<b>DFS (Depth-First Search):</b> Menyusuri satu jalur sampai buntu baru mundur. <i>Tidak menjamin rute terpendek</i>, tetapi bisa memeriksa lebih sedikit titik jika kebetulan menemukan target lebih awal.";
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
                resultBFS = null;
                resultDFS = null;
                drawBaseMap();
                document.getElementById('descBox').style.display = 'none';
                document.getElementById('conclusionBox').style.display = 'none';
                document.getElementById('validationBox').style.display = 'none';
                document.getElementById('instructionText').style.display = 'block';
                document.getElementById('bfsStats').innerHTML = 'Menunggu simulasi...';
                document.getElementById('dfsStats').innerHTML = 'Menunggu simulasi...';
            }}
        }});

        document.getElementById('modeStart').addEventListener('click', (e) => {{
            clickMode = 'START';
            e.target.classList.add('active');
            document.getElementById('modeTarget').classList.remove('active');
        }});

        document.getElementById('modeTarget').addEventListener('click', (e) => {{
            clickMode = 'TARGET';
            e.target.classList.add('active');
            document.getElementById('modeStart').classList.remove('active');
        }});

        document.getElementById('btnBFS').addEventListener('click', () => {{ generateHistory('BFS'); }});
        document.getElementById('btnDFS').addEventListener('click', () => {{ generateHistory('DFS'); }});
        
        document.getElementById('btnPlay').addEventListener('click', () => {{
            if (history.length === 0) return;
            if (playInterval) return;
            playInterval = setInterval(() => {{
                if (currentFrame < history.length - 1) {{
                    currentFrame++;
                    renderFrame();
                }} else {{
                    clearInterval(playInterval);
                    playInterval = null;
                }}
            }}, speedMs);
        }});

        document.getElementById('btnStop').addEventListener('click', () => {{
            clearInterval(playInterval); 
            playInterval = null;
        }});

        document.getElementById('btnBack').addEventListener('click', () => {{
            clearInterval(playInterval); playInterval = null;
            if (currentFrame > 0) {{ currentFrame--; renderFrame(); }}
        }});

        document.getElementById('btnForward').addEventListener('click', () => {{
            clearInterval(playInterval); playInterval = null;
            if (currentFrame < history.length - 1) {{ currentFrame++; renderFrame(); }}
        }});

        document.getElementById('btnReset').addEventListener('click', () => {{
            clearInterval(playInterval); playInterval = null;
            if (history.length > 0) {{
                currentFrame = 0;
                renderFrame();
            }}
        }});

        document.getElementById('speedSlider').addEventListener('input', (e) => {{
            speedMs = parseInt(e.target.value);
            document.getElementById('speedValue').innerText = speedMs + ' ms';
            if (playInterval) {{
                clearInterval(playInterval);
                playInterval = null;
                document.getElementById('btnPlay').click();
            }}
        }});

        drawBaseMap();
    </script>
</body>
</html>
"""

components.html(html_code, height=750)
