import platform
import subprocess as sb

# Get wifi based on OS
def get_wifi_name():
    try:
        if platform.system() == 'Windows':
            result = sb.check_output("netsh wlan show interfaces", shell=True, text=True)
            for line in result.split("\n"):
                if "SSID" in line:
                    wifi_name = line.split(':')[1].strip()
                    return wifi_name
                
        # Command for MacOS
        elif platform.system() == "Darwin":
            result = sb.check_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep SSID", shell=True, text=True)
            wifi_name = result.split(':')[1].strip()
            return wifi_name
        
        # Command for Linux
        elif platform.system() == "Linux":
            result = sb.check_output("nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d\' -f2", shell=True, text=True)
            wifi_name = result.split(":")[1].strip()
            return wifi_name
        else:
            return None
        
    except sb.CalledProcessError:
        return None