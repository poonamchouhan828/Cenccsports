import re
import urllib.request

URL = "https://raw.githubusercontent.com/mimipipi22/live/refs/heads/main/lelipur"

def convert_playlist():
    try:
        req = urllib.request.urlopen(URL)
        content = req.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return

    lines = content.splitlines()
    output_lines = ["#EXTM3U"]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("#EXTINF:"):
            extinf = line
            # Check if it belongs to sports or grab all/relevant sports channels
            # Group title ya channel name me Sports check kar sakte hain
            group_match = re.search(r'group-title="([^"]*)"', extinf, re.IGNORECASE)
            group_title = group_match.group(1) if group_match else ""
            
            # Agar group sports ka hai ya channel name me sports related keyword hai
            is_sports = "sport" in group_title.lower() or "sports" in extinf.lower()
            
            # Next lines collect karo (KODIPROP ya URL)
            props = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#EXTINF:"):
                current_line = lines[i].strip()
                if current_line:
                    props.append(current_line)
                i += 1
            
            if is_sports and props:
                # Extract stream URL (last non-property line usually)
                stream_url = ""
                drm_key = None
                manifest_type = "mpd" # Default
                
                for p in props:
                    if p.startswith("https://") or p.startswith("http://"):
                        stream_url = p
                    elif "license_key=" in p:
                        drm_key = p.split("license_key=")[1]
                
                if stream_url:
                    # Format write karo jaise tune bola
                    output_lines.append(extinf)
                    if drm_key:
                        output_lines.append("#KODIPROP:inputstream.adaptive.license_type=clearkey")
                        output_lines.append(f"#KODIPROP:inputstream.adaptive.license_key={drm_key}")
                    output_lines.append("#KODIPROP:inputstream=inputstream.adaptive")
                    output_lines.append(f"#KODIPROP:inputstream.adaptive.manifest.type={manifest_type}")
                    output_lines.append(stream_url)
            continue
        else:
            i += 1

    # Save to file
    with open("sports_output.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("Sports playlist successfully converted!")

if __name__ == "__main__":
    convert_playlist()
  
