import sys
import qbittorrentapi

def add_torrent(magnet_link):
    # Replace the following variables with your qBittorrent Web UI credentials and address
    qb_username = '<USERNAME>'
    qb_password = '<PASSWORD>'
    qb_address = 'http://IP:PORT'

    # Connect to the qBittorrent Web API
    qbt_client = qbittorrentapi.Client(host=qb_address, username=qb_username, password=qb_password)

    try:
        # Log in to the qBittorrent Web API
        qbt_client.auth_log_in()
        
        # Add the magnet link as a new torrent
        qbt_client.torrents_add(urls=magnet_link)
        
        print(f"Torrent added successfully: {magnet_link}")

    except qbittorrentapi.exceptions.LoginFailed as e:
        print(f"Failed to log in to qBittorrent Web API: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_torrent(sys.argv[1])
    else:
        print("Usage: python add_torrent.py <magnet_link>")
