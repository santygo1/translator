import subprocess
def apply_prettier_to_file(file_path):
    try:
        print("[+] Trying to start Prettier")
        subprocess.run(["npx", "prettier", "--write", file_path], check=True)
        print(f"[+] Prettier applied successfully to {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"[-] An error occurred while applying Prettier: {e}")