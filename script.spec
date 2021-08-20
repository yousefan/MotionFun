# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['script.py'],
             pathex=['C:\\Users\\whoismahd1\\PycharmProjects\\MotionFun'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
             
def get_mediapipe_path():
    import mediapipe
    mediapipe_path = mediapipe.__path__[0]
    return mediapipe_path             
             
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

mediapipe_tree = Tree(get_mediapipe_path(), prefix='mediapipe', excludes=["*.pyc"])

a.datas += mediapipe_tree

a.binaries = filter(lambda x: 'mediapipe' not in x[0], a.binaries)

a.datas += [
('assets/ui/start.ui','assets/ui/start.ui','DATA')
, ('assets/ui/main.ui','assets/ui/main.ui','DATA')
, ('assets/ui/login.ui','assets/ui/login.ui','DATA')
, ('assets/logo.png','assets/logo.png','DATA')
, ('assets/logo-light.png','assets/logo-light.png','DATA')
, ('assets/style.css','assets/style.css','DATA')
, ('README.md','README.md','DATA')
]
    
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='script',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=Non,
          console=False, icon='C:\\Users\\whoismahd1\\Desktop\\logo.ico' )
