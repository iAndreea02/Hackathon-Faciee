#!/usr/bin/env python3
"""
Build script for Raspberry Pi deployment
Packages the application for distribution to RPi
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_rpi_package():
    """Create a deployment package for Raspberry Pi"""
    
    project_root = Path(__file__).parent
    build_dir = project_root / "dist" / "rpi"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"faciee_rpi_{timestamp}"
    package_dir = build_dir / package_name
    
    # Create directories
    package_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Creating Raspberry Pi package: {package_name}")
    
    # Copy source code
    source_files = [
        "Recunostere",
        "assets",
        "requirements_rpi.txt",
        "setup_rpi.sh",
        "README.md"
    ]
    
    for item in source_files:
        src = project_root / item
        dst = package_dir / item
        
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
                print(f"✓ Copied directory: {item}")
            else:
                shutil.copy2(src, dst)
                print(f"✓ Copied file: {item}")
    
    # Create deployment info
    deployment_info = {
        "app": "Faciee",
        "version": "1.0.0",
        "target": "Raspberry Pi 4",
        "python_version": "3.9+",
        "build_date": timestamp,
        "instructions": [
            "1. Transfer to Raspberry Pi: scp -r dist/rpi/<package_name> pi@192.168.x.x:/home/pi/",
            "2. SSH into Pi: ssh pi@192.168.x.x",
            "3. Run setup: bash setup_rpi.sh",
            "4. Run app: python3 Recunostere/main.py"
        ]
    }
    
    info_file = package_dir / "DEPLOYMENT.json"
    with open(info_file, 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"✓ Created deployment info: DEPLOYMENT.json")
    
    # Create archive
    archive_path = build_dir / package_name
    shutil.make_archive(str(archive_path), 'zip', package_dir.parent, package_name)
    
    print(f"\n✅ Package created successfully!")
    print(f"📁 Location: {archive_path}.zip")
    print(f"📊 Size: {os.path.getsize(f'{archive_path}.zip') / (1024*1024):.2f} MB")
    
    # Print deployment instructions
    print("\n📝 Deployment Instructions:")
    print("=" * 60)
    for instruction in deployment_info["instructions"]:
        print(instruction)
    print("=" * 60)

if __name__ == "__main__":
    create_rpi_package()
    print("\n💡 Tip: Use scp or rsync to transfer the package to your Raspberry Pi")
