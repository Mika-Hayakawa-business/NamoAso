[app]

# アプリケーションのタイトル
title = 名もなきあの遊び

# パッケージ名 (一意である必要があります)
package.name = namoaso

# ドメイン名 (ユニークなリバースドメインを使用)
package.domain = com.google.android.apps.namoaso

# メインスクリプトが存在するディレクトリ
source.dir = .

# アプリケーションのバージョン
version = 1.0


source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.include_patterns = assets/*,images/*
source.exclude_patterns = tests/*,data/testdata/*
...
# Change the entry point from main.py to your desired filename
source.main = Namoaso_top.py

# アプリで使用する依存関係
requirements = python3,kivy,requests,Cython

# アプリケーションの向き (横向き)
orientation = landscape

# フルスクリーンモードを有効化
fullscreen = 1

# Androidでの最小APIレベル
android.minapi = 21

# Android SDKのターゲットAPIレベル
android.api = 31

# サポートするアーキテクチャ
android.archs = arm64-v8a, armeabi-v7a

# 使用するNDK APIレベル
android.ndk_api = 21

# インターネット権限をリクエスト
android.permissions = INTERNET

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
# Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug