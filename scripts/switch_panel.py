import sys

admin = 8 if len(sys.argv) < 2 else sys.argv[1]
with open('/root/app/supertvbit/public/panel/src/panel_config.json', 'w') as f:
    f.write(f'''{{
        "SITE_URL": "http://public.tvbit.local:10080/",
        "PUBLIC_HOST": "http://public.tvbit.local:10080/",
        "API_URL": "http://go.tvbit.local:182{admin}5/",
        "WEBSOCKET_URL": "ws://go.tvbit.local:182{admin}5/ws",
        "WEBSOCKET_ADMIN_URL": "ws://go.tvbit.local:182{admin}5/ws-admin",
        "SECURE_PUBLIC_HOST": "https://public.tvbit.local:10443/",
        "SECURE_API_URL": "https://go.tvbit.local:182{admin}6/",
        "SECURE_WEBSOCKET_URL": "wss://go.tvbit.local:182{admin}6/ws",
        "SECURE_WEBSOCKET_ADMIN_URL": "wss://go.tvbit.local:182{admin}6/ws-admin",
        "DOCS_URL": "docs",
        "PANEL_FEATURES": []
    }}''')
