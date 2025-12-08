#!/usr/bin/env python3
"""
Download Open Source AI Models
Script to download required AI models for the platform
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm
import argparse

# Import model configurations
try:
    from models_config import MODELS_CONFIG, MODELS_CONFIG_LITE, DOWNLOAD_SETTINGS
except ImportError:
    print("Error: models_config.py not found. Please ensure it exists in the same directory.")
    sys.exit(1)


def download_file(url, destination, chunk_size=8192):
    """Download a file with progress bar."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as file, tqdm(
            desc=os.path.basename(destination),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                progress_bar.update(size)
        
        return True
    except Exception as e:
        print(f"\n❌ Error downloading {url}: {str(e)}")
        return False


def verify_model_exists(model_path):
    """Check if model file already exists."""
    return os.path.exists(model_path) and os.path.getsize(model_path) > 0


def download_models(use_lite=False, models_to_download=None, skip_existing=True):
    """Download all required models."""
    models_dir = Path(DOWNLOAD_SETTINGS['models_dir'])
    models_dir.mkdir(exist_ok=True)
    
    # Select model configuration
    models_config = MODELS_CONFIG_LITE if use_lite else MODELS_CONFIG
    
    print("=" * 70)
    print("🤖 AI Platform - Model Downloader")
    print("=" * 70)
    print(f"\nModel variant: {'Lite (smaller models)' if use_lite else 'Standard'}")
    print(f"Download directory: {models_dir.absolute()}\n")
    
    # Filter models to download
    if models_to_download:
        models_to_process = {k: v for k, v in models_config.items() if k in models_to_download}
    else:
        models_to_process = models_config
    
    if not models_to_process:
        print("❌ No models to download.")
        return
    
    # Show summary
    print("Models to download:")
    total_size = 0
    for model_key, model_info in models_to_process.items():
        status = "Required" if model_info.get('required') else "Optional"
        print(f"  • {model_info['name']} ({model_info['size']}) - {status}")
        print(f"    Use case: {model_info['use_case']}")
    print()
    
    # Download each model
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for model_key, model_info in models_to_process.items():
        model_path = models_dir / model_info['filename']
        
        print("-" * 70)
        print(f"📥 {model_info['name']}")
        print(f"   {model_info['description']}")
        print(f"   Size: {model_info['size']}")
        print(f"   File: {model_info['filename']}")
        
        # Check if already exists
        if verify_model_exists(model_path) and skip_existing:
            print(f"   ✅ Already exists, skipping...")
            skip_count += 1
            continue
        
        print(f"   Downloading from: {model_info['url']}")
        
        # Download with retry
        success = False
        for attempt in range(DOWNLOAD_SETTINGS['retry_attempts']):
            if attempt > 0:
                print(f"   🔄 Retry attempt {attempt + 1}/{DOWNLOAD_SETTINGS['retry_attempts']}")
            
            success = download_file(
                model_info['url'],
                model_path,
                DOWNLOAD_SETTINGS['chunk_size']
            )
            
            if success:
                print(f"   ✅ Downloaded successfully!")
                success_count += 1
                break
        
        if not success:
            print(f"   ❌ Failed to download after {DOWNLOAD_SETTINGS['retry_attempts']} attempts")
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Download Summary")
    print("=" * 70)
    print(f"✅ Successfully downloaded: {success_count}")
    print(f"⏭️  Skipped (already exists): {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📁 Models directory: {models_dir.absolute()}")
    
    if fail_count > 0:
        print("\n⚠️  Some downloads failed. Please check your internet connection and try again.")
        print("   You can re-run this script and it will skip already downloaded files.")
    
    if success_count > 0 or skip_count > 0:
        print("\n✅ Models are ready! Update app/services/model_service.py to load them.")
        print("   See docs/INSTALL.md for integration instructions.")


def list_available_models(use_lite=False):
    """List all available models."""
    models_config = MODELS_CONFIG_LITE if use_lite else MODELS_CONFIG
    
    print("=" * 70)
    print("📋 Available Models")
    print("=" * 70)
    print(f"\nVariant: {'Lite' if use_lite else 'Standard'}\n")
    
    for model_key, model_info in models_config.items():
        print(f"🔹 {model_key}")
        print(f"   Name: {model_info['name']}")
        print(f"   Description: {model_info['description']}")
        print(f"   Size: {model_info['size']}")
        print(f"   Use case: {model_info['use_case']}")
        print(f"   Required: {'Yes' if model_info.get('required') else 'No'}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Download open source AI models for the platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all standard models
  python download_models.py
  
  # Download lite versions (smaller, faster)
  python download_models.py --lite
  
  # Download specific models only
  python download_models.py --models deepseek-coder gpt4all
  
  # List available models
  python download_models.py --list
  
  # Force re-download (overwrite existing)
  python download_models.py --force
        """
    )
    
    parser.add_argument(
        '--lite',
        action='store_true',
        help='Download lite versions (smaller models for limited resources)'
    )
    
    parser.add_argument(
        '--models',
        nargs='+',
        help='Download specific models only (e.g., deepseek-coder gpt4all)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available models without downloading'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download even if files exist'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_models(args.lite)
        return
    
    try:
        download_models(
            use_lite=args.lite,
            models_to_download=args.models,
            skip_existing=not args.force
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
