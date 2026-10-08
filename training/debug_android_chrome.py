import subprocess
import time
import json
import urllib.request
import asyncio
import websockets
import os

async def main():
    user_data = r'C:\Users\Tanish\AppData\Local\Temp\chrome_debug_temp'
    os.makedirs(user_data, exist_ok=True)
    chrome_proc = subprocess.Popen([
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={user_data}',
        '--remote-debugging-port=9222',
        '--window-size=390,844',
        'about:blank'
    ])
    try:
        await asyncio.sleep(2)
        # Get target websocket URL
        req = urllib.request.urlopen('http://localhost:9222/json')
        targets = json.loads(req.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']
        print(f"Connected to Chrome: {ws_url}")

        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                payload = {'id': msg_id, 'method': method, 'params': params or {}}
                msg_id += 1
                await ws.send(json.dumps(payload))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == payload['id']:
                        return res.get('result', {})

            # Navigate
            await send('Page.enable')
            await send('Runtime.enable')
            await send('Page.navigate', {'url': 'http://localhost:8080/'})
            await asyncio.sleep(2)

            # Evaluate Capacitor Native Mode
            setup_script = """
            (() => {
                window.Capacitor = {
                    isNativePlatform: () => true,
                    getPlatform: () => 'android',
                    Plugins: { App: { addListener: () => {} } }
                };
                document.body.classList.add('capacitor-native');
                document.documentElement.classList.add('capacitor-native');
                if (typeof initAndroidBottomNav === 'function') initAndroidBottomNav();
                if (typeof switchTab === 'function') switchTab('dashboard');
                return {
                    bodyClasses: Array.from(document.body.classList),
                    activeTabAttr: document.body.getAttribute('data-active-tab')
                };
            })()
            """
            init_res = await send('Runtime.evaluate', {'expression': setup_script, 'returnByValue': True})
            print("Init Result:", json.dumps(init_res, indent=2))

            # Helper to inspect tabs
            check_script = """
            (() => {
                const tabs = ['dashboard', 'weather', 'disease', 'fertilizer', 'market', 'bot'];
                const results = {};
                for (const t of tabs) {
                    switchTab(t);
                    const viewId = 'view-' + t;
                    const el = document.getElementById(viewId);
                    const mainEl = document.querySelector('main');
                    const heroEl = document.getElementById('farmLocationHeroBar');
                    const bNavEl = document.querySelector('.android-bottom-nav');
                    
                    const getInfo = (node) => {
                        if (!node) return null;
                        const cs = window.getComputedStyle(node);
                        const r = node.getBoundingClientRect();
                        return {
                            display: cs.display,
                            visibility: cs.visibility,
                            opacity: cs.opacity,
                            height: cs.height,
                            overflow: cs.overflow,
                            rect: { width: Math.round(r.width), height: Math.round(r.height), top: Math.round(r.top), bottom: Math.round(r.bottom) },
                            childCount: node.children.length,
                            hasText: node.innerText.trim().length > 0
                        };
                    };
                    
                    results[t] = {
                        activeTabAttr: document.body.getAttribute('data-active-tab'),
                        main: getInfo(mainEl),
                        hero: getInfo(heroEl),
                        view: getInfo(el),
                        bottomNav: getInfo(bNavEl)
                    };
                }
                return results;
            })()
            """
            eval_res = await send('Runtime.evaluate', {'expression': check_script, 'returnByValue': True})
            print("\n================ TABS INSPECTION RESULT ================")
            print(json.dumps(eval_res.get('result', {}).get('value', {}), indent=2))

            # Take screenshot of dashboard
            await send('Runtime.evaluate', {'expression': "switchTab('dashboard')"})
            await asyncio.sleep(0.5)
            ss = await send('Page.captureScreenshot', {'format': 'png'})
            import base64
            with open('training/screenshot_dashboard.png', 'wb') as f:
                f.write(base64.b64decode(ss['data']))
            print("Screenshot saved to training/screenshot_dashboard.png")

    finally:
        chrome_proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
