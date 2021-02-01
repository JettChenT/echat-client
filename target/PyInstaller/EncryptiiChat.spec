# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/jettchen/Documents/codes/chat/app/src/main/python/main.py'],
             pathex=['/Users/jettchen/Documents/codes/chat/app/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Users/jettchen/anaconda3/envs/chat-client/lib/python3.7/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/Users/jettchen/Documents/codes/chat/app/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='EncryptiiChat',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/jettchen/Documents/codes/chat/app/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='EncryptiiChat')
app = BUNDLE(coll,
             name='EncryptiiChat.app',
             icon='/Users/jettchen/Documents/codes/chat/app/target/Icon.icns',
             bundle_identifier=None)
