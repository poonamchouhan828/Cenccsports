import re
import urllib.request

URL = "https://raw.githubusercontent.com/mimipipi22/live/refs/heads/main/lelipur"

def convert_playlist():
    try:
        req = urllib.request.Request(
            URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
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
            
            # Extract group-title
            group_match = re.search(r'group-title="([^"]*)"', extinf, re.IGNORECASE)
            group_title = group_match.group(1).lower() if group_match else ""
            
            # Condition check: Sirf Amazon group HO YA Title me NITRO ho
            is_amazon = "amazon" in group_title
            is_nitro = "nitro" in extinf.lower()
            
            # Block of properties & URL collection
            props = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#EXTINF:"):
                curr = lines[i].strip()
                if curr:
                    props.append(curr)
                i += 1
            
            # Agar dono me se ek bhi condition match hui, tabhi proceed karo
            if (is_amazon or is_nitro) and props:
                stream_url = ""
                license_key = ""
                
                # Original block me se License Key aur Stream URL nikaalo
                for p in props:
                    if p.startswith("http://") or p.startswith("https://"):
                        stream_url = p
                    elif "license_key=" in p:
                        # Extract exact key value after '='
                        license_key = p.split("license_key=")[-1].strip()
                    elif "#KODIPROP:inputstream.adaptive.license_key=" in p:
                        license_key = p.split("license_key=")[-1].strip()
                
                if stream_url:
                    # Tere Exact App-compatible Format me format karna
                    output_lines.append(extinf)
                    output_lines.append("#KODIPROP:inputstream.adaptive.license_type=clearkey")
                    if license_key:
                        output_lines.append(f"#KODIPROP:inputstream.adaptive.license_key={license_key}")
                    else:
                        output_lines.append("#KODIPROP:inputstream.adaptive.license_key=")
                    output_lines.append("#KODIPROP:inputstream=inputstream.adaptive")
                    output_lines.append("#KODIPROP:inputstream.adaptive.manifest.type=mpd")
                    output_lines.append(stream_url)
            continue
        else:
            i += 1

    # Final Output File Output
    with open("sports_output.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"Successfully converted Amazon & Nitro channels!")

if __name__ == "__main__":
    convert_playlist()
