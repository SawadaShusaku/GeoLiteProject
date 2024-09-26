import streamlit as st
import socket
import requests
import time
import os

st.title("Get My IP Adress Streamlit App")
st.write("Welcome to Streamlit!")
st.balloons()

host = socket.gethostname()
st.write(host)
ip = socket.gethostbyname(host)
st.write(ip)
    
######################################

@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_ip_addresses():
    ipv4 = ipv6 = "取得できませんでした"
    
    try:
        # IPv4アドレスの取得
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            ipv4 = response.json()['ip']
    except requests.RequestException:
        pass

    try:
        # IPv6アドレスの取得
        response = requests.get('https://api6.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            ipv6 = response.json()['ip']
    except requests.RequestException:
        pass

    return ipv4, ipv6

def get_ip_info(ip):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', headers=headers, timeout=5)
        st.write(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            st.write(f"エラーレスポンス: {response.text}")
            return None
    except requests.RequestException as e:
        st.write(f"リクエストエラー: {str(e)}")
        return None

st.title("IP アドレス取得")

# 初期化。show_ipのキーがステートに含まれていない場合にFlase
if 'show_ip' not in st.session_state:
    st.session_state.show_ip = False

if st.button("IPアドレスを取得") or st.session_state.show_ip:
    st.session_state.show_ip = True
    ipv4, ipv6 = get_ip_addresses()
    st.write(f"あなたの IPv4 アドレス: {ipv4}")
    st.write(f"あなたの IPv6 アドレス: {ipv6}")

    if st.checkbox("IPv4の追加情報を表示"):
        with st.spinner("情報を取得中..."):
            time.sleep(1.0)  # レート制限回避のための遅延
            info = get_ip_info(ipv4)
            if info:
                st.json(info)
            else:
                st.write("追加情報の取得に失敗しました")

    if st.checkbox("IPv6の追加情報を表示"):
        st.write("注意: IPv6の地理情報は不正確な場合があります")
        with st.spinner("情報を取得中..."):
            time.sleep(1.0)  # レート制限回避のための遅延
            info = get_ip_info(ipv6)
            if info:
                st.json(info)
            else:
                st.write("追加情報の取得に失敗しました")

################################################


def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    return ip_data['ip']

def get_internal_ip():
    response = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/ip', headers={'Metadata-Flavor': 'Google'})
    return response.text

# セッション状態にIPアドレスを保存
if 'user_ip' not in st.session_state:
    st.session_state.user_ip = get_public_ip()
st.title('ユーザーIPアドレス表示')
if st.button('IPアドレスを表示'):
    st.success(f"あなたのIPアドレス: {st.session_state.user_ip}")
    st.success(f"あなたのインターナルIPアドレス: {get_internal_ip()}")

st.write("４注意: このIPアドレスは、あなたのネットワークの公開IPアドレスです。")


